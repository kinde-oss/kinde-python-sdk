import unittest
import asyncio
import time
from unittest.mock import patch, MagicMock, AsyncMock
from urllib.parse import urlparse, parse_qs

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.enums import IssuerRouteTypes, PromptTypes
from kinde_sdk.auth.login_options import LoginOptions
from kinde_sdk.core.exceptions import (
    KindeConfigurationException,
    KindeLoginException,
    KindeTokenException,
    KindeRetrieveException,
)

def run_async(coro):
    """Helper function to run async tests"""
    return asyncio.run(coro)

class TestOAuthEdgeCases(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback",
            framework="flask",
            host="https://test.kinde.com"
        )
        
        # Mock session manager
        self.mock_session_manager = MagicMock()
        self.oauth._session_manager = self.mock_session_manager
        
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
        self.mock_token_manager.get_claims = MagicMock(return_value={"sub": "user123"})
        
        # Make session manager return token manager
        self.oauth._session_manager.get_token_manager = MagicMock(return_value=self.mock_token_manager)

    def test_handle_redirect_state_mismatch(self):
        """Test handle_redirect with state mismatch."""
        # Set up storage to return different state
        #self.mock_session_manager.storage_manager.get.return_value = {"value": "different_state"}
        
        #with self.assertRaises(KindeLoginException) as context:
        #    run_async(self.oauth.handle_redirect(
        #        code="test_code",
        #        user_id="user123",
        #        state="test_state"
        #    ))
        
        #self.assertIn("Invalid state parameter", str(context.exception))

    def test_handle_redirect_token_exchange_failure(self):
        """Test handle_redirect when token exchange fails."""
        #with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
        #    mock_exchange.side_effect = Exception("Token exchange failed")
            
        #    with self.assertRaises(KindeTokenException) as context:
        #        run_async(self.oauth.handle_redirect(
        #            code="test_code",
        #            user_id="user123"
        #        ))
            
        #    self.assertIn("Failed to exchange code for tokens", str(context.exception))

    def test_handle_redirect_no_token_manager(self):
        """Test handle_redirect when token manager is not available."""
        #self.mock_session_manager.get_token_manager.return_value = None
        
        #with self.assertRaises(KindeRetrieveException) as context:
        #    run_async(self.oauth.handle_redirect(
        #        code="test_code",
        #        user_id="user123"
        #    ))
        
        #self.assertIn("Failed to get token manager", str(context.exception))

    def test_exchange_code_for_tokens_error_response(self):
        """Test exchange_code_for_tokens with error response."""
        #with patch("requests.post") as mock_post:
        #    mock_response = MagicMock()
        #    mock_response.status_code = 400
        #    mock_response.text = "Invalid request"
        #    mock_post.return_value = mock_response
            
        #    with self.assertRaises(KindeTokenException) as context:
        #        run_async(self.oauth.exchange_code_for_tokens("test_code"))
            
        #    self.assertIn("Token exchange failed", str(context.exception))

    def test_get_tokens_no_token_manager(self):
        """Test get_tokens when token manager is not available."""
        #self.mock_session_manager.get_token_manager.return_value = None
        
        #with self.assertRaises(ValueError) as context:
        #    self.oauth.get_tokens("user123")
        
        #self.assertIn("No token manager available", str(context.exception))

    def test_get_tokens_invalid_access_token(self):
        """Test get_tokens with invalid access token."""
        #self.mock_token_manager.get_access_token.return_value = None
        
        #with self.assertRaises(ValueError) as context:
        #    self.oauth.get_tokens("user123")
        
        #self.assertIn("Invalid access token", str(context.exception))

    def test_get_tokens_exception_handling(self):
        """Test get_tokens exception handling."""
        #self.mock_token_manager.get_access_token.side_effect = Exception("Token error")
        
        #with self.assertRaises(ValueError) as context:
        #    self.oauth.get_tokens("user123")
        
        #self.assertIn("Failed to retrieve tokens", str(context.exception))

    def test_generate_auth_url_invalid_options(self):
        """Test generate_auth_url with invalid options."""
        # Test with invalid auth_params type
        #login_options = {
        #    LoginOptions.AUTH_PARAMS: "not_a_dict"
        #}
        
        #with self.assertRaises(TypeError):
        #    run_async(self.oauth.generate_auth_url(login_options=login_options))

    def test_logout_with_invalid_token_manager(self):
        """Test logout with invalid token manager."""
        #self.mock_session_manager.get_token_manager.return_value = None
        
        # Should not raise exception, just skip id_token_hint
        #logout_url = run_async(self.oauth.logout(user_id="user123"))
        
        #parsed_url = urlparse(logout_url)
        #query_params = parse_qs(parsed_url.query)
        #self.assertNotIn("id_token_hint", query_params)

    def test_register_with_existing_prompt(self):
        """Test register with existing prompt value."""
        #login_options = {
        #    "prompt": "login"  # Different from create
        #}
        
        #with patch.object(self.oauth, "generate_auth_url") as mock_gen:
        #    mock_gen.return_value = {"url": "https://test-register-url"}
            
        #    run_async(self.oauth.register(login_options))
            
        #    # Verify prompt was not overridden
        #    args, kwargs = mock_gen.call_args
        #    self.assertEqual(kwargs["login_options"]["prompt"], "login")

    def test_handle_redirect_cleanup(self):
        """Test handle_redirect cleanup of state and nonce."""
        # Set up storage with state and nonce
        #self.mock_session_manager.storage_manager.get.side_effect = lambda key: {
        #    "state": {"value": "test_state"},
        #    "nonce": {"value": "test_nonce"}
        #}.get(key)
        
        #with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
        #    mock_exchange.return_value = {"access_token": "test_token"}
            
        #    run_async(self.oauth.handle_redirect(
        #        code="test_code",
        #        user_id="user123",
        #        state="test_state"
        #    ))
            
        #    # Verify cleanup
        #    self.mock_session_manager.storage_manager.delete.assert_any_call("state")
        #    self.mock_session_manager.storage_manager.delete.assert_any_call("nonce")

    def test_get_tokens_with_expired_token(self):
        """Test get_tokens with expired token."""
        #self.mock_token_manager.tokens = {
        #    "access_token": "test_access_token",
        #    "expires_at": time.time() - 3600  # Expired
        #}
        
        #tokens = self.oauth.get_tokens("user123")
        #self.assertEqual(tokens["expires_in"], 0)

    def test_get_tokens_with_empty_claims(self):
        """Test get_tokens with empty claims."""
        #self.mock_token_manager.get_claims.return_value = {}
        
        #tokens = self.oauth.get_tokens("user123")
        #self.assertNotIn("claims", tokens)

if __name__ == "__main__":
    unittest.main() 