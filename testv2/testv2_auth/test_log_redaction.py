"""
Regression tests: secrets must not reach logs or HTTP responses.

A full login -> callback -> refresh -> logout flow is driven for the
standalone client and for the real Flask / FastAPI routes with every SDK
logger at DEBUG. Afterwards no log output (including formatted exceptions)
and no HTTP response may contain the client secret, the authorization code,
the PKCE verifier, the OAuth state / nonce or any token value.

Failed token exchanges must not echo the token endpoint's response body,
either in the raised exception or in the callback's HTTP response.
"""
import asyncio
import logging
import tempfile
import threading
import time
from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import parse_qs, urlparse

import jwt
import pytest

from kinde_sdk.auth.api_options import ApiOptions
from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.token_manager import TokenManager
from kinde_sdk.core.exceptions import KindeTokenException
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.core.storage.storage_manager import StorageManager

CLIENT_ID = "redaction_client_id"
CLIENT_SECRET = "SECRET-client-secret-9f2c"
AUTH_CODE = "SECRET-auth-code-71bd"
REDIRECT_URI = "http://localhost/callback"
HOST = "https://example.kinde.com"
JWT_KEY = "test-secret-key-of-sufficient-length-123"
# Something a token endpoint might reflect back in an error body
REFLECTED = "SECRET-reflected-body-4e1a"


def _jwt(**claims):
    return jwt.encode(claims, JWT_KEY, algorithm="HS256")


class Tokens:
    def __init__(self, nonce, tag="1"):
        self.access = _jwt(sub="kp_user", tag=f"access-{tag}")
        self.refresh = f"SECRET-refresh-token-{tag}"
        self.id = _jwt(sub="kp_user", nonce=nonce, tag=f"id-{tag}")

    def response(self, expires_in=3600):
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {
            "access_token": self.access,
            "refresh_token": self.refresh,
            "id_token": self.id,
            "token_type": "bearer",
            "expires_in": expires_in,
        }
        resp.text = str(resp.json.return_value)
        return resp

    def values(self):
        return [self.access, self.refresh, self.id]


def _error_response(status=400):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = {"error": "invalid_grant", "error_description": f"bad code {REFLECTED}"}
    resp.text = f'{{"error":"invalid_grant","error_description":"bad code {REFLECTED}"}}'
    return resp


def _query(url):
    return {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}


def _assert_absent(haystack, secrets, where):
    for secret in secrets:
        assert secret and secret not in haystack, f"secret leaked into {where}: {secret[:12]}..."


@pytest.fixture
def isolated(monkeypatch):
    """Isolate the process-wide singletons the SDK relies on."""
    sm = StorageManager()
    saved = (sm._storage, sm._device_id, sm._storage_type)
    TokenManager.reset_instances()
    with patch.object(FrameworkFactory, "_framework_instance", None):
        yield
    sm._storage, sm._device_id, sm._storage_type = saved
    TokenManager.reset_instances()


class SdkLogs:
    """DEBUG output of the SDK's own loggers, exceptions included.

    Third-party access logs (e.g. the test client's) are left out: they log
    the callback URL, which carries the code and state by OAuth design.
    """

    def __init__(self, caplog):
        self._caplog = caplog

    @property
    def text(self):
        formatter = logging.Formatter("%(name)s %(message)s")
        return "\n".join(
            formatter.format(record)
            for record in self._caplog.records
            if record.name.startswith("kinde") or record.name == "root"
        )


@pytest.fixture
def debug_logs(caplog):
    caplog.set_level(logging.DEBUG)
    return SdkLogs(caplog)


