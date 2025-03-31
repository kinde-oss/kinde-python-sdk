import unittest
import pytest
from unittest.mock import patch, MagicMock
from urllib.parse import urlparse, parse_qs
import asyncio

from kinde_sdk.auth.oauth import OAuth, IssuerRouteTypes, LoginOptions


class TestOAuth(unittest.TestCase):
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
    async def test_login_url(self):
        """Test generating login URL"""
        login_url = await self.oauth.login()
        
        parsed_url = urlparse(login_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/oauth2/auth")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/callback")
        self.assertEqual(query_params["response_type"][0], "code")
        self.assertEqual(query_params["scope"][0], "openid profile email")
        self.assertTrue("state" in query_params)
        self.assertTrue("nonce" in query_params)
        self.assertTrue("code_challenge" in query_params)
        self.assertEqual(query_params["code_challenge_method"][0], "S256")

    @pytest.mark.asyncio
    async def test_register_url(self):
        """Test generating registration URL"""
        register_url = await self.oauth.register()
        
        parsed_url = urlparse(register_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/oauth2/auth")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/callback")
        self.assertEqual(query_params["prompt"][0], "create")
        self.assertEqual(query_params["response_type"][0], "code")
        self.assertEqual(query_params["scope"][0], "openid profile email")

    @pytest.mark.asyncio
    async def test_login_with_options(self):
        """Test login with specific options"""
        login_options = {
            LoginOptions.RESPONSE_TYPE: "code",
            LoginOptions.SCOPE: "openid profile email offline_access",
            LoginOptions.STATE: "custom_state",
            LoginOptions.NONCE: "custom_nonce",
            LoginOptions.ORG_CODE: "test_org",
            LoginOptions.IS_CREATE_ORG: True,
            LoginOptions.LANG: "en"
        }
        
        login_url = await self.oauth.login(login_options)
        
        parsed_url = urlparse(login_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["scope"][0], "openid profile email offline_access")
        self.assertEqual(query_params["state"][0], "custom_state")
        self.assertEqual(query_params["nonce"][0], "custom_nonce")
        self.assertEqual(query_params["org_code"][0], "test_org")
        self.assertEqual(query_params["is_create_org"][0], "true")
        self.assertEqual(query_params["lang"][0], "en")

    @pytest.mark.asyncio
    async def test_logout_url(self):
        """Test generating logout URL"""
        logout_url = await self.oauth.logout()
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/logout")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertTrue("redirect_uri" in query_params)

    @pytest.mark.asyncio
    async def test_logout_with_options(self):
        """Test logout with specific options"""
        logout_options = {
            "post_logout_redirect_uri": "http://example.com/post-logout",
            "state": "logout_state",
            "id_token_hint": "some_id_token"
        }
        
        logout_url = await self.oauth.logout(logout_options=logout_options)
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://example.com/post-logout")
        self.assertEqual(query_params["state"][0], "logout_state")
        self.assertEqual(query_params["id_token_hint"][0], "some_id_token")

    @pytest.mark.asyncio
    async def test_handle_redirect(self):
        """Test handling OAuth redirect"""
        # Set up mocks
        mock_exchange = patch.object(self.oauth, 'exchange_code_for_tokens')
        mock_user_details = patch.object(self.oauth, 'get_user_details')
        
        # Mock responses
        token_data = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_in": 3600
        }
        
        user_details = {
            "sub": "user123",
            "email": "test@example.com",
            "name": "Test User"
        }
        
        # Set state in storage for verification
        self.oauth.session_manager.storage.set("state", {"value": "test_state"})
        self.oauth.session_manager.storage.set("code_verifier", {"value": "test_verifier"})
        
        with mock_exchange as m_exchange, mock_user_details as m_user_details:
            m_exchange.return_value = token_data
            m_user_details.return_value = user_details
            
            result = await self.oauth.handle_redirect(
                code="test_code",
                user_id="user123",
                state="test_state"
            )
            
            # Check the exchange was called correctly
            m_exchange.assert_called_once_with("test_code", "test_verifier")
            
            # Check user details were fetched
            m_user_details.assert_called_once_with("user123")
            
            # Check result
            self.assertEqual(result["tokens"], token_data)
            self.assertEqual(result["user"], user_details)
            
            # Verify state was cleaned up
            self.assertIsNone(self.oauth.session_manager.storage.get("state"))
            self.assertIsNone(self.oauth.session_manager.storage.get("code_verifier"))

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])