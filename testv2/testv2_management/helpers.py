"""
Shared helpers for Management API regression tests.

Follows the "less mocking" approach used in test_management_client.py:
real ManagementClient + ApiClient, with only the token manager and HTTP
transport mocked so serialization/deserialization still runs.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Tuple
from unittest.mock import Mock, patch

from kinde_sdk.management.management_client import ManagementClient
from kinde_sdk.management.management_token_manager import ManagementTokenManager
from kinde_sdk.management.rest import RESTResponse


DOMAIN = "test.kinde.com"
CLIENT_ID = "test_client_id"
CLIENT_SECRET = "test_client_secret"
FAKE_TOKEN = "fake_token"


def make_mock_http_response(status: int, body: dict) -> RESTResponse:
    """Wrap a JSON body in a RESTResponse so real deserialization can run."""
    mock_urllib3_response = Mock()
    mock_urllib3_response.status = status
    mock_urllib3_response.reason = "OK" if 200 <= status < 300 else "Error"
    mock_urllib3_response.data = json.dumps(body).encode("utf-8")
    mock_urllib3_response.headers = {"Content-Type": "application/json"}
    return RESTResponse(mock_urllib3_response)


def build_management_client() -> ManagementClient:
    """Create a ManagementClient with token manager construction stubbed."""
    ManagementTokenManager.reset_instances()
    with patch.object(ManagementTokenManager, "__init__", return_value=None):
        with patch.object(
            ManagementTokenManager, "get_access_token", return_value=FAKE_TOKEN
        ):
            client = ManagementClient(DOMAIN, CLIENT_ID, CLIENT_SECRET)
            # Ensure subsequent token lookups succeed after construction.
            client.token_manager.get_access_token = Mock(return_value=FAKE_TOKEN)
            return client


def parse_request_call(mock_request) -> Tuple[str, str, Dict[str, Any], Any]:
    """Extract method, URL, headers, and body from a rest_client.request call."""
    mock_request.assert_called_once()
    call_args = mock_request.call_args
    method = call_args[0][0]
    url = call_args[0][1]
    headers = call_args[1].get("headers") or {}
    body = call_args[1].get("body")
    if isinstance(body, (bytes, bytearray)):
        body = body.decode("utf-8")
    if isinstance(body, str):
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            pass
    return method, url, headers, body


def assert_auth_header(headers: Dict[str, Any], token: str = FAKE_TOKEN) -> None:
    assert headers.get("Authorization") == f"Bearer {token}"


class ManagementHttpTestCase:
    """Mixin/base providing a real client with mocked HTTP for endpoint tests."""

    domain = DOMAIN
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET

    def setup_method(self):
        ManagementTokenManager.reset_instances()
        self._tm_init_patcher = patch.object(
            ManagementTokenManager, "__init__", return_value=None
        )
        self._tm_token_patcher = patch.object(
            ManagementTokenManager, "get_access_token", return_value=FAKE_TOKEN
        )
        self._tm_init_patcher.start()
        self._tm_token_patcher.start()
        self.client = ManagementClient(self.domain, self.client_id, self.client_secret)

    def teardown_method(self):
        self._tm_token_patcher.stop()
        self._tm_init_patcher.stop()
        ManagementTokenManager.reset_instances()

    def mock_response(self, status: int, body: dict) -> RESTResponse:
        return make_mock_http_response(status, body)

    def patch_http(self, response: RESTResponse):
        return patch.object(
            self.client.api_client.rest_client, "request", return_value=response
        )
