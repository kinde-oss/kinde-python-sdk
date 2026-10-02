import copy
import threading
import time
import unittest
from unittest.mock import MagicMock, patch

import jwt
import requests

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.token_manager import TokenManager
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.core.exceptions import KindeTokenPersistenceException
from kinde_sdk.core.storage.memory_storage import MemoryStorage
from kinde_sdk.core.storage.storage_manager import StorageManager

TOKEN_URL = "https://example.kinde.com/oauth2/token"
USER_INFO = {"client_id": "refresh_test_client", "token_url": TOKEN_URL}


def _jwt(sub="user_1"):
    return jwt.encode({"sub": sub, "iat": time.time()}, "key", algorithm="HS256")


class CopyingMemoryStorage(MemoryStorage):
    """Copies values on write and read, like a serialising session store (e.g. Flask-Session
    files), so tests can't pass by sharing a dict with the in-memory token manager."""

    def set(self, key, value):
        super().set(key, copy.deepcopy(value))

    def get(self, key):
        return copy.deepcopy(super().get(key))


def _token_response(status, body):
    response = requests.Response()
    response.status_code = status
    response._content = body.encode()
    return response


class TestTokenRefresh(unittest.TestCase):
    def setUp(self):
        StorageManager().reset()
        StorageManager().initialize({"type": "memory"}, storage=CopyingMemoryStorage())
        TokenManager.reset_instances()
        self.old_access_token = _jwt()
        self.new_access_token = _jwt()
        # Expired access token with a refresh token, as stored after a login with the offline scope
        self.expired_tokens = {
            "access_token": self.old_access_token,
            "refresh_token": "old_refresh_token",
            "expires_in": -10,
        }
        self.refresh_ok = _token_response(
            200,
            '{"access_token": "%s", "refresh_token": "new_refresh_token", "expires_in": 3600}'
            % self.new_access_token,
        )

    def tearDown(self):
        StorageManager().reset()
        TokenManager.reset_instances()

    def test_refresh_does_not_deadlock(self):
        token_manager = TokenManager("user_1", "refresh_test_client", "secret", TOKEN_URL)
        token_manager.set_tokens(self.expired_tokens)
        result = {}

        def get_token():
            result["token"] = token_manager.get_access_token()

        with patch("kinde_sdk.auth.token_manager.requests.post", return_value=self.refresh_ok):
            thread = threading.Thread(target=get_token, daemon=True)
            thread.start()
            thread.join(5)

        self.assertFalse(thread.is_alive(), "get_access_token() blocked while refreshing")
        self.assertEqual(result["token"], self.new_access_token)

    def test_refreshed_tokens_are_saved_to_session_storage(self):
        UserSession().set_user_data("user_1", dict(USER_INFO), self.expired_tokens)

        with patch("kinde_sdk.auth.token_manager.requests.post", return_value=self.refresh_ok):
            self.assertTrue(UserSession().is_authenticated("user_1"))

        stored_tokens = StorageManager().get("user_1")["tokens"]
        self.assertEqual(stored_tokens["access_token"], self.new_access_token)
        self.assertEqual(stored_tokens["refresh_token"], "new_refresh_token")

        # A restarted process restores the refreshed tokens, not the used refresh token
        TokenManager.reset_instances()
        restored = UserSession().get_token_manager("user_1")
        self.assertEqual(restored.tokens["refresh_token"], "new_refresh_token")

    def _saved_by_other_worker(self, tokens):
        """Overwrite the stored session as another worker's refresh would."""
        StorageManager().setItems("user_1", {"user_info": dict(USER_INFO), "tokens": tokens})

    def test_direct_refresh_access_token_call_saves_rotated_tokens(self):
        session = UserSession()
        session.set_user_data("user_1", dict(USER_INFO), self.expired_tokens)

        with patch("kinde_sdk.auth.token_manager.requests.post", return_value=self.refresh_ok):
            session.get_token_manager("user_1").refresh_access_token()

        self.assertEqual(StorageManager().get("user_1")["tokens"]["refresh_token"], "new_refresh_token")

    def test_get_access_token_saves_once_per_refresh(self):
        session = UserSession()
        session.set_user_data("user_1", dict(USER_INFO), self.expired_tokens)
        token_manager = session.get_token_manager("user_1")
        save = MagicMock(wraps=token_manager.on_tokens_refreshed)
        token_manager.on_tokens_refreshed = save

        with patch("kinde_sdk.auth.token_manager.requests.post", return_value=self.refresh_ok):
            token_manager.get_access_token()
            token_manager.get_access_token()  # Still valid: no refresh, no save

        self.assertEqual(save.call_count, 1)

    def test_uses_tokens_another_worker_already_refreshed(self):
        # This worker has the session cached with an expired access token
        session = UserSession()
        session.set_user_data("user_1", dict(USER_INFO), self.expired_tokens)
        # Another worker refreshed and saved new tokens, rotating the refresh token
        self._saved_by_other_worker({
            "access_token": self.new_access_token,
            "refresh_token": "rotated_by_other_worker",
            "expires_at": time.time() + 3600,
        })

        with patch("kinde_sdk.auth.token_manager.requests.post") as post:
            self.assertEqual(session.get_token_manager("user_1").get_access_token(), self.new_access_token)
        post.assert_not_called()

    def test_refreshes_with_the_latest_saved_refresh_token(self):
        session = UserSession()
        session.set_user_data("user_1", dict(USER_INFO), self.expired_tokens)
        # Another worker refreshed earlier; its access token has since expired too
        self._saved_by_other_worker({
            "access_token": _jwt(),
            "refresh_token": "rotated_by_other_worker",
            "expires_at": time.time() - 1,
        })

        with patch("kinde_sdk.auth.token_manager.requests.post", return_value=self.refresh_ok) as post:
            self.assertEqual(session.get_token_manager("user_1").get_access_token(), self.new_access_token)
        self.assertEqual(post.call_args.kwargs["data"]["refresh_token"], "rotated_by_other_worker")

    def test_failed_save_keeps_tokens_raises_and_is_retried_without_refreshing(self):
        session = UserSession()
        session.set_user_data("user_1", dict(USER_INFO), self.expired_tokens)
        token_manager = session.get_token_manager("user_1")

        with patch("kinde_sdk.auth.token_manager.requests.post", return_value=self.refresh_ok) as post:
            with patch.object(StorageManager, "setItems", side_effect=OSError("disk full")), \
                    self.assertRaises(KindeTokenPersistenceException) as raised:
                token_manager.get_access_token()
            # The refreshed tokens are kept and handed to the caller
            self.assertEqual(raised.exception.access_token, self.new_access_token)
            self.assertEqual(token_manager.tokens["refresh_token"], "new_refresh_token")
            self.assertEqual(StorageManager().get("user_1")["tokens"]["refresh_token"], "old_refresh_token")

            # Next call: storage works again, the save is retried and Kinde isn't called again
            self.assertEqual(token_manager.get_access_token(), self.new_access_token)
            self.assertEqual(post.call_count, 1)
        self.assertEqual(StorageManager().get("user_1")["tokens"]["refresh_token"], "new_refresh_token")

    def test_user_stays_authenticated_when_saving_refreshed_tokens_fails(self):
        session = UserSession()
        session.set_user_data("user_1", dict(USER_INFO), self.expired_tokens)

        with patch("kinde_sdk.auth.token_manager.requests.post", return_value=self.refresh_ok), \
                patch.object(StorageManager, "setItems", side_effect=OSError("disk full")):
            self.assertTrue(session.is_authenticated("user_1"))

    def test_refresh_failure_is_logged_without_token_values(self):
        UserSession().set_user_data("user_1", dict(USER_INFO), self.expired_tokens)
        rejected = _token_response(400, '{"error": "invalid_grant", "error_description": "expired"}')

        with patch("kinde_sdk.auth.token_manager.requests.post", return_value=rejected), \
                self.assertLogs("kinde_sdk.auth", level="WARNING") as logs:
            self.assertFalse(UserSession().is_authenticated("user_1"))

        output = "\n".join(logs.output)
        self.assertIn("Token refresh failed: HTTP 400 (invalid_grant)", output)
        self.assertNotIn("old_refresh_token", output)
        self.assertNotIn(self.old_access_token, output)


