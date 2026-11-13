"""
Step-up authentication through the Flask integration.

A real Flask app, the real Kinde routes and the real OAuth client. Only the
network is faked (the ``http`` fixture in ``testv2/conftest.py``).
"""

import asyncio
import threading
import time
from contextlib import contextmanager
from types import SimpleNamespace

import pytest
from flask import Flask, jsonify, redirect

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.core.exceptions import (
    KindeCallbackError,
    LoginRequiredError,
    UnmetAuthenticationRequirementsError,
)
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from testv2.step_up_helpers import (
    HOST,
    query,
    token_response,
)

UNMET = "unmet_authentication_requirements"
UNMET_DESCRIPTION = "The requested authentication context could not be met"


def build_app(configure=None):
    """A Flask app with Kinde wired in, and a route that requires recent MFA."""
    app = Flask(__name__)
    app.testing = True
    if configure:
        configure(app)

    oauth = OAuth(
        client_id="test_client_id",
        client_secret="test_client_secret",
        redirect_uri="http://localhost/callback",
        framework="flask",
        app=app,
        host=HOST,
    )

    @app.route("/payouts", methods=["GET", "POST"])
    def payouts():
        if not oauth.is_authenticated():
            return redirect("/login")
        if not oauth.has_authentication_context(acr="mfa", max_age=300):
            return redirect(asyncio.run(oauth.step_up(acr="mfa", max_age=300)))
        return "payouts"

    @app.route("/transfer", methods=["POST"])
    def transfer():
        return redirect(
            asyncio.run(
                oauth.step_up(acr="phr", post_login_redirect_url="/transfer/confirm")
            )
        )

    @app.route("/mfa-login")
    def mfa_login():
        return redirect(asyncio.run(oauth.login({"acr_values": "mfa"})))

    # A request that is still in flight while other requests come and go
    app.gate = SimpleNamespace(entered=threading.Event(), release=threading.Event())

    @app.route("/slow")
    def slow():
        app.gate.entered.set()
        app.gate.release.wait(10)
        return jsonify(
            authenticated=oauth.is_authenticated(),
            context=oauth.get_authentication_context(),
        )

    @app.route("/whoami")
    def whoami():
        return jsonify(
            authenticated=oauth.is_authenticated(),
            context=oauth.get_authentication_context(),
        )

    return app, oauth


@pytest.fixture
def flask_env(http, monkeypatch, tmp_path):
    monkeypatch.setenv("SECRET_KEY", "test-secret")
    monkeypatch.setenv("SESSION_FILE_DIR", str(tmp_path))
    # The framework is a process-wide singleton: start each test without one
    monkeypatch.setattr(FrameworkFactory, "_framework_instance", None)
    return http


@pytest.fixture
def site(flask_env):
    app, oauth = build_app()
    return SimpleNamespace(
        app=app, oauth=oauth, client=app.test_client(), http=flask_env
    )


def sign_in(site):
    response = site.client.get("/login")
    assert response.status_code == 302
    site.http.token_responses.append(
        token_response("login", id_claims={"auth_time": int(time.time()) - 3600})
    )
    response = site.client.get(
        f"/callback?code=login_code&state={query(response.location)['state']}"
    )
    assert response.status_code == 302
    return response


def sign_in_with_an_expired_access_token(site):
    """Sign in with a refresh token and an access token that has already expired."""
    response = site.client.get("/login")
    site.http.token_responses.append({**token_response("login"), "expires_in": -1})
    return site.client.get(
        f"/callback?code=login_code&state={query(response.location)['state']}"
    )


def start_step_up(site, path="/payouts?tab=bank"):
    response = site.client.get(path)
    assert response.status_code == 302
    assert response.location.startswith(f"{HOST}/oauth2/auth?")
    return query(response.location)


def stepped_up_tokens():
    claims = {"acr": "mfa", "amr": ["pwd", "totp"], "auth_time": int(time.time())}
    return token_response("step-up", access_claims={"acr": "mfa"}, id_claims=claims)


