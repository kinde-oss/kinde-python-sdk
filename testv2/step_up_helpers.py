"""
Shared helpers for the step-up authentication tests.

``FakeHttp`` stands in for ``requests``. The ``http`` fixture in
``testv2/conftest.py`` installs it, so the tests never touch the network.
"""

from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlparse

import jwt

HOST = "https://test.kinde.com"
JWT_KEY = "k" * 32

ENDPOINTS = {
    "authorization_endpoint": f"{HOST}/oauth2/auth",
    "token_endpoint": f"{HOST}/oauth2/token",
    "end_session_endpoint": f"{HOST}/logout",
    "userinfo_endpoint": f"{HOST}/oauth2/userinfo",
}
WITH_STEP_UP = {**ENDPOINTS, "acr_values_supported": ["mfa", "phr"]}
WITHOUT_STEP_UP = dict(ENDPOINTS)


class FakeHttp:
    """Stands in for ``requests``: serves discovery and the token endpoint."""

    def __init__(self):
        self.discovery = WITH_STEP_UP
        self.discovery_status = 200
        self.token_responses = []
        self.get = MagicMock(side_effect=self._get)
        self.post = MagicMock(side_effect=self._post)

    def _get(self, url, **kwargs):
        assert (
            url == f"{HOST}/.well-known/openid-configuration"
        ), f"unexpected GET {url}"
        response = MagicMock()
        response.status_code = self.discovery_status
        response.json.return_value = self.discovery
        return response

    def _post(self, url, data=None, **kwargs):
        assert url == f"{HOST}/oauth2/token", f"unexpected POST {url}"
        assert self.token_responses, "unexpected request to the token endpoint"
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = self.token_responses.pop(0)
        return response

    @property
    def token_requests(self):
        return [call.kwargs["data"] for call in self.post.call_args_list]


def make_jwt(**claims):
    return jwt.encode({"sub": "kp_user", **claims}, JWT_KEY, algorithm="HS256")


def token_response(
    label, access_claims=None, id_claims=None, refresh=True, id_token=True
):
    """A token endpoint response. ``label`` makes each token distinguishable."""
    response = {
        "access_token": make_jwt(jti=f"access-{label}", **(access_claims or {})),
        "expires_in": 3600,
    }
    if id_token:
        response["id_token"] = make_jwt(jti=f"id-{label}", **(id_claims or {}))
    if refresh:
        response["refresh_token"] = f"refresh-{label}"
    return response


def query(url):
    """The query parameters of a URL, as a flat dict."""
    return {
        key: values[0]
        for key, values in parse_qs(urlparse(url).query, keep_blank_values=True).items()
    }
