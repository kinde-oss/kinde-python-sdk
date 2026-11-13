"""
Step-up authentication (RFC 9470), phase 1: core behaviour.

Every test runs against a real OAuth client with in-memory storage. The
network is replaced by the ``http`` fixture in ``testv2/conftest.py``, so
nothing leaves the machine.
"""

import time
from unittest.mock import MagicMock

import pytest
import requests

from kinde_sdk import AcrValues
from kinde_sdk.auth.async_oauth import AsyncOAuth
from kinde_sdk.auth.enums import PromptTypes
from kinde_sdk.auth.login_options import LoginOptions
from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.smart_oauth import SmartOAuth
from kinde_sdk.auth.step_up import (
    authentication_context_from_claims,
    discovery_supports_step_up,
    has_authentication_context,
    normalize_acr_values,
    normalize_max_age,
    normalize_step_up_auth_param,
    strongest_acr,
)
from kinde_sdk.core.exceptions import (
    KindeCallbackError,
    KindeConfigurationException,
    KindeLoginException,
    KindeRetrieveException,
    LoginRequiredError,
    UnmetAuthenticationRequirementsError,
)
from kinde_sdk.core.framework.null_framework import NullFramework
from kinde_sdk.core.storage.storage_manager import StorageManager
from testv2.step_up_helpers import (
    HOST,
    WITHOUT_STEP_UP,
    query,
    token_response,
)

USER_ID = "session_1"

# Login URLs produced by main before step-up was added (fixed state, nonce and challenge)
FIXED = {
    "state": "fixed_state",
    "nonce": "fixed_nonce",
    "code_challenge": "fixed_challenge",
}
LOGIN_URL_BEFORE = (
    "https://test.kinde.com/oauth2/auth?client_id=test_client_id&response_type=code"
    "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcallback&scope=openid+profile+email"
    "&supports_reauth=true&state=fixed_state&nonce=fixed_nonce"
    "&code_challenge=fixed_challenge&code_challenge_method=S256"
)
REGISTER_URL_BEFORE = (
    "https://test.kinde.com/oauth2/auth?client_id=test_client_id&response_type=code"
    "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcallback&scope=openid+profile+email"
    "&prompt=create&supports_reauth=true&state=fixed_state&nonce=fixed_nonce"
    "&code_challenge=fixed_challenge&code_challenge_method=S256"
)
AUTH_PARAMS_URL_BEFORE = (
    "https://test.kinde.com/oauth2/auth?client_id=test_client_id&response_type=code"
    "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcallback&scope=openid+profile+email"
    "&org_code=org_1&supports_reauth=true&custom=x&empty=&state=fixed_state&nonce=fixed_nonce"
    "&code_challenge=fixed_challenge&code_challenge_method=S256"
)


def make_client(cls=OAuth):
    return cls(
        client_id="test_client_id",
        client_secret="test_client_secret",
        redirect_uri="http://localhost:8000/callback",
        host=HOST,
    )


@pytest.fixture
def oauth(http):
    return make_client()


async def complete_callback(client, http, url, response, user_id=USER_ID):
    """Finish the authorization request behind ``url`` with a token response."""
    http.token_responses.append(response)
    result = await client.handle_redirect("auth_code", user_id, query(url)["state"])
    NullFramework().set_user_id(user_id)
    return result


async def sign_in(client, http, response=None, user_id=USER_ID):
    response = response or token_response(
        "login", id_claims={"auth_time": int(time.time()) - 3600}
    )
    return await complete_callback(
        client, http, await client.login(), response, user_id
    )


def stored_state():
    return StorageManager().get("user:state")


# ---------------------------------------------------------------------------
# Login options
# ---------------------------------------------------------------------------


