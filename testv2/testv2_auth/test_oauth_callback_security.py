"""
Security regression tests for the OAuth callback (``OAuth.handle_redirect``).

Covers:
  * state is always required: a callback is rejected unless a login was
    started by the SDK in this session (state stored) and the callback
    presents the same state (login CSRF / authorization code injection),
  * a nonce must have been stored for the login, the token response must
    contain an ID token, and its ``nonce`` claim must match the nonce sent
    in the authorization request,
  * stored state / nonce are single-use and cleared after the callback.

The standalone tests use the real in-memory storage path (null framework);
the Flask / FastAPI tests drive the real ``/login`` and ``/callback`` routes.
Only the network calls (token endpoint, userinfo) are mocked.
"""
import asyncio
import tempfile
from unittest.mock import patch, MagicMock, AsyncMock
from urllib.parse import urlparse, parse_qs

import jwt
import pytest

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.core.exceptions import KindeLoginException
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.core.storage.storage_manager import StorageManager

CLIENT_ID = "test_client_id"
REDIRECT_URI = "http://localhost/callback"


def _id_token(**claims):
    payload = {"sub": "kp_user", "aud": CLIENT_ID, "iss": "https://example.kinde.com"}
    payload.update(claims)
    # Signature is irrelevant here: the SDK decodes the ID token without
    # verifying the signature (token comes straight from the token endpoint).
    return jwt.encode(payload, "test-secret-key-of-sufficient-length-123", algorithm="HS256")


def _token_response(id_token=None, include_id_token=True):
    resp = MagicMock()
    resp.status_code = 200
    body = {
        "access_token": jwt.encode({"sub": "kp_user"}, "test-secret-key-of-sufficient-length-123", algorithm="HS256"),
        "token_type": "bearer",
        "expires_in": 3600,
    }
    if include_id_token:
        body["id_token"] = id_token
    resp.json.return_value = body
    resp.text = "ok"
    return resp


def _query(url):
    return {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}


@pytest.fixture
def isolated_singletons():
    """Isolate the process-wide StorageManager / FrameworkFactory singletons."""
    sm = StorageManager()
    saved = (sm._storage, sm._device_id, sm._storage_type)
    with patch.object(FrameworkFactory, "_framework_instance", None):
        yield
    sm._storage, sm._device_id, sm._storage_type = saved


@pytest.fixture
def standalone_oauth(isolated_singletons):
    oauth = OAuth(
        client_id=CLIENT_ID,
        client_secret="test_client_secret",
        redirect_uri=REDIRECT_URI,
        host="https://example.kinde.com",
    )
    return oauth


@pytest.fixture
def network():
    """Mock the token endpoint and userinfo lookup."""
    with patch("kinde_sdk.auth.oauth.requests.post") as post, \
         patch("kinde_sdk.auth.oauth.helper_get_user_details", new=AsyncMock(return_value={"id": "kp_user"})):
        yield post


def _storage():
    return StorageManager()


# ---------------------------------------------------------------------------
# Standalone (null framework, real memory storage)
# ---------------------------------------------------------------------------

class TestCallbackStateStandalone:

    def test_callback_without_state_rejected_when_state_stored(self, standalone_oauth, network):
        """(a) A callback with no `state` param must not reach token exchange."""
        asyncio.run(standalone_oauth.login())
        assert _storage().get("user:state") is not None

        network.return_value = _token_response(_id_token(nonce="whatever"))
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("attacker_code", "victim", None))
        network.assert_not_called()

    def test_callback_with_empty_state_rejected_when_state_stored(self, standalone_oauth, network):
        asyncio.run(standalone_oauth.login())
        network.return_value = _token_response(_id_token(nonce="whatever"))
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("attacker_code", "victim", ""))
        network.assert_not_called()

    def test_callback_with_wrong_state_rejected(self, standalone_oauth, network):
        asyncio.run(standalone_oauth.login())
        network.return_value = _token_response(_id_token(nonce="whatever"))
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("code", "victim", "not-the-state"))
        network.assert_not_called()

    def test_state_is_single_use(self, standalone_oauth, network):
        q = _query(asyncio.run(standalone_oauth.login()))
        network.return_value = _token_response(_id_token(nonce=q["nonce"]))
        asyncio.run(standalone_oauth.handle_redirect("code", "u1", q["state"]))
        assert _storage().get("user:state") is None
        assert _storage().get("user:nonce") is None
        assert _storage().get("user:code_verifier") is None

        network.reset_mock()
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("code", "u1", q["state"]))
        network.assert_not_called()

    def test_forged_callback_cannot_clear_pending_state(self, standalone_oauth, network):
        """A rejected callback must not consume the pending state; otherwise an
        attacker could send one forged callback to clear it and a second,
        state-less one that would then be accepted."""
        q = _query(asyncio.run(standalone_oauth.login()))
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("code", "victim", "not-the-state"))
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("attacker_code", "victim", None))
        network.assert_not_called()

        # The victim's genuine callback still completes.
        network.return_value = _token_response(_id_token(nonce=q["nonce"]))
        asyncio.run(standalone_oauth.handle_redirect("code", "victim", q["state"]))
        assert network.call_count == 1
        assert _storage().get("user:state") is None
        assert _storage().get("user:nonce") is None


