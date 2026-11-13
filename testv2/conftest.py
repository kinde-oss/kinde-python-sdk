"""Fixtures shared by the test suite."""

from unittest.mock import AsyncMock

import pytest
import requests

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