class TestLoginOptions:
    async def test_login_url_is_unchanged_without_the_new_options(self, oauth):
        assert await oauth.login(dict(FIXED)) == LOGIN_URL_BEFORE
        assert await oauth.register(dict(FIXED)) == REGISTER_URL_BEFORE

    async def test_existing_auth_params_passthrough_is_unchanged(self, oauth):
        options = {
            **FIXED,
            "org_code": "org_1",
            "auth_params": {"custom": "x", "empty": None},
        }
        assert await oauth.login(options) == AUTH_PARAMS_URL_BEFORE

    @pytest.mark.parametrize("method", ["login", "register"])
    async def test_acr_values_is_sent(self, oauth, method):
        url = await getattr(oauth, method)({LoginOptions.ACR_VALUES: "mfa"})
        assert query(url)["acr_values"] == "mfa"
        assert "max_age" not in query(url)

    @pytest.mark.parametrize("method", ["login", "register"])
    async def test_acr_values_list_is_space_joined(self, oauth, method):
        url = await getattr(oauth, method)({LoginOptions.ACR_VALUES: ["mfa", "phr"]})
        assert query(url)["acr_values"] == "mfa phr"
        # urlencode writes the space as "+", as it already does for scope
        assert "acr_values=mfa+phr" in url

    async def test_acr_values_accepts_the_constants_and_is_lower_cased(self, oauth):
        url = await oauth.login({LoginOptions.ACR_VALUES: AcrValues.PHR})
        assert query(url)["acr_values"] == "phr"
        url = await oauth.login({LoginOptions.ACR_VALUES: "MFA"})
        assert query(url)["acr_values"] == "mfa"

    @pytest.mark.parametrize("method", ["login", "register"])
    async def test_max_age_zero_is_sent(self, oauth, method):
        url = await getattr(oauth, method)({LoginOptions.MAX_AGE: 0})
        assert query(url)["max_age"] == "0"

    async def test_max_age_is_sent_as_a_decimal_string(self, oauth):
        url = await oauth.login({LoginOptions.MAX_AGE: 300})
        assert "max_age=300" in url

    @pytest.mark.parametrize(
        "options",
        [
            {},
            {LoginOptions.MAX_AGE: None},
            {LoginOptions.ACR_VALUES: None},
            {LoginOptions.AUTH_PARAMS: {"max_age": None}},
            {LoginOptions.AUTH_PARAMS: {"max_age": ""}},
            {LoginOptions.AUTH_PARAMS: {"max_age": "  "}},
            {LoginOptions.AUTH_PARAMS: {"acr_values": None}},
            {LoginOptions.AUTH_PARAMS: {"acr_values": ""}},
            {LoginOptions.AUTH_PARAMS: {"acr_values": []}},
        ],
    )
    @pytest.mark.parametrize("method", ["login", "register"])
    async def test_unset_values_are_never_sent(self, oauth, method, options):
        url = await getattr(oauth, method)(dict(options))
        assert "max_age" not in query(url)
        assert "acr_values" not in query(url)
        assert "max_age" not in url and "acr_values" not in url

    @pytest.mark.parametrize(
        "value", [-1, 1.5, 300.0, True, False, "300", "", "NaN", float("nan"), [300]]
    )
    @pytest.mark.parametrize("method", ["login", "register"])
    async def test_invalid_max_age_is_rejected_before_the_url_is_built(
        self, oauth, method, value
    ):
        with pytest.raises(ValueError, match="max_age"):
            await getattr(oauth, method)({LoginOptions.MAX_AGE: value})
        assert stored_state() is None

    @pytest.mark.parametrize(
        "value", ["undefined", "null", "NaN", "-1", "1.5", "five", -1, 1.5, True]
    )
    async def test_invalid_max_age_in_auth_params_is_rejected(self, oauth, value):
        with pytest.raises(ValueError, match="max_age"):
            await oauth.login({LoginOptions.AUTH_PARAMS: {"max_age": value}})
        assert stored_state() is None

    @pytest.mark.parametrize(
        "value, sent", [(0, "0"), (300, "300"), ("300", "300"), (" 60 ", "60")]
    )
    async def test_valid_max_age_in_auth_params_is_sent(self, oauth, value, sent):
        url = await oauth.login({LoginOptions.AUTH_PARAMS: {"max_age": value}})
        assert query(url)["max_age"] == sent

    async def test_acr_values_in_auth_params_is_passed_through(self, oauth):
        url = await oauth.login(
            {LoginOptions.AUTH_PARAMS: {"acr_values": ["mfa", "phr"]}}
        )
        assert query(url)["acr_values"] == "mfa phr"
        # A raw passthrough keeps accepting values Kinde reads as mfa
        url = await oauth.login(
            {LoginOptions.AUTH_PARAMS: {"acr_values": "urn:okta:loa:2fa:any"}}
        )
        assert query(url)["acr_values"] == "urn:okta:loa:2fa:any"

    @pytest.mark.parametrize(
        "value", ["", "  ", [], "gold", ["mfa", "gold"], 1, ["mfa", 2], {"mfa"}]
    )
    async def test_invalid_acr_values_is_rejected(self, oauth, value):
        with pytest.raises(ValueError, match="acr"):
            await oauth.login({LoginOptions.ACR_VALUES: value})
        assert stored_state() is None


class TestNormalizers:
    def test_normalize_acr_values(self):
        assert normalize_acr_values("mfa") == "mfa"
        assert normalize_acr_values("phr mfa") == "phr mfa"
        assert normalize_acr_values(("MFA", "mfa", "Phr")) == "mfa phr"

    def test_normalize_max_age(self):
        assert normalize_max_age(0) == 0
        assert normalize_max_age(300) == 300

    def test_normalize_step_up_auth_param_rejects_other_keys(self):
        with pytest.raises(ValueError):
            normalize_step_up_auth_param("prompt", "none")

    def test_strongest_acr(self):
        assert strongest_acr(None) is None
        assert strongest_acr("mfa") == "mfa"
        assert strongest_acr("mfa phr") == "phr"
        assert strongest_acr(["PHR", "mfa"]) == "phr"
        assert strongest_acr("gold") is None
        assert strongest_acr("urn:okta:loa:2fa:any") == "mfa"
        assert strongest_acr("urn:okta:loa:2fa:any:ifpossible") is None


# ---------------------------------------------------------------------------
# step_up()
# ---------------------------------------------------------------------------


