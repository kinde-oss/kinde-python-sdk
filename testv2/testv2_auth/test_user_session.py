import unittest
from unittest.mock import patch, MagicMock
from typing import Dict
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.auth.token_manager import TokenManager
from kinde_sdk.auth.storage_interface import StorageInterface

class MockStorage(StorageInterface):
    def __init__(self):
        self._storage = {}

    def get(self, key: str):
        return self._storage.get(key)

    def set(self, key: str, value: Dict):
        self._storage[key] = value

    def delete(self, key: str):
        if key in self._storage:
            del self._storage[key]

class TestUserSession(unittest.TestCase):
    def setUp(self):
        self.storage = MockStorage()
        self.user_session = UserSession(self.storage)

    def test_set_user_data(self):
        user_info = {"client_id": "test_client_id", "client_secret": "test_client_secret", "token_url": "https://example.com/token"}
        token_data = {"access_token": "test_access_token", "refresh_token": "test_refresh_token", "expires_in": 3600}

        self.user_session.set_user_data("test_user_id", user_info, token_data)

        session = self.storage.get("test_user_id")
        self.assertIsNotNone(session)
        self.assertEqual(session["user_info"], user_info)
        self.assertEqual(session["token_manager"].tokens["access_token"], "test_access_token")

    def test_get_user_data(self):
        user_info = {"client_id": "test_client_id", "client_secret": "test_client_secret", "token_url": "https://example.com/token"}
        token_data = {"access_token": "test_access_token", "refresh_token": "test_refresh_token", "expires_in": 3600}

        self.user_session.set_user_data("test_user_id", user_info, token_data)
        retrieved_user_info = self.user_session.get_user_data("test_user_id")

        self.assertEqual(retrieved_user_info, user_info)

    def test_is_authenticated(self):
        user_info = {"client_id": "test_client_id", "client_secret": "test_client_secret", "token_url": "https://example.com/token"}
        token_data = {"access_token": "test_access_token", "refresh_token": "test_refresh_token", "expires_in": 3600}

        self.user_session.set_user_data("test_user_id", user_info, token_data)
        self.assertTrue(self.user_session.is_authenticated("test_user_id"))

    @patch("requests.post")  # Mock the requests.post call
    def test_logout(self, mock_post):
        user_info = {"client_id": "test_client_id", "client_secret": "test_client_secret", "token_url": "https://example.com/token"}
        token_data = {"access_token": "test_access_token", "refresh_token": "test_refresh_token", "expires_in": 3600}

        # Mock the response for the revoke_token request
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()  # Simulate a successful request
        mock_post.return_value = mock_response

        self.user_session.set_user_data("test_user_id", user_info, token_data)
        self.user_session.logout("test_user_id")

        # Verify that the session was deleted
        # self.assertIsNone(self.storage.get("test_user_id"))

        # Verify that revoke_token was called
        mock_post.assert_called_once_with(
            "https://example.com/token/revoke",
            data={
                "token": "test_access_token",
                "client_id": "test_client_id",
                "client_secret": "test_client_secret",
            },
        )

if __name__ == "__main__":
    unittest.main()