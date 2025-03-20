import unittest
import pytest
from unittest.mock import patch, MagicMock
import time
import threading

from kinde_sdk.auth.token_manager import TokenManager


class TestTokenManager(unittest.TestCase):
    def setUp(self):
        # Clear the singleton instances before each test
        TokenManager._instances = {}
        
        # Set up a token manager for testing
        self.token_manager = TokenManager(
            "test_user_id",
            "test_client_id",
            "test_client_secret",
            "https://example.com/oauth2/token"
        )
        
        # Verify it's initialized correctly
        self.assertEqual(self.token_manager.user_id, "test_user_id")
        self.assertEqual(self.token_manager.client_id, "test_client_id")
        self.assertEqual(self.token_manager.client_secret, "test_client_secret")
        self.assertEqual(self.token_manager.token_url, "https://example.com/oauth2/token")
        self.assertEqual(self.token_manager.tokens, {})

    def test_singleton_pattern(self):
        """Test the singleton pattern is working correctly"""
        # Create another instance with the same user_id
        another_manager = TokenManager(
            "test_user_id",
            "different_client_id",
            "different_secret",
            "different_url"
        )
        
        # Should be the same instance
        self.assertIs(self.token_manager, another_manager)
        
        # Properties should not have been reinitialized
        self.assertEqual(another_manager.client_id, "test_client_id")
        self.assertEqual(another_manager.client_secret, "test_client_secret")
        self.assertEqual(another_manager.token_url, "https://example.com/oauth2/token")
        
        # Create an instance with a different user_id
        different_user_manager = TokenManager(
            "different_user_id",
            "client_id",
            "secret",
            "url"
        )
        
        # Should be a different instance
        self.assertIsNot(self.token_manager, different_user_manager)

    def test_set_tokens(self):
        """Test setting tokens"""
        # Test with minimal token data
        token_data = {
            "access_token": "test_access_token",
            "expires_in": 3600
        }
        
        self.token_manager.set_tokens(token_data)
        
        self.assertEqual(self.token_manager.tokens["access_token"], "test_access_token")
        self.assertTrue("expires_at" in self.token_manager.tokens)
        self.assertTrue(self.token_manager.tokens["expires_at"] > time.time())
        self.assertTrue(self.token_manager.tokens["expires_at"] <= time.time() + 3600 + 1)  # Allow 1s buffer
        
        # Test with refresh token
        token_data = {
            "access_token": "new_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 7200
        }
        
        self.token_manager.set_tokens(token_data)
        
        self.assertEqual(self.token_manager.tokens["access_token"], "new_access_token")
        self.assertEqual(self.token_manager.tokens["refresh_token"], "test_refresh_token")
        
        # Test with ID token
        token_data = {
            "access_token": "another_access_token",
            "refresh_token": "another_refresh_token",
            "id_token": "test_id_token",
            "expires_in": 3600
        }
        
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123", "name": "Test User"}
            
            self.token_manager.set_tokens(token_data)
            
            self.assertEqual(self.token_manager.tokens["access_token"], "another_access_token")
            self.assertEqual(self.token_manager.tokens["id_token"], "test_id_token")
            self.assertEqual(self.token_manager.tokens["claims"], {"sub": "user123", "name": "Test User"})

    def test_get_access_token_valid(self):
        """Test getting a valid access token"""
        # Set up valid token
        token_data = {
            "access_token": "valid_access_token",
            "expires_in": 3600
        }
        
        self.token_manager.set_tokens(token_data)
        
        # Get token
        token = self.token_manager.get_access_token()
        
        self.assertEqual(token, "valid_access_token")

    def test_get_access_token_expired_no_refresh(self):
        """Test getting an expired token with no refresh token"""
        # Set up expired token
        token_data = {
            "access_token": "expired_token",
            "expires_in": -100  # Expired
        }
        
        self.token_manager.set_tokens(token_data)
        
        # Try to get token - should raise exception
        with self.assertRaises(ValueError) as context:
            self.token_manager.get_access_token()
        
        self.assertIn("Access token expired and no refresh token available", str(context.exception))

    def test_get_access_token_expired_with_refresh(self):
        """Test getting an expired token with refresh token"""
        # Set up expired token with refresh token
        token_data = {
            "access_token": "expired_token",
            "refresh_token": "valid_refresh_token",
            "expires_in": -100  # Expired
        }
        
        self.token_manager.set_tokens(token_data)
        
        # Mock refresh_access_token
        with patch.object(self.token_manager, 'refresh_access_token') as mock_refresh:
            mock_refresh.return_value = "refreshed_access_token"
            
            # Get token
            token = self.token_manager.get_access_token()
            
            # Check refresh was called
            mock_refresh.assert_called_once()
            
            # Check refreshed token was returned
            self.assertEqual(token, "refreshed_access_token")

    def test_refresh_access_token(self):
        """Test refreshing access token"""
        # Set up token data
        token_data = {
            "access_token": "old_access_token",
            "refresh_token": "valid_refresh_token",
            "expires_in": 3600
        }
        
        self.token_manager.set_tokens(token_data)
        
        # Mock the requests.post call
        with patch('requests.post') as mock_post:
            # Set up mock response
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
                "expires_in": 7200
            }
            mock_post.return_value = mock_response
            
            # Call refresh
            new_token = self.token_manager.refresh_access_token()
            
            # Check the POST request
            mock_post.assert_called_once_with(
                "https://example.com/oauth2/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": "valid_refresh_token",
                    "client_id": "test_client_id",
                    "client_secret": "test_client_secret",
                }
            )
            
            # Check the returned token
            self.assertEqual(new_token, "new_access_token")
            
            # Check the stored tokens were updated
            self.assertEqual(self.token_manager.tokens["access_token"], "new_access_token")
            self.assertEqual(self.token_manager.tokens["refresh_token"], "new_refresh_token")

    def test_revoke_token(self):
        """Test revoking a token"""
        # Set up token data
        token_data = {
            "access_token": "token_to_revoke",
            "refresh_token": "refresh_token",
            "expires_in": 3600
        }
        
        self.token_manager.set_tokens(token_data)
        
        # Mock the requests.post call
        with patch('requests.post') as mock_post:
            # Set up mock response
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_post.return_value = mock_response
            
            # Call revoke
            self.token_manager.revoke_token()
            
            # Check the POST request
            mock_post.assert_called_once_with(
                "https://example.com/oauth2/revoke",
                data={
                    "token": "token_to_revoke",
                    "client_id": "test_client_id",
                    "client_secret": "test_client_secret",
                }
            )
            
            # Check tokens were cleared
            self.assertEqual(self.token_manager.tokens, {})

    @pytest.mark.asyncio
    async def test_exchange_code_for_token(self):
        """Test exchanging authorization code for token"""
        # Set redirect URI
        self.token_manager.set_redirect_uri("http://localhost/callback")
        
        # Mock the requests.post call
        with patch('requests.post') as mock_post:
            # Set up mock response
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {
                "access_token": "exchanged_access_token",
                "refresh_token": "exchanged_refresh_token",
                "id_token": "exchanged_id_token",
                "expires_in": 3600
            }
            mock_post.return_value = mock_response
            
            # Call exchange
            with patch('jwt.decode') as mock_decode:
                mock_decode.return_value = {"sub": "user123"}
                
                token = await self.token_manager.exchange_code_for_token("auth_code", "code_verifier")
            
            # Check the POST request
            mock_post.assert_called_once_with(
                "https://example.com/oauth2/token",
                data={
                    "grant_type": "authorization_code",
                    "code": "auth_code",
                    "redirect_uri": "http://localhost/callback",
                    "client_id": "test_client_id",
                    "client_secret": "test_client_secret",
                    "code_verifier": "code_verifier",
                }
            )
            
            # Check the returned token
            self.assertEqual(token, "exchanged_access_token")
            
            # Check the stored tokens were updated
            self.assertEqual(self.token_manager.tokens["access_token"], "exchanged_access_token")
            self.assertEqual(self.token_manager.tokens["refresh_token"], "exchanged_refresh_token")
            self.assertEqual(self.token_manager.tokens["id_token"], "exchanged_id_token")


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])