class TestStepUp:
    async def test_step_up_is_an_interactive_login_with_the_extra_options(self, oauth):
        url = await oauth.step_up(acr="mfa", max_age=300)
        params = query(url)

        assert url.startswith(f"{HOST}/oauth2/auth?")
        assert params["acr_values"] == "mfa"
        assert params["max_age"] == "300"
        assert "prompt" not in params
        # The SDK's usual state, nonce and PKCE handling is reused
        assert params["state"] == stored_state()["value"]
        assert params["nonce"] == StorageManager().get("user:nonce")["value"]
        assert params["code_challenge"] and params["code_challenge_method"] == "S256"
        assert StorageManager().get("user:code_verifier")["value"]
        assert params["supports_reauth"] == "true"

    async def test_step_up_with_acr_only_or_max_age_only(self, oauth):
        params = query(await oauth.step_up(acr=AcrValues.PHR))
        assert params["acr_values"] == "phr" and "max_age" not in params

        params = query(await oauth.step_up(max_age=0))
        assert params["max_age"] == "0" and "acr_values" not in params

    async def test_step_up_keeps_the_usual_login_options(self, oauth):
        url = await oauth.step_up(
            acr="mfa", login_options={"org_code": "org_1", "lang": "fr"}
        )
        params = query(url)
        assert params["org_code"] == "org_1" and params["lang"] == "fr"

    async def test_step_up_reads_the_options_from_login_options_too(self, oauth):
        options = {LoginOptions.ACR_VALUES: "mfa", LoginOptions.MAX_AGE: 60}
        params = query(await oauth.step_up(login_options=options))
        assert params["acr_values"] == "mfa" and params["max_age"] == "60"
        assert options == {
            LoginOptions.ACR_VALUES: "mfa",
            LoginOptions.MAX_AGE: 60,
        }  # not mutated

        params = query(
            await oauth.step_up(
                login_options={"auth_params": {"acr_values": "phr", "max_age": "0"}}
            )
        )
        assert params["acr_values"] == "phr" and params["max_age"] == "0"

    @pytest.mark.parametrize(
        "login_options",
        [
            {LoginOptions.PROMPT: "none"},
            {LoginOptions.PROMPT: "NONE"},
            {LoginOptions.PROMPT: PromptTypes.NONE},
            {LoginOptions.PROMPT: "login none"},
            {LoginOptions.AUTH_PARAMS: {"prompt": "none"}},
            {
                LoginOptions.PROMPT: "login",
                LoginOptions.AUTH_PARAMS: {"prompt": "none"},
            },
        ],
    )
    async def test_step_up_rejects_prompt_none(self, oauth, login_options):
        with pytest.raises(ValueError, match="prompt=none"):
            await oauth.step_up(acr="mfa", login_options=login_options)
        assert stored_state() is None

    async def test_step_up_allows_other_prompts(self, oauth):
        params = query(
            await oauth.step_up(acr="mfa", login_options={LoginOptions.PROMPT: "login"})
        )
        assert params["prompt"] == "login"

    async def test_step_up_requires_something_to_step_up_to(self, oauth):
        with pytest.raises(ValueError, match="requires acr, max_age"):
            await oauth.step_up()
        with pytest.raises(ValueError, match="requires acr, max_age"):
            await oauth.step_up(login_options={"org_code": "org_1"})

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"acr": "gold"},
            {"acr": ""},
            {"max_age": -1},
            {"max_age": 1.5},
            {"max_age": True},
            {"acr": "mfa", "max_age": "300"},
            {"login_options": {"auth_params": {"acr_values": "gold"}}},
            {"acr": "mfa", "login_options": {"auth_params": {"max_age": "undefined"}}},
        ],
    )
    async def test_step_up_rejects_invalid_requests(self, oauth, kwargs):
        with pytest.raises(ValueError):
            await oauth.step_up(**kwargs)
        assert stored_state() is None

    async def test_step_up_keeps_the_current_tokens(self, oauth, http):
        await sign_in(oauth, http)
        before = dict(oauth.get_tokens(USER_ID))

        await oauth.step_up(acr="mfa")

        after = oauth.get_tokens(USER_ID)
        assert after["access_token"] == before["access_token"]
        assert after["refresh_token"] == before["refresh_token"]
        assert oauth.is_authenticated()

    async def test_step_up_asks_the_framework_to_bring_the_user_back(self, oauth):
        oauth._framework = MagicMock()

        await oauth.step_up(acr="mfa")
        oauth._framework.set_post_login_redirect_url.assert_called_once_with(None)

        oauth._framework.reset_mock()
        await oauth.step_up(acr="mfa", post_login_redirect_url="/payouts")
        oauth._framework.set_post_login_redirect_url.assert_called_once_with("/payouts")

        # A rejected request leaves the framework's redirect alone
        oauth._framework.reset_mock()
        with pytest.raises(ValueError):
            await oauth.step_up(acr="mfa", login_options={LoginOptions.PROMPT: "none"})
        oauth._framework.set_post_login_redirect_url.assert_not_called()

    async def test_step_up_works_without_a_framework_integration(self, oauth):
        # NullFramework inherits the no-op hook
        assert NullFramework().set_post_login_redirect_url("/payouts") is None
        assert await oauth.step_up(acr="mfa", post_login_redirect_url="/payouts")


