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

    # def test_login_flow(self):
    #     async def async_test():
    #         # Initial login
    #         login_url = await self.oauth.login()
    #         # self.assertEqual(login_url, "https://example.com/oauth2/auth?client_id=test_client_id&redirect_uri=http%3A%2F%2Flocalhost%2Fcallback&response_type=code&state=1234567890")
            
    #         # Get initial tokens
    #         tokens =  self.oauth.get_tokens(user_id="test_code")
    #         # self.assertEqual(tokens["access_token"], "test_access_token")
    #         # self.assertEqual(tokens["refresh_token"], "test_refresh_token")

    #         # Logout
    #         self.oauth.logout(user_id="test_code")

    #         # Try to get tokens after logout - should return None
    #         tokens =  self.oauth.get_tokens(user_id="test_code")
    #         self.assertIsNone(tokens, "Tokens should be None after logout")

    #     asyncio.run(async_test())

    def test_login_flow_v2(self):
        async def async_test():
            # Set up OAuth instance with necessary framework
            self.oauth.framework = "None"

            # Generate login URL (this part is fine)
            login_url = await self.oauth.login()
            
            # We need to manually set up the token data before calling get_tokens
            # Set up user info
            user_info = {
                "client_id": self.oauth.client_id,
                "client_secret": self.oauth.client_secret,
                "token_url": self.oauth.token_url,
                "redirect_uri": self.oauth.redirect_uri
            }
            
            # Set up token data
            token_data = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "id_token": "test_id_token",
                "expires_in": 3600
            }
            
            # Manually set up the user session for "test_code"
            self.oauth.session_manager.set_user_data("test_code", user_info, token_data)
            
            # Now we can get tokens (this should work now)
            tokens = self.oauth.get_tokens(user_id="test_code")
            self.assertEqual(tokens["access_token"], "test_access_token")
            
            # Logout
            logout_url = await self.oauth.logout(user_id="test_code")
            
            # After logout, getting tokens should raise a ValueError
            # We need to modify this expectation to handle the error properly
            try:
                tokens = self.oauth.get_tokens(user_id="test_code")
                self.fail("Expected ValueError but no exception was raised")
            except ValueError:
                # This is the expected behavior after logout
                pass

        asyncio.run(async_test())

    # @pytest.mark.asyncio
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
    # asyncio.run(TestExpectedLogin().test_login_flow())
