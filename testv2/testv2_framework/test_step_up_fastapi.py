"""
Step-up authentication through the FastAPI integration.

A real FastAPI app, the real Kinde routes and the real OAuth client. Only the
network is faked (the ``http`` fixture in ``testv2/conftest.py``).
"""

import time
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.testclient import TestClient

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.core.exceptions import (
    KindeCallbackError,
    KindeLoginException,
    KindeTokenException,
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
    """A FastAPI app with Kinde wired in, and a route that requires recent MFA."""
    app = FastAPI()
    app.add_middleware(SessionMiddleware, secret_key="test-secret")
    if configure:
        configure(app)

    oauth = OAuth(
        client_id="test_client_id",
        client_secret="test_client_secret",
        redirect_uri="http://testserver/callback",
        framework="fastapi",
        app=app,
        host=HOST,
    )

    async def payouts():
        if not oauth.is_authenticated():
            return RedirectResponse("/login")
        if not oauth.has_authentication_context(acr="mfa", max_age=300):
            return RedirectResponse(
                await oauth.step_up(acr="mfa", max_age=300), status_code=303
            )
        return PlainTextResponse("payouts")

    app.add_api_route("/payouts", payouts, methods=["GET", "POST"])

    @app.post("/transfer")
    async def transfer():
        url = await oauth.step_up(
            acr="phr", post_login_redirect_url="/transfer/confirm"
        )
        return RedirectResponse(url, status_code=303)

    @app.get("/mfa-login")
    async def mfa_login():
        return RedirectResponse(
            await oauth.login({"acr_values": "mfa"}), status_code=303
        )

    @app.get("/whoami")
    async def whoami():
        return {
            "authenticated": oauth.is_authenticated(),
            "context": oauth.get_authentication_context(),
        }

    return app, oauth


@pytest.fixture
def fastapi_env(http, monkeypatch):
    # The framework is a process-wide singleton: start each test without one
    monkeypatch.setattr(FrameworkFactory, "_framework_instance", None)
    return http


@pytest.fixture
def site(fastapi_env):
    app, oauth = build_app()
    return SimpleNamespace(
        app=app,
        oauth=oauth,
        client=TestClient(app, follow_redirects=False),
        http=fastapi_env,
    )


def location(response):
    return response.headers["location"]


def sign_in(site):
    response = site.client.get("/login")
    assert response.status_code == 307
    site.http.token_responses.append(
        token_response("login", id_claims={"auth_time": int(time.time()) - 3600})
    )
    response = site.client.get(
        "/callback",
        params={"code": "login_code", "state": query(location(response))["state"]},
    )
    assert response.status_code == 307
    return response


def start_step_up(site, path="/payouts?tab=bank"):
    response = site.client.get(path)
    assert response.status_code == 303
    assert location(response).startswith(f"{HOST}/oauth2/auth?")
    return query(location(response))


def stepped_up_tokens():
    claims = {"acr": "mfa", "amr": ["pwd", "totp"], "auth_time": int(time.time())}
    return token_response("step-up", access_claims={"acr": "mfa"}, id_claims=claims)


def assert_not_sent_anywhere(response):
    """The response is not a redirect, to login or anywhere else."""
    assert response.status_code not in (301, 302, 303, 307, 308)
    assert "location" not in response.headers


class TestFastAPIStepUp:
    def test_login_callback_is_unchanged(self, site):
        response = sign_in(site)
        assert location(response).startswith("http://testserver/?state=")
        assert site.client.get("/whoami").json()["authenticated"] is True

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
            "/callback", params={"code": "step_up_code", "state": params["state"]}
        )

        assert response.status_code == 307
        # The existing callback appends the state to the post-login redirect
        assert (
            location(response)
            == f"http://testserver/payouts?tab=bank&state={params['state']}"
        )
        response = site.client.get(location(response))
        assert response.status_code == 200 and response.text == "payouts"

    def test_successful_step_up_replaces_the_session_tokens(self, site):
        sign_in(site)
        assert site.client.get("/whoami").json()["context"]["acr"] is None
        user_id = next(iter(site.oauth._session_manager.user_sessions))
        before = dict(site.oauth.get_tokens(user_id))
        params = start_step_up(site)

        tokens = stepped_up_tokens()
        site.http.token_responses.append(tokens)
        site.client.get(
            "/callback", params={"code": "step_up_code", "state": params["state"]}
        )

        context = site.client.get("/whoami").json()["context"]
        assert context["acr"] == "mfa" and context["amr"] == ["pwd", "totp"]
        assert list(site.oauth._session_manager.user_sessions) == [user_id]
        after = site.oauth.get_tokens(user_id)
        assert after["access_token"] == tokens["access_token"] != before["access_token"]
        assert after["id_token"] == tokens["id_token"] != before["id_token"]
        assert after["refresh_token"] == "refresh-step-up" != before["refresh_token"]

    def test_a_post_is_not_replayed(self, site):
        sign_in(site)
        response = site.client.post("/payouts")
        params = query(location(response))

        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            "/callback", params={"code": "step_up_code", "state": params["state"]}
        )

        assert location(response) == f"http://testserver/?state={params['state']}"

    def test_a_post_does_not_inherit_an_abandoned_return_location(self, site):
        sign_in(site)
        start_step_up(site, "/payouts?tab=bank")  # started, then abandoned

        params = query(location(site.client.post("/payouts")))
        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            "/callback", params={"code": "step_up_code", "state": params["state"]}
        )

        assert location(response) == f"http://testserver/?state={params['state']}"

    def test_explicit_return_location(self, site):
        sign_in(site)
        response = site.client.post("/transfer")
        params = query(location(response))
        assert params["acr_values"] == "phr"

        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            "/callback", params={"code": "step_up_code", "state": params["state"]}
        )

        assert (
            location(response)
            == f"http://testserver/transfer/confirm?state={params['state']}"
        )