class TestStepUpWithoutDiscoverySupport:
    @pytest.fixture
    def oauth(self, http):
        http.discovery = WITHOUT_STEP_UP
        return make_client()

    async def test_acr_raises_a_not_supported_error(self, oauth):
        with pytest.raises(KindeConfigurationException, match="not supported"):
            await oauth.step_up(acr="mfa")
        with pytest.raises(KindeConfigurationException, match="not supported"):
            await oauth.step_up(acr="mfa", max_age=300)
        assert stored_state() is None

    async def test_max_age_raises_too(self, oauth):
        # Kinde would ignore max_age, and auth_time is not reported here, so a
        # fallback sign-in could never satisfy has_authentication_context()
        with pytest.raises(KindeConfigurationException, match="not supported"):
            await oauth.step_up(max_age=300)
        with pytest.raises(KindeConfigurationException, match="prompt=login"):
            await oauth.step_up(login_options={"auth_params": {"max_age": "300"}})
        assert stored_state() is None

    async def test_guard_on_max_age_cannot_loop(self, oauth, http):
        await sign_in(oauth, http)
        http.post.reset_mock()

        # The check an app would guard a page with is never met here...
        assert oauth.has_authentication_context(max_age=300) is False
        # ...and the step-up it would start raises every time, instead of redirecting
        for _ in range(3):
            with pytest.raises(KindeConfigurationException):
                await oauth.step_up(max_age=300)
        http.post.assert_not_called()

    async def test_login_options_are_still_sent_as_given(self, oauth):
        # login() is a plain passthrough: only step_up() consults discovery
        params = query(
            await oauth.login({LoginOptions.ACR_VALUES: "mfa", LoginOptions.MAX_AGE: 0})
        )
        assert params["acr_values"] == "mfa" and params["max_age"] == "0"


# ---------------------------------------------------------------------------
# Callback errors
# ---------------------------------------------------------------------------


class TestCallbackErrors:
    async def test_unmet_authentication_requirements_reaches_the_app(self, oauth, http):
        await sign_in(oauth, http)
        tokens_before = dict(oauth.get_tokens(USER_ID))
        state = query(await oauth.step_up(acr="phr", max_age=300))["state"]
        http.post.reset_mock()

        with pytest.raises(UnmetAuthenticationRequirementsError) as raised:
            await oauth.handle_redirect(
                None,
                USER_ID,
                state,
                error="unmet_authentication_requirements",
                error_description="The requested authentication context could not be met",
            )

        error = raised.value
        assert error.error == "unmet_authentication_requirements"
        assert (
            error.error_description
            == "The requested authentication context could not be met"
        )
        assert error.state == state
        assert str(error) == "The requested authentication context could not be met"
        # What the step-up asked for, so the app can say what is missing
        assert error.acr_values == "phr"
        assert error.max_age == 300
        assert isinstance(error, KindeCallbackError) and isinstance(
            error, KindeLoginException
        )

        # No retry, no token request, and the user is still signed in with the same tokens
        http.post.assert_not_called()
        assert oauth.is_authenticated()
        assert (
            oauth.get_tokens(USER_ID)["access_token"] == tokens_before["access_token"]
        )
        assert (
            oauth.get_tokens(USER_ID)["refresh_token"] == tokens_before["refresh_token"]
        )

    async def test_login_required_has_its_own_error(self, oauth):
        state = query(
            await oauth.login({LoginOptions.PROMPT: "none", LoginOptions.MAX_AGE: 300})
        )["state"]

        with pytest.raises(LoginRequiredError) as raised:
            await oauth.handle_redirect(None, None, state, error="login_required")

        assert raised.value.error == "login_required"
        assert raised.value.error_description == ""
        assert raised.value.state == state
        assert str(raised.value) == "login_required"
        assert not isinstance(raised.value, UnmetAuthenticationRequirementsError)

    async def test_other_errors_are_reported_with_their_code(self, oauth):
        state = query(await oauth.login())["state"]

        with pytest.raises(KindeCallbackError) as raised:
            await oauth.handle_redirect(
                None, None, state, error="access_denied", error_description="Denied"
            )

        assert type(raised.value) is KindeCallbackError
        assert raised.value.error == "access_denied"
        assert raised.value.error_description == "Denied"

    @pytest.mark.parametrize(
        "error", ["unmet_authentication_requirements", "login_required"]
    )
    @pytest.mark.parametrize("state", [None, "", "not-the-stored-state"])
    async def test_state_is_validated_before_the_error_is_reported(
        self, oauth, error, state
    ):
        await oauth.step_up(acr="mfa")

        with pytest.raises(KindeLoginException, match="Invalid state") as raised:
            await oauth.handle_redirect(None, None, state, error=error)

        assert not isinstance(raised.value, KindeCallbackError)
        # The genuine request is still pending
        assert stored_state() is not None

    async def test_error_without_a_pending_request_fails_state_validation(self, oauth):
        with pytest.raises(KindeLoginException, match="Invalid state"):
            await oauth.handle_redirect(
                None, None, "anything", error="unmet_authentication_requirements"
            )

    async def test_error_callback_cannot_be_replayed(self, oauth, http):
        state = query(await oauth.step_up(acr="mfa"))["state"]
        with pytest.raises(UnmetAuthenticationRequirementsError):
            await oauth.handle_redirect(
                None, None, state, error="unmet_authentication_requirements"
            )

        # The request is finished: nothing is left to resume or retry
        for key in ("user:state", "user:nonce", "user:code_verifier", "user:step_up"):
            assert StorageManager().get(key) is None
        with pytest.raises(KindeLoginException, match="Invalid state"):
            await oauth.handle_redirect(
                None, None, state, error="unmet_authentication_requirements"
            )
        with pytest.raises(KindeLoginException, match="Invalid state"):
            await oauth.handle_redirect("auth_code", USER_ID, state)
        http.post.assert_not_called()

    async def test_error_takes_precedence_over_a_code(self, oauth, http):
        state = query(await oauth.step_up(acr="mfa"))["state"]
        with pytest.raises(UnmetAuthenticationRequirementsError):
            await oauth.handle_redirect(
                "auth_code", USER_ID, state, error="unmet_authentication_requirements"
            )
        http.post.assert_not_called()

    async def test_request_details_are_not_taken_from_another_request(self, oauth):
        await oauth.step_up(acr="phr")
        # A later plain login replaces the pending request
        state = query(await oauth.login())["state"]

        with pytest.raises(UnmetAuthenticationRequirementsError) as raised:
            await oauth.handle_redirect(
                None, None, state, error="unmet_authentication_requirements"
            )

        assert raised.value.acr_values is None and raised.value.max_age is None


