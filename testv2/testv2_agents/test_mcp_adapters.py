"""
The MCP adapters, run inside a real ``MCPServer`` from the ``mcp`` package.

Skipped when the ``mcp`` extra isn't installed (it needs Python 3.10+).
"""

import sys

import pytest

if sys.version_info < (3, 10):
    pytest.skip("the mcp package needs Python 3.10+", allow_module_level=True)
pytest.importorskip("mcp")

from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402
from mcp.server.transport_security import TransportSecuritySettings  # noqa: E402
from mcp.shared.auth import OAuthClientInformationFull, OAuthMetadata, OAuthToken  # noqa: E402
from starlette.testclient import TestClient  # noqa: E402

from kinde_sdk.agents import AgentAuthConfig, KindeAgentAuth, find_bearer_challenge, has_permission  # noqa: E402
from kinde_sdk.agents.mcp import (  # noqa: E402
    KindeOAuthClientProvider,
    KindeTokenStorage,
    KindeTokenVerifier,
    get_agent_auth_context,
    kinde_auth_settings,
    mount_authorization_server_metadata,
)
from testv2.testv2_agents.kinde_fake import (  # noqa: E402
    APP_ID,
    APP_SECRET,
    ISSUER,
    RESOURCE_URL,
    FakeKinde,
    authorization_server_metadata,
    make_token,
)

INITIALIZE = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}},
}
HEADERS = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}


@pytest.fixture
def fake():
    return FakeKinde()


@pytest.fixture
def auth(fake):
    config = AgentAuthConfig(
        domain="test.kinde.com", client_id=APP_ID, client_secret=APP_SECRET, resource_url=RESOURCE_URL
    )
    return KindeAgentAuth(config, async_http_client=fake.async_client())


def make_server(auth):
    server = MCPServer("Test", token_verifier=KindeTokenVerifier(auth), auth=kinde_auth_settings(auth))

    @server.tool()
    async def whoami() -> str:
        context = get_agent_auth_context()
        if not has_permission(context, "read:docs"):
            raise ToolError("You don't have permission to read docs.")
        return f"{context.user_id} via {context.client_id}"

    mount_authorization_server_metadata(server, auth)
    app = server.streamable_http_app(
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )
    return app


class TestTokenVerifier:
    async def test_access_token_fields(self, fake, auth):
        token = fake.issue(permissions=["read:docs"])
        access = await KindeTokenVerifier(auth).verify_token(token)
        assert access.resource == RESOURCE_URL
        assert access.expires_at
        assert access.subject == "kp_user"
        assert access.client_id == "https://agent.example.com/cimd.json"
        assert access.scopes == ["offline"]
        assert access.claims["permissions"] == ["read:docs"]

    async def test_invalid_token_is_none(self, auth):
        assert await KindeTokenVerifier(auth).verify_token(make_token()) is None

    def test_auth_settings(self, auth):
        settings = kinde_auth_settings(auth)
        assert str(settings.issuer_url) == ISSUER
        assert str(settings.resource_server_url) == RESOURCE_URL
        assert settings.required_scopes == ["offline"]
        assert settings.validate_token_resource is True


class TestInsideMCPServer:
    def test_no_token_is_401_with_challenge(self, auth):
        with TestClient(make_server(auth)) as client:
            response = client.post("/mcp", json=INITIALIZE, headers=HEADERS)
        assert response.status_code == 401
        challenge = find_bearer_challenge(response.headers["www-authenticate"])
        assert challenge.get("resource_metadata") == "https://api.example.com/.well-known/oauth-protected-resource/mcp"

    def test_invalid_token_is_401_not_500(self, auth):
        with TestClient(make_server(auth)) as client:
            response = client.post(
                "/mcp", json=INITIALIZE, headers={**HEADERS, "Authorization": f"Bearer {make_token()}"}
            )
        assert response.status_code == 401

    def test_valid_token_and_permission_check_in_tool(self, fake, auth):
        allowed = fake.issue(permissions=["read:docs"])
        denied = fake.issue()
        call = {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "whoami", "arguments": {}}}
        with TestClient(make_server(auth)) as client:
            for token in (allowed, denied):
                assert (
                    client.post(
                        "/mcp", json=INITIALIZE, headers={**HEADERS, "Authorization": f"Bearer {token}"}
                    ).status_code
                    == 200
                )
            ok = client.post("/mcp", json=call, headers={**HEADERS, "Authorization": f"Bearer {allowed}"})
            refused = client.post("/mcp", json=call, headers={**HEADERS, "Authorization": f"Bearer {denied}"})
        assert ok.status_code == 200
        assert ok.json()["result"]["content"][0]["text"] == "kp_user via https://agent.example.com/cimd.json"
        # A missing permission is a tool error, never an HTTP 403 that would loop the agent through login
        assert refused.status_code == 200
        assert refused.json()["result"]["isError"] is True

    def test_kinde_outage_is_not_401(self, fake, auth):
        fake.introspection_raises = True
        with TestClient(make_server(auth), raise_server_exceptions=False) as client:
            response = client.post(
                "/mcp", json=INITIALIZE, headers={**HEADERS, "Authorization": f"Bearer {fake.issue()}"}
            )
        assert response.status_code >= 500

    def test_metadata_routes(self, auth):
        with TestClient(make_server(auth)) as client:
            prm = client.get("/.well-known/oauth-protected-resource/mcp").json()
            as_metadata = client.get("/.well-known/oauth-authorization-server").json()
        assert prm["authorization_servers"] == [ISSUER]
        assert prm["resource"] == RESOURCE_URL
        # Without offline here, agents never get a refresh token
        assert prm["scopes_supported"] == ["offline"]
        assert as_metadata["client_id_metadata_document_supported"] is True