class TestFrameworkSessionSurvivesRestart(unittest.TestCase):
    def setUp(self):
        StorageManager().reset()
        TokenManager.reset_instances()
        # Stands in for the framework's session store (e.g. Flask-Session files),
        # which outlives the process
        self.session_store = MemoryStorage()

    def tearDown(self):
        StorageManager().reset()
        TokenManager.reset_instances()

    def _start_process(self):
        """Simulate an app process starting: a new random device id, then OAuth set-up."""
        StorageManager()._device_id = None
        TokenManager.reset_instances()
        framework = MagicMock()
        framework.get_name.return_value = "flask"
        with patch("kinde_sdk.auth.oauth.FrameworkFactory.create_framework", return_value=framework), \
                patch("kinde_sdk.auth.oauth.StorageFactory.create_storage", return_value=self.session_store), \
                patch("requests.get", side_effect=Exception("offline")):
            OAuth(
                client_id="refresh_test_client",
                redirect_uri="http://localhost/callback",
                host="https://example.kinde.com",
                framework="flask",
                app=MagicMock(),
            )

    def test_session_is_found_after_restart(self):
        self._start_process()
        self.assertEqual(StorageManager().get_device_id(), "flask")
        UserSession().set_user_data(
            "user_1", dict(USER_INFO), {"access_token": _jwt(), "expires_in": 3600}
        )

        self._start_process()

        self.assertEqual(StorageManager().get_device_id(), "flask")
        self.assertIsNotNone(UserSession().get_token_manager("user_1"))


if __name__ == "__main__":
    unittest.main()
