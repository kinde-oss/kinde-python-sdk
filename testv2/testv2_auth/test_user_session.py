import unittest
import pytest
import time
from unittest.mock import patch, MagicMock, Mock

from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.auth.token_manager import TokenManager
from kinde_sdk.auth.storage_interface import StorageInterface


class MockStorage(StorageInterface):
    """Mock storage implementation for testing"""
    def __init__(self):
        self._storage = {}

    def get(self, key):
        return self._storage.get(key)

    def set(self, key, value):
        self._storage[key] = value

    def delete(self, key):
        if key in self._storage:
            del self._storage[key]


class TestUserSession(unittest.TestCase):
    def setUp(self):
        # Clear token manager instances
        TokenManager._instances = {}
        
        # Set up storage and session
        self.storage = MockStorage()
        self.user_session = UserSession(self.storage)
        
        # Set up user info and token data
        self.user_id = "test_user_id"
        self.user_info = {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "token_url": "https://example.com/oauth2/token",
            "redirect_uri": "http://localhost/callback"
        }
        self.token_data = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_in": 3600
        }


    def test_set_user_data(self):
        """Test setting user data"""
        # Set up JWT decode mock
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123", "name": "Test User"}
            
            # Set user data
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Check storage was set correctly
        stored_data = self.storage.get(self.user_id)
        self.assertIsNotNone(stored_data)
        self.assertEqual(stored_data["user_info"], self.user_info)
        self.assertIn("tokens", stored_data)
        
        # Verify tokens
        tokens = stored_data["tokens"]
        self.assertEqual(tokens["access_token"], "test_access_token")
        self.assertEqual(tokens["refresh_token"], "test_refresh_token")
        self.assertEqual(tokens["id_token"], "test_id_token")
        self.assertTrue("expires_at" in tokens)
        
        # Check memory state
        self.assertIn(self.user_id, self.user_session.user_sessions)
        self.assertEqual(self.user_session.user_sessions[self.user_id]["user_info"], self.user_info)
        
        # Check token manager
        token_manager = self.user_session.user_sessions[self.user_id]["token_manager"]
        self.assertIsInstance(token_manager, TokenManager)
        self.assertEqual(token_manager.tokens["access_token"], "test_access_token")

    def test_get_user_data_from_memory(self):
        """Test getting user data from memory"""
        # Set up user data with JWD decode mock
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Get user data
        retrieved_user_info = self.user_session.get_user_data(self.user_id)
        
        # Check user info
        self.assertEqual(retrieved_user_info, self.user_info)

    def test_get_user_data_from_storage(self):
        """Test getting user data from storage"""
        # Prepare storage data without setting in memory
        token_manager = TokenManager(
            self.user_id, 
            self.user_info["client_id"],
            self.user_info["client_secret"],
            self.user_info["token_url"]
        )
        
        # Set tokens with JWT decode mock
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            token_manager.set_tokens(self.token_data)
        
        # Clear the token manager from instances
        if self.user_id in TokenManager._instances:
            del TokenManager._instances[self.user_id]
        
        # Store directly in storage
        self.storage.set(self.user_id, {
            "user_info": self.user_info,
            "tokens": token_manager.tokens,
        })
        
        # Get user data
        retrieved_user_info = self.user_session.get_user_data(self.user_id)
        
        # Check user info
        self.assertEqual(retrieved_user_info, self.user_info)
        
        # Check memory was populated
        self.assertIn(self.user_id, self.user_session.user_sessions)

    def test_get_token_manager(self):
        """Test getting token manager"""
        # Set up with JWD decode mock
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Get token manager
        token_manager = self.user_session.get_token_manager(self.user_id)
        
        # Check token manager
        self.assertIsInstance(token_manager, TokenManager)
        self.assertEqual(token_manager.user_id, self.user_id)
        self.assertEqual(token_manager.tokens["access_token"], "test_access_token")

    # @pytest.mark.timeout(5)  # 5 second timeout
    # def test_is_authenticated_expired(self):
    #     """Test is_authenticated with expired token"""
    #     # Set token data with expired token
    #     expired_token_data = {
    #         "access_token": "expired_token",
    #         "expires_in": -100  # Expired
    #     }
        
    #     # Set up with JWT decode mock
    #     with patch('jwt.decode') as mock_decode, \
    #         patch('requests.post', side_effect=Exception("Network requests disabled in tests")), \
    #         patch('kinde_sdk.auth.token_manager.TokenManager.get_access_token', 
    #             side_effect=ValueError("Token expired")):
            
    #         mock_decode.return_value = {"sub": "user123"}
    #         self.user_session.set_user_data(self.user_id, self.user_info, expired_token_data)
            
    #         # Check authentication - should fail
    #         self.assertFalse(self.user_session.is_authenticated(self.user_id))

    # @pytest.mark.timeout(5)  # 5 second timeout
    # def test_is_authenticated_valid(self):
    #     """Test is_authenticated with valid token"""
    #     # Set up with valid token
    #     valid_token_data = {
    #         "access_token": "valid_access_token",
    #         "expires_in": 3600
    #     }
        
    #     # Set up with JWT decode mock
    #     with patch('jwt.decode') as mock_decode, \
    #         patch('requests.post', side_effect=Exception("Network requests disabled in tests")), \
    #         patch('kinde_sdk.auth.token_manager.TokenManager.get_access_token', 
    #             return_value="valid_access_token"):
            
    #         mock_decode.return_value = {"sub": "user123"}
    #         self.user_session.set_user_data(self.user_id, self.user_info, valid_token_data)
            
    #         # Check authentication - should succeed
    #         self.assertTrue(self.user_session.is_authenticated(self.user_id))


    def test_logout(self):
        """Test logout"""
        # Set up with JWD decode mock
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Mock token revocation
        with patch.object(TokenManager, 'revoke_token') as mock_revoke:
            # Perform logout
            self.user_session.logout(self.user_id)
            
            # Check revoke was called
            mock_revoke.assert_called_once()
            
            # Check memory and storage were cleaned
            self.assertNotIn(self.user_id, self.user_session.user_sessions)
            self.assertIsNone(self.storage.get(self.user_id))

    def test_cleanup_expired_sessions(self):
        """Test cleanup of expired sessions"""
        # Set up multiple users
        user1 = "user1"
        user2 = "user2"
        user3 = "user3"
        
        # User 1 - valid token
        valid_token_data = {
            "access_token": "valid_token",
            "expires_in": 3600
        }
        
        # User 2 - expired token, has refresh token
        expired_with_refresh_data = {
            "access_token": "expired_token",
            "refresh_token": "valid_refresh",
            "expires_in": -100  # Expired
        }
        
        # User 3 - expired token, no refresh token
        expired_no_refresh_data = {
            "access_token": "expired_token",
            "expires_in": -100  # Expired
        }
        
        # Set up all users
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "mock_sub"}
            
            # User 1 - valid
            self.user_session.set_user_data(user1, self.user_info, valid_token_data)
            
            # User 2 - expired with refresh
            self.user_session.set_user_data(user2, self.user_info, expired_with_refresh_data)
            
            # User 3 - expired without refresh
            self.user_session.set_user_data(user3, self.user_info, expired_no_refresh_data)
        
        # Run cleanup
        self.user_session.cleanup_expired_sessions()
        
        # Check results
        self.assertIn(user1, self.user_session.user_sessions)  # Valid token - kept
        self.assertIn(user2, self.user_session.user_sessions)  # Has refresh token - kept
        self.assertNotIn(user3, self.user_session.user_sessions)  # Expired without refresh - removed
        
        # Check storage
        self.assertIsNotNone(self.storage.get(user1))
        self.assertIsNotNone(self.storage.get(user2))
        self.assertIsNone(self.storage.get(user3))


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])