# ---------------------------------------------------------------------------
# Session update
# ---------------------------------------------------------------------------


class TestSessionUpdate:
    async def test_successful_step_up_replaces_all_three_tokens(self, oauth, http):
        first = token_response("login", id_claims={"auth_time": 1000})
        await sign_in(oauth, http, first)
        assert oauth.get_authentication_context()["acr"] is None

        second = token_response(
            "step-up",
            access_claims={"acr": "mfa"},
            id_claims={"acr": "mfa", "amr": ["pwd", "totp"], "auth_time": 2000},
        )
        # The user is already signed in: the callback is processed all the same
        assert oauth.is_authenticated()
        await complete_callback(oauth, http, await oauth.step_up(acr="mfa"), second)

        tokens = oauth.get_tokens(USER_ID)
        assert tokens["access_token"] == second["access_token"] != first["access_token"]
        assert tokens["id_token"] == second["id_token"] != first["id_token"]
        assert tokens["refresh_token"] == "refresh-step-up"
        assert oauth.get_authentication_context() == {
            "acr": "mfa",
            "amr": ["pwd", "totp"],
            "auth_time": 2000,
        }
        assert StorageManager().get("user:step_up") is None
        # The stored session matches what is in memory
        assert (
            StorageManager().get(USER_ID)["tokens"]["refresh_token"]
            == "refresh-step-up"
        )

    async def test_tokens_from_before_the_step_up_are_never_kept(self, oauth, http):
        await sign_in(
            oauth, http, token_response("login", id_claims={"auth_time": 1000})
        )

        # The step-up response has no refresh token and no ID token
        second = token_response(
            "step-up", access_claims={"acr": "mfa"}, refresh=False, id_token=False
        )
        await complete_callback(oauth, http, await oauth.step_up(acr="mfa"), second)

        token_manager = oauth._session_manager.get_token_manager(USER_ID)
        assert "refresh_token" not in token_manager.tokens
        assert "id_token" not in token_manager.tokens
        assert token_manager.get_claims("id_token") == {}
        assert token_manager.tokens["access_token"] == second["access_token"]

    async def test_refresh_after_step_up_uses_the_new_refresh_token(self, oauth, http):
        await sign_in(oauth, http)
        stepped_up = token_response(
            "step-up", access_claims={"acr": "mfa"}, id_claims={"acr": "mfa"}
        )
        await complete_callback(oauth, http, await oauth.step_up(acr="mfa"), stepped_up)

        token_manager = oauth._session_manager.get_token_manager(USER_ID)
        token_manager.tokens["expires_at"] = time.time() - 1
        refreshed = token_response(
            "refreshed", access_claims={"acr": "mfa"}, refresh=False, id_token=False
        )
        http.token_responses.append(refreshed)
        http.post.reset_mock()

        assert token_manager.get_access_token() == refreshed["access_token"]

        assert len(http.token_requests) == 1
        assert http.token_requests[0]["grant_type"] == "refresh_token"
        assert http.token_requests[0]["refresh_token"] == "refresh-step-up"
        # A refresh merges: the stepped-up ID token and refresh token stay
        assert oauth.get_authentication_context()["acr"] == "mfa"
        assert token_manager.tokens["refresh_token"] == "refresh-step-up"

    async def test_has_authentication_context_never_refreshes_to_satisfy_a_step_up(
        self, oauth, http
    ):
        await sign_in(oauth, http)
        http.post.reset_mock()

        assert oauth.has_authentication_context(acr="mfa") is False

        http.post.assert_not_called()


# ---------------------------------------------------------------------------
# get_authentication_context()
# ---------------------------------------------------------------------------