class TestCallbackNoLoginInProgressStandalone:
    """Nothing stored (no SDK-started login in this session / already logged in)."""

    @pytest.mark.parametrize("state", [None, "", "attacker-state"])
    def test_callback_rejected_when_no_login_in_progress(self, standalone_oauth, network, state):
        assert _storage().get("user:state") is None
        network.return_value = _token_response(_id_token(nonce="x"))
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("attacker_code", "victim", state))
        network.assert_not_called()
        assert standalone_oauth._session_manager.get_token_manager("victim") is None

    def test_callback_rejected_after_completed_login(self, standalone_oauth, network):
        """Once a login has completed, a further (forged) callback is rejected
        and does not replace the established session."""
        q = _query(asyncio.run(standalone_oauth.login()))
        network.return_value = _token_response(_id_token(nonce=q["nonce"]))
        asyncio.run(standalone_oauth.handle_redirect("code", "victim", q["state"]))
        network.reset_mock()

        for state in (None, q["state"]):
            with pytest.raises(KindeLoginException):
                asyncio.run(standalone_oauth.handle_redirect("attacker_code", "victim", state))
        network.assert_not_called()


class TestCallbackNonceStandalone:

    def test_valid_state_and_nonce_accepted(self, standalone_oauth, network):
        q = _query(asyncio.run(standalone_oauth.login()))
        verifier = _storage().get("user:code_verifier")["value"]
        network.return_value = _token_response(_id_token(nonce=q["nonce"]))

        result = asyncio.run(standalone_oauth.handle_redirect("code", "u1", q["state"]))

        assert result["user"] == {"id": "kp_user"}
        sent = network.call_args.kwargs["data"]
        assert sent["code"] == "code"
        assert sent["code_verifier"] == verifier

    def test_id_token_with_wrong_nonce_rejected(self, standalone_oauth, network):
        """(b) An ID token whose nonce doesn't match the stored nonce is rejected."""
        q = _query(asyncio.run(standalone_oauth.login()))
        network.return_value = _token_response(_id_token(nonce="attacker-nonce"))
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("code", "u1", q["state"]))
        # No session must have been established for the user
        assert standalone_oauth._session_manager.get_token_manager("u1") is None
        assert _storage().get("user:nonce") is None

    def test_id_token_without_nonce_rejected(self, standalone_oauth, network):
        """(b) An ID token with no nonce claim is rejected when a nonce was sent."""
        q = _query(asyncio.run(standalone_oauth.login()))
        network.return_value = _token_response(_id_token())
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("code", "u1", q["state"]))
        assert standalone_oauth._session_manager.get_token_manager("u1") is None

    def test_undecodable_id_token_rejected(self, standalone_oauth, network):
        q = _query(asyncio.run(standalone_oauth.login()))
        network.return_value = _token_response("not-a-jwt")
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("code", "u1", q["state"]))

    def test_token_response_without_id_token_rejected(self, standalone_oauth, network):
        """Without an ID token the nonce can't be checked, so a swapped code from an
        authorization request without `openid` must not establish a session."""
        q = _query(asyncio.run(standalone_oauth.login()))
        network.return_value = _token_response(include_id_token=False)
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("code", "u1", q["state"]))
        assert standalone_oauth._session_manager.get_token_manager("u1") is None

    def test_missing_stored_nonce_rejected_before_token_exchange(self, standalone_oauth, network):
        """Losing the stored nonce must not turn nonce validation off."""
        q = _query(asyncio.run(standalone_oauth.login()))
        _storage().delete("user:nonce")
        network.return_value = _token_response(_id_token(nonce=q["nonce"]))
        with pytest.raises(KindeLoginException):
            asyncio.run(standalone_oauth.handle_redirect("code", "u1", q["state"]))
        network.assert_not_called()
        assert standalone_oauth._session_manager.get_token_manager("u1") is None


# ---------------------------------------------------------------------------
# Flask routes
# ---------------------------------------------------------------------------

@pytest.fixture
def flask_client(isolated_singletons, monkeypatch):
    from flask import Flask
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("SESSION_FILE_DIR", tempfile.mkdtemp(prefix="kinde_cb_test_"))
    app = Flask(__name__)
    OAuth(
        client_id=CLIENT_ID,
        client_secret="test_client_secret",
        redirect_uri=REDIRECT_URI,
        host="https://example.kinde.com",
        framework="flask",
        app=app,
    )
    app.config["TESTING"] = True
    return app.test_client()


