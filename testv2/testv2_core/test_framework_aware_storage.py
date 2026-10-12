import unittest
from types import SimpleNamespace
from unittest.mock import patch

from kinde_sdk.core.storage.framework_aware_storage import FrameworkAwareStorage

LOGGER = "kinde_sdk.core.storage.framework_aware_storage"


class TestFrameworkAwareStorage(unittest.TestCase):
    def setUp(self):
        # A FastAPI-style request: the session is a dict on the request
        self.request = SimpleNamespace(session={})
        patcher = patch(f"{LOGGER}.FrameworkContext.get_request", return_value=self.request)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.storage = FrameworkAwareStorage()

    def test_values_round_trip_through_the_session_without_being_logged(self):
        with self.assertLogs(LOGGER, level="DEBUG") as logs:
            self.storage.set("user_1", {"access_token": "secret-token"})
            self.assertEqual(self.storage.get("user_1"), {"access_token": "secret-token"})
            self.storage.set_flat("secret-flat-value")

        self.assertEqual(self.request.session["_flat_data"], "secret-flat-value")
        output = "\n".join(logs.output)
        self.assertIn("Setting key 'user_1' in session", output)
        self.assertIn("Getting key 'user_1' from session", output)
        self.assertNotIn("secret", output)

    def test_without_a_request_nothing_is_read_or_written(self):
        with patch(f"{LOGGER}.FrameworkContext.get_request", return_value=None):
            self.storage.set("user_1", {"access_token": "token"})
            self.assertIsNone(self.storage.get("user_1"))
        self.assertEqual(self.request.session, {})


if __name__ == "__main__":
    unittest.main()