@pytest.fixture
def network():
    """Token endpoint (exchange vs refresh / revoke) and userinfo lookup.

    Both SDK modules share the global ``requests.post``, so a single mock
    routes on the grant type.
    """
    exchange, token_manager_post = MagicMock(), MagicMock()

    def route(url, data=None, **kwargs):
        if url.endswith("/oauth2/token") and data and data.get("grant_type") == "authorization_code":
            return exchange(url, data=data, **kwargs)
        return token_manager_post(url, data=data, **kwargs)

    with patch("requests.post", side_effect=route), \
         patch("kinde_sdk.auth.oauth.helper_get_user_details", new=AsyncMock(return_value={"id": "kp_user"})):
        yield exchange, token_manager_post


# ---------------------------------------------------------------------------
# Standalone client
# ---------------------------------------------------------------------------

class TestStandaloneFlowLogs:

    def test_full_flow_logs_no_secrets(self, isolated, debug_logs, network):
        exchange, token_manager_post = network
        oauth = OAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, host=HOST)

        q = _query(asyncio.run(oauth.login()))
        verifier = StorageManager().get("user:code_verifier")["value"]
        first = Tokens(q["nonce"], "1")
        second = Tokens(q["nonce"], "2")
        # Expired right away, so the next access goes through the refresh path
        exchange.return_value = first.response(expires_in=0)
        token_manager_post.return_value = second.response()

        asyncio.run(oauth.handle_redirect(AUTH_CODE, "u1", q["state"]))
        assert oauth._session_manager.get_token_manager("u1").get_access_token() == second.access
        asyncio.run(oauth.logout("u1"))

        _assert_absent(
            debug_logs.text,
            [CLIENT_SECRET, AUTH_CODE, verifier, q["state"], q["nonce"], *first.values(), *second.values()],
            "logs",
        )

    def test_failed_exchange_does_not_echo_response_body(self, isolated, debug_logs, network):
        exchange, _ = network
        oauth = OAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, host=HOST)
        q = _query(asyncio.run(oauth.login()))
        exchange.return_value = _error_response()

        with pytest.raises(KindeTokenException) as exc_info:
            asyncio.run(oauth.handle_redirect(AUTH_CODE, "u1", q["state"]))

        message = str(exc_info.value)
        assert "400" in message and "invalid_grant" in message
        _assert_absent(message, [REFLECTED, AUTH_CODE, CLIENT_SECRET], "exception message")
        _assert_absent(debug_logs.text, [REFLECTED, AUTH_CODE, CLIENT_SECRET], "logs")

    def test_failed_exchange_with_non_json_body(self, isolated, network):
        exchange, _ = network
        oauth = OAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, host=HOST)
        q = _query(asyncio.run(oauth.login()))
        resp = MagicMock(status_code=502, text=f"<html>{REFLECTED}</html>")
        resp.json.side_effect = ValueError("not json")
        exchange.return_value = resp

        with pytest.raises(KindeTokenException) as exc_info:
            asyncio.run(oauth.handle_redirect(AUTH_CODE, "u1", q["state"]))
        assert "502" in str(exc_info.value)
        assert REFLECTED not in str(exc_info.value)

    def test_untrusted_error_code_is_dropped(self, isolated, network):
        exchange, _ = network
        oauth = OAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, host=HOST)
        q = _query(asyncio.run(oauth.login()))
        resp = _error_response()
        resp.json.return_value = {"error": f"<script>{REFLECTED}</script>"}
        exchange.return_value = resp

        with pytest.raises(KindeTokenException) as exc_info:
            asyncio.run(oauth.handle_redirect(AUTH_CODE, "u1", q["state"]))
        assert REFLECTED not in str(exc_info.value)


class TestExpiredTokenRefresh:

    def test_get_access_token_refreshes_without_deadlock(self, isolated, network):
        """get_access_token holds the lock while refreshing; set_tokens re-acquires it."""
        _, token_manager_post = network
        fresh = Tokens("n", "fresh")
        token_manager_post.return_value = fresh.response()
        tm = TokenManager("deadlock-user", CLIENT_ID, None, f"{HOST}/oauth2/token")
        tm.tokens = {"access_token": "old", "refresh_token": "r", "expires_at": time.time() - 1}

        result = {}
        worker = threading.Thread(target=lambda: result.setdefault("token", tm.get_access_token()), daemon=True)
        worker.start()
        worker.join(5)

        assert not worker.is_alive(), "get_access_token deadlocked while refreshing"
        assert result["token"] == fresh.access


