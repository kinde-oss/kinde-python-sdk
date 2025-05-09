import unittest
import asyncio
import pytest
import time
import os
from unittest.mock import patch, MagicMock, AsyncMock
from urllib.parse import urlparse, parse_qs
import requests

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.enums import IssuerRouteTypes, PromptTypes
from kinde_sdk.auth.login_options import LoginOptions
from kinde_sdk.core.exceptions import (
    KindeConfigurationException,
    KindeLoginException,
    KindeTokenException,
    KindeRetrieveException,
)

# Helper function to run async tests in unittest
# def run_async(coro):
#     loop = asyncio.get_event_loop()
#     return loop.run_until_complete(coro)

def run_async(coro):
    try:
        # Use the running event loop if available
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Create a new event loop if none exists
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

class TestOAuthExtended(unittest.TestCase):
    def setUp(self):
        """Set up for each test"""
        # Set up OAuth with minimal required parameters
        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback",
            framework="flask",  # Use a specific framework
            host="https://example.com",
            audience="test_audience"  # Adding audience parameter to test line 94
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
        self.oauth._session_manager = MagicMock()
        self.oauth._session_manager.storage_manager = self.mock_storage
        
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
        self.oauth._session_manager.get_token_manager = MagicMock(return_value=self.mock_token_manager)
        
    # Test for None value handling in auth_params
    def test_none_values_in_auth_params(self):
        """Test how None values are handled in auth_params"""
        login_options = {
            LoginOptions.AUTH_PARAMS: {
                "param_with_value": "test_value",
                "param_with_none": None
            }
        }
        
        auth_url_data = run_async(self.oauth.generate_auth_url(login_options=login_options))
        
        # Parse URL to check parameters
        parsed_url = urlparse(auth_url_data["url"])
        query_params = parse_qs(parsed_url.query)
        query_string = parsed_url.query
        
        # Check that param_with_value is included
        self.assertIn("param_with_value", query_params)
        self.assertEqual(query_params["param_with_value"][0], "test_value")
        
        # This test helps us understand how None values are handled
        # Based on your implementation, adjust this assert accordingly
        self.assertNotIn("param_with_none", query_params)
    
    # Test for URL generation with various login options (fixed to not check for None values)
    def test_generate_auth_url_with_all_options(self):
        """Test auth URL generation with all possible options"""
        login_options = {
            # Standard OAuth params
            LoginOptions.RESPONSE_TYPE: "code",
            LoginOptions.REDIRECT_URI: "http://localhost/custom-callback",
            LoginOptions.SCOPE: "openid profile email offline_access",
            LoginOptions.AUDIENCE: "custom_audience",
            # Organization params
            LoginOptions.ORG_CODE: "org123",
            LoginOptions.ORG_NAME: "Test Organization",
            LoginOptions.IS_CREATE_ORG: True,
            # User experience params
            LoginOptions.PROMPT: PromptTypes.CONSENT.value,
            LoginOptions.LANG: "en",
            LoginOptions.LOGIN_HINT: "user@example.com",
            LoginOptions.CONNECTION_ID: "conn123",
            LoginOptions.REDIRECT_URL: "http://localhost/success",
            LoginOptions.HAS_SUCCESS_PAGE: True,
            LoginOptions.WORKFLOW_DEPLOYMENT_ID: "workflow123",
            # Additional auth params
            LoginOptions.AUTH_PARAMS: {
                "custom_param1": "value1",
                "custom_param2": "value2",
                # Don't include custom_param3: None, since it won't be included in the URL
            },
            # Security params
            LoginOptions.STATE: "custom_state",
            LoginOptions.NONCE: "custom_nonce",
            LoginOptions.CODE_CHALLENGE: "custom_challenge",
            LoginOptions.CODE_CHALLENGE_METHOD: "plain",
        }
        
        auth_url_data = run_async(self.oauth.generate_auth_url(
            route_type=IssuerRouteTypes.LOGIN,
            login_options=login_options
        ))
        
        # Verify URL and parameters
        parsed_url = urlparse(auth_url_data["url"])
        query_params = parse_qs(parsed_url.query)
        
        # Check all parameters made it to the URL
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["response_type"][0], "code")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/custom-callback")
        self.assertEqual(query_params["scope"][0], "openid profile email offline_access")
        self.assertEqual(query_params["audience"][0], "custom_audience")
        self.assertEqual(query_params["org_code"][0], "org123")
        self.assertEqual(query_params["org_name"][0], "Test Organization")
        self.assertEqual(query_params["is_create_org"][0], "true")
        self.assertEqual(query_params["prompt"][0], "consent")
        self.assertEqual(query_params["lang"][0], "en")
        self.assertEqual(query_params["login_hint"][0], "user@example.com")
        self.assertEqual(query_params["connection_id"][0], "conn123")
        self.assertEqual(query_params["redirect_url"][0], "http://localhost/success")
        self.assertEqual(query_params["has_success_page"][0], "true")
        self.assertEqual(query_params["workflow_deployment_id"][0], "workflow123")
        self.assertEqual(query_params["custom_param1"][0], "value1")
        self.assertEqual(query_params["custom_param2"][0], "value2")
        # We don't check for custom_param3 since it won't be in the URL
        
        # Verify returned values
        self.assertEqual(auth_url_data["state"], "custom_state")
        self.assertEqual(auth_url_data["nonce"], "custom_nonce")
        self.assertEqual(auth_url_data["code_challenge"], "custom_challenge")
        self.assertEqual(auth_url_data["code_verifier"], "")
    
    # Test for handling errors when getting user details (coverage for line 146-148, 163)
    def test_handle_redirect_token_manager_failure(self):
        """Test handling redirect when token manager can't be retrieved"""
        # Make get_token_manager return None
        self.oauth._session_manager.get_token_manager.return_value = None
        
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            async def mock_exchange_async(*args, **kwargs):
                return {"access_token": "test_token"}
            mock_exchange.side_effect = mock_exchange_async
            
            # Test should raise KindeRetrieveException
            with self.assertRaises(KindeRetrieveException):
                run_async(self.oauth.handle_redirect(
                    code="test_code",
                    user_id="user123"
                ))

    # Test for helper_get_user_details failure (for line 177)
    def test_handle_redirect_user_details_failure(self):
        """Test handling redirect when user details retrieval fails"""
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            async def mock_exchange_async(*args, **kwargs):
                return {"access_token": "test_token"}
            mock_exchange.side_effect = mock_exchange_async
            
            # Mock helper_get_user_details to raise an exception
            with patch("kinde_sdk.auth.oauth.helper_get_user_details") as mock_get_user:
                async def mock_get_user_async(*args, **kwargs):
                    raise Exception("User details error")
                mock_get_user.side_effect = mock_get_user_async
                
                # Test should propagate the exception
                with self.assertRaises(Exception):
                    run_async(self.oauth.handle_redirect(
                        code="test_code",
                        user_id="user123"
                    ))

    # Test for generating PKCE pair when code challenge is not provided (line 217)
    def test_generate_auth_url_with_pkce(self):
        """Test auth URL generation with PKCE code challenge generation"""
        # Don't provide CODE_CHALLENGE to trigger PKCE pair generation
        login_options = {
            "response_type": "code",
            "redirect_uri": "http://localhost/callback",
        }
        
        # Mock generate_pkce_pair to control return value
        with patch("kinde_sdk.auth.oauth.generate_pkce_pair") as mock_pkce:
            async def mock_pkce_async(*args, **kwargs):
                return {
                    "code_verifier": "test_verifier_generated",
                    "code_challenge": "test_challenge_generated"
                }
            mock_pkce.side_effect = mock_pkce_async
            
            auth_url_data = run_async(self.oauth.generate_auth_url(
                login_options=login_options
            ))
            
            # Verify PKCE pair was generated and used
            parsed_url = urlparse(auth_url_data["url"])
            query_params = parse_qs(parsed_url.query)
            
            self.assertEqual(query_params["code_challenge"][0], "test_challenge_generated")
            self.assertEqual(auth_url_data["code_verifier"], "test_verifier_generated")
            
            # Verify storage was updated with code_verifier
            self.oauth._session_manager.storage_manager.setItems.assert_any_call(
                "code_verifier", {"value": "test_verifier_generated"}
            )

    # Test logout with all options (line 314)
    def test_logout_with_all_options(self):
        """Test logout with all possible options"""
        logout_options = {
            "post_logout_redirect_uri": "http://localhost/logged-out",
            "state": "logout_state",
            "id_token_hint": "id_token_value"
        }
        
        logout_url = run_async(self.oauth.logout(user_id="user123", logout_options=logout_options))
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/logout")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/logged-out")
        self.assertEqual(query_params["state"][0], "logout_state")
        self.assertEqual(query_params["id_token_hint"][0], "id_token_value")
        
        # Verify logout was called
        self.oauth._session_manager.logout.assert_called_with("user123")

    # Test get_tokens with various edge cases (line 428-430, 446)
    def test_get_tokens_with_minimal_fields(self):
        """Test get_tokens with minimal token fields available"""
        # Set up token manager with minimal fields
        self.mock_token_manager.tokens = {
            "access_token": "test_access_token",
            # No refresh_token, id_token, or expires_at
        }
        
        # Get tokens
        tokens = self.oauth.get_tokens("user123")
        
        # Verify only access_token is returned
        self.assertEqual(tokens["access_token"], "test_access_token")
        self.assertNotIn("refresh_token", tokens)
        self.assertNotIn("id_token", tokens)
        self.assertNotIn("expires_at", tokens)
        self.assertNotIn("expires_in", tokens)

    def test_get_tokens_with_null_claims(self):
        """Test get_tokens when claims returns None"""
        # Make get_claims return None
        self.mock_token_manager.get_claims.return_value = None
        
        # Get tokens
        tokens = self.oauth.get_tokens("user123")
        
        # Verify claims is not added to tokens
        self.assertNotIn("claims", tokens)

    def test_handle_redirect_user_details_failure(self):
        """Test error handling when user details retrieval fails"""
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            mock_exchange.return_value = {"access_token": "test_token"}
            
            # Mock helper_get_user_details to raise exception
            with patch("kinde_sdk.auth.oauth.helper_get_user_details") as mock_get_user:
                mock_get_user.side_effect = Exception("User details error")
                
                with self.assertRaises(Exception):
                    run_async(self.oauth.handle_redirect(
                        code="test_code",
                        user_id="user123"
                    ))

    def test_generate_auth_url_with_pkce_generation(self):
        """Test PKCE code challenge generation when not provided"""
        with patch("kinde_sdk.auth.oauth.generate_pkce_pair") as mock_pkce:
            mock_pkce.return_value = {
                "code_verifier": "test_verifier",
                "code_challenge": "test_challenge"
            }
            
            auth_url_data = run_async(self.oauth.generate_auth_url())
            
            # Verify PKCE was generated and stored
            self.assertEqual(auth_url_data["code_challenge"], "test_challenge")
            self.assertEqual(auth_url_data["code_verifier"], "test_verifier")
            self.oauth._session_manager.storage_manager.setItems.assert_called_with(
                "code_verifier", {"value": "test_verifier"}
            )

    def test_register_sets_prompt_create(self):
        """Test register automatically sets prompt=create"""
        with patch.object(self.oauth, "generate_auth_url") as mock_gen:
            mock_gen.return_value = {"url": "test_url"}
            
            # Call register without prompt
            run_async(self.oauth.register())
            
            # Verify prompt was set to create
            args, kwargs = mock_gen.call_args
            self.assertEqual(
                kwargs["login_options"].get("prompt"),
                PromptTypes.CREATE.value
            )

    def test_exchange_code_with_client_secret(self):
        """Test code exchange includes client secret when available"""
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"access_token": "test"}
            
            run_async(self.oauth.exchange_code_for_tokens("test_code"))
            
            # Verify client_secret was included
            args, kwargs = mock_post.call_args
            self.assertEqual(kwargs["data"]["client_secret"], "test_client_secret")

    def test_auth_params_with_none_value(self):
        """Test auth params with None value handling."""
        login_options = {
            LoginOptions.AUTH_PARAMS: {
                "param_with_none": None,
                "param_with_value": "test_value"  
            }
        }
        
        auth_url_data = run_async(self.oauth.generate_auth_url(login_options=login_options))
        parsed_url = urlparse(auth_url_data["url"])
        query_params = parse_qs(parsed_url.query)
        
        # Verify param with value is included
        self.assertIn("param_with_value", query_params)
        # Verify param with None is excluded
        self.assertNotIn("param_with_none", query_params)

    def test_handle_redirect_with_try_catch(self):
        """Test handle_redirect with exception catching."""
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            async def mock_exchange_async(*args, **kwargs):
                return {"access_token": "test_token"}
            mock_exchange.side_effect = mock_exchange_async
            
            # Mock helper_get_user_details to raise exception
            with patch("kinde_sdk.auth.oauth.helper_get_user_details") as mock_get_user:
                async def mock_get_user_async(*args, **kwargs):
                    raise Exception("Test exception in user details")
                mock_get_user.side_effect = mock_get_user_async
                
                # Should raise the exception through (not catch it)
                with self.assertRaises(Exception):
                    run_async(self.oauth.handle_redirect(
                        code="test_code", 
                        user_id="user123"
                    ))

    def test_logout(self):
        """Test logout functionality."""
        # Setup
        user_id = "user123"
        self.oauth._session_manager.logout = MagicMock()
        
        # Execute
        result = self.oauth.logout(user_id)
        
        # Verify
        self.oauth._session_manager.logout.assert_called_with(user_id)

    def test_handle_redirect(self):
        """Test handle_redirect functionality."""
        # Setup
        code = "test_code"
        user_id = "test_user"
        state = "test_state"
        token_data = {"access_token": "test_token"}
        user_info = {"id": user_id, "email": "test@example.com"}
        
        # Mock the necessary methods
        self.oauth._session_manager.storage_manager.get = MagicMock(return_value={"value": state})
        self.oauth._session_manager.set_user_data = MagicMock()
        self.oauth._session_manager.get_token_manager = MagicMock(return_value=self.mock_token_manager)
        
        # Execute
        result = self.oauth.handle_redirect(code, user_id, state)
        
        # Verify
        self.oauth._session_manager.set_user_data.assert_called_with(user_id, user_info, token_data)

