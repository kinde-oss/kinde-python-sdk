import asyncio
import os
import stat
import sys
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
    TokenRequestError,
)
from kinde_sdk.agents.client import (
    _LoopbackListener,
    authorization_server_metadata_urls,
    protected_resource_metadata_urls,
    resource_covers,
)
from testv2.testv2_agents.kinde_fake import APP_ID, DOMAIN, ISSUER, RESOURCE_URL, FakeKinde

CIMD_URL = "https://agent.onzs.co.za/oauth/client-metadata.json"
REDIRECT = "http://127.0.0.1:8765/callback"
REGISTRATION_KEY = f"dcr|{RESOURCE_URL}|default"


@pytest.fixture
def fake():
    return FakeKinde()


def make_client(fake: FakeKinde, **options) -> KindeAgentClient:
    async def browser(url: str) -> str:
        return fake.authorize(url)

    options.setdefault("authorization_handler", browser)
    options.setdefault("redirect_uri", REDIRECT)
    return KindeAgentClient(RESOURCE_URL, http_client=fake.async_client(), **options)


def client_with_handler(handler, **options) -> KindeAgentClient:
    """A CIMD client whose HTTP calls go through ``handler`` (sync or async) instead of the fake directly."""
    fake = options.pop("fake")
    client = make_client(fake, client_metadata_url=CIMD_URL, **options)
    client._http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return client