# ---------------------------------------------------------------------------
# Flask routes
# ---------------------------------------------------------------------------

@pytest.fixture
def flask_app(isolated, monkeypatch):
    from flask import Flask
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("SESSION_FILE_DIR", tempfile.mkdtemp(prefix="kinde_redaction_test_"))
    app = Flask(__name__)
    oauth = OAuth(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,
        host=HOST, framework="flask", app=app,
    )
    app.config["TESTING"] = True
    return app, oauth


class TestFlaskRoutes:

    def test_full_flow_logs_and_responses_have_no_secrets(self, flask_app, debug_logs, network):
        exchange, token_manager_post = network
        app, oauth = flask_app
        client = app.test_client()

        q = _query(client.get("/login").headers["Location"])
        tokens = Tokens(q["nonce"])
        exchange.return_value = tokens.response()
        token_manager_post.return_value = MagicMock(status_code=200)

        callback = client.get(f"/callback?code={AUTH_CODE}&state={q['state']}")
        logout = client.get("/logout")

        assert callback.status_code == 302
        assert logout.status_code == 302
        _assert_absent(debug_logs.text, [CLIENT_SECRET, AUTH_CODE, q["state"], q["nonce"], *tokens.values()], "logs")
        _assert_absent(callback.get_data(as_text=True), [CLIENT_SECRET, *tokens.values()], "callback body")
        _assert_absent(callback.headers["Location"], [CLIENT_SECRET, AUTH_CODE, q["state"]], "callback redirect")
        # OIDC logout carries only the ID token, as id_token_hint
        assert _query(logout.headers["Location"]).get("id_token_hint") == tokens.id
        _assert_absent(logout.headers["Location"], [CLIENT_SECRET, tokens.access, tokens.refresh], "logout redirect")

    def test_failed_exchange_returns_generic_error(self, flask_app, debug_logs, network):
        exchange, _ = network
        app, _ = flask_app
        client = app.test_client()
        q = _query(client.get("/login").headers["Location"])
        exchange.return_value = _error_response()

        r = client.get(f"/callback?code={AUTH_CODE}&state={q['state']}")

        assert r.status_code == 400
        body = r.get_data(as_text=True)
        _assert_absent(body, [REFLECTED, AUTH_CODE, CLIENT_SECRET, "invalid_grant"], "response body")
        _assert_absent(debug_logs.text, [REFLECTED, AUTH_CODE, CLIENT_SECRET], "logs")

    def test_failed_callback_does_not_bind_session_user(self, flask_app, network):
        exchange, _ = network
        app, _ = flask_app
        client = app.test_client()
        q = _query(client.get("/login").headers["Location"])
        exchange.return_value = _error_response()

        client.get(f"/callback?code={AUTH_CODE}&state={q['state']}")

        with client.session_transaction() as session:
            assert "user_id" not in session


# ---------------------------------------------------------------------------
# FastAPI routes
# ---------------------------------------------------------------------------

@pytest.fixture
def fastapi_app(isolated):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from starlette.middleware.sessions import SessionMiddleware
    app = FastAPI()
    oauth = OAuth(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,
        host=HOST, framework="fastapi", app=app,
    )
    app.add_middleware(SessionMiddleware, secret_key="test-secret")
    return TestClient(app, raise_server_exceptions=False, follow_redirects=False), oauth


