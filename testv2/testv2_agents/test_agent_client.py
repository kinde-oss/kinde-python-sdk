import asyncio
import os
import stat
import time
from urllib.parse import parse_qs, urlsplit

import httpx
import pytest

from kinde_sdk.agents import (
    AgentConfigError,
    AuthorizationError,
    AuthorizationRequiredError,
    DiscoveryError,
    FileAgentStorage,
    InMemoryAgentStorage,
    KindeAgentClient,
    PendingAuthorization,
    RegistrationError,
)
from kinde_sdk.agents.client import (
    authorization_server_metadata_urls,
    protected_resource_metadata_urls,
    resource_covers,
)
from testv2.testv2_agents.kinde_fake import APP_ID, DOMAIN, ISSUER, RESOURCE_URL, FakeKinde

CIMD_URL = "https://agent.onzs.co.za/oauth/client-metadata.json"
REDIRECT = "http://127.0.0.1:8765/callback"


@pytest.fixture
def fake():
    return FakeKinde()


def make_client(fake: FakeKinde, **options) -> KindeAgentClient:
    async def browser(url: str) -> str:
        return fake.authorize(url)

    options.setdefault("authorization_handler", browser)
    options.setdefault("redirect_uri", REDIRECT)
    return KindeAgentClient(RESOURCE_URL, http_client=fake.async_client(), **options)


def form_of(request: httpx.Request) -> dict:
    return {k: v[0] for k, v in parse_qs(request.content.decode()).items()}


def query_of(url: str) -> dict:
    return {k: v[0] for k, v in parse_qs(urlsplit(url).query).items()}


class TestHelpers:
    def test_metadata_urls(self):
        assert protected_resource_metadata_urls("https://api.example.com/mcp/") == [
            "https://api.example.com/.well-known/oauth-protected-resource/mcp",
            "https://api.example.com/.well-known/oauth-protected-resource",
        ]
        assert authorization_server_metadata_urls(ISSUER) == [
            f"{DOMAIN}/.well-known/oauth-authorization-server/oauth2/agents/{APP_ID}",
            f"{DOMAIN}/.well-known/openid-configuration/oauth2/agents/{APP_ID}",
            f"{ISSUER}/.well-known/openid-configuration",
        ]

    @pytest.mark.parametrize(
        "prm_resource, expected",
        [
            ("https://api.example.com/mcp", True),
            ("https://api.example.com/mcp/", True),
            ("https://api.example.com/", True),
            ("https://API.example.com:443/mcp", True),
            ("https://api.example.com/other", False),
            ("https://api.example.com/mc", False),
            ("https://evil.example.com/mcp", False),
            ("http://api.example.com/mcp", False),
        ],
    )
    def test_resource_covers(self, prm_resource, expected):
        assert resource_covers(prm_resource, RESOURCE_URL) is expected

    def test_rejects_insecure_resource(self):
        with pytest.raises(AgentConfigError):
            KindeAgentClient("http://api.example.com/mcp")