def is_grant(request: httpx.Request, grant: str) -> bool:
    return request.url.path.endswith("/token") and f"grant_type={grant}".encode() in request.content


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
        registration = await storage.get_registration(REGISTRATION_KEY)
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

    async def test_non_json_registration_response(self, fake):
        fake._register = lambda request: httpx.Response(201, content=b"<html>ok</html>")
        with pytest.raises(RegistrationError, match="not JSON"):
            await make_client(fake).connect()

    async def test_non_string_client_id_in_registration(self, fake):
        fake._register = lambda request: httpx.Response(201, json={"client_id": 123, "client_secret": "s"})
        with pytest.raises(RegistrationError, match="no client_id"):
            await make_client(fake).connect()

    async def test_non_string_client_secret_in_registration(self, fake):
        fake._register = lambda request: httpx.Response(201, json={"client_id": "c", "client_secret": 123})
        with pytest.raises(RegistrationError, match="invalid client_secret"):
            await make_client(fake).connect()

    async def test_public_registration_without_secret(self, fake):
        storage = InMemoryAgentStorage()
        fake_register = fake._register

        def without_secret(request):
            body = fake_register(request).json()
            del body["client_secret"]
            body["token_endpoint_auth_method"] = "none"
            fake.registrations[body["client_id"]]["client_secret"] = None
            return httpx.Response(201, json=body)

        fake._register = without_secret
        await make_client(fake, storage=storage).connect()
        registration = await storage.get_registration(REGISTRATION_KEY)
        assert registration["client_secret"] is None
        assert registration["token_endpoint_auth_method"] == "none"
        exchange = next(r for r in fake.requests if b"grant_type=authorization_code" in r.content)
        assert "client_secret" not in form_of(exchange)

    async def test_accounts_get_their_own_registrations(self, fake):
        storage = InMemoryAgentStorage()
        await make_client(fake, storage=storage, account="a").connect()
        await make_client(fake, storage=storage, account="b").connect()
        a = await storage.get_registration(f"dcr|{RESOURCE_URL}|a")
        b = await storage.get_registration(f"dcr|{RESOURCE_URL}|b")
        assert a["client_id"] != b["client_id"]

    async def test_forget_leaves_other_accounts_working(self, fake):
        storage = InMemoryAgentStorage()
        await make_client(fake, storage=storage, account="a").connect()
        b = make_client(fake, storage=storage, account="b")
        await b.connect()
        await make_client(fake, storage=storage, account="a").disconnect(forget=True)
        assert await storage.get_registration(f"dcr|{RESOURCE_URL}|a") is None
        # b still refreshes with its own registration
        tokens = await storage.get_tokens(f"{RESOURCE_URL}|b")
        tokens["expires_at"] = time.time() - 10
        await storage.set_tokens(f"{RESOURCE_URL}|b", tokens)
        assert await b.refresh(stale_access_token=tokens["access_token"]) is not None
        assert fake.count("/register") == 2

    async def test_new_redirect_uri_replaces_the_registration(self, fake):
        storage = InMemoryAgentStorage()
        await make_client(fake, storage=storage, redirect_uri="http://127.0.0.1:8001/callback").connect()
        await storage.delete_tokens(f"{RESOURCE_URL}|default")
        await make_client(fake, storage=storage, redirect_uri="http://127.0.0.1:8002/callback").connect()
        assert fake.count("/register") == 2
        # One registration slot per account, holding the latest
        registration = await storage.get_registration(REGISTRATION_KEY)
        assert registration["redirect_uri"] == "http://127.0.0.1:8002/callback"
        assert set(storage._registrations) == {REGISTRATION_KEY}

    async def test_invalid_client_keeps_a_newer_registration(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, storage=storage)
        await client.connect()
        tokens = await storage.get_tokens(f"{RESOURCE_URL}|default")
        # Another process re-registered this account since these tokens were issued
        newer = {**(await storage.get_registration(REGISTRATION_KEY)), "client_id": "newer"}
        await storage.set_registration(REGISTRATION_KEY, newer)
        await client._drop_registration({"client_id": tokens["client_id"], "registration_key": REGISTRATION_KEY})
        assert (await storage.get_registration(REGISTRATION_KEY))["client_id"] == "newer"

    async def test_invalid_client_on_code_exchange_drops_registration(self, fake):
        storage = InMemoryAgentStorage()

        async def browser(url: str) -> str:
            callback = fake.authorize(url)
            fake.registrations.clear()  # Kinde dropped the registration mid sign-in
            return callback

        with pytest.raises(TokenRequestError, match="invalid_client"):
            await make_client(fake, storage=storage, authorization_handler=browser).connect()
        assert await storage.get_registration(REGISTRATION_KEY) is None
        # The next sign-in registers again and works
        await make_client(fake, storage=storage).connect()
        assert fake.count("/register") == 2

    async def test_tokens_for_a_replaced_registration_need_a_new_sign_in(self, fake):
        storage = InMemoryAgentStorage()
        await make_client(fake, storage=storage, redirect_uri="http://127.0.0.1:8001/callback").connect()
        old_tokens = await storage.get_tokens(f"{RESOURCE_URL}|default")
        # Another sign-in on a new port replaced this account's registration
        await make_client(fake, storage=storage, redirect_uri="http://127.0.0.1:8002/callback").authorize()
        assert fake.count("/register") == 2
        await storage.set_tokens(f"{RESOURCE_URL}|default", {**old_tokens, "expires_at": time.time() - 10})
        client = make_client(fake, storage=storage, redirect_uri="http://127.0.0.1:8002/callback")
        assert await client.refresh(stale_access_token=old_tokens["access_token"]) is None
        assert await storage.get_tokens(f"{RESOURCE_URL}|default") is None

    @pytest.mark.parametrize("value", ["2030-01-01", True, [1]])
    async def test_invalid_secret_expiry_in_registration(self, fake, value):
        fake._register = lambda request: httpx.Response(
            201, json={"client_id": "c", "client_secret": "s", "client_secret_expires_at": value}
        )
        with pytest.raises(RegistrationError, match="client_secret_expires_at"):
            await make_client(fake).connect()

    @pytest.mark.parametrize("storage_class", ["memory", "file"])
    async def test_drop_registration_is_compare_and_delete(self, fake, tmp_path, storage_class):
        storage = InMemoryAgentStorage() if storage_class == "memory" else FileAgentStorage(str(tmp_path / "t.json"))
        client = make_client(fake, storage=storage)
        await storage.set_registration(REGISTRATION_KEY, {"client_id": "newer"})
        await client._drop_registration({"client_id": "older", "registration_key": REGISTRATION_KEY})
        assert (await storage.get_registration(REGISTRATION_KEY))["client_id"] == "newer"
        await client._drop_registration({"client_id": "newer", "registration_key": REGISTRATION_KEY})
        assert await storage.get_registration(REGISTRATION_KEY) is None

    async def test_drop_registration_without_compare_and_delete(self, fake):
        class BasicStorage:
            """A custom store with only the required methods."""

            def __init__(self):
                self.inner = InMemoryAgentStorage()

            def __getattr__(self, name):
                if name == "delete_registration_if_client":
                    raise AttributeError(name)
                return getattr(self.inner, name)

        storage = BasicStorage()
        client = make_client(fake, storage=storage)
        await storage.set_registration(REGISTRATION_KEY, {"client_id": "newer"})
        await client._drop_registration({"client_id": "older", "registration_key": REGISTRATION_KEY})
        assert (await storage.get_registration(REGISTRATION_KEY))["client_id"] == "newer"
        await client._drop_registration({"client_id": "newer", "registration_key": REGISTRATION_KEY})
        assert await storage.get_registration(REGISTRATION_KEY) is None

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

    async def test_signs_in_again_when_the_refreshed_token_is_refused(self, fake):
        refused = set()

        def handler(request):
            response = fake.handle(request)
            if is_grant(request, "refresh_token"):
                refused.add(response.json()["access_token"])  # the resource refuses refreshed tokens too
            bearer = request.headers.get("authorization", "")[7:]
            if request.url.host == "api.example.com" and bearer in refused:
                return httpx.Response(401, headers={"WWW-Authenticate": 'Bearer error="invalid_token"'})
            return response

        client = client_with_handler(handler, fake=fake)
        await client.connect()
        refused.add(await client.get_access_token())
        response = await client.request("GET")
        assert response.status_code == 200
        assert len([r for r in fake.requests if is_grant(r, "authorization_code")]) == 2

    async def test_scope_missing_from_the_token_response_is_the_requested_scope(self, fake):
        def handler(request):
            response = fake.handle(request)
            if request.url.path.endswith("/token"):
                body = {k: v for k, v in response.json().items() if k != "scope"}
                return httpx.Response(response.status_code, json=body)
            return response

        client = client_with_handler(handler, fake=fake, scopes=["offline", "email"])
        await client.connect()
        assert (await client.get_token_info())["scopes"] == ["offline", "email"]

    async def test_short_lived_tokens_are_not_refreshed_on_every_call(self, fake):
        def handler(request):
            response = fake.handle(request)
            if request.url.path.endswith("/token") and response.status_code == 200:
                return httpx.Response(200, json={**response.json(), "expires_in": 60})
            return response

        client = client_with_handler(handler, fake=fake)
        await client.connect()
        for _ in range(3):
            assert (await client.request("GET")).status_code == 200
        assert not [r for r in fake.requests if is_grant(r, "refresh_token")]

    def test_refresh_margin_is_at_most_half_the_lifetime(self):
        now = time.time()
        assert KindeAgentClient._expiring({"expires_at": now + 40, "expires_in": 60}) is False
        assert KindeAgentClient._expiring({"expires_at": now + 20, "expires_in": 60}) is True
        # Long-lived, and tokens stored before the lifetime was kept: the usual 60 seconds
        assert KindeAgentClient._expiring({"expires_at": now + 50, "expires_in": 86400}) is True
        assert KindeAgentClient._expiring({"expires_at": now + 50}) is True
        assert KindeAgentClient._expiring({"expires_at": now + 120}) is False

    @pytest.mark.parametrize("storage_class", ["memory", "file", "basic"])
    async def test_invalid_grant_keeps_tokens_another_client_just_rotated(self, fake, tmp_path, storage_class):
        class BasicStorage:
            """A custom store with only the required methods."""

            def __init__(self):
                self.inner = InMemoryAgentStorage()

            def __getattr__(self, name):
                if name == "delete_tokens_if_refresh_token":
                    raise AttributeError(name)
                return getattr(self.inner, name)

        storage = {
            "memory": InMemoryAgentStorage,
            "file": lambda: FileAgentStorage(str(tmp_path / "t.json")),
            "basic": BasicStorage,
        }[storage_class]()
        fake.rotate_refresh_tokens = True
        other = make_client(fake, client_metadata_url=CIMD_URL, storage=storage)
        await other.connect()

        async def handler(request):
            if is_grant(request, "refresh_token"):
                # The other client (another process) rotates the same refresh token first
                await other.refresh()
            return fake.handle(request)

        client = client_with_handler(handler, fake=fake, storage=storage)
        tokens = await client.refresh()
        stored = await storage.get_tokens(f"{RESOURCE_URL}|default")
        assert stored is not None and tokens == stored
        assert stored["refresh_token"] in fake.refresh_tokens

    async def test_invalid_client_keeps_tokens_another_client_just_saved(self, fake):
        storage = InMemoryAgentStorage()
        await make_client(fake, storage=storage).connect()
        key = f"{RESOURCE_URL}|default"
        old = await storage.get_tokens(key)
        newer = {**old, "access_token": "newer-access", "refresh_token": "newer-refresh"}

        async def handler(request):
            if is_grant(request, "refresh_token"):
                # Another process signs in again and saves a new pair before Kinde answers
                await storage.set_tokens(key, newer)
                return httpx.Response(401, json={"error": "invalid_client"})
            return fake.handle(request)

        client = make_client(fake, storage=storage)
        client._http = httpx.AsyncClient(transport=httpx.MockTransport(handler))
        assert await client.refresh() == newer
        assert await storage.get_tokens(key) == newer

    async def test_missing_registration_keeps_tokens_another_client_just_saved(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, storage=storage)
        await client.connect()
        key = f"{RESOURCE_URL}|default"
        old = await storage.get_tokens(key)
        newer = {**old, "access_token": "newer-access", "refresh_token": "newer-refresh"}

        async def no_identity(tokens):
            # Another process replaced the registration and saved a new pair in the meantime
            await storage.set_tokens(key, newer)
            return None

        client._identity_for_tokens = no_identity
        assert await client.refresh() == newer
        assert await storage.get_tokens(key) == newer

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
        assert await storage.get_registration(REGISTRATION_KEY) is None

    async def test_disconnect_forget_without_tokens_drops_registration(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, storage=storage)
        await client.connect()
        await storage.delete_tokens(f"{RESOURCE_URL}|default")  # e.g. after invalid_grant
        await client.disconnect(forget=True)
        assert await storage.get_registration(REGISTRATION_KEY) is None

    async def test_disconnect_forget_works_without_discovery(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, storage=storage)
        await client.connect()
        await storage.delete_tokens(f"{RESOURCE_URL}|default")
        fake.prm = None  # discovery now fails
        client._metadata_at = 0
        await client.disconnect(forget=True)
        assert await storage.get_registration(REGISTRATION_KEY) is None

    async def test_disconnect_forget_finds_registration_under_bound_port(self, fake):
        async def open_browser(url: str):
            callback = fake.authorize(url)

            async def follow():
                async with httpx.AsyncClient() as browser:
                    await browser.get(callback)

            asyncio.get_running_loop().create_task(follow())

        storage = InMemoryAgentStorage()
        # The default redirect has no port, so the registration is stored under the port the listener bound
        client = KindeAgentClient(
            RESOURCE_URL, storage=storage, open_browser=open_browser, http_client=fake.async_client()
        )
        await client.connect()
        key = (await storage.get_tokens(f"{RESOURCE_URL}|default"))["registration_key"]
        assert (await storage.get_registration(key))["redirect_uri"] != "http://127.0.0.1/callback"
        await storage.delete_tokens(f"{RESOURCE_URL}|default")
        await client.disconnect(forget=True)
        assert await storage.get_registration(key) is None

    async def test_disconnect_never_revokes_at_a_new_issuer(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, storage=storage)
        await client.connect()
        key = f"{RESOURCE_URL}|default"
        tokens = await storage.get_tokens(key)
        await storage.set_tokens(key, {**tokens, "issuer": "https://old.example.com"})
        client._metadata_at = 0
        await client.disconnect()
        assert fake.count("/revoke") == 0
        assert await storage.get_tokens(key) is None

    async def test_refresh_never_sends_tokens_to_a_new_issuer(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, client_metadata_url=CIMD_URL, storage=storage)
        await client.connect()
        key = f"{RESOURCE_URL}|default"
        tokens = await storage.get_tokens(key)
        await storage.set_tokens(key, {**tokens, "issuer": "https://old.example.com"})
        client._metadata_at = 0  # metadata cache expired, so refresh() discovers again
        assert await client.refresh() is None
        assert not [r for r in fake.requests if b"grant_type=refresh_token" in r.content]

    async def test_tokens_dropped_when_issuer_changes(self, fake):
        storage = InMemoryAgentStorage()
        client = make_client(fake, client_metadata_url=CIMD_URL, storage=storage)
        await client.connect()
        tokens = await storage.get_tokens(f"{RESOURCE_URL}|default")
        await storage.set_tokens(f"{RESOURCE_URL}|default", {**tokens, "issuer": "https://old.example.com"})
        await client.discover(force=True)
        assert await storage.get_tokens(f"{RESOURCE_URL}|default") is None