class TestFastAPIRoutes:

    def test_full_flow_logs_and_responses_have_no_secrets(self, fastapi_app, debug_logs, network):
        exchange, token_manager_post = network
        client, oauth = fastapi_app

        q = _query(client.get("/login").headers["location"])
        tokens = Tokens(q["nonce"])
        exchange.return_value = tokens.response()
        token_manager_post.return_value = MagicMock(status_code=200)

        callback = client.get(f"/callback?code={AUTH_CODE}&state={q['state']}")
        assert callback.status_code in (302, 307)
        assert len(oauth._session_manager.user_sessions) == 1

        logout = client.get("/logout")
        assert logout.status_code in (302, 307)

        _assert_absent(debug_logs.text, [CLIENT_SECRET, AUTH_CODE, q["state"], q["nonce"], *tokens.values()], "logs")
        _assert_absent(callback.text, [CLIENT_SECRET, *tokens.values()], "callback body")
        # The consumed state is not forwarded to the post-login page
        _assert_absent(callback.headers["location"], [AUTH_CODE, q["state"]], "callback redirect")
        assert _query(logout.headers["location"]).get("id_token_hint") == tokens.id
        _assert_absent(logout.headers["location"], [CLIENT_SECRET, tokens.access, tokens.refresh], "logout redirect")

    def test_logout_clears_server_side_tokens(self, fastapi_app, network):
        exchange, token_manager_post = network
        client, oauth = fastapi_app
        q = _query(client.get("/login").headers["location"])
        exchange.return_value = Tokens(q["nonce"]).response()
        token_manager_post.return_value = MagicMock(status_code=200)
        client.get(f"/callback?code={AUTH_CODE}&state={q['state']}")
        assert oauth._session_manager.user_sessions

        client.get("/logout")

        assert oauth._session_manager.user_sessions == {}
        # Best-effort revocation of the access token was attempted
        assert token_manager_post.call_args.args[0].endswith("/oauth2/revoke")

    def test_failed_exchange_returns_400_without_body_echo(self, fastapi_app, debug_logs, network):
        exchange, _ = network
        client, _ = fastapi_app
        q = _query(client.get("/login").headers["location"])
        exchange.return_value = _error_response()

        r = client.get(f"/callback?code={AUTH_CODE}&state={q['state']}")

        assert r.status_code == 400
        _assert_absent(r.text, [REFLECTED, AUTH_CODE, CLIENT_SECRET, "invalid_grant"], "response body")
        _assert_absent(debug_logs.text, [REFLECTED, AUTH_CODE, CLIENT_SECRET], "logs")


# ---------------------------------------------------------------------------
# Account API helpers
# ---------------------------------------------------------------------------

class TestAccountApiErrorLogs:
    """A failed Account API call logs the exception type and status, never the response body."""

    @pytest.fixture
    def api_error(self):
        from kinde_sdk.frontend.exceptions import ApiException
        error = ApiException(status=401, reason="Unauthorized")
        error.body = f'{{"errors":[{{"detail":"{REFLECTED}"}}]}}'
        return error

    @pytest.mark.parametrize("helper_name, api_path, method, call", [
        ("permissions", "kinde_sdk.auth.permissions.PermissionsApi", "get_user_permissions",
         lambda h: h.get_permission("read:x", ApiOptions(force_api=True))),
        ("roles", "kinde_sdk.auth.roles.RolesApi", "get_user_roles",
         lambda h: h.get_roles(ApiOptions(force_api=True))),
        ("feature_flags", "kinde_sdk.auth.feature_flags.FeatureFlagsApi", "get_feature_flags",
         lambda h: h.get_all_flags(ApiOptions(force_api=True))),
    ])
    def test_body_not_logged(self, debug_logs, api_error, helper_name, api_path, method, call):
        import importlib
        helper = getattr(importlib.import_module("kinde_sdk.auth"), helper_name)
        api = MagicMock()
        getattr(api, method).side_effect = api_error
        with patch.object(type(helper), "_create_authenticated_api_client", return_value=api), \
             patch.object(type(helper), "_get_token_manager", return_value=MagicMock()):
            try:
                asyncio.run(call(helper))
            except Exception:
                pass
        assert "ApiException (HTTP 401)" in debug_logs.text
        assert REFLECTED not in debug_logs.text
