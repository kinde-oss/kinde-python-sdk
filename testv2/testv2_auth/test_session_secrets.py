import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import jwt

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.token_manager import TokenManager
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.core.storage.storage_manager import StorageManager


class TestClientSecretNotPersisted(unittest.TestCase):
    def setUp(self):
        StorageManager().initialize({"type": "memory"})
        TokenManager.reset_instances()
        with patch("requests.get", side_effect=Exception("offline")):
            self.oauth = OAuth(
                client_id="secret_test_client",
                client_secret="super_secret",
                redirect_uri="http://localhost/callback",
                host="https://example.kinde.com",
            )

    def tearDown(self):
        StorageManager().initialize({"type": "memory"})
        TokenManager.reset_instances()

    def test_session_storage_has_no_client_secret_but_restored_token_manager_does(self):
        token_data = {
            "access_token": jwt.encode({"sub": "user_1"}, "key", algorithm="HS256"),
            "refresh_token": "refresh",
            "expires_in": 3600,
        }
        with patch.object(OAuth, "exchange_code_for_tokens", AsyncMock(return_value=token_data)), \
                patch("kinde_sdk.auth.oauth.helper_get_user_details", AsyncMock(return_value={})):
            asyncio.run(self.oauth.handle_redirect("code", "user_1"))

        stored = StorageManager().get("user_1")
        self.assertNotIn("client_secret", stored["user_info"])
        self.assertNotIn("super_secret", repr(stored))

        # Simulate a fresh process restoring the session from storage.
        TokenManager.reset_instances()
        token_manager = UserSession().get_token_manager("user_1")
        self.assertEqual(token_manager.client_secret, "super_secret")


if __name__ == "__main__":
    unittest.main()