class TestGetAuthenticationContext:
    def test_without_a_signed_in_user(self, oauth):
        assert oauth.get_authentication_context() == {
            "acr": None,
            "amr": [],
            "auth_time": None,
        }

    async def test_single_factor_sign_in_has_no_acr_or_amr(self, oauth, http):
        await sign_in(
            oauth, http, token_response("login", id_claims={"auth_time": 1716800000})
        )
        assert oauth.get_authentication_context() == {
            "acr": None,
            "amr": [],
            "auth_time": 1716800000,
        }

    async def test_reads_acr_amr_and_auth_time(self, oauth, http):
        id_claims = {"acr": "mfa", "amr": ["pwd", "totp"], "auth_time": 1716800000}
        await sign_in(
            oauth,
            http,
            token_response("login", access_claims={"acr": "mfa"}, id_claims=id_claims),
        )
        assert oauth.get_authentication_context() == {
            "acr": "mfa",
            "amr": ["pwd", "totp"],
            "auth_time": 1716800000,
        }

    async def test_auth_time_comes_from_the_id_token(self, oauth, http):
        response = token_response(
            "login", access_claims={"auth_time": 1111}, id_claims={"auth_time": 2222}
        )
        await sign_in(oauth, http, response)
        assert oauth.get_authentication_context()["auth_time"] == 2222

    async def test_access_token_is_the_fallback_without_an_id_token(self, oauth, http):
        response = token_response(
            "login",
            access_claims={"acr": "phr", "amr": ["passkey"], "auth_time": 1111},
            id_token=False,
        )
        await sign_in(oauth, http, response)
        assert oauth.get_authentication_context() == {
            "acr": "phr",
            "amr": ["passkey"],
            "auth_time": 1111,
        }

    async def test_auth_time_is_not_reported_without_discovery_support(self, http):
        http.discovery = WITHOUT_STEP_UP
        oauth = make_client()
        await sign_in(
            oauth, http, token_response("login", id_claims={"auth_time": 1716800000})
        )

        assert oauth.get_authentication_context() == {
            "acr": None,
            "amr": [],
            "auth_time": None,
        }
        assert oauth.has_authentication_context(max_age=10**12) is False

    def test_malformed_claims_are_ignored(self):
        context = authentication_context_from_claims(
            {"acr": ["mfa"], "amr": "pwd", "auth_time": "soon"},
            {"acr": 2, "amr": None, "auth_time": True},
        )
        assert context == {"acr": None, "amr": [], "auth_time": None}
        assert authentication_context_from_claims(None, None) == {
            "acr": None,
            "amr": [],
            "auth_time": None,
        }

    def test_tokens_of_different_users_give_no_context(self):
        context = authentication_context_from_claims(
            {"sub": "kp_one", "acr": "mfa", "auth_time": 1},
            {"sub": "kp_two", "acr": "mfa"},
        )
        assert context == {"acr": None, "amr": [], "auth_time": None}


# ---------------------------------------------------------------------------
# has_authentication_context()
# ---------------------------------------------------------------------------

NOW = 1_716_800_000


class TestHasAuthenticationContext:
    @pytest.mark.parametrize(
        "token_acr, required_acr, expected",
        [
            (None, None, True),  # absent / none -> meets
            (None, "mfa", False),  # absent / mfa -> doesn't meet
            ("mfa", "mfa", True),
            ("mfa", "phr", False),
            ("phr", "mfa", True),
            ("phr", "phr", True),
            (None, "phr", False),
            ("mfa", None, True),
            ("gold", "mfa", False),  # Kinde only returns mfa or phr
            ("MFA", "mfa", True),
            ("mfa", ["mfa", "phr"], False),  # the highest requested context applies
            ("phr", ["mfa", "phr"], True),
        ],
    )
    def test_acr_table(self, token_acr, required_acr, expected):
        context = {"acr": token_acr, "amr": [], "auth_time": NOW}
        assert (
            has_authentication_context(context, acr=required_acr, now=NOW) is expected
        )

    @pytest.mark.parametrize("token_acr", [None, "mfa", "phr"])
    def test_max_age_with_missing_auth_time_does_not_meet(self, token_acr):
        context = {"acr": token_acr, "amr": [], "auth_time": None}
        assert has_authentication_context(context, max_age=300, now=NOW) is False
        assert (
            has_authentication_context({"acr": token_acr}, max_age=300, now=NOW)
            is False
        )
        assert (
            has_authentication_context(context, acr=token_acr, max_age=10**9, now=NOW)
            is False
        )

    @pytest.mark.parametrize(
        "age, max_age, leeway, expected",
        [
            (0, 300, 0, True),
            (300, 300, 0, True),  # now - auth_time <= max_age
            (301, 300, 0, False),
            (600, 300, 0, False),
            (0, 0, 0, True),
            (1, 0, 0, False),
            (305, 300, 10, True),  # clock tolerance
            (311, 300, 10, False),
        ],
    )
    def test_max_age(self, age, max_age, leeway, expected):
        context = {"acr": "mfa", "amr": [], "auth_time": NOW - age}
        assert (
            has_authentication_context(context, max_age=max_age, now=NOW, leeway=leeway)
            is expected
        )

    def test_both_requirements_must_be_met(self):
        recent_single_factor = {"acr": None, "auth_time": NOW}
        old_mfa = {"acr": "mfa", "auth_time": NOW - 3600}
        recent_mfa = {"acr": "mfa", "auth_time": NOW - 10}
        assert (
            has_authentication_context(
                recent_single_factor, acr="mfa", max_age=300, now=NOW
            )
            is False
        )
        assert (
            has_authentication_context(old_mfa, acr="mfa", max_age=300, now=NOW)
            is False
        )
        assert (
            has_authentication_context(recent_mfa, acr="mfa", max_age=300, now=NOW)
            is True
        )

    def test_amr_is_never_used_to_decide(self):
        context = {
            "acr": None,
            "amr": ["pwd", "totp", "passkey", "mfa"],
            "auth_time": NOW,
        }
        assert has_authentication_context(context, acr="mfa", now=NOW) is False
        assert (
            has_authentication_context({"acr": "mfa", "amr": []}, acr="mfa", now=NOW)
            is True
        )

    def test_uses_the_clock_by_default(self):
        assert (
            has_authentication_context({"auth_time": int(time.time())}, max_age=60)
            is True
        )
        assert (
            has_authentication_context(
                {"auth_time": int(time.time()) - 120}, max_age=60
            )
            is False
        )

    def test_works_on_verified_token_claims(self):
        claims = {
            "sub": "kp_user",
            "acr": "phr",
            "amr": ["passkey"],
            "auth_time": NOW - 5,
        }
        assert (
            has_authentication_context(claims, acr="mfa", max_age=60, now=NOW) is True
        )

    @pytest.mark.parametrize(
        "kwargs",
        [
            {"acr": "gold"},
            {"acr": ""},
            {"max_age": -1},
            {"max_age": 1.5},
            {"max_age": True},
        ],
    )
    def test_invalid_requirement_raises(self, oauth, kwargs):
        with pytest.raises(ValueError):
            has_authentication_context(
                {"acr": "phr", "auth_time": NOW}, now=NOW, **kwargs
            )
        # Also on the client, and before looking at the session
        with pytest.raises(ValueError):
            oauth.has_authentication_context(**kwargs)

    async def test_client_checks_the_current_session(self, oauth, http):
        assert oauth.has_authentication_context() is False  # nobody is signed in
        assert oauth.has_authentication_context(acr="mfa") is False

        await sign_in(
            oauth,
            http,
            token_response("login", id_claims={"auth_time": int(time.time()) - 3600}),
        )
        assert oauth.has_authentication_context() is True
        assert oauth.has_authentication_context(acr="mfa") is False
        assert oauth.has_authentication_context(max_age=300) is False
        assert oauth.has_authentication_context(max_age=7200) is True

        now = int(time.time())
        stepped_up = token_response(
            "step-up",
            id_claims={"acr": "mfa", "amr": ["pwd", "totp"], "auth_time": now},
        )
        await complete_callback(
            oauth, http, await oauth.step_up(acr="mfa", max_age=300), stepped_up
        )
        assert oauth.has_authentication_context(acr="mfa", max_age=300) is True
        assert oauth.has_authentication_context(acr="phr") is False

    async def test_client_requires_a_live_session(self, oauth, http):
        response = token_response(
            "login",
            id_claims={"acr": "mfa", "auth_time": int(time.time())},
            refresh=False,
        )
        await sign_in(oauth, http, response)
        assert oauth.has_authentication_context(acr="mfa") is True

        # Expired, and nothing to refresh with
        oauth._session_manager.get_token_manager(USER_ID).tokens["expires_at"] = (
            time.time() - 1
        )
        assert oauth.has_authentication_context(acr="mfa") is False


