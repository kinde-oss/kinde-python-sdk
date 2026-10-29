import pytest
from fastapi import Depends, FastAPI
from flask import Flask
from starlette.testclient import TestClient

from kinde_sdk.agents import (
    AgentAuthConfig,
    AgentConfigError,
    AgentAuthContext,
    KindeAgentAuth,
    build_client_metadata_document,
    find_bearer_challenge,
)
from kinde_fastapi.agents import FastAPIAgentAuth, client_metadata_router
from kinde_flask.agents import FlaskAgentAuth, client_metadata_blueprint, current_agent_auth
from testv2.testv2_agents.kinde_fake import APP_ID, APP_SECRET, ISSUER, RESOURCE_URL, FakeKinde, make_token

PRM_PATH = "/.well-known/oauth-protected-resource/mcp"
CIMD = build_client_metadata_document(
    "https://agent.onzs.co.za/oauth/client-metadata.json", "Onzs Agent", ["http://127.0.0.1/callback"]
)


@pytest.fixture
def fake():
    return FakeKinde()


@pytest.fixture
def auth(fake):
    config = AgentAuthConfig(
        domain="test.kinde.com", client_id=APP_ID, client_secret=APP_SECRET, resource_url=RESOURCE_URL
    )
    return KindeAgentAuth(config, http_client=fake.client(), async_http_client=fake.async_client())


@pytest.fixture
def fastapi_client(auth):
    app = FastAPI()
    agents = FastAPIAgentAuth(auth)
    agents.install(app)
    app.include_router(client_metadata_router(CIMD))

    @app.get("/mcp")
    async def mcp(context: AgentAuthContext = Depends(agents.require())):
        return {"user": context.user_id}

    @app.get("/docs-api")
    async def docs(context: AgentAuthContext = Depends(agents.require_permission("read:docs"))):
        return {"user": context.user_id}

    @app.get("/email")
    async def email(context: AgentAuthContext = Depends(agents.require("email"))):
        return {"user": context.user_id}

    return TestClient(app)


@pytest.fixture
def flask_client(auth):
    app = Flask(__name__)
    agents = FlaskAgentAuth(auth, app=app)
    app.register_blueprint(client_metadata_blueprint(CIMD))

    @app.get("/mcp")
    @agents.require()
    def mcp():
        return {"user": current_agent_auth().user_id}

    @app.get("/docs-api")
    @agents.require_permission("read:docs")
    async def docs():
        return {"user": current_agent_auth().user_id}

    @app.get("/email")
    @agents.require("email")
    def email():
        return {"user": current_agent_auth().user_id}

    return app.test_client()


# Both integrations must answer identically, so every test runs against each
@pytest.fixture(params=["fastapi", "flask"])
def client(request, fastapi_client, flask_client):
    return fastapi_client if request.param == "fastapi" else flask_client


def body(response):
    return response.json() if hasattr(response, "json") and callable(response.json) else response.get_json()