@contextmanager
def request_in_flight(site):
    """
    A request from the same browser that has loaded its session and is still
    running. It finishes, and writes its session back, when the block ends.
    """
    cookie = site.client.get_cookie("session").value
    result = {}

    def run():
        client = site.app.test_client()
        client.set_cookie("session", cookie)
        result["response"] = client.get("/slow")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    assert site.app.gate.entered.wait(10)
    try:
        yield result
    finally:
        site.app.gate.release.set()
        thread.join(10)
    assert not thread.is_alive()


def assert_not_sent_anywhere(response):
    """The response is not a redirect, to login or anywhere else."""
    assert response.status_code not in (301, 302, 303, 307, 308)
    assert "Location" not in response.headers


class TestFlaskStepUp:
    def test_login_callback_is_unchanged(self, site):
        response = sign_in(site)
        assert response.location == "http://localhost/"
        assert site.client.get("/whoami").get_json()["authenticated"] is True

    def test_step_up_request_is_interactive_and_carries_the_requirement(self, site):
        sign_in(site)
        params = start_step_up(site)
        assert params["acr_values"] == "mfa"
        assert params["max_age"] == "300"
        assert "prompt" not in params

    def test_user_lands_back_where_they_started(self, site):
        sign_in(site)
        params = start_step_up(site, "/payouts?tab=bank")

        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            f"/callback?code=step_up_code&state={params['state']}"
        )

        assert response.status_code == 302
        assert response.location == "http://localhost/payouts?tab=bank"
        response = site.client.get("/payouts?tab=bank")
        assert (
            response.status_code == 200 and response.get_data(as_text=True) == "payouts"
        )

    def test_successful_step_up_replaces_the_session_tokens(self, site):
        sign_in(site)
        assert site.client.get("/whoami").get_json()["context"]["acr"] is None
        params = start_step_up(site)

        tokens = stepped_up_tokens()
        site.http.token_responses.append(tokens)
        site.client.get(f"/callback?code=step_up_code&state={params['state']}")

        context = site.client.get("/whoami").get_json()["context"]
        assert context["acr"] == "mfa" and context["amr"] == ["pwd", "totp"]
        # What the session holds, not only what is in memory
        with site.client.session_transaction() as session:
            session_key = next(
                key for key in session if key.endswith(f":{session['user_id']}")
            )
            stored = session[session_key]["tokens"]
        assert stored["access_token"] == tokens["access_token"]
        assert stored["id_token"] == tokens["id_token"]
        assert stored["refresh_token"] == "refresh-step-up"

    def test_a_post_is_not_replayed(self, site):
        sign_in(site)
        response = site.client.post("/payouts")
        params = query(response.location)

        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            f"/callback?code=step_up_code&state={params['state']}"
        )

        assert response.location == "http://localhost/"

    def test_a_post_does_not_inherit_an_abandoned_return_location(self, site):
        sign_in(site)
        start_step_up(site, "/payouts?tab=bank")  # started, then abandoned

        params = query(site.client.post("/payouts").location)
        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            f"/callback?code=step_up_code&state={params['state']}"
        )

        assert response.location == "http://localhost/"

    def test_explicit_return_location(self, site):
        sign_in(site)
        response = site.client.post("/transfer")
        params = query(response.location)
        assert params["acr_values"] == "phr"

        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            f"/callback?code=step_up_code&state={params['state']}"
        )

        assert response.location == "http://localhost/transfer/confirm"


