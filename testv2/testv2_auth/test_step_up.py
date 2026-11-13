"""
Step-up authentication (RFC 9470), phase 1: core behaviour.

Every test runs against a real OAuth client with in-memory storage. The
network is replaced by the ``http`` fixture in ``testv2/conftest.py``, so
nothing leaves the machine.
"""

import pytest

from kinde_sdk import AcrValues
from kinde_sdk.auth.login_options import LoginOptions
from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.step_up import (
    normalize_acr_values,
    normalize_max_age,
    normalize_step_up_auth_param,
)
from kinde_sdk.core.storage.storage_manager import StorageManager
from testv2.step_up_helpers import HOST, query

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
