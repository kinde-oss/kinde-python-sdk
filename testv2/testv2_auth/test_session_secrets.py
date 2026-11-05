import asyncio
import time
import unittest
from unittest.mock import AsyncMock, patch
from urllib.parse import parse_qs, urlparse

import jwt

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.token_manager import TokenManager
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.core.storage.storage_manager import StorageManager


class TestClientSecretNotPersisted(unittest.TestCase):
    def setUp(self):
        StorageManager().initialize({"type": "memory"})
        TokenManager.reset_instances()
        UserSession.client_secrets.clear()
        self.oauth = self._make_oauth(client_secret="super_secret")

    def tearDown(self):
        StorageManager().initialize({"type": "memory"})
        TokenManager.reset_instances()
        UserSession.client_secrets.clear()

    def _make_oauth(self, client_secret=None):
        with patch("requests.get", side_effect=Exception("offline")):
            return OAuth(
                client_id="secret_test_client",
                client_secret=client_secret,
                redirect_uri="http://localhost/callback",
                host="https://example.kinde.com",
            )

    def _token_data(self):
        return {
            "access_token": jwt.encode({"sub": "user_1"}, "key", algorithm="HS256"),
            "refresh_token": "refresh",
            "expires_in": 3600,
        }

    def _complete_login(self, user_id="user_1"):
        # Start the login through the SDK so a state and nonce are stored, then
        # return them on the callback and in the ID token like Kinde would.
        login_url = asyncio.run(self.oauth.login())
        query = parse_qs(urlparse(login_url).query)
        state, nonce = query["state"][0], query["nonce"][0]
        token_data = {
            **self._token_data(),
            "id_token": jwt.encode({
                "sub": "user_1", "nonce": nonce, "iss": "https://example.kinde.com",
                "aud": ["secret_test_client"], "exp": int(time.time()) + 3600,
            }, "key", algorithm="HS256"),
        }
        with patch.object(OAuth, "exchange_code_for_tokens", AsyncMock(return_value=token_data)), \
                patch("kinde_sdk.auth.oauth.helper_get_user_details", AsyncMock(return_value={})):
            asyncio.run(self.oauth.handle_redirect("code", user_id, state))

    def test_session_storage_has_no_client_secret_but_restored_token_manager_does(self):
        self._complete_login()

        stored = StorageManager().get("user_1")
        self.assertNotIn("client_secret", stored["user_info"])
        self.assertNotIn("super_secret", repr(stored))

        # Simulate a fresh process restoring the session from storage.
        TokenManager.reset_instances()
        token_manager = UserSession().get_token_manager("user_1")
        self.assertEqual(token_manager.client_secret, "super_secret")

    def test_secretless_oauth_instance_does_not_clear_configured_secret(self):
        self._make_oauth(client_secret=None)

        self.assertEqual(UserSession.client_secrets.get("secret_test_client"), "super_secret")

    def test_secret_passed_to_set_user_data_is_used_but_not_stored(self):
        # Using UserSession directly, without an OAuth client registering the secret
        UserSession.client_secrets.clear()
        user_info = {
            "client_id": "direct_client",
            "client_secret": "direct_secret",
            "token_url": "https://example.kinde.com/oauth2/token",
        }

        session = UserSession()
        session.set_user_data("user_2", user_info, self._token_data())

        self.assertEqual(session.get_token_manager("user_2").client_secret, "direct_secret")
        self.assertNotIn("direct_secret", repr(StorageManager().get("user_2")))

    def test_secret_in_user_info_does_not_replace_the_configured_secret(self):
        UserSession().set_user_data("user_3", {
            "client_id": "secret_test_client",
            "client_secret": "other_secret",
            "token_url": "https://example.kinde.com/oauth2/token",
        }, self._token_data())

        self.assertEqual(UserSession.client_secrets["secret_test_client"], "super_secret")

    def _direct_user_info(self, client_secret=None):
        user_info = {"client_id": "direct_client", "token_url": "https://example.kinde.com/oauth2/token"}
        if client_secret:
            user_info["client_secret"] = client_secret
        return user_info

    def test_secret_passed_to_set_user_data_is_not_shared_with_other_sessions(self):
        session = UserSession()
        session.set_user_data("user_2", self._direct_user_info("direct_secret"), self._token_data())
        session.set_user_data("user_4", self._direct_user_info(), self._token_data())

        self.assertNotIn("direct_client", UserSession.client_secrets)
        self.assertIsNone(session.get_token_manager("user_4").client_secret)

    def test_updating_a_session_gives_its_manager_a_new_secret_but_keeps_an_existing_one(self):
        session = UserSession()
        session.set_user_data("user_5", self._direct_user_info(), self._token_data())
        session.set_user_data("user_5", self._direct_user_info("first_secret"), self._token_data())
        self.assertEqual(session.get_token_manager("user_5").client_secret, "first_secret")

        session.set_user_data("user_5", self._direct_user_info("second_secret"), self._token_data())
        self.assertEqual(session.get_token_manager("user_5").client_secret, "first_secret")

    def test_updating_a_session_without_a_secret_uses_the_configured_one(self):
        session = UserSession()
        session.set_user_data("user_6", self._direct_user_info(), self._token_data())
        UserSession.client_secrets["direct_client"] = "configured_secret"

        session.set_user_data("user_6", self._direct_user_info(), self._token_data())
        self.assertEqual(session.get_token_manager("user_6").client_secret, "configured_secret")

    def test_legacy_session_secret_is_dropped_on_load_and_not_saved_again(self):
        # A session written by an older SDK version, with client_secret in user_info
        StorageManager().setItems("user_1", {
            "user_info": {
                "client_id": "secret_test_client",
                "client_secret": "super_secret",
                "token_url": "https://example.kinde.com/oauth2/token",
            },
            "tokens": self._token_data(),
        })

        session = UserSession()
        user_info = session.get_user_data("user_1")
        self.assertNotIn("client_secret", user_info)
        self.assertEqual(session.get_token_manager("user_1").client_secret, "super_secret")
        # Loading alone cleans the stored session, without waiting for a later save
        self.assertNotIn("super_secret", repr(StorageManager().get("user_1")))
        self.assertIn("access_token", StorageManager().get("user_1")["tokens"])

        # Saving the session again must not write the secret back
        session.set_user_data("user_1", {**user_info, "client_secret": "super_secret"}, self._token_data())
        self.assertNotIn("super_secret", repr(StorageManager().get("user_1")))


if __name__ == "__main__":
    unittest.main()