# ---------------------------------------------------------------------------
# is_step_up_supported()
# ---------------------------------------------------------------------------


class TestIsStepUpSupported:
    def test_true_when_discovery_lists_acr_values_supported(self, oauth, http):
        assert oauth.is_step_up_supported() is True
        assert oauth.is_step_up_supported() is True
        # Cached with the rest of discovery: fetched once, when the client was created
        assert http.get.call_count == 1

    def test_false_when_discovery_lacks_it(self, http):
        http.discovery = WITHOUT_STEP_UP
        oauth = make_client()
        assert oauth.is_step_up_supported() is False
        assert oauth.is_step_up_supported() is False
        assert http.get.call_count == 1

    @pytest.mark.parametrize("value", [None, [], "mfa", {}])
    def test_false_for_empty_or_malformed_values(self, value):
        assert discovery_supports_step_up({"acr_values_supported": value}) is False
        assert discovery_supports_step_up(None) is False
        assert discovery_supports_step_up({"acr_values_supported": ["mfa"]}) is True

    def test_failed_discovery_is_retried_at_most_once_a_minute(self, http):
        http.discovery_status = 503
        oauth = make_client()
        assert oauth.auth_url == f"{HOST}/oauth2/auth"  # existing fallback
        assert http.get.call_count == 1

        assert oauth.is_step_up_supported() is False
        assert oauth.is_step_up_supported() is False
        assert http.get.call_count == 2  # one retry, then rate limited

        http.discovery_status = 200
        assert oauth.is_step_up_supported() is False  # still inside the minute
        oauth._openid_configuration_tried_at = 0
        assert oauth.is_step_up_supported() is True
        assert oauth.is_step_up_supported() is True
        assert http.get.call_count == 3

    def test_discovery_errors_mean_not_supported(self, http):
        http.get.side_effect = requests.ConnectionError("offline")
        oauth = make_client()
        assert oauth.is_step_up_supported() is False