# Tests for lines 46-58 - Initialization with environment variables
class TestOAuthInitialization(unittest.TestCase):
    
    def test_init_with_env_variables(self):
        """Test initialization using environment variables"""
        # Save original environment
        original_env = {}
        for key in ['KINDE_CLIENT_ID', 'KINDE_CLIENT_SECRET', 'KINDE_REDIRECT_URI', 'KINDE_HOST', 'KINDE_AUDIENCE']:
            original_env[key] = os.environ.get(key)
        
        try:
            # Set environment variables
            os.environ['KINDE_CLIENT_ID'] = 'env_client_id'
            os.environ['KINDE_CLIENT_SECRET'] = 'env_client_secret'
            os.environ['KINDE_REDIRECT_URI'] = 'http://localhost/env-callback'
            os.environ['KINDE_HOST'] = 'https://env-example.com'
            os.environ['KINDE_AUDIENCE'] = 'env_audience'
            
            # Create OAuth instance without explicit parameters
            oauth = OAuth(framework="flask")
            
            # Verify environment variables were used
            self.assertEqual(oauth.client_id, 'env_client_id')
            self.assertEqual(oauth.client_secret, 'env_client_secret')
            self.assertEqual(oauth.redirect_uri, 'http://localhost/env-callback')
            self.assertEqual(oauth.host, 'https://env-example.com')
            self.assertEqual(oauth.audience, 'env_audience')
            
            # Verify URLs were set correctly
            self.assertEqual(oauth.auth_url, 'https://env-example.com/oauth2/auth')
            self.assertEqual(oauth.token_url, 'https://env-example.com/oauth2/token')
            self.assertEqual(oauth.logout_url, 'https://env-example.com/logout')
            self.assertEqual(oauth.userinfo_url, 'https://env-example.com/oauth2/userinfo')
            
        finally:
            # Restore original environment
            for key, value in original_env.items():
                if value is None:
                    if key in os.environ:
                        del os.environ[key]
                else:
                    os.environ[key] = value