class TestFlaskOverlappingRequests:
    """
    Flask-Session writes a request's whole session back when the request ends,
    so a request that began before the tokens changed puts the old ones back.
    """

    def test_request_in_flight_during_a_step_up_does_not_undo_it(self, site):
        sign_in(site)

        with request_in_flight(site) as slow:
            params = start_step_up(site, "/payouts")
            tokens = stepped_up_tokens()
            site.http.token_responses.append(tokens)
            site.client.get(f"/callback?code=step_up_code&state={params['state']}")
            assert site.client.get("/payouts").status_code == 200

        # The in-flight request saw the stepped-up tokens, and didn't restore the old ones
        assert slow["response"].get_json()["context"]["acr"] == "mfa"
        response = site.client.get("/payouts")
        assert (
            response.status_code == 200 and response.get_data(as_text=True) == "payouts"
        )
        with site.client.session_transaction() as session:
            session_key = next(
                key for key in session if key.endswith(f":{session['user_id']}")
            )
            assert (
                session[session_key]["tokens"]["access_token"] == tokens["access_token"]
            )

    def test_request_in_flight_during_a_later_sign_in_does_not_restore_mfa(self, site):
        sign_in(site)
        params = start_step_up(site, "/payouts")
        site.http.token_responses.append(stepped_up_tokens())
        site.client.get(f"/callback?code=step_up_code&state={params['state']}")
        assert site.client.get("/payouts").status_code == 200

        with request_in_flight(site) as slow:
            sign_in(site)  # a plain, single-factor sign-in in the same browser session
            assert site.client.get("/payouts").status_code == 302

        assert slow["response"].get_json()["context"]["acr"] is None
        response = site.client.get("/payouts")
        assert response.status_code == 302
        assert query(response.location)["acr_values"] == "mfa"

    def test_overlapping_requests_refresh_once(self, site):
        sign_in_with_an_expired_access_token(site)
        site.http.post.reset_mock()

        with request_in_flight(site) as slow:
            # The fake token endpoint has one response: a second refresh would fail the test
            site.http.token_responses.append(
                token_response("refreshed", refresh=False, id_token=False)
            )
            assert site.client.get("/whoami").get_json()["authenticated"] is True

        assert slow["response"].get_json()["authenticated"] is True
        assert site.client.get("/whoami").get_json()["authenticated"] is True
        assert [request["grant_type"] for request in site.http.token_requests] == [
            "refresh_token"
        ]
        assert site.http.token_requests[0]["refresh_token"] == "refresh-login"


