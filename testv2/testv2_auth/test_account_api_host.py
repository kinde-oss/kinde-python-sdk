"""
Account API calls (force_api) must target the configured Kinde domain, not the
generated client's placeholder host or an unverified token's issuer.
"""
import logging
from unittest.mock import MagicMock, patch

import pytest

from kinde_sdk.auth.base_auth import BaseAuth
from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.frontend.api.permissions_api import PermissionsApi

PLACEHOLDER = "your_kinde_subdomain"


@pytest.fixture(autouse=True)
def _no_registered_client_hosts(monkeypatch):
    monkeypatch.setattr(UserSession, "client_hosts", {})


def _auth_with_claims(claims, client_id=None):
    auth = BaseAuth()
    token_manager = MagicMock()
    token_manager.client_id = client_id
    token_manager.get_access_token.return_value = "access-token"
    token_manager.get_claims.return_value = claims
    auth._get_token_manager = lambda: token_manager
    return auth


def test_matching_issuer_is_used(monkeypatch):
    monkeypatch.setenv("KINDE_HOST", "https://acme.kinde.com")
    auth = _auth_with_claims({"iss": "https://ACME.kinde.com/"})

    api = auth._create_authenticated_api_client(PermissionsApi)

    assert api.api_client.configuration.host == "https://acme.kinde.com"
    assert api.api_client.configuration.access_token == "access-token"


def test_issuer_selects_the_oauth_client_host(monkeypatch):
    # e.g. a custom domain passed as OAuth(host=...) while KINDE_HOST is the kinde.com domain
    monkeypatch.setenv("KINDE_HOST", "https://acme.kinde.com")
    UserSession.client_hosts["client_1"] = "https://auth.example.com/"
    auth = _auth_with_claims({"iss": "https://auth.example.com"}, client_id="client_1")

    api = auth._create_authenticated_api_client(PermissionsApi)

    assert api.api_client.configuration.host == "https://auth.example.com"


@pytest.mark.parametrize("issuer", [
    "https://attacker.example",
    "https://acme.kinde.com.attacker.example",
    "https://acme.kinde.com@attacker.example",
    "https://acme.kinde.com:8443",
    "https://acme.kinde.com/evil",
])
def test_mismatched_issuer_is_ignored(monkeypatch, caplog, issuer):
    monkeypatch.setenv("KINDE_HOST", "https://acme.kinde.com")
    auth = _auth_with_claims({"iss": issuer})

    with caplog.at_level(logging.WARNING, logger="kinde_sdk"):
        api = auth._create_authenticated_api_client(PermissionsApi)

    assert api.api_client.configuration.host == "https://acme.kinde.com"
    assert "does not match the configured Kinde host" in caplog.text
    assert "access-token" not in caplog.text


def test_mismatched_issuer_without_a_configured_host_is_refused(monkeypatch):
    monkeypatch.delenv("KINDE_HOST", raising=False)
    auth = _auth_with_claims({"iss": "https://attacker.example"})

    assert auth._create_authenticated_api_client(PermissionsApi) is None


def test_oauth_registers_its_configured_host(monkeypatch):
    monkeypatch.delenv("KINDE_HOST", raising=False)
    with patch("requests.get", side_effect=Exception("offline")):
        OAuth(client_id="client_1", redirect_uri="http://localhost/callback", host="https://acme.kinde.com")
    auth = _auth_with_claims({"iss": "https://acme.kinde.com"}, client_id="client_1")

    api = auth._create_authenticated_api_client(PermissionsApi)

    assert api.api_client.configuration.host == "https://acme.kinde.com"


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


def test_http_kinde_host_fallback_is_refused(monkeypatch):
    # The client would send the access token, so it must not be created for a plain HTTP host
    monkeypatch.setenv("KINDE_HOST", "http://acme.kinde.com")
    for claims in ({}, {"iss": "http://acme.kinde.com"}, {"iss": "https://acme.kinde.com"}):
        assert _auth_with_claims(claims)._create_authenticated_api_client(PermissionsApi) is None


def test_no_client_without_a_host(monkeypatch):
    monkeypatch.delenv("KINDE_HOST", raising=False)
    auth = _auth_with_claims({})

    assert auth._create_authenticated_api_client(PermissionsApi) is None


def test_never_uses_placeholder_host(monkeypatch):
    monkeypatch.setenv("KINDE_HOST", "https://acme.kinde.com")
    for claims in ({}, {"iss": "https://acme.kinde.com"}):
        api = _auth_with_claims(claims)._create_authenticated_api_client(PermissionsApi)
        assert PLACEHOLDER not in api.api_client.configuration.host