# Tests to catch missing lines in get_tokens for lines 456-462, 478-497, 515, 523, 528, 551-553
class TestOAuthTokensEdgeCases(unittest.TestCase):
    
    def setUp(self):
        """Set up for each test"""
        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback",
            framework="flask"
        )
        
        # Mock session manager
        self.oauth._session_manager = MagicMock()
        self.mock_token_manager = MagicMock()
        self.oauth._session_manager.get_token_manager = MagicMock(return_value=self.mock_token_manager)
        
        # Mock logger
        self.oauth.logger = MagicMock()
    
    def test_get_tokens_without_expires_at(self):
        """Test get_tokens without expires_at in tokens"""
        # Set up tokens without expires_at
        self.mock_token_manager.tokens = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token"
            # No expires_at
        }
        self.mock_token_manager.get_access_token = MagicMock(return_value="test_access_token")
        self.mock_token_manager.get_claims = MagicMock(return_value={"sub": "user123"})
        
        # Get tokens
        tokens = self.oauth.get_tokens("user123")
        
        # Verify no expires_at or expires_in in result
        self.assertNotIn("expires_at", tokens)
        self.assertNotIn("expires_in", tokens)
    
    def test_get_tokens_with_exception(self):
        """Test get_tokens with an exception during processing"""
        # Make get_access_token raise an exception to test the except branch
        self.mock_token_manager.get_access_token = MagicMock(side_effect=Exception("Test exception"))
        
        # Test should raise ValueError
        with self.assertRaises(ValueError):
            self.oauth.get_tokens("user123")
        
        # Verify error was logged
        self.oauth.logger.error.assert_called_once()

    def test_get_tokens_with_expired_token(self):
        """Test get_tokens with expired token"""
        # Set up tokens with an access_token first
        self.mock_token_manager.tokens = {
            "access_token": "test_access_token",  
            "expires_at": time.time() - 3600
        }
        self.mock_token_manager.get_access_token = MagicMock(return_value="test_access_token")  
        
        tokens = self.oauth.get_tokens("user123")
        
        # Verify expires_in is 0
        self.assertEqual(tokens["expires_in"], 0)

    def test_get_tokens_with_empty_claims(self):
        """Test get_tokens with empty claims"""
        # You need to set up tokens with an access_token before setting claims
        self.mock_token_manager.tokens = {
            "access_token": "test_access_token"  
        }
        self.mock_token_manager.get_access_token = MagicMock(return_value="test_access_token")  
        self.mock_token_manager.get_claims.return_value = {}
        
        tokens = self.oauth.get_tokens("user123")
        
        # Verify claims not included when empty
        self.assertNotIn("claims", tokens)

    def test_get_tokens_with_empty_token_dict(self):
        """Test get_tokens with empty tokens dictionary."""
        self.mock_token_manager.tokens = {}
        
        with self.assertRaises(ValueError) as context:
            self.oauth.get_tokens("user123")
        
        self.assertIn("No access token available", str(context.exception))

    def test_get_tokens_with_refresh_token_edge_case(self):
        """Test get_tokens with refresh token edge case."""
        # Test with refresh_token as None
        self.mock_token_manager.tokens = {
            "access_token": "test_access_token",
            "refresh_token": None
        }
        self.mock_token_manager.get_access_token.return_value = "test_access_token"
        
        tokens = self.oauth.get_tokens("user123")
        
        # refresh_token should not be included since it's None
        self.assertNotIn("refresh_token", tokens)