class TestIntegrations:
    def test_prm_at_path_suffixed_and_root(self, client):
        for path in (PRM_PATH, "/.well-known/oauth-protected-resource"):
            response = client.get(path)
            assert response.status_code == 200
            assert body(response)["authorization_servers"] == [ISSUER]
            assert body(response)["scopes_supported"] == ["offline"]
            assert response.headers["Access-Control-Allow-Origin"] == "*"

    def test_prm_preflight(self, client):
        response = client.options(PRM_PATH)
        assert response.status_code == 204
        assert "GET" in response.headers["Access-Control-Allow-Methods"]

    def test_as_mirror(self, client):
        response = client.get("/.well-known/oauth-authorization-server")
        assert body(response)["client_id_metadata_document_supported"] is True

    def test_no_token(self, client):
        response = client.get("/mcp")
        assert response.status_code == 401
        challenge = find_bearer_challenge(response.headers["WWW-Authenticate"])
        assert challenge.get("resource_metadata") == f"https://api.example.com{PRM_PATH}"
        assert challenge.get("error") is None
        assert response.headers["Access-Control-Expose-Headers"] == "WWW-Authenticate"
        assert body(response)["error"] == "unauthorized"

    def test_invalid_token(self, client):
        response = client.get("/mcp", headers={"Authorization": f"Bearer {make_token()}"})
        assert response.status_code == 401
        assert find_bearer_challenge(response.headers["WWW-Authenticate"]).get("error") == "invalid_token"
        assert body(response) == {"error": "invalid_token", "error_description": "The access token is not active"}

    def test_valid_token(self, client, fake):
        response = client.get("/mcp", headers={"Authorization": f"Bearer {fake.issue()}"})
        assert response.status_code == 200
        assert body(response) == {"user": "kp_user"}

    def test_missing_permission_is_plain_403(self, client, fake):
        response = client.get("/docs-api", headers={"Authorization": f"Bearer {fake.issue()}"})
        assert response.status_code == 403
        assert "WWW-Authenticate" not in response.headers
        assert body(response)["error"] == "forbidden"

    def test_permission_granted(self, client, fake):
        token = fake.issue(permissions=["read:docs"])
        assert client.get("/docs-api", headers={"Authorization": f"Bearer {token}"}).status_code == 200

    def test_missing_scope_is_insufficient_scope(self, client, fake):
        response = client.get("/email", headers={"Authorization": f"Bearer {fake.issue()}"})
        assert response.status_code == 403
        challenge = find_bearer_challenge(response.headers["WWW-Authenticate"])
        assert challenge.get("error") == "insufficient_scope"
        assert challenge.get("scope") == "email"

    def test_granted_scope_passes(self, client, fake):
        response = client.get("/email", headers={"Authorization": f"Bearer {fake.issue(scope='offline email')}"})
        assert response.status_code == 200
        assert body(response) == {"user": "kp_user"}

    def test_kinde_outage_is_503(self, client, fake):
        fake.introspection_status = 502
        response = client.get("/mcp", headers={"Authorization": f"Bearer {fake.issue()}"})
        assert response.status_code == 503
        assert "WWW-Authenticate" not in response.headers

    def test_query_string_token_ignored(self, client, fake):
        response = client.get(f"/mcp?access_token={fake.issue()}")
        assert response.status_code == 401

    def test_client_metadata_document(self, client):
        response = client.get("/oauth/client-metadata.json")
        assert response.status_code == 200
        assert body(response) == CIMD
        assert response.headers["Content-Type"] == "application/json"
        assert response.headers["Cache-Control"] == "public, max-age=3600"


ENCODED_CIMD = build_client_metadata_document(
    "https://agent.onzs.co.za/oauth/%66oo%20bar.json", "Onzs Agent", ["http://127.0.0.1/callback"]
)


def test_fastapi_serves_percent_encoded_client_id_path():
    app = FastAPI()
    app.include_router(client_metadata_router(ENCODED_CIMD))
    response = TestClient(app).get("/oauth/foo%20bar.json")
    assert response.status_code == 200
    assert response.json() == ENCODED_CIMD


def test_flask_serves_percent_encoded_client_id_path():
    app = Flask(__name__)
    app.register_blueprint(client_metadata_blueprint(ENCODED_CIMD))
    response = app.test_client().get("/oauth/foo%20bar.json")
    assert response.status_code == 200
    assert response.get_json() == ENCODED_CIMD


@pytest.mark.parametrize(
    "build, encoded",
    [(client_metadata_router, "%7Bname%7D"), (client_metadata_blueprint, "%3Cname%3E")],
)
def test_client_id_path_that_would_become_a_route_variable(build, encoded):
    document = build_client_metadata_document(
        f"https://agent.onzs.co.za/oauth/{encoded}.json", "Onzs Agent", ["http://127.0.0.1/callback"]
    )
    with pytest.raises(AgentConfigError):
        build(document)
