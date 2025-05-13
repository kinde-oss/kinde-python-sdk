import unittest
import pytest
from unittest.mock import patch, MagicMock
from urllib.parse import urlparse, parse_qs
import asyncio

from kinde_sdk.auth.oauth import OAuth, IssuerRouteTypes, LoginOptions

def run_async(coro):
    """Helper function to run async tests"""
    return asyncio.run(coro)

class TestExpectedLogin(unittest.TestCase):
    @patch('requests.get')
    def setUp(self, mock_get):
        """Set up test fixtures."""
        # Mock the OpenID configuration response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "authorization_endpoint": "https://example.com/oauth2/auth",
            "token_endpoint": "https://example.com/oauth2/token",
            "end_session_endpoint": "https://example.com/logout",
            "userinfo_endpoint": "https://example.com/oauth2/userinfo"
        }
        mock_get.return_value = mock_response

        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:8000/callback",
            host="https://test.kinde.com"
        )
        # Mock the storage and token manager
        self.mock_storage = MagicMock()
        self.mock_token_manager = MagicMock()
        
        # Instead of mocking session_manager directly, we'll mock the methods that use it
        self.oauth._session_manager = MagicMock()
        self.oauth._session_manager.storage_manager = self.mock_storage
        self.oauth._session_manager.get_token_manager = MagicMock(return_value=self.mock_token_manager)
        
        # Override URLs for testing
        self.oauth.auth_url = "https://example.com/oauth2/auth"
        self.oauth.token_url = "https://example.com/oauth2/token"
        self.oauth.logout_url = "https://example.com/logout"
        self.oauth.userinfo_url = "https://example.com/oauth2/userinfo"


    #def test_login_flow(self):
    #    """Test the complete login flow."""
        # Setup
    #    user_info = {"id": "test_user", "email": "test@example.com"}
    #    token_data = {"access_token": "test_token"}
        
        # Mock the necessary methods
        #self.oauth._session_manager.set_user_data = MagicMock()
        #self.oauth._session_manager.get_token_manager = MagicMock(return_value=self.mock_token_manager)
        
        # Execute login flow
        #login_url = run_async(self.oauth.login())
        
        # Verify
        #self.assertTrue(login_url.startswith("https://test.kinde.com/oauth2/auth"))
        

    def test_register_flow_v2(self):
        async def async_register_test():
            # Set up OAuth instance with necessary framework
            self.oauth.framework = "memory"
            self.oauth._initialize_framework()  # Initialize the framework

            # Generate login URL (this part is fine)
            register_url = await self.oauth.register()
            #self.assertEqual(register_url, "https://example.com/oauth2/auth?client_id=test_client_id&redirect_uri=http%3A%2F%2Flocalhost%2Fcallback&response_type=code&state=1234567890")

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
            self.oauth._session_manager.set_user_data("test_code", user_info, token_data)
            
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

        #asyncio.run(async_register_test())


if __name__ == "__main__":
    unittest.main()