class TestFastAPICallbackErrors:
    def test_unmet_error_reaches_the_app(self, site):
        seen = []

        @site.app.exception_handler(UnmetAuthenticationRequirementsError)
        async def unmet(request, error):
            seen.append(error)
            return JSONResponse(
                {"reason": "Add an authenticator app to continue"}, status_code=403
            )

        sign_in(site)
        before = site.client.get("/whoami").json()
        params = start_step_up(site)
        token_requests = site.http.post.call_count

        response = site.client.get(
            "/callback",
            params={
                "error": UNMET,
                "error_description": UNMET_DESCRIPTION,
                "state": params["state"],
            },
        )

        # The app's handler got the error, with everything it needs
        assert response.status_code == 403
        assert response.json() == {"reason": "Add an authenticator app to continue"}
        assert len(seen) == 1
        assert seen[0].error == UNMET
        assert seen[0].error_description == UNMET_DESCRIPTION
        assert seen[0].state == params["state"]
        assert seen[0].acr_values == "mfa" and seen[0].max_age == 300
        # Not a login redirect, not retried, and the user is still signed in as before
        assert_not_sent_anywhere(response)
        assert site.http.post.call_count == token_requests
        assert site.client.get("/whoami").json() == before

    def test_unmet_error_has_a_default_page(self, site):
        sign_in(site)
        params = start_step_up(site)

        response = site.client.get(
            "/callback",
            params={
                "error": UNMET,
                "error_description": UNMET_DESCRIPTION,
                "state": params["state"],
            },
        )

        assert response.status_code == 403
        assert response.headers["content-type"].startswith("text/plain")
        assert "couldn't complete the extra verification" in response.text
        assert UNMET_DESCRIPTION in response.text
        assert_not_sent_anywhere(response)
        assert site.client.get("/whoami").json()["authenticated"] is True

    def test_login_required_reaches_the_app(self, site):
        seen = []

        @site.app.exception_handler(LoginRequiredError)
        async def login_required(request, error):
            seen.append(error)
            return PlainTextResponse("sign in again", status_code=401)

        state = query(location(site.client.get("/login")))["state"]
        response = site.client.get(
            "/callback", params={"error": "login_required", "state": state}
        )

        assert response.status_code == 401 and response.text == "sign in again"
        assert seen[0].error == "login_required" and seen[0].state == state
        assert_not_sent_anywhere(response)
        site.http.post.assert_not_called()

    def test_login_required_has_a_default_page(self, site):
        state = query(location(site.client.get("/login")))["state"]
        response = site.client.get(
            "/callback", params={"error": "login_required", "state": state}
        )

        assert response.status_code == 401
        assert "sign in again" in response.text
        assert_not_sent_anywhere(response)

    def test_app_handler_for_all_callback_errors(self, site):
        @site.app.exception_handler(KindeCallbackError)
        async def any_callback_error(request, error):
            return PlainTextResponse(f"app handled {error.error}", status_code=400)

        sign_in(site)
        params = start_step_up(site)
        response = site.client.get(
            "/callback", params={"error": UNMET, "state": params["state"]}
        )

        assert response.text == f"app handled {UNMET}"

    def test_app_handler_registered_before_the_sdk_is_kept(self, fastapi_env):
        async def registered_first(request, error):
            return PlainTextResponse("registered first", status_code=400)

        app, _oauth = build_app(
            lambda app: app.add_exception_handler(KindeCallbackError, registered_first)
        )
        client = TestClient(app, follow_redirects=False)
        state = query(location(client.get("/login")))["state"]

        response = client.get("/callback", params={"error": UNMET, "state": state})

        assert response.text == "registered first"

    @pytest.mark.parametrize("state", [None, "forged"])
    def test_state_is_validated_before_the_error_is_reported(self, site, state):
        seen = []

        @site.app.exception_handler(KindeCallbackError)
        async def any_callback_error(request, error):
            seen.append(error)
            return PlainTextResponse("handled", status_code=403)

        sign_in(site)
        start_step_up(site)

        params = {"error": UNMET, "error_description": "<script>alert(1)</script>"}
        if state:
            params["state"] = state
        response = site.client.get("/callback", params=params)

        assert response.status_code == 400
        assert "Invalid state parameter" in response.text
        assert "<script>" not in response.text
        assert seen == []
        assert_not_sent_anywhere(response)

    @pytest.mark.parametrize("error", [UNMET, "login_required"])
    def test_error_callback_with_a_wrong_state_keeps_the_return_location(
        self, site, error
    ):
        sign_in(site)
        params = start_step_up(site, "/payouts?tab=bank")

        forged = site.client.get(
            "/callback", params={"error": error, "state": "forged"}
        )
        assert forged.status_code == 400

        # The genuine callback still brings the user back
        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            "/callback", params={"code": "step_up_code", "state": params["state"]}
        )
        assert (
            location(response)
            == f"http://testserver/payouts?tab=bank&state={params['state']}"
        )

    def test_callback_with_a_code_and_a_wrong_state_keeps_the_return_location(
        self, site
    ):
        sign_in(site)
        params = start_step_up(site, "/payouts?tab=bank")

        with pytest.raises(KindeLoginException, match="Invalid state"):
            site.client.get("/callback", params={"code": "whatever", "state": "forged"})

        site.http.token_responses.append(stepped_up_tokens())
        response = site.client.get(
            "/callback", params={"code": "step_up_code", "state": params["state"]}
        )
        assert (
            location(response)
            == f"http://testserver/payouts?tab=bank&state={params['state']}"
        )

    def test_default_page_does_not_claim_the_user_is_signed_in(self, site):
        # A first sign-in that asks for mfa, by a user with no factor
        state = query(location(site.client.get("/mfa-login")))["state"]
        response = site.client.get("/callback", params={"error": UNMET, "state": state})

        assert response.status_code == 403
        assert "signed in" not in response.text
        assert site.client.get("/whoami").json()["authenticated"] is False

    def test_error_callback_cannot_be_replayed(self, site):
        sign_in(site)
        params = start_step_up(site)
        url_params = {"error": UNMET, "state": params["state"]}

        assert site.client.get("/callback", params=url_params).status_code == 403
        assert site.client.get("/callback", params=url_params).status_code == 400

    def test_failed_step_up_does_not_leave_a_return_location_behind(self, site):
        sign_in(site)
        params = start_step_up(site, "/payouts?tab=bank")
        site.client.get("/callback", params={"error": UNMET, "state": params["state"]})

        # A later, ordinary login goes to the default page
        assert location(sign_in(site)).startswith("http://testserver/?state=")

    def test_other_callback_errors_are_unchanged(self, site):
        # As before this change, any other error falls through to the code exchange
        state = query(location(site.client.get("/login")))["state"]
        with pytest.raises(KindeTokenException):
            site.client.get(
                "/callback", params={"error": "access_denied", "state": state}
            )
