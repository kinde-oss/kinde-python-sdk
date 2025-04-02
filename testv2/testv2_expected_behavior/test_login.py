import unittest
import pytest
from unittest.mock import patch, MagicMock
from urllib.parse import urlparse, parse_qs
import asyncio

from kinde_sdk.auth.oauth import OAuth, IssuerRouteTypes, LoginOptions


class TestExpectedLogin(unittest.TestCase):
    def setUp(self):
        # Set up OAuth with minimal required parameters
        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback",
            framework="None",
            host="https://example.com"  # Use host parameter instead of individual URLs
        )
        
        # Override URLs for testing
        self.oauth.auth_url = "https://example.com/oauth2/auth"
        self.oauth.token_url = "https://example.com/oauth2/token"
        self.oauth.logout_url = "https://example.com/logout"
        self.oauth.userinfo_url = "https://example.com/oauth2/userinfo"

    @pytest.mark.asyncio
    async def test_login_flow(self):
        # Initial login
        login_url = await self.oauth.login()
        self.assertEqual(login_url, "https://example.com/oauth2/auth?client_id=test_client_id&redirect_uri=http%3A%2F%2Flocalhost%2Fcallback&response_type=code&state=1234567890")
        
        # Get initial tokens
        tokens = await self.oauth.get_tokens(user_id="test_code")
        self.assertEqual(tokens["access_token"], "test_access_token")
        self.assertEqual(tokens["refresh_token"], "test_refresh_token")

        # Logout
        self.oauth.logout(user_id="test_code")

        # Try to get tokens after logout - should return None
        tokens = await self.oauth.get_tokens(user_id="test_code")
        self.assertIsNone(tokens, "Tokens should be None after logout")

    @pytest.mark.asyncio
    async def test_register_flow(self):
        # Initial register
        register_url = await self.oauth.register()
        self.assertEqual(register_url, "https://example.com/oauth2/auth?client_id=test_client_id&redirect_uri=http%3A%2F%2Flocalhost%2Fcallback&response_type=code&state=1234567890")
        
        # Get initial tokens
        tokens = await self.oauth.get_tokens(user_id="test_code")
        self.assertEqual(tokens["access_token"], "test_access_token")
        self.assertEqual(tokens["refresh_token"], "test_refresh_token")

        # Logout
        self.oauth.logout(user_id="test_code")

        # Try to get tokens after logout - should return None
        tokens = await self.oauth.get_tokens(user_id="test_code")
        self.assertIsNone(tokens, "Tokens should be None after logout")


if __name__ == "__main__":
    unittest.main()