class TestCimdFlow:
    async def test_full_flow_uses_cimd_without_registration(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        response = await client.request("POST", json={"jsonrpc": "2.0"})
        assert response.status_code == 200
        assert fake.count("/register") == 0

        token_request = next(r for r in fake.requests if r.url.path.endswith("/token"))
        form = form_of(token_request)
        assert form["client_id"] == CIMD_URL
        assert "client_secret" not in form
        assert form["resource"] == RESOURCE_URL
        assert "authorization" not in token_request.headers

        info = await client.get_token_info()
        assert info["client_id"] == CIMD_URL
        assert info["scopes"] == ["offline"]
        assert info["has_refresh_token"] is True
        assert "access_token" not in info

    async def test_authorization_request(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        pending = await client.begin_authorization()
        query = query_of(pending.authorization_url)
        assert pending.authorization_url.startswith(f"{ISSUER}/authorize?")
        assert query["client_id"] == CIMD_URL
        assert query["scope"] == "offline"
        assert query["code_challenge_method"] == "S256"
        assert len(query["state"]) >= 8
        assert query["resource"] == RESOURCE_URL
        assert pending.code_verifier not in repr(pending)

    async def test_discovery_uses_path_insertion_only(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        await client.discover()
        urls = [str(r.url) for r in fake.requests]
        assert urls == [
            "https://api.example.com/.well-known/oauth-protected-resource/mcp",
            f"{DOMAIN}/.well-known/oauth-authorization-server/oauth2/agents/{APP_ID}",
        ]

    async def test_never_sends_openid(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL, scopes=["openid", "offline", "profile"])
        pending = await client.begin_authorization()
        assert query_of(pending.authorization_url)["scope"] == "offline profile"

    async def test_falls_back_to_dcr_when_cimd_unsupported(self, fake):
        fake.as_metadata["client_id_metadata_document_supported"] = False
        client = make_client(fake, client_metadata_url=CIMD_URL)
        await client.connect()
        assert fake.count("/register") == 1


class TestDcrFlow:
    async def test_registers_and_uses_returned_secret(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, storage=storage, client_name="Onzs Agent")
        await client.connect()

        register = next(r for r in fake.requests if r.url.path.endswith("/register"))
        import json

        body = json.loads(register.content)
        assert body["token_endpoint_auth_method"] == "none"
        assert body["redirect_uris"] == [REDIRECT]
        assert body["client_name"] == "Onzs Agent"
        assert "scope" not in body and "resource" not in body

        token_form = form_of(next(r for r in fake.requests if r.url.path.endswith("/token")))
        registration = await storage.get_registration(f"{ISSUER}|{REDIRECT}")
        assert token_form["client_id"] == registration["client_id"]
        assert token_form["client_secret"] == registration["client_secret"]
        assert registration["token_endpoint_auth_method"] == "client_secret_post"

    async def test_reuses_stored_registration(self, fake):
        storage = InMemoryAgentStorage()
        await make_client(fake, storage=storage).connect()
        await storage.delete_tokens(f"{RESOURCE_URL}|default")
        await make_client(fake, storage=storage).connect()
        assert fake.count("/register") == 1

    async def test_reregisters_when_expiring_within_a_day(self, fake):
        fake.secret_expires_in = 3600
        storage = InMemoryAgentStorage()
        await make_client(fake, storage=storage).connect()
        await storage.delete_tokens(f"{RESOURCE_URL}|default")
        await make_client(fake, storage=storage).connect()
        assert fake.count("/register") == 2
        # The code is exchanged by the same client that started the attempt
        exchange = [r for r in fake.requests if b"grant_type=authorization_code" in r.content][-1]
        assert form_of(exchange)["client_id"] == list(fake.registrations)[-1]

    async def test_invalid_redirect_uri_surfaces_description(self, fake):
        fake.register_status = 400
        fake.register_error = {
            "error": "invalid_redirect_uri",
            "error_description": "redirect host agent.example.org is not a trusted agent host",
        }
        with pytest.raises(RegistrationError, match="agent.example.org is not a trusted agent host"):
            await make_client(fake).connect()

    async def test_too_many_registrations(self, fake):
        fake.register_status = 429
        with pytest.raises(RegistrationError, match="try again later"):
            await make_client(fake).connect()

    async def test_invalid_client_on_refresh_reregisters(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, storage=storage)
        await client.connect()
        fake.registrations.clear()  # Kinde forgot the registration (expired)
        tokens = await storage.get_tokens(f"{RESOURCE_URL}|default")
        tokens["expires_at"] = time.time() - 10
        await storage.set_tokens(f"{RESOURCE_URL}|default", tokens)
        response = await client.request("GET")
        assert response.status_code == 200
        assert fake.count("/register") == 2


class TestTokens:
    async def test_proactive_refresh_keeps_unrotated_refresh_token(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, client_metadata_url=CIMD_URL, storage=storage)
        await client.connect()
        key = f"{RESOURCE_URL}|default"
        before = await storage.get_tokens(key)
        await storage.set_tokens(key, {**before, "expires_at": time.time() + 30})
        await client.request("GET")
        after = await storage.get_tokens(key)
        assert after["access_token"] != before["access_token"]
        assert after["refresh_token"] == before["refresh_token"]
        refresh = next(r for r in fake.requests if r.url.path.endswith("/token") and b"refresh_token" in r.content)
        assert form_of(refresh)["resource"] == RESOURCE_URL

    async def test_rotated_refresh_token_replaces_old(self, fake):
        fake.rotate_refresh_tokens = True
        storage = InMemoryAgentStorage()
        client = make_client(fake, client_metadata_url=CIMD_URL, storage=storage)
        await client.connect()
        key = f"{RESOURCE_URL}|default"
        before = await storage.get_tokens(key)
        await client.refresh()
        assert (await storage.get_tokens(key))["refresh_token"] != before["refresh_token"]

    async def test_concurrent_401s_share_one_refresh(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        await client.connect()
        fake.active_tokens.clear()  # the resource now rejects the access token
        responses = await asyncio.gather(*(client.request("GET") for _ in range(5)))
        assert all(r.status_code == 200 for r in responses)
        refreshes = [
            r for r in fake.requests if r.url.path.endswith("/token") and b"grant_type=refresh_token" in r.content
        ]
        assert len(refreshes) == 1

    async def test_invalid_grant_restarts_sign_in(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        await client.connect()
        fake.active_tokens.clear()
        fake.refresh_tokens.clear()
        response = await client.request("GET")
        assert response.status_code == 200
        assert fake.count("/authorize") == 0  # the handler stands in for the browser
        assert len([r for r in fake.requests if b"authorization_code" in r.content]) == 2

    async def test_step_up_on_insufficient_scope(self, fake):
        fake.resource_required_scope = "email"
        client = make_client(fake, client_metadata_url=CIMD_URL)
        response = await client.request("GET")
        assert response.status_code == 200
        assert (await client.get_token_info())["scopes"] == ["offline", "email"]

    async def test_token_never_sent_to_another_origin(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        with pytest.raises(AgentConfigError):
            await client.request("GET", "https://evil.example.com/steal")

    async def test_relative_path_on_resource_origin(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        response = await client.request("GET", "/mcp/tools")
        assert str(response.request.url) == "https://api.example.com/mcp/tools"

    async def test_disconnect_revokes_and_clears(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, storage=storage)
        await client.connect()
        refresh_token = (await storage.get_tokens(f"{RESOURCE_URL}|default"))["refresh_token"]
        await client.disconnect(forget=True)
        revoke = fake.requests[-1]
        form = form_of(revoke)
        assert str(revoke.url) == f"{ISSUER}/revoke"
        assert form["token"] == refresh_token
        assert form["token_type_hint"] == "refresh_token"
        assert "client_secret" in form  # DCR client: same auth as the token endpoint
        assert await client.get_token_info() is None
        assert await storage.get_registration(f"{ISSUER}|{REDIRECT}") is None

    async def test_tokens_dropped_when_issuer_changes(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, client_metadata_url=CIMD_URL, storage=storage)
        await client.connect()
        tokens = await storage.get_tokens(f"{RESOURCE_URL}|default")
        await storage.set_tokens(f"{RESOURCE_URL}|default", {**tokens, "issuer": "https://old.example.com"})
        await client.discover(force=True)
        assert await storage.get_tokens(f"{RESOURCE_URL}|default") is None


class TestDiscovery:
    async def test_falls_back_to_challenge_when_well_known_missing(self, fake):
        fake.serve_prm_at_well_known = False
        client = make_client(fake, client_metadata_url=CIMD_URL)
        await client.discover()
        assert any(r.url.path == "/hidden-prm" for r in fake.requests)

    async def test_prm_for_other_resource_aborts(self, fake):
        fake.prm["resource"] = "https://other.example.com/mcp"
        with pytest.raises(DiscoveryError, match="different resource"):
            await make_client(fake).discover()

    async def test_issuer_mismatch_aborts(self, fake):
        fake.as_metadata["issuer"] = DOMAIN
        with pytest.raises(DiscoveryError, match="issuer mismatch"):
            await make_client(fake).discover()

    async def test_missing_s256_aborts(self, fake):
        del fake.as_metadata["code_challenge_methods_supported"]
        with pytest.raises(DiscoveryError, match="S256"):
            await make_client(fake).discover()

    async def test_metadata_cached(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        await client.discover()
        await client.discover()
        assert len(fake.requests) == 2


class TestAuthorizationStep:
    async def test_state_mismatch(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        pending = await client.begin_authorization()
        callback = fake.authorize(pending.authorization_url).replace(pending.state, "x" * 43)
        with pytest.raises(AuthorizationError, match="state"):
            await client.complete_authorization(pending, callback)

    async def test_pending_is_single_use_and_serialisable(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        pending = PendingAuthorization.from_dict((await client.begin_authorization()).to_dict())
        callback = fake.authorize(pending.authorization_url)
        await client.complete_authorization(pending, callback)
        with pytest.raises(AuthorizationError, match="already used"):
            await client.complete_authorization(pending, callback)

    async def test_error_on_callback(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        pending = await client.begin_authorization()
        callback = f"{REDIRECT}?error=invalid_client&error_description=untrusted&state={pending.state}"
        with pytest.raises(AuthorizationError, match="Trusted agent hosts"):
            await client.complete_authorization(pending, callback)

    async def test_wrong_iss_on_callback(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        pending = await client.begin_authorization()
        callback = fake.authorize(pending.authorization_url).replace(f"iss={ISSUER}", "iss=https://evil.example.com")
        with pytest.raises(AuthorizationError, match="different authorization server"):
            await client.complete_authorization(pending, callback)

    async def test_server_hosted_agent_without_handler(self, fake):
        client = KindeAgentClient(
            RESOURCE_URL,
            client_metadata_url=CIMD_URL,
            redirect_uri="https://agent.onzs.co.za/oauth/callback",
            http_client=fake.async_client(),
        )
        with pytest.raises(AuthorizationRequiredError):
            await client.connect()
        pending = await client.begin_authorization()
        await client.complete_authorization(pending, fake.authorize(pending.authorization_url))
        assert (await client.request("GET")).status_code == 200

    async def test_loopback_listener(self, fake):
        opened = []

        async def open_browser(url: str):
            opened.append(url)
            callback = fake.authorize(url)

            async def follow():
                async with httpx.AsyncClient() as browser:
                    await browser.get(callback)

            asyncio.get_running_loop().create_task(follow())

        client = KindeAgentClient(
            RESOURCE_URL,
            client_metadata_url=CIMD_URL,
            open_browser=open_browser,
            http_client=fake.async_client(),
            callback_timeout_seconds=5,
        )
        await client.connect()
        redirect_uri = query_of(opened[0])["redirect_uri"]
        assert redirect_uri.startswith("http://127.0.0.1:") and redirect_uri.endswith("/callback")
        assert (await client.get_token_info())["client_id"] == CIMD_URL


class TestFileStorage:
    async def test_round_trip_with_private_permissions(self, tmp_path):
        path = tmp_path / "agent" / "tokens.json"
        storage = FileAgentStorage(str(path))
        await storage.set_tokens("k", {"access_token": "a"})
        await storage.set_registration("r", {"client_id": "c"})
        assert await FileAgentStorage(str(path)).get_tokens("k") == {"access_token": "a"}
        assert await storage.get_registration("r") == {"client_id": "c"}
        assert stat.S_IMODE(os.stat(path).st_mode) == 0o600
        await storage.delete_tokens("k")
        assert await storage.get_tokens("k") is None


class TestConcurrentSignIn:
    async def test_concurrent_first_requests_sign_in_once(self, fake):
        signins = []

        async def browser(url: str) -> str:
            signins.append(url)
            await asyncio.sleep(0.01)
            return fake.authorize(url)

        client = make_client(fake, client_metadata_url=CIMD_URL, authorization_handler=browser)
        responses = await asyncio.gather(*(client.request("GET") for _ in range(5)))
        assert all(r.status_code == 200 for r in responses)
        assert len(signins) == 1

    async def test_concurrent_dead_tokens_sign_in_once(self, fake):
        signins = []

        async def browser(url: str) -> str:
            signins.append(url)
            await asyncio.sleep(0.01)
            return fake.authorize(url)

        client = make_client(fake, client_metadata_url=CIMD_URL, authorization_handler=browser)
        await client.connect()
        fake.active_tokens.clear()
        fake.refresh_tokens.clear()
        responses = await asyncio.gather(*(client.request("GET") for _ in range(5)))
        assert all(r.status_code == 200 for r in responses)
        assert len(signins) == 2  # the first connect, then one shared sign-in
