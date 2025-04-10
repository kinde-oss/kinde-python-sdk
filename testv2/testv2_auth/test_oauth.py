import unittest
import asyncio
import pytest
import time
from unittest.mock import patch, MagicMock, AsyncMock
from urllib.parse import urlparse, parse_qs
import requests

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.enums import IssuerRouteTypes, PromptTypes
from kinde_sdk.auth.login_options import LoginOptions
from kinde_sdk.exceptions import (
    KindeConfigurationException,
    KindeLoginException,
    KindeTokenException,
)

# Helper function to run async tests in unittest
def run_async(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)

class TestOAuth(unittest.TestCase):
    def setUp(self):
        """Set up for each test"""
        # Set up OAuth with minimal required parameters
        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback",
            framework="flask",  # Use a specific framework
            host="https://example.com"
        )
        
        # Override URLs for testing
        self.oauth.auth_url = "https://example.com/oauth2/auth"
        self.oauth.token_url = "https://example.com/oauth2/token"
        self.oauth.logout_url = "https://example.com/logout"
        self.oauth.userinfo_url = "https://example.com/oauth2/userinfo"
        
        # Setup mocks
        self.setup_mocks()
        
    def setup_mocks(self):
        """Set up mocks for the tests"""
        # Mock storage manager
        self.mock_storage = MagicMock()
        
        # Set up storage get to return values
        def mock_get_side_effect(key):
            if key == "state":
                mock = MagicMock()
                mock.get = lambda k: "test_state" if k == "value" else None
                return mock
            elif key == "code_verifier":
                mock = MagicMock()
                mock.get = lambda k: "test_verifier" if k == "value" else None
                return mock
            elif key == "nonce":
                mock = MagicMock()
                mock.get = lambda k: "test_nonce" if k == "value" else None
                return mock
            return None
        
        self.mock_storage.get = MagicMock(side_effect=mock_get_side_effect)
        
        # Mock session manager
        self.oauth.session_manager = MagicMock()
        self.oauth.session_manager.storage_manager = self.mock_storage
        
        # Mock token manager
        self.mock_token_manager = MagicMock()
        self.mock_token_manager.tokens = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_at": time.time() + 3600
        }
        self.mock_token_manager.get_access_token = MagicMock(return_value="test_access_token")
        self.mock_token_manager.get_id_token = MagicMock(return_value="test_id_token")
        self.mock_token_manager.get_claims = MagicMock(return_value={"sub": "user123", "email": "test@example.com"})
        
        # Make session manager return token manager
        self.oauth.session_manager.get_token_manager = MagicMock(return_value=self.mock_token_manager)

    # Tests for initialization (Lines 46-58)
    def test_init_without_client_id(self):
        """Test initialization without client_id raises exception"""
        with self.assertRaises(KindeConfigurationException):
            OAuth(client_id=None, client_secret="test_secret", redirect_uri="http://localhost/callback")

    def test_init_with_config_file(self):
        """Test initialization with config file"""
        mock_config = {"storage": {"type": "redis", "host": "localhost", "port": 6379}}
        
        with patch("kinde_sdk.auth.oauth.load_config", return_value=mock_config):
            with patch("kinde_sdk.auth.oauth.StorageManager"):
                with patch("kinde_sdk.auth.oauth.UserSession"):
                    oauth = OAuth(
                        client_id="test_client_id",
                        config_file="config.json"
                    )
                    
                    # Just verify it was created without errors
                    self.assertEqual(oauth.client_id, "test_client_id")

    # Tests for Login URL (with proper async handling)
    def test_login_url(self):
        """Test generating login URL"""
        login_url = run_async(self.oauth.login())
        
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

    # Test for empty login options (Line 94)
    def test_login_with_empty_options(self):
        """Test login with empty options dictionary"""
        with patch.object(self.oauth, "generate_auth_url") as mock_gen_url:
            mock_gen_url.return_value = {"url": "https://example.com/oauth2/auth?empty=true"}
            
            # Test with None
            run_async(self.oauth.login(None))
            mock_gen_url.assert_called_with(route_type=IssuerRouteTypes.LOGIN, login_options={})
            
            # Test with empty dict
            run_async(self.oauth.login({}))
            mock_gen_url.assert_called_with(route_type=IssuerRouteTypes.LOGIN, login_options={})

    # Test register URL (with proper async handling)
    def test_register_url(self):
        """Test generating registration URL"""
        register_url = run_async(self.oauth.register())
        
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

    # Test for framework validation in register (Line 254)
    def test_register_without_framework(self):
        """Test register without framework raises exception"""
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback"
            # framework is missing
        )
        
        with self.assertRaises(KindeConfigurationException):
            run_async(oauth.register())

    # Test logout URL
    def test_logout_url(self):
        """Test generating logout URL"""
        logout_url = run_async(self.oauth.logout())
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/logout")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertTrue("redirect_uri" in query_params)

    # Test for framework validation in logout (Line 284)
    def test_logout_without_framework(self):
        """Test logout without framework raises exception"""
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback"
            # framework is missing
        )
        
        with self.assertRaises(KindeConfigurationException):
            run_async(oauth.logout())

    # Test logout with user_id (Lines 289-301)
    def test_logout_with_user_id(self):
        """Test logout with user_id fetches token and clears session"""
        user_id = "user123"
        
        logout_url = run_async(self.oauth.logout(user_id=user_id))
        
        # Verify token manager was accessed
        self.oauth.session_manager.get_token_manager.assert_called_with(user_id)
        # Verify logout was called
        self.oauth.session_manager.logout.assert_called_with(user_id)
        
        # Verify URL
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        self.assertEqual(query_params["client_id"][0], "test_client_id")

    # Tests for handle_redirect (Lines 337-392)
    def test_handle_redirect(self):
        """Test handling OAuth redirect"""
        # Setup mock for exchange_code_for_tokens
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            token_data = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "id_token": "test_id_token",
                "expires_in": 3600
            }
            async def mock_exchange_async(*args, **kwargs):
                return token_data
            mock_exchange.side_effect = mock_exchange_async
            
            # Setup mock for helper_get_user_details
            with patch("kinde_sdk.auth.oauth.helper_get_user_details") as mock_user_details:
                user_details = {
                    "sub": "user123",
                    "email": "test@example.com",
                    "name": "Test User"
                }
                async def mock_user_details_async(*args, **kwargs):
                    return user_details
                mock_user_details.side_effect = mock_user_details_async
                
                # Call handle_redirect
                result = run_async(self.oauth.handle_redirect(
                    code="test_code",
                    user_id="user123",
                    state="test_state"
                ))
                
                # Verify the result
                self.assertEqual(result["tokens"], token_data)
                self.assertEqual(result["user"], user_details)

    # Test for invalid state in handle_redirect (Lines 337-341)
    def test_handle_redirect_invalid_state(self):
        """Test handle_redirect with invalid state"""
        # Make get return None for state
        with patch.object(self.mock_storage, "get", return_value=None):
            with self.assertRaises(KindeLoginException):
                run_async(self.oauth.handle_redirect(
                    code="test_code",
                    user_id="user123",
                    state="test_state"
                ))

    # Test exchange_code_for_tokens (Lines 408-427)
    def test_exchange_code_for_tokens(self):
        """Test exchange_code_for_tokens"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_in": 3600
        }
        
        # Patch requests.post
        with patch("requests.post", return_value=mock_response) as mock_post:
            result = run_async(self.oauth.exchange_code_for_tokens(
                code="test_code",
                code_verifier="test_verifier"
            ))
            
            # Verify post was called with correct data
            args, kwargs = mock_post.call_args
            self.assertEqual(args[0], self.oauth.token_url)
            self.assertEqual(kwargs["data"]["code"], "test_code")
            self.assertEqual(kwargs["data"]["code_verifier"], "test_verifier")
            
            # Verify result
            self.assertEqual(result["access_token"], "test_access_token")

    # Test exchange_code_for_tokens error (Lines 423-425)
    def test_exchange_code_for_tokens_error(self):
        """Test exchange_code_for_tokens with error response"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Invalid grant"
        
        # Patch requests.post
        with patch("requests.post", return_value=mock_response) as mock_post:
            with self.assertRaises(KindeTokenException):
                run_async(self.oauth.exchange_code_for_tokens("test_code"))

    # Test get_tokens (success case)
    def test_get_tokens(self):
        """Test get_tokens success case"""
        result = self.oauth.get_tokens("user123")
        
        self.assertEqual(result["access_token"], "test_access_token")
        self.assertEqual(result["refresh_token"], "test_refresh_token")
        self.assertEqual(result["id_token"], "test_id_token")
        self.assertTrue("expires_at" in result)
        self.assertTrue("expires_in" in result)
        self.assertEqual(result["claims"]["sub"], "user123")
        self.assertEqual(result["claims"]["email"], "test@example.com")

    # Test get_tokens error cases (Lines 552-582)
    def test_get_tokens_no_token_manager(self):
        """Test get_tokens with no token manager"""
        self.oauth.session_manager.get_token_manager.return_value = None
        
        with self.assertRaises(ValueError):
            self.oauth.get_tokens("user123")

    def test_get_tokens_no_access_token(self):
        """Test get_tokens with no access token in tokens"""
        self.mock_token_manager.tokens = {}
        
        with self.assertRaises(ValueError):
            self.oauth.get_tokens("user123")

    def test_get_tokens_invalid_access_token(self):
        """Test get_tokens with invalid access token"""
        self.mock_token_manager.get_access_token.return_value = None
        
        with self.assertRaises(ValueError):
            self.oauth.get_tokens("user123")

if __name__ == "__main__":
    unittest.main()