class TestStepUpWhileDiscoveryIsUnavailable:
    @pytest.fixture
    def oauth(self, http):
        # The environment supports step-up, but discovery fails as the client starts
        http.discovery_status = 503
        return make_client()

    @pytest.mark.parametrize("kwargs", [{"acr": "mfa"}, {"max_age": 300}])
    async def test_step_up_raises_a_retryable_error(self, oauth, kwargs):
        with pytest.raises(KindeRetrieveException, match="Try again") as raised:
            await oauth.step_up(**kwargs)

        # Not the "this environment doesn't support step-up" answer
        assert not isinstance(raised.value, KindeConfigurationException)
        assert stored_state() is None

    async def test_step_up_works_within_seconds_of_discovery_coming_back(
        self, oauth, http
    ):
        assert oauth.is_step_up_supported() is False  # uses up this minute's retry
        oauth._openid_configuration_tried_at -= 5
        with pytest.raises(KindeRetrieveException):
            await oauth.step_up(acr="mfa")

        http.discovery_status = 200
        oauth._openid_configuration_tried_at -= 5  # a few seconds later

        params = query(await oauth.step_up(acr="mfa"))
        assert params["acr_values"] == "mfa"
        assert oauth.is_step_up_supported() is True

    async def test_step_up_does_not_fetch_discovery_on_every_call(self, oauth, http):
        fetched = http.get.call_count
        for _ in range(3):
            with pytest.raises(KindeRetrieveException):
                await oauth.step_up(acr="mfa")
        # One attempt, then the next few seconds of calls fail without waiting on the host
        assert http.get.call_count == fetched + 1

        oauth._openid_configuration_tried_at -= 5
        with pytest.raises(KindeRetrieveException):
            await oauth.step_up(acr="mfa")
        assert http.get.call_count == fetched + 2

    async def test_invalid_requests_are_rejected_before_discovery_is_tried(
        self, oauth, http
    ):
        fetched = http.get.call_count
        with pytest.raises(ValueError):
            await oauth.step_up(acr="mfa", login_options={LoginOptions.PROMPT: "none"})
        assert http.get.call_count == fetched


# ---------------------------------------------------------------------------
# Async and smart clients
# ---------------------------------------------------------------------------


class TestAsyncAndSmartClients:
    @pytest.mark.parametrize("cls", [AsyncOAuth, SmartOAuth])
    async def test_full_step_up_flow(self, http, cls):
        client = make_client(cls)
        assert client.is_step_up_supported() is True
        assert client.get_authentication_context() == {
            "acr": None,
            "amr": [],
            "auth_time": None,
        }

        await sign_in(client, http)
        assert client.has_authentication_context(acr="mfa") is False

        url = await client.step_up(acr="mfa", max_age=300, login_options={"lang": "fr"})
        params = query(url)
        assert (
            params["acr_values"] == "mfa"
            and params["max_age"] == "300"
            and params["lang"] == "fr"
        )

        now = int(time.time())
        stepped_up = token_response(
            "step-up",
            id_claims={"acr": "mfa", "amr": ["pwd", "totp"], "auth_time": now},
        )
        await complete_callback(client, http, url, stepped_up)

        assert client.get_authentication_context() == {
            "acr": "mfa",
            "amr": ["pwd", "totp"],
            "auth_time": now,
        }
        assert client.has_authentication_context(acr="mfa", max_age=300) is True
        assert client.get_tokens(USER_ID)["refresh_token"] == "refresh-step-up"

    @pytest.mark.parametrize("cls", [AsyncOAuth, SmartOAuth])
    async def test_callback_errors(self, http, cls):
        client = make_client(cls)

        state = query(await client.step_up(acr="phr"))["state"]
        with pytest.raises(UnmetAuthenticationRequirementsError) as raised:
            await client.handle_redirect(
                None,
                None,
                state,
                error="unmet_authentication_requirements",
                error_description="Not met",
            )
        assert (
            raised.value.error_description == "Not met" and raised.value.state == state
        )

        state = query(await client.login({LoginOptions.PROMPT: "none"}))["state"]
        with pytest.raises(LoginRequiredError):
            await client.handle_redirect(None, None, state, error="login_required")
        http.post.assert_not_called()

    @pytest.mark.parametrize("cls", [AsyncOAuth, SmartOAuth])
    async def test_validation(self, http, cls):
        client = make_client(cls)
        with pytest.raises(ValueError, match="prompt=none"):
            await client.step_up(
                acr="mfa", login_options={LoginOptions.AUTH_PARAMS: {"prompt": "none"}}
            )
        with pytest.raises(ValueError, match="max_age"):
            await client.login({LoginOptions.MAX_AGE: -1})
        with pytest.raises(ValueError):
            client.has_authentication_context(acr="gold")

    @pytest.mark.parametrize("cls", [AsyncOAuth, SmartOAuth])
    async def test_step_up_without_discovery_support(self, http, cls):
        http.discovery = WITHOUT_STEP_UP
        client = make_client(cls)
        assert client.is_step_up_supported() is False
        with pytest.raises(KindeConfigurationException, match="not supported"):
            await client.step_up(acr="mfa")
        with pytest.raises(KindeConfigurationException, match="not supported"):
            await client.step_up(max_age=60)

    @pytest.mark.parametrize("cls", [AsyncOAuth, SmartOAuth])
    async def test_step_up_while_discovery_is_unavailable(self, http, cls):
        http.discovery_status = 503
        client = make_client(cls)
        with pytest.raises(KindeRetrieveException, match="Try again"):
            await client.step_up(acr="mfa")
        http.discovery_status = 200
        # A few seconds later (step_up() goes through the wrapped sync client)
        core = getattr(client, "_async_oauth", client)._sync_oauth
        core._openid_configuration_tried_at -= 5
        assert query(await client.step_up(acr="mfa"))["acr_values"] == "mfa"
