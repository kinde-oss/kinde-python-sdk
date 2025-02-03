import unittest
import time
from unittest.mock import patch, MagicMock
from kinde_sdk.auth.token_manager import TokenManager

class TestTokenManager(unittest.TestCase):
    def setUp(self):
        self.token_manager = TokenManager(
            client_id="test_client_id",
            client_secret="test_client_secret",
            token_url="https://example.com/token",
        )

    def test_set_tokens(self):
        self.token_manager.set_tokens("access123", "refresh123", 3600)
        self.assertEqual(self.token_manager.tokens["access_token"], "access123")
        self.assertEqual(self.token_manager.tokens["refresh_token"], "refresh123")
        self.assertTrue(self.token_manager.tokens["expires_at"] > time.time())

    def test_get_access_token_valid(self):
        self.token_manager.set_tokens("valid_access_token", "refresh123", 3600)
        access_token = self.token_manager.get_access_token()
        self.assertEqual(access_token, "valid_access_token")

    def test_get_access_token_expired_refresh_success(self):
        self.token_manager.set_tokens("expired_access_token", "refresh123", -10)  # Expired token
        
        with patch("requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "expires_in": 3600,
            }
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response

            new_access_token = self.token_manager.get_access_token()

            self.assertEqual(new_access_token, "new_access_token")
            self.assertEqual(self.token_manager.tokens["refresh_token"], "new_refresh_token")

    def test_get_access_token_expired_no_refresh_token(self):
        self.token_manager.set_tokens("expired_access_token", None, -10)  # No refresh token

        with self.assertRaises(ValueError) as context:
            self.token_manager.get_access_token()
        
        self.assertEqual(str(context.exception), "No valid tokens available")

    def test_refresh_access_token(self):
        self.token_manager.set_tokens("expired_access_token", "valid_refresh_token", -10)  # Expired access token
        
        with patch("requests.post") as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "expires_in": 3600,
            }
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response

            refreshed_token = self.token_manager.refresh_access_token()

            self.assertEqual(refreshed_token, "new_access_token")
            self.assertEqual(self.token_manager.tokens["refresh_token"], "new_refresh_token")

if __name__ == "__main__":
    unittest.main()