class TestDiscovery:
    async def test_remote_resource_cannot_point_metadata_at_loopback(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        challenge = httpx.Response(
            401, headers={"WWW-Authenticate": 'Bearer resource_metadata="http://127.0.0.1:9/admin"'}
        )
        await client.discover(challenge)
        assert not [r for r in fake.requests if r.url.host == "127.0.0.1"]

    async def test_remote_resource_cannot_name_a_loopback_issuer(self, fake):
        fake.prm["authorization_servers"] = ["http://127.0.0.1:9/oauth2"]
        with pytest.raises(DiscoveryError, match="loopback authorization server"):
            await make_client(fake, client_metadata_url=CIMD_URL).discover()
        assert not [r for r in fake.requests if r.url.host == "127.0.0.1"]

    @pytest.mark.parametrize("endpoint", ["token_endpoint", "registration_endpoint", "revocation_endpoint"])
    async def test_remote_authorization_server_cannot_name_loopback_endpoints(self, fake, endpoint):
        fake.as_metadata[endpoint] = "http://localhost:9/admin"
        with pytest.raises(DiscoveryError, match="loopback"):
            await make_client(fake).discover()

    def test_loopback_resource_may_use_a_loopback_issuer(self):
        from kinde_sdk.agents.client import _refuse_loopback_from_remote

        _refuse_loopback_from_remote("http://127.0.0.1:8000/oauth2", "http://localhost:3001/mcp", "issuer")
        with pytest.raises(DiscoveryError):
            _refuse_loopback_from_remote("http://127.0.0.1:8000/oauth2", RESOURCE_URL, "issuer")

    async def test_sends_the_resource_the_metadata_names(self, fake):
        fake.prm["resource"] = "https://api.example.com/"  # a parent of the URL the agent calls
        storage = InMemoryAgentStorage()
        client = make_client(fake, client_metadata_url=CIMD_URL, storage=storage)
        authorizations = []

        async def browser(url):
            authorizations.append(url)
            return fake.authorize(url)

        client.authorization_handler = browser
        assert (await client.request("GET")).status_code == 200
        await client.refresh()
        assert query_of(authorizations[0])["resource"] == "https://api.example.com/"
        grants = [form_of(r) for r in fake.requests if r.url.path.endswith("/token")]
        assert [grant["resource"] for grant in grants] == ["https://api.example.com/"] * 2
        # Requests still go to the URL the developer gave
        assert any(str(r.url) == RESOURCE_URL for r in fake.requests)

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
    async def test_code_never_exchanged_with_a_new_issuer(self, fake):
        client = make_client(fake, client_metadata_url=CIMD_URL)
        pending = await client.begin_authorization()
        callback = fake.authorize(pending.authorization_url)
        other = {
            **client._as_metadata,
            "issuer": "https://evil.example.com",
            "token_endpoint": "https://evil.example.com/t",
        }

        async def discover(*args, **kwargs):
            return other

        client.discover = discover
        with pytest.raises(AuthorizationError, match="changed since sign-in started"):
            await client.complete_authorization(pending, callback)
        assert not [r for r in fake.requests if r.url.host == "evil.example.com"]

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

        forged = []

        async def open_browser(url: str):
            opened.append(url)
            callback = fake.authorize(url)

            async def follow():
                async with httpx.AsyncClient() as browser:
                    # Another local process calls the callback first: ignored, and sign-in still completes
                    redirect = query_of(url)["redirect_uri"]
                    forged.append((await browser.get(f"{redirect}?code=x&state=wrong")).status_code)
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
        assert forged == [404]
        assert redirect_uri.startswith("http://127.0.0.1:") and redirect_uri.endswith("/callback")
        assert (await client.get_token_info())["client_id"] == CIMD_URL


async def test_loopback_listener_keeps_the_redirect_query():
    listener = _LoopbackListener("http://127.0.0.1/callback?tenant=1")
    await listener.start()
    try:
        assert listener.redirect_uri.startswith("http://127.0.0.1:")
        assert listener.redirect_uri.endswith("/callback?tenant=1")
        listener.expected_state = "s"
        async with httpx.AsyncClient() as browser:
            response = await browser.get(listener.redirect_uri + "&code=c&state=s")
        assert response.status_code == 200
        assert query_of(await listener.wait(1)) == {"tenant": "1", "code": "c", "state": "s"}
    finally:
        await listener.close()


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

    async def test_concurrent_processes_do_not_lose_updates(self, tmp_path):
        path = str(tmp_path / "tokens.json")
        script = (
            "import asyncio, sys\n"
            "from kinde_sdk.agents import FileAgentStorage\n"
            "async def main():\n"
            "    storage = FileAgentStorage(sys.argv[1])\n"
            "    for i in range(25):\n"
            "        await storage.set_tokens(f'{sys.argv[2]}-{i}', {'access_token': 'a'})\n"
            "asyncio.run(main())\n"
        )
        processes = [
            await asyncio.create_subprocess_exec(sys.executable, "-c", script, path, f"p{n}") for n in range(4)
        ]
        assert [await p.wait() for p in processes] == [0, 0, 0, 0]
        storage = FileAgentStorage(path)
        for n in range(4):
            for i in range(25):
                assert await storage.get_tokens(f"p{n}-{i}") is not None


    async def test_failed_lock_closes_the_file_and_keeps_the_error(self, tmp_path, monkeypatch):
        from kinde_sdk.agents import storage as storage_module

        calls = []

        class FakeMsvcrt:
            LK_LOCK, LK_UNLCK = 1, 0

            @staticmethod
            def locking(fd, mode, size):
                calls.append(mode)
                if mode == FakeMsvcrt.LK_LOCK:
                    raise OSError("lock timed out")  # what Windows does after about 10 seconds

        closed = []
        real_close = os.close
        monkeypatch.setattr(storage_module, "fcntl", None)
        monkeypatch.setattr(storage_module, "msvcrt", FakeMsvcrt, raising=False)
        monkeypatch.setattr(storage_module.os, "close", lambda fd: (closed.append(fd), real_close(fd)))
        storage = FileAgentStorage(str(tmp_path / "tokens.json"))
        with pytest.raises(OSError, match="lock timed out"):
            await storage.set_tokens("k", {"access_token": "a"})
        assert calls == [FakeMsvcrt.LK_LOCK]  # never unlocks a lock it didn't get
        assert len(closed) == 1

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
