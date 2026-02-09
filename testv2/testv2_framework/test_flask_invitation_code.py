import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from flask import Flask

from kinde_flask.framework.flask_framework import FlaskFramework


class TestFlaskLoginInvitationCode(unittest.TestCase):
    """Tests for invitation_code extraction in the Flask /login route."""

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "test-secret"
        self.app.config["TESTING"] = True

        self.framework = FlaskFramework(app=self.app)

        # Mock OAuth so no real auth happens
        self.mock_oauth = MagicMock()
        self.mock_oauth.login = AsyncMock(return_value="https://kinde.example.com/authorize")
        self.framework._oauth = self.mock_oauth

        # Register routes
        self.framework._initialized = False
        self.framework._register_kinde_routes()

        self.client = self.app.test_client()

    def test_login_with_invitation_code(self):
        """invitation_code query param is forwarded to oauth.login()."""
        with self.app.test_request_context():
            resp = self.client.get("/login?invitation_code=inv_abc123")

        self.mock_oauth.login.assert_called_once()
        login_options = self.mock_oauth.login.call_args[0][0]
        self.assertEqual(login_options["invitation_code"], "inv_abc123")

    def test_login_without_invitation_code(self):
        """No invitation_code means oauth.login() gets an empty dict."""
        with self.app.test_request_context():
            resp = self.client.get("/login")

        self.mock_oauth.login.assert_called_once()
        login_options = self.mock_oauth.login.call_args[0][0]
        self.assertNotIn("invitation_code", login_options)

    def test_login_with_empty_invitation_code(self):
        """An empty invitation_code query param is not forwarded."""
        with self.app.test_request_context():
            resp = self.client.get("/login?invitation_code=")

        self.mock_oauth.login.assert_called_once()
        login_options = self.mock_oauth.login.call_args[0][0]
        self.assertNotIn("invitation_code", login_options)

    def test_login_redirects_to_oauth_url(self):
        """The route returns a redirect to the URL from oauth.login()."""
        with self.app.test_request_context():
            resp = self.client.get("/login?invitation_code=inv_xyz")

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers["Location"], "https://kinde.example.com/authorize")


if __name__ == "__main__":
    unittest.main()