class TestClientProvider:
    def provider(self, **options):
        return KindeOAuthClientProvider(
            RESOURCE_URL,
            client_name="Onzs Agent",
            client_metadata_url="https://agent.onzs.co.za/oauth/client-metadata.json",
            **options,
        )

    def test_client_metadata_defaults(self):
        metadata = self.provider().context.client_metadata
        assert metadata.scope == "offline"
        assert metadata.token_endpoint_auth_method == "none"
        assert metadata.grant_types == ["authorization_code", "refresh_token"]
        assert [str(uri) for uri in metadata.redirect_uris] == ["http://127.0.0.1:8765/callback"]

    def test_scope_strips_openid_and_adds_offline_on_kinde(self):
        provider = self.provider()
        provider.context.oauth_metadata = OAuthMetadata.model_validate(authorization_server_metadata())
        assert provider._kinde_scope("openid profile email") == "offline profile email"
        assert provider._kinde_scope(None) == "offline"

    def test_scope_untouched_on_servers_that_support_openid(self):
        provider = self.provider()
        metadata = {**authorization_server_metadata(), "scopes_supported": ["openid", "profile"]}
        provider.context.oauth_metadata = OAuthMetadata.model_validate(metadata)
        assert provider._kinde_scope("openid profile") == "openid profile"

    def test_rejects_bad_metadata_url(self):
        from kinde_sdk.agents import AgentConfigError

        with pytest.raises(AgentConfigError):
            KindeOAuthClientProvider(RESOURCE_URL, client_metadata_url="https://agent.onzs.co.za/")

    async def run_flow(self, fake, prm_scopes, **options):
        """Drive the real MCP client auth flow against the fake Kinde; return the authorization URL."""
        import httpx
        import httpx2
        from mcp.shared.auth import AuthorizationCodeResult

        fake.prm["scopes_supported"] = prm_scopes
        seen = {}

        def transport(request):
            response = fake.handle(
                httpx.Request(request.method, str(request.url), headers=request.headers.raw, content=request.read())
            )
            return httpx2.Response(
                response.status_code, headers=response.headers.raw, content=response.content, request=request
            )

        async def redirect_handler(url):
            seen["url"] = url

        async def callback_handler():
            callback = fake.authorize(seen["url"])
            query = {k: v[0] for k, v in __import__("urllib.parse").parse.parse_qs(callback.split("?", 1)[1]).items()}
            return AuthorizationCodeResult(code=query["code"], state=query["state"], iss=query.get("iss"))

        provider = self.provider(redirect_handler=redirect_handler, callback_handler=callback_handler, **options)
        async with httpx2.AsyncClient(transport=httpx2.MockTransport(transport), auth=provider) as client:
            response = await client.get(RESOURCE_URL)
        assert response.status_code == 200
        return seen["url"]

    async def test_real_flow_uses_cimd_and_offline(self, fake):
        from urllib.parse import parse_qs, urlsplit

        url = await self.run_flow(fake, ["offline"])
        query = {k: v[0] for k, v in parse_qs(urlsplit(url).query).items()}
        assert query["client_id"] == "https://agent.onzs.co.za/oauth/client-metadata.json"
        assert query["scope"] == "offline"
        assert fake.count("/register") == 0

    async def test_real_flow_strips_openid_from_a_challenge(self, fake):
        from urllib.parse import parse_qs, urlsplit

        # A resource advertising openid (as a generic OIDC-minded server might) must not break Kinde sign-in
        url = await self.run_flow(fake, ["openid", "profile"])
        scope = parse_qs(urlsplit(url).query)["scope"][0]
        assert scope.split() == ["offline", "profile"]

    async def test_real_flow_falls_back_to_dcr(self, fake):
        fake.as_metadata["client_id_metadata_document_supported"] = False
        await self.run_flow(fake, ["offline"])
        assert fake.count("/register") == 1

    async def test_token_storage_round_trip(self, tmp_path):
        from kinde_sdk.agents import FileAgentStorage

        storage = KindeTokenStorage(FileAgentStorage(str(tmp_path / "tokens.json")), key=RESOURCE_URL)
        await storage.set_tokens(OAuthToken(access_token="a", refresh_token="r", expires_in=60, scope="offline"))
        await storage.set_client_info(
            OAuthClientInformationFull(
                client_id="c", client_secret="s", redirect_uris=["http://127.0.0.1:8765/callback"]
            )
        )
        assert (await storage.get_tokens()).refresh_token == "r"
        assert (await storage.get_client_info()).client_secret == "s"
