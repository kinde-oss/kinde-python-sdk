"""
Account API calls (force_api) must target the Kinde domain, not the
generated client's placeholder host.
"""
from unittest.mock import MagicMock

from kinde_sdk.auth.base_auth import BaseAuth
from kinde_sdk.frontend.api.permissions_api import PermissionsApi

PLACEHOLDER = "your_kinde_subdomain"


def _auth_with_claims(claims):
    auth = BaseAuth()
    token_manager = MagicMock()
    token_manager.get_access_token.return_value = "access-token"
    token_manager.get_claims.return_value = claims
    auth._get_token_manager = lambda: token_manager
    return auth


def test_host_comes_from_token_issuer(monkeypatch):
    monkeypatch.setenv("KINDE_HOST", "https://fallback.kinde.com")
    auth = _auth_with_claims({"iss": "https://auth.example.com/"})

    api = auth._create_authenticated_api_client(PermissionsApi)

    assert api.api_client.configuration.host == "https://auth.example.com"
    assert api.api_client.configuration.access_token == "access-token"


def test_host_falls_back_to_kinde_host(monkeypatch):
    monkeypatch.setenv("KINDE_HOST", "https://acme.kinde.com")
    auth = _auth_with_claims({})

    api = auth._create_authenticated_api_client(PermissionsApi)

    assert api.api_client.configuration.host == "https://acme.kinde.com"


def test_non_https_issuer_is_ignored(monkeypatch):
    monkeypatch.setenv("KINDE_HOST", "https://acme.kinde.com")
    auth = _auth_with_claims({"iss": "http://attacker.example"})

    api = auth._create_authenticated_api_client(PermissionsApi)

    assert api.api_client.configuration.host == "https://acme.kinde.com"


def test_no_client_without_a_host(monkeypatch):
    monkeypatch.delenv("KINDE_HOST", raising=False)
    auth = _auth_with_claims({})

    assert auth._create_authenticated_api_client(PermissionsApi) is None


def test_never_uses_placeholder_host(monkeypatch):
    monkeypatch.setenv("KINDE_HOST", "https://acme.kinde.com")
    for claims in ({}, {"iss": "https://acme.kinde.com"}):
        api = _auth_with_claims(claims)._create_authenticated_api_client(PermissionsApi)
        assert PLACEHOLDER not in api.api_client.configuration.host
