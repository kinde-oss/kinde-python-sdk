import unittest
import pytest
from unittest.mock import patch, MagicMock
import time
import threading
import jwt

from kinde_sdk.auth.token_manager import TokenManager


class TestTokenManagerExtended(unittest.TestCase):
    def setUp(self):
        # Clear the singleton instances before each test
        TokenManager.reset_instances()
        
        # Set up a token manager for testing
        self.token_manager = TokenManager(
            "test_user_id",
            "test_client_id",
            "test_client_secret",
            "https://example.com/oauth2/token"
        )

    def test_reset_instances(self):
        """Test the reset_instances class method"""
        # Create a token manager instance
        manager1 = TokenManager(
            "user1",
            "client_id",
            "client_secret",
            "token_url"
        )
        
        # Create another token manager instance with different user_id
        manager2 = TokenManager(
            "user2",
            "client_id",
            "client_secret",
            "token_url"
        )
        
        # Verify we have multiple instances
        self.assertEqual(len(TokenManager._instances), 3)  # includes test_user_id from setUp
        
        # Reset instances
        TokenManager.reset_instances()
        
        # Verify instances were cleared
        self.assertEqual(len(TokenManager._instances), 0)
        
        # Creating a new instance should create a fresh one
        manager3 = TokenManager(
            "user1",
            "new_client_id",
            "new_secret",
            "new_url"
        )
        
        # Should have different properties than the original
        self.assertEqual(manager3.client_id, "new_client_id")
        self.assertNotEqual(manager3.client_id, manager1.client_id)

    def test_thread_safety(self):
        """Test thread safety of singleton pattern"""
        # This test creates multiple threads that try to create TokenManager instances
        # simultaneously, then verifies that we still get proper singleton behavior
        
        # List to store created managers
        managers = []
        
        # Function for thread to create a TokenManager
        def create_manager():
            manager = TokenManager(
                "shared_user_id",
                "client_id",
                "secret",
                "url"
            )
            managers.append(manager)
        
        # Create and start multiple threads
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=create_manager)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all managers are the same instance
        for i in range(1, len(managers)):
            self.assertIs(managers[0], managers[i])

    def test_set_redirect_uri(self):
        """Test setting redirect URI"""
        redirect_uri = "https://example.com/callback"
        
        # Set redirect URI
        self.token_manager.set_redirect_uri(redirect_uri)
        
        # Verify it was set correctly
        self.assertEqual(self.token_manager.redirect_uri, redirect_uri)

    def test_get_id_token(self):
        """Test get_id_token method"""
        # Initially should be None
        self.assertIsNone(self.token_manager.get_id_token())
        
        # Set a token
        self.token_manager.tokens = {"id_token": "test_id_token"}
        
        # Now should return the token
        self.assertEqual(self.token_manager.get_id_token(), "test_id_token")

    def test_set_tokens_with_invalid_id_token(self):
        """Test set_tokens with an ID token that can't be decoded"""
        # Token data with ID token
        token_data = {
            "access_token": "test_access_token",
            "id_token": "invalid_id_token",
            "expires_in": 3600
        }
        
        # Mock jwt.decode to raise an exception
        with patch('jwt.decode') as mock_decode:
            mock_decode.side_effect = Exception("Invalid token")
            
            # Should handle the exception and set empty claims
            self.token_manager.set_tokens(token_data)
            
            # Verify claims is empty
            self.assertEqual(self.token_manager.tokens.get("claims", None), {})

    def test_exchange_code_missing_redirect_uri(self):
        """Test exchange_code_for_token without setting redirect URI"""
        # Don't set redirect_uri
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            asyncio_test(self.token_manager.exchange_code_for_token("code"))
        
        self.assertIn("Redirect URI is not set", str(context.exception))

    def test_exchange_code_no_client_secret(self):
        """Test exchange_code_for_token without client_secret"""
        # Create manager with no client_secret
        manager = TokenManager(
            "user_without_secret",
            "client_id",
            None,  # No client_secret
            "https://example.com/token"
        )
        
        # Set redirect URI
        manager.set_redirect_uri("http://localhost/callback")
        
        # Mock requests.post
        with patch('requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {
                "access_token": "new_token",
                "expires_in": 3600
            }
            mock_post.return_value = mock_response
            
            # Call the exchange method
            token = asyncio_test(manager.exchange_code_for_token("auth_code"))
            
            # Verify the request was made without client_secret
            args, kwargs = mock_post.call_args
            self.assertEqual(args[0], "https://example.com/token")
            self.assertNotIn("client_secret", kwargs["data"])
            self.assertEqual(token, "new_token")

    def test_get_access_token_no_token(self):
        """Test get_access_token when no token is available"""
        # Empty tokens dictionary
        self.token_manager.tokens = {}
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.token_manager.get_access_token()
        
        self.assertIn("No access token available", str(context.exception))

    def test_refresh_access_token_no_refresh_token(self):
        """Test refresh_access_token when no refresh token is available"""
        # Set tokens without refresh token
        self.token_manager.tokens = {
            "access_token": "test_access_token"
        }
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.token_manager.refresh_access_token()
        
        self.assertIn("No refresh token available", str(context.exception))

    def test_revoke_token_no_token(self):
        """Test revoke_token when no token is available"""
        # Empty tokens dictionary
        self.token_manager.tokens = {}
        
        # Should not raise exception, just return
        self.token_manager.revoke_token()  # This should not raise

    def test_refresh_token_without_client_secret(self):
        """Test refreshing token without client secret"""
        # Create manager with no client_secret
        manager = TokenManager(
            "refresh_without_secret",
            "client_id",
            None,  # No client_secret
            "https://example.com/token"
        )
        
        # Set tokens
        manager.tokens = {
            "access_token": "old_token",
            "refresh_token": "refresh_token"
        }
        
        # Mock requests.post
        with patch('requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {
                "access_token": "new_token",
                "refresh_token": "new_refresh",
                "expires_in": 3600
            }
            mock_post.return_value = mock_response
            
            # Refresh token
            token = manager.refresh_access_token()
            
            # Verify request was made without client_secret
            args, kwargs = mock_post.call_args
            self.assertEqual(args[0], "https://example.com/token")
            self.assertNotIn("client_secret", kwargs["data"])
            self.assertEqual(token, "new_token")

    def test_revoke_token_with_error(self):
        """Test revoking token when the request fails"""
        # Set token
        self.token_manager.tokens = {
            "access_token": "token_to_revoke"
        }
        
        # Mock requests.post to raise an exception
        with patch('requests.post') as mock_post:
            mock_post.side_effect = Exception("Network error")
            
            # Should not raise exception
            self.token_manager.revoke_token()  # This should not raise
            
            # Tokens should be cleared
            self.assertEqual(self.token_manager.tokens, {})

    def test_revoke_token_without_client_secret(self):
        """Test revoking token without client secret"""
        # Create manager with no client_secret
        manager = TokenManager(
            "revoke_without_secret",
            "client_id",
            None,  # No client_secret
            "https://example.com/token"
        )
        
        # Set token
        manager.tokens = {
            "access_token": "token_to_revoke"
        }
        
        # Mock requests.post
        with patch('requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response
            
            # Revoke token
            manager.revoke_token()
            
            # Verify request was made without client_secret
            args, kwargs = mock_post.call_args
            self.assertEqual(args[0], "https://example.com/revoke")
            self.assertNotIn("client_secret", kwargs["data"])


# Helper function to run async tests
def asyncio_test(coro):
    """Run a coroutine in the event loop and return its result."""
    import asyncio
    return asyncio.run(coro)


if __name__ == "__main__":
    unittest.main()