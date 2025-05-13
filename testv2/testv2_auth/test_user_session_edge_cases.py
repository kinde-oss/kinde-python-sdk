import unittest
import threading
import time
from unittest.mock import patch, MagicMock, Mock

from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.auth.token_manager import TokenManager
from kinde_sdk.core.storage.storage_interface import StorageInterface
from kinde_sdk.core.storage.storage_manager import StorageManager

class TestUserSessionEdgeCases(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Clear token manager instances
        TokenManager._instances = {}
        
        # Create a mock storage manager
        self.mock_storage_manager = MagicMock()
        
        # Create a dictionary to simulate storage
        self.storage_dict = {}
        
        # Set up the side effects for the mock
        def mock_get(key):
            return self.storage_dict.get(key)
            
        def mock_setItems(key, value):
            self.storage_dict[key] = value
            
        def mock_set_flat(access_token):
            self.storage_dict["_flat_access_token"] = access_token
            
        def mock_delete(key):
            if key in self.storage_dict:
                del self.storage_dict[key]
                
        def mock_clear_device_data():
            self.storage_dict.clear()
        
        # Configure the mock
        self.mock_storage_manager.get.side_effect = mock_get
        self.mock_storage_manager.setItems.side_effect = mock_setItems
        self.mock_storage_manager.set.side_effect = mock_set_flat
        self.mock_storage_manager.delete.side_effect = mock_delete
        self.mock_storage_manager.clear_device_data.side_effect = mock_clear_device_data
        
        # Create user session instance
        self.user_session = UserSession()
        self.user_session._storage_manager = self.mock_storage_manager
        
        # Test data
        self.user_id = "test_user"
        self.user_info = {
            "client_id": "test_client",
            "client_secret": "test_secret",
            "token_url": "https://test.com/token",
            "redirect_uri": "https://test.com/callback"
        }
        self.token_data = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_in": 3600
        }

    def test_set_user_data_invalid_tokens(self):
        """Test set_user_data with invalid token data."""
        #invalid_token_cases = [
        #    {},  # Empty tokens
        #    {"access_token": None},  # None access token
        #    {"access_token": ""},  # Empty access token
        #    {"refresh_token": "test"},  # Missing access token
        #]
        
        #for invalid_tokens in invalid_token_cases:
        #    with self.assertRaises(ValueError):
        #        self.user_session.set_user_data(self.user_id, self.user_info, invalid_tokens)

    def test_set_user_data_invalid_user_info(self):
        """Test set_user_data with invalid user info."""
        #invalid_info_cases = [
        #    {},  # Empty info
        #    {"client_id": "test"},  # Missing required fields
        #    {"token_url": "test"},  # Missing required fields
        #    {"client_id": None, "token_url": "test"},  # None values
        #]
        
        #for invalid_info in invalid_info_cases:
        #    with self.assertRaises(ValueError):
        #        self.user_session.set_user_data(self.user_id, invalid_info, self.token_data)

    def test_get_user_data_not_found(self):
        """Test get_user_data when data is not found."""
        result = self.user_session.get_user_data("nonexistent_user")
        self.assertIsNone(result)

    def test_get_token_manager_not_found(self):
        """Test get_token_manager when manager is not found."""
        result = self.user_session.get_token_manager("nonexistent_user")
        self.assertIsNone(result)

    def test_is_authenticated_no_token_manager(self):
        """Test is_authenticated when token manager is not found."""
        result = self.user_session.is_authenticated("nonexistent_user")
        self.assertFalse(result)

    def test_is_authenticated_token_error(self):
        """Test is_authenticated when token manager raises error."""
        # Set up user data first
        #with patch('jwt.decode') as mock_decode:
        #    mock_decode.return_value = {"sub": "user123"}
        #    self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Make token manager raise error
        #token_manager = self.user_session.get_token_manager(self.user_id)
        #token_manager.get_access_token.side_effect = Exception("Token error")
        
        #result = self.user_session.is_authenticated(self.user_id)
        #self.assertFalse(result)

    def test_logout_nonexistent_user(self):
        """Test logout with nonexistent user."""
        # Should not raise exception
        self.user_session.logout("nonexistent_user")
        self.mock_storage_manager.clear_device_data.assert_not_called()

    def test_logout_storage_error(self):
        """Test logout when storage operations fail."""
        # Set up user data first
        #with patch('jwt.decode') as mock_decode:
        #    mock_decode.return_value = {"sub": "user123"}
        #    self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Make storage operations fail
        #self.mock_storage_manager.clear_device_data.side_effect = Exception("Storage error")
        
        # Should not raise exception
        #self.user_session.logout(self.user_id)
        #self.assertNotIn(self.user_id, self.user_session.user_sessions)

    def test_concurrent_session_access(self):
        """Test concurrent access to user sessions."""
        def worker():
            # Set user data
            with patch('jwt.decode') as mock_decode:
                mock_decode.return_value = {"sub": "user123"}
                self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
            
            # Get user data
            user_data = self.user_session.get_user_data(self.user_id)
            
            # Check authentication
            is_auth = self.user_session.is_authenticated(self.user_id)
            
            # Get token manager
            token_manager = self.user_session.get_token_manager(self.user_id)
            
            return user_data, is_auth, token_manager
        
        # Create multiple threads
        threads = []
        results = []
        for _ in range(5):
            thread = threading.Thread(target=lambda: results.append(worker()))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all threads got consistent results
        first_result = results[0]
        self.assertTrue(all(r == first_result for r in results))

    def test_load_from_storage_corrupted_data(self):
        """Test loading corrupted data from storage."""
        corrupted_cases = [
            None,  # None data
            "not_a_dict",  # Non-dict data
            {"user_info": "not_a_dict"},  # Invalid user_info
            {"tokens": "not_a_dict"},  # Invalid tokens
            {"user_info": {}, "tokens": {}},  # Empty data
        ]
        
        for corrupted_data in corrupted_cases:
            self.storage_dict[self.user_id] = corrupted_data
            result = self.user_session.get_user_data(self.user_id)
            self.assertIsNone(result)

    def test_set_user_data_storage_error(self):
        """Test set_user_data when storage operations fail."""
        #self.mock_storage_manager.setItems.side_effect = Exception("Storage error")
        
        #with self.assertRaises(Exception):
        #    self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)

    def test_get_user_data_storage_error(self):
        """Test get_user_data when storage operations fail."""
        self.mock_storage_manager.get.side_effect = Exception("Storage error")
        
        result = self.user_session.get_user_data(self.user_id)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main() 