class TestFlaskCallbackErrors:
    def test_unmet_error_reaches_the_app(self, site):
        seen = []

        @site.app.errorhandler(UnmetAuthenticationRequirementsError)
        def unmet(error):
            seen.append(error)
            return jsonify(reason="Add an authenticator app to continue"), 403

        sign_in(site)
        before = site.client.get("/whoami").get_json()
        params = start_step_up(site)
        token_requests = site.http.post.call_count

        response = site.client.get(
            "/callback",
            query_string={
                "error": UNMET,
                "error_description": UNMET_DESCRIPTION,
                "state": params["state"],
            },
        )

        # The app's handler got the error, with everything it needs
        assert response.status_code == 403
        assert response.get_json() == {"reason": "Add an authenticator app to continue"}
        assert len(seen) == 1
        assert seen[0].error == UNMET
        assert seen[0].error_description == UNMET_DESCRIPTION
        assert seen[0].state == params["state"]
        assert seen[0].acr_values == "mfa" and seen[0].max_age == 300
        # Not a login redirect, not retried, and the user is still signed in as before
        assert_not_sent_anywhere(response)
        assert site.http.post.call_count == token_requests
        assert site.client.get("/whoami").get_json() == before

    def test_unmet_error_has_a_default_page(self, site):
        sign_in(site)
        params = start_step_up(site)

        response = site.client.get(
            "/callback",
            query_string={
                "error": UNMET,
                "error_description": UNMET_DESCRIPTION,
                "state": params["state"],
            },
        )

        assert response.status_code == 403
        assert response.mimetype == "text/plain"
        body = response.get_data(as_text=True)
        assert "couldn't complete the extra verification" in body
        assert UNMET_DESCRIPTION in body
        assert_not_sent_anywhere(response)
        assert site.client.get("/whoami").get_json()["authenticated"] is True

    def test_login_required_reaches_the_app(self, site):
        seen = []

        @site.app.errorhandler(LoginRequiredError)
        def login_required(error):
            seen.append(error)
            return "sign in again", 401

        state = query(site.client.get("/login").location)["state"]
        response = site.client.get(
            "/callback", query_string={"error": "login_required", "state": state}
        )

        assert (
            response.status_code == 401
            and response.get_data(as_text=True) == "sign in again"
        )
        assert seen[0].error == "login_required" and seen[0].state == state
        assert_not_sent_anywhere(response)
        site.http.post.assert_not_called()

    def test_login_required_has_a_default_page(self, site):
        state = query(site.client.get("/login").location)["state"]
        response = site.client.get(
            "/callback", query_string={"error": "login_required", "state": state}
        )

        assert response.status_code == 401
        assert "sign in again" in response.get_data(as_text=True)
        assert_not_sent_anywhere(response)

    def test_app_handler_for_all_callback_errors(self, site):
        @site.app.errorhandler(KindeCallbackError)
        def any_callback_error(error):
            return f"app handled {error.error}", 400

        sign_in(site)
        params = start_step_up(site)
        response = site.client.get(
            "/callback", query_string={"error": UNMET, "state": params["state"]}
        )

        assert response.get_data(as_text=True) == f"app handled {UNMET}"

    def test_app_handler_registered_before_the_sdk_is_kept(self, flask_env):
        def configure(app):
            app.register_error_handler(
                KindeCallbackError, lambda error: ("registered first", 400)
            )

        app, _oauth = build_app(configure)
        client = app.test_client()
        state = query(client.get("/login").location)["state"]

        response = client.get(
            "/callback", query_string={"error": UNMET, "state": state}
        )

        assert response.get_data(as_text=True) == "registered first"

    @pytest.mark.parametrize("state", [None, "forged"])
    def test_state_is_validated_before_the_error_is_reported(self, site, state):
        seen = []
        site.app.register_error_handler(
            KindeCallbackError, lambda error: (seen.append(error), ("handled", 403))[1]
        )
        sign_in(site)
        start_step_up(site)

        params = {"error": UNMET, "error_description": "<script>alert(1)</script>"}
        if state:
            params["state"] = state
        response = site.client.get("/callback", query_string=params)

        assert response.status_code == 400
        assert "Invalid state parameter" in response.get_data(as_text=True)
        assert "<script>" not in response.get_data(as_text=True)
        assert seen == []
        assert_not_sent_anywhere(response)

    @pytest.mark.parametrize("error", [UNMET, "login_required"])
    def test_error_callback_with_a_wrong_state_keeps_the_return_location(
        self, site, error
    ):
        sign_in(site)
        params = start_step_up(site, "/payouts?tab=bank")

        forged = site.client.get(
            "/callback", query_string={"error": error, "state": "forged"}
        )
        assert forged.status_code == 400

        # The genuine callback still brings the user back
        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            f"/callback?code=step_up_code&state={params['state']}"
        )
        assert response.location == "http://localhost/payouts?tab=bank"

    def test_callback_with_a_code_and_a_wrong_state_keeps_the_return_location(
        self, site
    ):
        sign_in(site)
        params = start_step_up(site, "/payouts?tab=bank")

        forged = site.client.get("/callback?code=whatever&state=forged")
        assert forged.status_code == 400

        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            f"/callback?code=step_up_code&state={params['state']}"
        )
        assert response.location == "http://localhost/payouts?tab=bank"
        # Used once: the next sign-in goes to the default page
        assert sign_in(site).location == "http://localhost/"

    def test_default_page_does_not_claim_the_user_is_signed_in(self, site):
        # A first sign-in that asks for mfa, by a user with no factor
        state = query(site.client.get("/mfa-login").location)["state"]
        response = site.client.get(
            "/callback", query_string={"error": UNMET, "state": state}
        )

        assert response.status_code == 403
        assert "signed in" not in response.get_data(as_text=True)
        assert site.client.get("/whoami").get_json()["authenticated"] is False

    def test_error_callback_cannot_be_replayed(self, site):
        sign_in(site)
        params = start_step_up(site)
        url_params = {"error": UNMET, "state": params["state"]}

        assert site.client.get("/callback", query_string=url_params).status_code == 403
        assert site.client.get("/callback", query_string=url_params).status_code == 400

    def test_failed_step_up_does_not_leave_a_return_location_behind(self, site):
        sign_in(site)
        params = start_step_up(site, "/payouts?tab=bank")
        site.client.get(
            "/callback", query_string={"error": UNMET, "state": params["state"]}
        )

        # A later, ordinary login goes to the default page
        assert sign_in(site).location == "http://localhost/"

    def test_other_callback_errors_are_unchanged(self, site):
        state = query(site.client.get("/login").location)["state"]
        response = site.client.get(
            "/callback", query_string={"error": "access_denied", "state": state}
        )

        assert response.status_code == 400
        assert (
            response.get_data(as_text=True)
            == "Authentication failed: Missing authorization code"
        )
        site.http.post.assert_not_called()
