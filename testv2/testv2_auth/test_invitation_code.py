import unittest
import asyncio
from unittest.mock import patch, MagicMock
from urllib.parse import urlparse, parse_qs

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.enums import IssuerRouteTypes
from kinde_sdk.auth.login_options import LoginOptions


def run_async(coro):
    """Helper function to run async tests"""
    return asyncio.run(coro)


class TestInvitationCode(unittest.TestCase):
    """Tests for invitation code support in OAuth login flow."""

    @patch("requests.get")
    def setUp(self, mock_get):
        """Set up test fixtures."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "authorization_endpoint": "https://example.com/oauth2/auth",
            "token_endpoint": "https://example.com/oauth2/token",
            "end_session_endpoint": "https://example.com/logout",
            "userinfo_endpoint": "https://example.com/oauth2/userinfo",
        }
        mock_get.return_value = mock_response

        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:8000/callback",
            host="https://test.kinde.com",
        )
        self.mock_storage = MagicMock()
        self.oauth._session_manager = MagicMock()
        self.oauth._session_manager.storage_manager = self.mock_storage
        self.oauth.auth_url = "https://example.com/oauth2/auth"

    # -- LoginOptions constants --

    def test_login_options_has_invitation_code_constant(self):
        """INVITATION_CODE constant is defined on LoginOptions."""
        self.assertEqual(LoginOptions.INVITATION_CODE, "invitation_code")

    def test_login_options_has_is_invitation_constant(self):
        """IS_INVITATION constant is defined on LoginOptions."""
        self.assertEqual(LoginOptions.IS_INVITATION, "is_invitation")

    # -- generate_auth_url: invitation_code --

    def test_invitation_code_appears_in_auth_url(self):
        """invitation_code is forwarded as a query parameter."""
        result = run_async(
            self.oauth.generate_auth_url(
                login_options={LoginOptions.INVITATION_CODE: "abc123"}
            )
        )
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["invitation_code"], ["abc123"])

    def test_invitation_code_auto_sets_is_invitation(self):
        """is_invitation is automatically set to 'true' when invitation_code is present."""
        result = run_async(
            self.oauth.generate_auth_url(
                login_options={LoginOptions.INVITATION_CODE: "abc123"}
            )
        )
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["is_invitation"], ["true"])

    def test_invitation_code_with_explicit_is_invitation_true(self):
        """Explicit is_invitation=True is honoured alongside invitation_code."""
        result = run_async(
            self.oauth.generate_auth_url(
                login_options={
                    LoginOptions.INVITATION_CODE: "abc123",
                    LoginOptions.IS_INVITATION: True,
                }
            )
        )
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["invitation_code"], ["abc123"])
        self.assertEqual(params["is_invitation"], ["true"])

    def test_invitation_code_with_explicit_is_invitation_false(self):
        """When invitation_code is present but is_invitation is explicitly False,
        the auto-set logic still adds is_invitation='true'."""
        result = run_async(
            self.oauth.generate_auth_url(
                login_options={
                    LoginOptions.INVITATION_CODE: "abc123",
                    LoginOptions.IS_INVITATION: False,
                }
            )
        )
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["is_invitation"], ["true"])

    def test_is_invitation_alone_without_invitation_code(self):
        """is_invitation=True can be set independently of invitation_code."""
        result = run_async(
            self.oauth.generate_auth_url(
                login_options={LoginOptions.IS_INVITATION: True}
            )
        )
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["is_invitation"], ["true"])
        self.assertNotIn("invitation_code", params)

    def test_is_invitation_false_alone_not_in_url(self):
        """is_invitation=False without invitation_code produces no is_invitation param."""
        result = run_async(
            self.oauth.generate_auth_url(
                login_options={LoginOptions.IS_INVITATION: False}
            )
        )
        params = parse_qs(urlparse(result["url"]).query)
        self.assertNotIn("is_invitation", params)

    def test_no_invitation_params_by_default(self):
        """Neither invitation_code nor is_invitation appear when not requested."""
        result = run_async(self.oauth.generate_auth_url(login_options={}))
        params = parse_qs(urlparse(result["url"]).query)
        self.assertNotIn("invitation_code", params)
        self.assertNotIn("is_invitation", params)

    def test_invitation_code_empty_string_not_set(self):
        """An empty invitation_code does not add is_invitation."""
        result = run_async(
            self.oauth.generate_auth_url(
                login_options={LoginOptions.INVITATION_CODE: ""}
            )
        )
        params = parse_qs(urlparse(result["url"]).query)
        self.assertNotIn("is_invitation", params)

    def test_invitation_code_none_not_set(self):
        """invitation_code=None is ignored."""
        result = run_async(
            self.oauth.generate_auth_url(
                login_options={LoginOptions.INVITATION_CODE: None}
            )
        )
        params = parse_qs(urlparse(result["url"]).query)
        self.assertNotIn("invitation_code", params)
        self.assertNotIn("is_invitation", params)

    # -- login() wrapper --

    def test_login_passes_invitation_code(self):
        """login() forwards invitation_code to the generated URL."""
        url = run_async(
            self.oauth.login(
                login_options={LoginOptions.INVITATION_CODE: "inv_xyz"}
            )
        )
        params = parse_qs(urlparse(url).query)
        self.assertEqual(params["invitation_code"], ["inv_xyz"])
        self.assertEqual(params["is_invitation"], ["true"])

    def test_login_without_invitation_code(self):
        """login() without invitation options produces no invitation params."""
        url = run_async(self.oauth.login())
        params = parse_qs(urlparse(url).query)
        self.assertNotIn("invitation_code", params)
        self.assertNotIn("is_invitation", params)

    # -- register() wrapper --

    def test_register_passes_invitation_code(self):
        """register() forwards invitation_code to the generated URL."""
        url = run_async(
            self.oauth.register(
                login_options={LoginOptions.INVITATION_CODE: "inv_reg"}
            )
        )
        params = parse_qs(urlparse(url).query)
        self.assertEqual(params["invitation_code"], ["inv_reg"])
        self.assertEqual(params["is_invitation"], ["true"])

    # -- Coexistence with other params --

    def test_invitation_code_with_org_code(self):
        """invitation_code works alongside org_code."""
        result = run_async(
            self.oauth.generate_auth_url(
                login_options={
                    LoginOptions.INVITATION_CODE: "abc123",
                    LoginOptions.ORG_CODE: "org_456",
                }
            )
        )
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["invitation_code"], ["abc123"])
        self.assertEqual(params["is_invitation"], ["true"])
        self.assertEqual(params["org_code"], ["org_456"])


if __name__ == "__main__":
    unittest.main()
