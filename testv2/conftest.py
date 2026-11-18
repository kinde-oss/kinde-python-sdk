"""Fixtures shared by the test suite."""

from unittest.mock import AsyncMock

import pytest
import requests

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.token_manager import TokenManager
from kinde_sdk.core.framework.null_framework import NullFramework
from testv2.step_up_helpers import FakeHttp


@pytest.fixture
def http(monkeypatch):
    """
    Replace the network with a fake Kinde (discovery and the token endpoint).

    Opt-in: only tests that ask for ``http`` get it. Any other request fails
    the test.
    """
    fake = FakeHttp()
    monkeypatch.setattr(requests, "get", fake.get)
    monkeypatch.setattr(requests, "post", fake.post)

    # Kinde returns the nonce of an authorization request in the ID token it
    # issues for that request's code. The fake does the same.
    generate_auth_url = OAuth.generate_auth_url

    async def generate_auth_url_and_note_nonce(self, *args, **kwargs):
        auth_url_data = await generate_auth_url(self, *args, **kwargs)
        fake.nonce = auth_url_data["nonce"]
        return auth_url_data

    monkeypatch.setattr(OAuth, "generate_auth_url", generate_auth_url_and_note_nonce)
    monkeypatch.setattr(
        "kinde_sdk.auth.oauth.helper_get_user_details",
        AsyncMock(return_value={"id": "kp_user"}),
    )
    # Creating a client gives the storage manager a fresh store
    TokenManager.reset_instances()
    NullFramework().clear_user_id()
    yield fake
    NullFramework().clear_user_id()
    TokenManager.reset_instances()