class TestFlaskCallback:

    def test_callback_without_state_rejected(self, flask_client, network):
        r = flask_client.get("/login")
        assert r.status_code == 302
        network.return_value = _token_response(_id_token(nonce="x"))

        r = flask_client.get("/callback?code=attacker_code")

        assert r.status_code == 400
        network.assert_not_called()

    @pytest.mark.parametrize("qs", ["code=attacker_code", "code=attacker_code&state=attacker-state"])
    def test_callback_rejected_when_no_login_in_progress(self, flask_client, network, qs):
        network.return_value = _token_response(_id_token(nonce="x"))
        r = flask_client.get(f"/callback?{qs}")
        assert r.status_code == 400
        network.assert_not_called()

    def test_callback_wrong_nonce_rejected(self, flask_client, network):
        q = _query(flask_client.get("/login").headers["Location"])
        network.return_value = _token_response(_id_token(nonce="attacker-nonce"))
        r = flask_client.get(f"/callback?code=c&state={q['state']}")
        assert r.status_code == 400

    def test_callback_without_code_rejected_and_keeps_pending_login(self, flask_client, network):
        q = _query(flask_client.get("/login").headers["Location"])
        r = flask_client.get(f"/callback?state={q['state']}")
        assert r.status_code == 400
        network.assert_not_called()

        network.return_value = _token_response(_id_token(nonce=q["nonce"]))
        r = flask_client.get(f"/callback?code=c&state={q['state']}")
        assert r.status_code == 302
        assert network.call_args.kwargs["data"].get("code_verifier")

    def test_callback_happy_path(self, flask_client, network):
        q = _query(flask_client.get("/login").headers["Location"])
        network.return_value = _token_response(_id_token(nonce=q["nonce"]))
        r = flask_client.get(f"/callback?code=c&state={q['state']}")
        assert r.status_code == 302
        assert network.call_count == 1

    def test_unexpected_callback_error_returns_500_without_details(self, flask_client, network):
        q = _query(flask_client.get("/login").headers["Location"])
        failure = AsyncMock(side_effect=RuntimeError("internal-detail-do-not-show"))

        with patch.object(OAuth, "handle_redirect", failure):
            r = flask_client.get(f"/callback?code=c&state={q['state']}")

        assert failure.await_count == 1
        assert r.status_code == 500
        body = r.get_data(as_text=True)
        assert "internal-detail-do-not-show" not in body
        assert "RuntimeError" not in body
        with flask_client.session_transaction() as session:
            assert "user_id" not in session


# ---------------------------------------------------------------------------
# FastAPI routes
# ---------------------------------------------------------------------------

@pytest.fixture
def fastapi_client(isolated_singletons):
    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from starlette.middleware.sessions import SessionMiddleware
    app = FastAPI()
    OAuth(
        client_id=CLIENT_ID,
        client_secret="test_client_secret",
        redirect_uri=REDIRECT_URI,
        host="https://example.kinde.com",
        framework="fastapi",
        app=app,
    )
    app.add_middleware(SessionMiddleware, secret_key="test-secret")
    return TestClient(app, raise_server_exceptions=False, follow_redirects=False)


class TestFastAPICallback:

    def test_callback_without_state_rejected(self, fastapi_client, network):
        r = fastapi_client.get("/login")
        assert r.status_code in (302, 307)
        network.return_value = _token_response(_id_token(nonce="x"))

        r = fastapi_client.get("/callback?code=attacker_code")

        assert r.status_code == 400
        network.assert_not_called()

    @pytest.mark.parametrize("qs", ["code=attacker_code", "code=attacker_code&state=attacker-state"])
    def test_callback_rejected_when_no_login_in_progress(self, fastapi_client, network, qs):
        network.return_value = _token_response(_id_token(nonce="x"))
        r = fastapi_client.get(f"/callback?{qs}")
        assert r.status_code == 400
        network.assert_not_called()

    def test_callback_wrong_nonce_rejected(self, fastapi_client, network):
        q = _query(fastapi_client.get("/login").headers["location"])
        network.return_value = _token_response(_id_token(nonce="attacker-nonce"))
        r = fastapi_client.get(f"/callback?code=c&state={q['state']}")
        assert r.status_code == 400

    def test_callback_without_code_rejected_and_keeps_pending_login(self, fastapi_client, network):
        q = _query(fastapi_client.get("/login").headers["location"])
        r = fastapi_client.get(f"/callback?state={q['state']}")
        assert r.status_code == 400
        network.assert_not_called()

        # State, nonce and code verifier weren't consumed: the genuine callback still completes
        network.return_value = _token_response(_id_token(nonce=q["nonce"]))
        r = fastapi_client.get(f"/callback?code=c&state={q['state']}")
        assert r.status_code in (302, 307)
        assert network.call_args.kwargs["data"].get("code_verifier")

    def test_callback_happy_path(self, fastapi_client, network):
        q = _query(fastapi_client.get("/login").headers["location"])
        network.return_value = _token_response(_id_token(nonce=q["nonce"]))
        r = fastapi_client.get(f"/callback?code=c&state={q['state']}")
        assert r.status_code in (302, 307)
        assert network.call_count == 1

    def test_unexpected_callback_error_returns_500_without_details(self, fastapi_client, network):
        q = _query(fastapi_client.get("/login").headers["location"])
        failure = AsyncMock(side_effect=RuntimeError("internal-detail-do-not-show"))

        with patch.object(OAuth, "handle_redirect", failure):
            r = fastapi_client.get(f"/callback?code=c&state={q['state']}")

        assert failure.await_count == 1
        assert r.status_code == 500
        assert "internal-detail-do-not-show" not in r.text
        assert "RuntimeError" not in r.text
