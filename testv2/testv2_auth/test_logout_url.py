"""Logout URL parameters understood by Kinde's /logout endpoint."""
import asyncio
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import pytest

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.core.storage.storage_manager import StorageManager


@pytest.fixture
def oauth():
    sm = StorageManager()
    saved = (sm._storage, sm._device_id, sm._storage_type)
    with patch.object(FrameworkFactory, "_framework_instance", None):
        yield OAuth(
            client_id="logout_client",
            redirect_uri="http://localhost/callback",
            host="https://example.kinde.com",
        )
    sm._storage, sm._device_id, sm._storage_type = saved


def _params(url):
    return {k: v[0] for k, v in parse_qs(urlparse(url).query).items()}


def test_explicit_post_logout_redirect(oauth, monkeypatch):
    monkeypatch.setenv("KINDE_POST_LOGOUT_REDIRECT_URI", "http://localhost/from-env")
    url = asyncio.run(oauth.logout(logout_options={"post_logout_redirect_uri": "http://localhost/bye"}))

    params = _params(url)
    assert params["redirect"] == "http://localhost/bye"
    assert params["redirect_uri"] == "http://localhost/bye"


def test_post_logout_redirect_from_env(oauth, monkeypatch):
    monkeypatch.setenv("KINDE_POST_LOGOUT_REDIRECT_URI", "http://localhost/")
    assert _params(asyncio.run(oauth.logout()))["redirect"] == "http://localhost/"


def test_falls_back_to_redirect_uri(oauth, monkeypatch):
    monkeypatch.delenv("KINDE_POST_LOGOUT_REDIRECT_URI", raising=False)
    params = _params(asyncio.run(oauth.logout()))
    assert params["redirect"] == "http://localhost/callback"
    assert params["client_id"] == "logout_client"