# Tests for exchange_code_for_tokens (line 253-267, 284, 287, 293-297)
class TestOAuthCodeExchange(unittest.TestCase):
    
    def setUp(self):
        """Set up for each test"""
        self.oauth = OAuth(
            client_id="test_client_id",
            redirect_uri="http://localhost/callback",
            framework="flask"
            # No client_secret
        )
        self.oauth.token_url = "https://example.com/oauth2/token"
    
    def test_exchange_code_without_client_secret(self):
        """Test exchange_code_for_tokens without client_secret"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test_access_token"}
        
        # Patch requests.post
        with patch("requests.post", return_value=mock_response) as mock_post:
            result = run_async(self.oauth.exchange_code_for_tokens(
                code="test_code",
                code_verifier="test_verifier"
            ))
            
            # Verify post data doesn't include client_secret
            args, kwargs = mock_post.call_args
            self.assertEqual(args[0], self.oauth.token_url)
            self.assertEqual(kwargs["data"]["code"], "test_code")
            self.assertEqual(kwargs["data"]["code_verifier"], "test_verifier")
            self.assertNotIn("client_secret", kwargs["data"])
            
            # Verify result
            self.assertEqual(result["access_token"], "test_access_token")

# Additional tests for even more coverage
class TestForIncreasedCoverage(unittest.TestCase):
    def setUp(self):
        """Set up for each test"""
        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback",
            framework="flask",
            host="https://example.com"
        )
        self.oauth._session_manager = MagicMock()
        self.oauth.logger = MagicMock()
        
        # Add mock_token_manager setup
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
        self.oauth._session_manager.get_token_manager = MagicMock(return_value=self.mock_token_manager)

    def test_handle_redirect_with_state_cleanup(self):
        """Test handle_redirect with state cleanup"""
        # Mock token manager
        mock_token_manager = MagicMock()
        mock_token_manager.get_access_token.return_value = "test_access_token"
        self.oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        # Mock storage manager with properly structured state
        mock_storage = MagicMock()
        # Make get("state") return a mock with a proper get("value") method
        state_mock = MagicMock()
        state_mock.get.return_value = "test_state"  # Return matching state
        mock_storage.get.return_value = state_mock
        
        self.oauth._session_manager.storage_manager = mock_storage
        
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            async def mock_exchange_async(*args, **kwargs):
                return {"access_token": "test_token"}
            mock_exchange.side_effect = mock_exchange_async
            
            with patch("kinde_sdk.auth.oauth.helper_get_user_details") as mock_get_user:
                async def mock_get_user_async(*args, **kwargs):
                    return {"sub": "user123", "name": "Test User"}
                mock_get_user.side_effect = mock_get_user_async
                
                # Call with state parameter to test state cleanup
                result = run_async(self.oauth.handle_redirect(
                    code="test_code",
                    user_id="user123",
                    state="test_state"
                ))
                
                # Verify state and nonce were deleted
                mock_storage.delete.assert_any_call("state")
                mock_storage.delete.assert_any_call("nonce")
                
                # Verify result
                self.assertEqual(result["user"]["name"], "Test User")
    
    # Test for lines 253-267, 284, 287 (Register with login options)
    def test_register_with_login_options(self):
        """Test register method with login options"""
        login_options = {
            LoginOptions.REDIRECT_URI: "http://localhost/custom-register-callback",
            LoginOptions.SCOPE: "openid profile",
            # Do not specify prompt - should be set to 'create' by default for register
        }
        
        # Use patch to not actually call generate_auth_url
        with patch.object(self.oauth, "generate_auth_url") as mock_gen_url:
            mock_gen_url.return_value = {"url": "https://example.com/register"}
            
            register_url = run_async(self.oauth.register(login_options))
            
            # Verify generate_auth_url was called with correct parameters
            args, kwargs = mock_gen_url.call_args
            self.assertEqual(kwargs["route_type"], IssuerRouteTypes.REGISTER)
            self.assertEqual(kwargs["login_options"], login_options)
            self.assertEqual(kwargs["login_options"].get("prompt"), PromptTypes.CREATE.value)
    
    # Test for lines 293-297 (Logout with id_token_hint from token manager)
    def test_logout_with_id_token_from_manager(self):
        """Test logout with id_token from token manager"""
        # Mock token manager to return id_token
        mock_token_manager = MagicMock()
        mock_token_manager.get_id_token.return_value = "test_id_token"
        self.oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        # Call logout without specifying id_token_hint
        logout_url = run_async(self.oauth.logout(user_id="user123"))
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        # Verify id_token_hint was included from token manager
        self.assertEqual(query_params["id_token_hint"][0], "test_id_token")
    

    def test_get_tokens_with_empty_claims(self):
        """Test get_tokens with empty claims dictionary"""
        # Mock token manager
        mock_token_manager = MagicMock()
        mock_token_manager.tokens = {
            "access_token": "test_access_token",
            "expires_at": time.time() + 3600
        }
        mock_token_manager.get_access_token.return_value = "test_access_token"
        mock_token_manager.get_claims.return_value = {}  # Empty claims
        
        self.oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        # Get tokens
        tokens = self.oauth.get_tokens("user123")
        
        # In the OAuth implementation, empty claims dictionaries aren't added
        # so we should verify claims key is not present
        self.assertNotIn("claims", tokens)
    
    # Test for lines 495, 515 (State parameter in logout)
    def test_logout_with_state(self):
        """Test logout with state parameter"""
        logout_options = {
            "state": "test_logout_state"
        }
        
        logout_url = run_async(self.oauth.logout(logout_options=logout_options))
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(query_params["state"][0], "test_logout_state")
    
    # Test for line 487 (Logout without redirect URI)
    def test_logout_without_redirect_uri(self):
        """Test logout without redirect URI"""
        # Create OAuth with no redirect_uri
        oauth = OAuth(client_id="test_client_id", framework="flask")
        oauth._session_manager = MagicMock()
        oauth.redirect_uri = None
        
        logout_url = run_async(oauth.logout())
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        # Verify redirect_uri is not in the URL
        self.assertNotIn("redirect_uri", query_params)
    
    # Test for line 57-58 (Config file handling)
    def test_init_with_custom_storage_config(self):
        """Test initialization with custom storage configuration"""
        with patch("kinde_sdk.auth.oauth.StorageManager") as mock_storage_manager:
            mock_storage = MagicMock()
            mock_storage_manager.return_value = mock_storage
            
            # Create OAuth with storage_config
            oauth = OAuth(
                client_id="test_client_id",
                storage_config={"type": "redis", "host": "localhost", "port": 6379}
            )
            
            # Verify storage was initialized with config
            mock_storage.initialize.assert_called_once_with(
                {"type": "redis", "host": "localhost", "port": 6379}
            )

        # Test for lines 46-58 (Config initialization)
    def test_init_with_config_file(self):
        """Test initialization with a config file"""
        with patch("kinde_sdk.auth.oauth.load_config") as mock_load_config:
            mock_load_config.return_value = {
                "storage": {
                    "type": "memory"
                }
            }
            
            with patch("kinde_sdk.auth.oauth.StorageManager") as mock_storage_manager:
                oauth = OAuth(
                    client_id="test_client_id",
                    config_file="test_config.json"
                )
                
                # Verify config was loaded
                mock_load_config.assert_called_once_with("test_config.json")
                self.assertEqual(oauth.client_id, "test_client_id")

    # Test for line 177 (User details error handling)
    def test_handle_redirect_full_cycle(self):
        """Test complete handle_redirect cycle with cleanup"""
        # Setup token manager
        mock_token_manager = MagicMock()
        mock_token_manager.get_access_token.return_value = "test_access_token"
        
        # Setup session manager
        self.oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        # Setup storage with proper state
        mock_state = MagicMock()
        mock_state.get.return_value = "test_state"
        
        mock_verifier = MagicMock()
        mock_verifier.get.return_value = "test_verifier"
        
        mock_storage = MagicMock()
        def mock_get(key):
            if key == "state":
                return mock_state
            elif key == "code_verifier":
                return mock_verifier
            return None
        
        mock_storage.get.side_effect = mock_get
        self.oauth._session_manager.storage_manager = mock_storage
        
        # Setup mocks for methods
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            async def mock_exchange_impl(*args, **kwargs):
                return {
                    "access_token": "test_token",
                    "refresh_token": "test_refresh",
                    "id_token": "test",
                    "access_token": "test_token",
                    "refresh_token": "test_refresh",
                    "id_token": "test_id_token" 
                }
            mock_exchange.side_effect = mock_exchange_impl
            
            with patch("kinde_sdk.auth.oauth.helper_get_user_details") as mock_get_user:
                async def mock_get_user_impl(*args, **kwargs):
                    return {"sub": "test_user", "email": "test@example.com"}
                mock_get_user.side_effect = mock_get_user_impl
                
                # Call handle_redirect
                result = run_async(self.oauth.handle_redirect(
                    code="test_code",
                    user_id="user123",
                    state="test_state"
                ))
                
                # Verify everything worked and proper cleanup
                mock_storage.delete.assert_any_call("code_verifier")
                mock_storage.delete.assert_any_call("state")
                mock_storage.delete.assert_any_call("nonce")
                
                self.assertEqual(result["user"]["sub"], "test_user")
                self.assertEqual(result["tokens"]["access_token"], "test_token")

    # Test for line 254, 257, 284 (Register method)
    def test_register_without_prompt(self):
        """Test register method adds prompt=create if not specified"""
        with patch.object(self.oauth, "generate_auth_url") as mock_gen:
            mock_gen.return_value = {"url": "https://test-register-url"}
            
            run_async(self.oauth.register())
            
            args, kwargs = mock_gen.call_args
            # Check prompt is set to create
            self.assertEqual(kwargs["login_options"].get("prompt"), PromptTypes.CREATE.value)

    # Test for line 487, 495 (Logout without redirect URI)
    def test_logout_without_redirect(self):
        """Test logout URL generation without redirect URI"""
        # Create instance without redirect_uri
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            framework="flask"
            # No redirect_uri
        )
        oauth._session_manager = MagicMock()
        
        logout_url = run_async(oauth.logout())
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        # Verify redirect_uri is not in URL
        self.assertNotIn("redirect_uri", query_params)

    def test_init_without_client_id(self):
        """Test initialization without client ID raises exception."""
        with self.assertRaises(KindeConfigurationException):
            OAuth(client_secret="test_secret", redirect_uri="http://localhost/callback")

    def test_generate_auth_url_with_audience_option(self):
        """Test auth URL generation with audience from options."""
        # Create instance without audience
        oauth = OAuth(
            client_id="test_client_id",
            redirect_uri="http://localhost/callback",
            framework="flask"
            # No audience
        )
        
        # Provide audience in options
        login_options = {
            LoginOptions.AUDIENCE: "option_audience"
        }
        
        auth_url_data = run_async(oauth.generate_auth_url(login_options=login_options))
        
        # Parse URL to check parameters
        parsed_url = urlparse(auth_url_data["url"])
        query_params = parse_qs(parsed_url.query)
        
        # Verify audience from options was used
        self.assertIn("audience", query_params)
        self.assertEqual(query_params["audience"][0], "option_audience")

    def test_generate_auth_url_with_pkce_generation(self):
        """Test auth URL generation with PKCE code challenge generation."""
        with patch("kinde_sdk.auth.oauth.generate_pkce_pair") as mock_pkce:
            # Setup mock to return specific PKCE values
            async def mock_pkce_async(*args, **kwargs):
                return {
                    "code_verifier": "test_verifier_123",
                    "code_challenge": "test_challenge_456"
                }
            mock_pkce.side_effect = mock_pkce_async
            
            # Generate auth URL without providing code challenge
            auth_url_data = run_async(self.oauth.generate_auth_url())
            
            # Parse URL to check parameters
            parsed_url = urlparse(auth_url_data["url"])
            query_params = parse_qs(parsed_url.query)
            
            # Verify PKCE was generated and added to URL
            self.assertIn("code_challenge", query_params)
            self.assertEqual(query_params["code_challenge"][0], "test_challenge_456")
            self.assertEqual(auth_url_data["code_verifier"], "test_verifier_123")
            
            # Verify storage was updated
            self.oauth._session_manager.storage_manager.setItems.assert_any_call(
                "code_verifier", {"value": "test_verifier_123"}
            )

    def test_handle_redirect_user_details_error(self):
        """Test handling redirect when user details retrieval fails."""
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            async def mock_exchange_async(*args, **kwargs):
                return {"access_token": "test_token"}
            mock_exchange.side_effect = mock_exchange_async
            
            # Make helper_get_user_details raise an exception
            with patch("kinde_sdk.auth.oauth.helper_get_user_details") as mock_user_details:
                async def mock_details_async(*args, **kwargs):
                    raise Exception("User details error")
                mock_user_details.side_effect = mock_details_async
                
                # Should propagate the exception
                with self.assertRaises(Exception):
                    run_async(self.oauth.handle_redirect(
                        code="test_code",
                        user_id="user123",
                        state="test_state"
                    ))

    def test_register_with_options(self):
        """Test register method with custom options."""
        login_options = {
            LoginOptions.REDIRECT_URI: "http://localhost/register-callback",
            LoginOptions.SCOPE: "openid profile email",
            LoginOptions.LANG: "en",
            # No prompt, should be added automatically
        }
        
        with patch.object(self.oauth, "generate_auth_url") as mock_gen_url:
            async def mock_gen_url_async(*args, **kwargs):
                return {"url": "https://example.com/register"}
            mock_gen_url.side_effect = mock_gen_url_async
            
            # Call register
            result = run_async(self.oauth.register(login_options))
            
            # Verify generate_auth_url was called with correct parameters
            call_args = mock_gen_url.call_args[1]
            self.assertEqual(call_args["route_type"], IssuerRouteTypes.REGISTER)
            
            # Verify prompt was added
            passed_options = call_args["login_options"]
            self.assertEqual(passed_options.get("prompt"), PromptTypes.CREATE.value)
            self.assertEqual(passed_options.get(LoginOptions.REDIRECT_URI), "http://localhost/register-callback")

    def test_get_tokens_no_token_manager(self):
        """Test get_tokens when no token manager is available."""
        # Make get_token_manager return None
        self.oauth._session_manager.get_token_manager.return_value = None
        
        # Should raise ValueError
        with self.assertRaises(ValueError):
            self.oauth.get_tokens("user123")
    
    def test_get_tokens_empty_tokens(self):
        """Test get_tokens with empty tokens dictionary."""
        # Set empty tokens
        self.mock_token_manager.tokens = {}
        
        # Should raise ValueError
        with self.assertRaises(ValueError):
            self.oauth.get_tokens("user123")

    def test_logout_url_options(self):
        """Test logout URL generation with various options."""
        # Test without post_logout_redirect_uri
        oauth = OAuth(
            client_id="test_client_id",
            framework="flask"
            # No redirect_uri
        )
        oauth._session_manager = MagicMock()
        
        # Generate logout URL with state but no redirect
        logout_options = {
            "state": "logout_state"
        }
        
        logout_url = run_async(oauth.logout(logout_options=logout_options))
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        # Verify URL parameters
        self.assertIn("client_id", query_params)
        self.assertIn("state", query_params)
        self.assertEqual(query_params["state"][0], "logout_state")
        self.assertNotIn("redirect_uri", query_params)

    def test_get_tokens_exception(self):
        """Test exception handling in get_tokens."""
        # Make get_access_token raise an exception
        self.mock_token_manager.get_access_token.side_effect = Exception("Token error")
        
        # Should raise ValueError with error message
        with self.assertRaises(ValueError) as cm:
            self.oauth.get_tokens("user123")
        
        # Verify error was logged
        self.oauth.logger.error.assert_called_once()
        
        # Verify error message
        self.assertIn("Failed to retrieve tokens", str(cm.exception))

    def test_register_with_existing_prompt(self):
        """Test register method with an already set prompt."""
        login_options = {
            "prompt": "login"  # Different from create
        }
        
        with patch.object(self.oauth, "generate_auth_url") as mock_gen_auth:
            mock_gen_auth.return_value = {"url": "https://example.com/register"}
            
            url = run_async(self.oauth.register(login_options))
            
            # Verify generate_auth_url was called with login_options
            mock_gen_auth.assert_called_once()
            args, kwargs = mock_gen_auth.call_args
            
            # Prompt should not be overridden
            self.assertEqual(kwargs["login_options"]["prompt"], "login")

if __name__ == "__main__":
    unittest.main()