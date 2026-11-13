import unittest
import pytest
import time
from unittest.mock import patch, MagicMock, Mock, call

from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.auth.token_manager import TokenManager
from kinde_sdk.core.storage.storage_interface import StorageInterface
from kinde_sdk.core.storage.storage_manager import StorageManager


class TestUserSession(unittest.TestCase):
    def setUp(self):
        # Clear token manager instances
        TokenManager._instances = {}
        
        # Create a real mock for the StorageManager
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
            # This would clear all device-specific data
            # For test simplicity, let's just remove the user_id we're testing with
            if self.user_id in self.storage_dict:
                del self.storage_dict[self.user_id]
        
        # Configure the mock with the correct method names
        self.mock_storage_manager.get.side_effect = mock_get
        self.mock_storage_manager.setItems.side_effect = mock_setItems
        self.mock_storage_manager.set.side_effect = mock_set_flat
        self.mock_storage_manager.delete.side_effect = mock_delete
        self.mock_storage_manager.clear_device_data.side_effect = mock_clear_device_data
        
        # Patch the StorageManager's __new__ method to return our mock
        patcher = patch('kinde_sdk.auth.user_session.StorageManager')
        self.mock_storage_manager_class = patcher.start()
        self.mock_storage_manager_class.return_value = self.mock_storage_manager
        self.addCleanup(patcher.stop)
        
        # Create a UserSession (which will use our mocked storage manager)
        self.user_session = UserSession()
        
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

    def test_set_user_data_replace_tokens(self):
        """Test that replace_tokens drops the tokens of an earlier authorization"""
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}

            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)

            # By default a response without a refresh or ID token is merged
            self.user_session.set_user_data(
                self.user_id, self.user_info, {"access_token": "second_access_token", "expires_in": 3600}
            )
            tokens = self.user_session.get_token_manager(self.user_id).tokens
            self.assertEqual(tokens["access_token"], "second_access_token")
            self.assertEqual(tokens["refresh_token"], "test_refresh_token")
            self.assertEqual(tokens["id_token"], "test_id_token")

            self.user_session.set_user_data(
                self.user_id,
                self.user_info,
                {"access_token": "third_access_token", "expires_in": 3600},
                replace_tokens=True,
            )

        tokens = self.user_session.get_token_manager(self.user_id).tokens
        self.assertEqual(tokens["access_token"], "third_access_token")
        self.assertNotIn("refresh_token", tokens)
        self.assertNotIn("id_token", tokens)
        # The stored session matches
        self.assertNotIn("refresh_token", self.storage_dict[self.user_id]["tokens"])

    def test_set_user_data(self):
        """Test setting user data"""
        # Set up JWT decode mock
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123", "name": "Test User"}
            
            # Set user data
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Check storage was set correctly
        self.mock_storage_manager.setItems.assert_called()
        
        # Check the key and ensure at least some of the data was stored
        args, kwargs = self.mock_storage_manager.setItems.call_args
        self.assertEqual(args[0], self.user_id)  # First arg should be the key (user_id)
        
        # Check memory state
        self.assertIn(self.user_id, self.user_session.user_sessions)
        self.assertEqual(self.user_session.user_sessions[self.user_id]["user_info"], self.user_info)
        
        # Check storage dict reflects the data
        self.assertIn(self.user_id, self.storage_dict)
        stored_data = self.storage_dict[self.user_id]
        self.assertEqual(stored_data["user_info"], self.user_info)
        self.assertIn("tokens", stored_data)
        
        # Verify tokens
        tokens = stored_data["tokens"]
        self.assertEqual(tokens["access_token"], "test_access_token")
        self.assertEqual(tokens["refresh_token"], "test_refresh_token")
        self.assertEqual(tokens["id_token"], "test_id_token")
        self.assertTrue("expires_at" in tokens)
        
        # Check token manager
        token_manager = self.user_session.user_sessions[self.user_id]["token_manager"]
        self.assertIsInstance(token_manager, TokenManager)
        self.assertEqual(token_manager.tokens["access_token"], "test_access_token")

    def test_get_user_data_from_memory(self):
        """Test getting user data from memory"""
        # Set up user data with JWT decode mock
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Reset mock counts for clarity
        self.mock_storage_manager.get.reset_mock()
        
        # Get user data
        retrieved_user_info = self.user_session.get_user_data(self.user_id)
        
        # Check user info
        self.assertEqual(retrieved_user_info, self.user_info)
        
        # Since it's in memory, storage.get shouldn't be called
        self.mock_storage_manager.get.assert_not_called()

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
        
        # Store directly in our storage dict
        self.storage_dict[self.user_id] = {
            "user_info": self.user_info,
            "tokens": token_manager.tokens,
        }
        
        # Get user data
        retrieved_user_info = self.user_session.get_user_data(self.user_id)
        
        # Check user info
        self.assertEqual(retrieved_user_info, self.user_info)
        
        # Verify storage.get was called
        self.mock_storage_manager.get.assert_called_with(self.user_id)
        
        # Check memory was populated
        self.assertIn(self.user_id, self.user_session.user_sessions)

    def test_get_token_manager(self):
        """Test getting token manager"""
        # Set up with JWT decode mock
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Reset mock counts
        self.mock_storage_manager.get.reset_mock()
        
        # Get token manager
        token_manager = self.user_session.get_token_manager(self.user_id)
        
        # Check token manager
        self.assertIsInstance(token_manager, TokenManager)
        self.assertEqual(token_manager.user_id, self.user_id)
        self.assertEqual(token_manager.tokens["access_token"], "test_access_token")
        
        # The stored session is checked for tokens replaced by another process.
        # It is unchanged here, so the cached token manager is kept as it is.
        self.mock_storage_manager.get.assert_called_once_with(self.user_id)
        self.assertIs(self.user_session.get_token_manager(self.user_id), token_manager)

    def _stored_copy(self):
        """The stored session as a serializing backend holds it: a copy, not the cached dict."""
        stored = dict(self.storage_dict[self.user_id])
        stored["tokens"] = dict(stored["tokens"])
        return stored

    def _store_tokens_from_another_process(self, token_data):
        """Replace the stored session's tokens, as another worker process would."""
        stored = self._stored_copy()
        stored["tokens"] = dict(token_data)
        stored["revision"] = [stored["revision"][0] + 1, time.time()]
        self.storage_dict[self.user_id] = stored

    def test_get_token_manager_picks_up_tokens_stored_by_another_process(self):
        """Test that the stored session wins over a cached one when it changes"""
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        token_manager = self.user_session.get_token_manager(self.user_id)

        # Another worker handled a step-up callback for this session
        self._store_tokens_from_another_process({
            "access_token": "stepped_up_access_token",
            "id_token": "stepped_up_id_token",
            "refresh_token": "stepped_up_refresh_token",
            "expires_at": time.time() + 3600,
            "id_token_claims": {"sub": "user123", "acr": "mfa"},
        })

        self.assertIs(self.user_session.get_token_manager(self.user_id), token_manager)
        self.assertEqual(token_manager.tokens["access_token"], "stepped_up_access_token")
        self.assertEqual(token_manager.tokens["refresh_token"], "stepped_up_refresh_token")
        self.assertEqual(token_manager.get_claims("id_token")["acr"], "mfa")
        self.assertTrue(self.user_session.is_authenticated(self.user_id))

    def test_get_token_manager_keeps_unsaved_changes_while_the_store_is_unchanged(self):
        """Test that tokens changed in memory are not overwritten by an unchanged store"""
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        token_manager = self.user_session.get_token_manager(self.user_id)

        # Changed in memory only; the store still holds what was saved
        self.storage_dict[self.user_id] = self._stored_copy()
        token_manager.tokens = {"access_token": "changed_in_memory", "expires_at": time.time() + 3600}

        self.assertEqual(
            self.user_session.get_token_manager(self.user_id).tokens["access_token"], "changed_in_memory"
        )
        self.assertEqual(self.storage_dict[self.user_id]["tokens"]["access_token"], "test_access_token")

    def test_get_token_manager_never_adopts_an_older_stored_session(self):
        """Test that an older copy of the session is not adopted, and is repaired"""
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
            # What a request that is still in flight loaded when it began
            older_copy = self._stored_copy()

            # Meanwhile a step-up callback replaces the session's tokens
            self.user_session.set_user_data(
                self.user_id,
                self.user_info,
                {"access_token": "stepped_up_access_token", "refresh_token": "stepped_up_refresh_token", "expires_in": 3600},
                replace_tokens=True,
            )

        # The in-flight request's session is what this process now reads as the store
        self.storage_dict[self.user_id] = older_copy

        token_manager = self.user_session.get_token_manager(self.user_id)
        self.assertEqual(token_manager.tokens["access_token"], "stepped_up_access_token")
        self.assertEqual(token_manager.tokens["refresh_token"], "stepped_up_refresh_token")
        # ...and the current tokens are written back over the older ones
        stored = self.storage_dict[self.user_id]
        self.assertEqual(stored["tokens"]["access_token"], "stepped_up_access_token")
        self.assertEqual(stored["revision"][0], older_copy["revision"][0] + 1)

    def test_revisions_increase_across_processes(self):
        """Test that a process with nothing cached saves a revision above the stored one"""
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
            self.assertEqual(self.storage_dict[self.user_id]["revision"][0], 2)
            self.storage_dict[self.user_id] = self._stored_copy()

            # Another process: its own caches, the same store
            TokenManager._instances = {}
            other_process = UserSession()
            other_process.set_user_data(
                self.user_id, self.user_info, {"access_token": "from_other_process", "expires_in": 3600},
                replace_tokens=True,
            )

        self.assertEqual(self.storage_dict[self.user_id]["revision"][0], 3)
        self.assertEqual(self.storage_dict[self.user_id]["tokens"]["access_token"], "from_other_process")

    def test_load_from_storage_keeps_newer_tokens_already_in_this_process(self):
        """Test that loading an older stored copy doesn't replace newer shared tokens"""
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
            older_copy = self._stored_copy()
            self.user_session.set_user_data(
                self.user_id, self.user_info, {"access_token": "newer_access_token", "expires_in": 3600},
                replace_tokens=True,
            )
        self.storage_dict[self.user_id] = older_copy

        # A second session object in the same process shares the token manager
        other_session = UserSession()
        token_manager = other_session.get_token_manager(self.user_id)

        self.assertEqual(token_manager.tokens["access_token"], "newer_access_token")

    def test_session_stored_without_a_revision_is_loaded(self):
        """Test that a session saved before revisions existed still loads and updates"""
        self.storage_dict[self.user_id] = {
            "user_info": self.user_info,
            "tokens": {"access_token": "legacy_access_token", "expires_at": time.time() + 3600},
        }

        token_manager = self.user_session.get_token_manager(self.user_id)
        self.assertEqual(token_manager.tokens["access_token"], "legacy_access_token")
        self.assertEqual(self.user_session.get_token_manager(self.user_id), token_manager)

        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        self.assertEqual(self.storage_dict[self.user_id]["revision"][0], 1)

    def test_refreshed_tokens_are_saved(self):
        """Test that a token refresh is written back to the stored session"""
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
            token_manager = self.user_session.get_token_manager(self.user_id)
            # Stored sessions are serialized, so they don't share the cached dict
            self.storage_dict[self.user_id] = self._stored_copy()
            saved_revision = self.storage_dict[self.user_id]["revision"]
            token_manager.tokens["expires_at"] = time.time() - 100  # Expired

            with patch('requests.post') as mock_post:
                mock_post.return_value.json.return_value = {
                    "access_token": "refreshed_access_token",
                    "refresh_token": "rotated_refresh_token",
                    "expires_in": 3600,
                }
                self.assertTrue(self.user_session.is_authenticated(self.user_id))

        self.assertEqual(mock_post.call_args.kwargs["data"]["refresh_token"], "test_refresh_token")
        stored_tokens = self.storage_dict[self.user_id]["tokens"]
        self.assertEqual(stored_tokens["access_token"], "refreshed_access_token")
        self.assertEqual(stored_tokens["refresh_token"], "rotated_refresh_token")
        self.assertEqual(self.storage_dict[self.user_id]["revision"][0], saved_revision[0] + 1)
        # The session's own save is not mistaken for another process's
        self.assertEqual(
            self.user_session.get_token_manager(self.user_id).tokens["access_token"], "refreshed_access_token"
        )

    def test_logout(self):
        """Test logout"""
        # Set up with JWT decode mock
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Reset the mock count
        self.mock_storage_manager.clear_device_data.reset_mock()
        
        # Mock token revocation
        with patch.object(TokenManager, 'revoke_token') as mock_revoke:
            # Perform logout
            self.user_session.logout(self.user_id)
            
            # Check revoke was called
            mock_revoke.assert_called_once()
            
            # Check memory was cleaned
            self.assertNotIn(self.user_id, self.user_session.user_sessions)
            
            # Check clear_device_data was called instead of delete
            self.mock_storage_manager.clear_device_data.assert_called_once()
            
            # Check storage dict was updated
            self.assertNotIn(self.user_id, self.storage_dict)

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
        
        # Reset mock
        self.mock_storage_manager.delete.reset_mock()
        
        # Run cleanup
        self.user_session.cleanup_expired_sessions()
        
        # Check results
        self.assertIn(user1, self.user_session.user_sessions)  # Valid token - kept
        self.assertIn(user2, self.user_session.user_sessions)  # Has refresh token - kept
        self.assertNotIn(user3, self.user_session.user_sessions)  # Expired without refresh - removed
        
        # Check storage delete was called for user3
        self.mock_storage_manager.delete.assert_called_once_with(user3)
        
        # Check storage dict reflects the changes
        self.assertIn(user1, self.storage_dict)
        self.assertIn(user2, self.storage_dict)
        self.assertNotIn(user3, self.storage_dict)

    def test_reset(self):
        """Test the reset method"""
        # Set up data
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
            
        # Add a patch for TokenManager.reset_instances
        with patch('kinde_sdk.auth.token_manager.TokenManager.reset_instances') as mock_reset:
            # Call reset
            self.user_session.reset()
            
            # Verify method was called
            mock_reset.assert_called_once()
            
        # Verify user sessions are cleared
        self.assertEqual(self.user_session.user_sessions, {})

    def test_load_from_storage_invalid_data(self):
        """Test loading invalid data from storage"""
        # Set up invalid stored data cases
        invalid_cases = [
            {"user_info": {}},  # Missing tokens
            {"tokens": {}},     # Missing user_info
            {"user_info": {"token_url": "url"}, "tokens": {}},  # Missing client_id
            {"user_info": {"client_id": "id"}, "tokens": {}},   # Missing token_url
            {"user_info": {"client_id": "id", "token_url": "url"}, "tokens": {}}  # Missing access_token
        ]
        
        # Test each invalid case
        for i, invalid_data in enumerate(invalid_cases):
            test_user_id = f"invalid_user_{i}"
            self.storage_dict[test_user_id] = invalid_data
            
            # Try to get data
            result = self.user_session.get_user_data(test_user_id)
            
            # Should return None
            self.assertIsNone(result)
            
            # Verify it's not in memory
            self.assertNotIn(test_user_id, self.user_session.user_sessions)

    @pytest.mark.timeout(5)
    def test_is_authenticated_exceptions(self):
        """Test is_authenticated with exceptions using a custom mock approach"""
        # We won't set up a real token manager - instead create a mock directly
        mock_token_manager = MagicMock()
        
        # First test: ValueError
        # Set up the mock to raise ValueError when get_access_token is called
        mock_token_manager.get_access_token.side_effect = ValueError("Token expired")
        
        # Patch the get_token_manager method to return our mock
        with patch.object(UserSession, 'get_token_manager', return_value=mock_token_manager):
            result = self.user_session.is_authenticated(self.user_id)
            self.assertFalse(result)
            
        # Second test: Generic Exception
        # Reset the mock and set up for generic exception
        mock_token_manager.reset_mock()
        mock_token_manager.get_access_token.side_effect = Exception("Unknown error")
        
        # Patch again with the updated mock
        with patch.object(UserSession, 'get_token_manager', return_value=mock_token_manager):
            result = self.user_session.is_authenticated(self.user_id)
            self.assertFalse(result)

    def test_is_authenticated_minimal(self):
        """Minimal test for is_authenticated exceptions"""
        # Create a fresh UserSession instance
        user_session = UserSession()
        
        # Patch get_token_manager to control what it returns
        with patch.object(UserSession, 'get_token_manager') as mock_get_tm:
            # First test - no token manager
            mock_get_tm.return_value = None
            self.assertFalse(user_session.is_authenticated("any_user"))
            
            # Second test - token manager raises ValueError
            mock_tm = MagicMock()
            mock_tm.get_access_token.side_effect = ValueError()
            mock_get_tm.return_value = mock_tm
            self.assertFalse(user_session.is_authenticated("any_user"))
            
            # Third test - token manager raises generic Exception
            mock_tm = MagicMock()
            mock_tm.get_access_token.side_effect = Exception()
            mock_get_tm.return_value = mock_tm
            self.assertFalse(user_session.is_authenticated("any_user"))

    def test_logout_with_revoke_exception(self):
        """Test logout with token revocation exception"""
        # Set up the user session
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            self.user_session.set_user_data(self.user_id, self.user_info, self.token_data)
        
        # Mock revoke_token to raise an exception
        with patch.object(TokenManager, 'revoke_token') as mock_revoke:
            mock_revoke.side_effect = Exception("Network error")
            
            # Call logout - should complete without error
            self.user_session.logout(self.user_id)
            
            # Check that the user session was still removed
            self.assertNotIn(self.user_id, self.user_session.user_sessions)
            
            # Check that clear_device_data was still called
            self.mock_storage_manager.clear_device_data.assert_called_once()

    def test_cleanup_expired_sessions_edge_cases(self):
        """Test various cases in cleanup_expired_sessions"""
        # Case 1: Session without token manager
        user1 = "user1"
        self.user_session.user_sessions[user1] = {"user_info": self.user_info}  # No token_manager
        
        # Case 2: Session with token manager but no tokens
        user2 = "user2"
        token_manager2 = TokenManager(
            user2, 
            self.user_info["client_id"],
            self.user_info["client_secret"],
            self.user_info["token_url"]
        )
        token_manager2.tokens = {}  # Empty tokens
        self.user_session.user_sessions[user2] = {
            "user_info": self.user_info,
            "token_manager": token_manager2
        }
        
        # Case 3: Session with expired token but with refresh token (should be kept)
        user3 = "user3"
        with patch('jwt.decode') as mock_decode:
            mock_decode.return_value = {"sub": "user123"}
            expired_with_refresh = {
                "access_token": "expired",
                "refresh_token": "refresh",
                "expires_at": time.time() - 100  # Expired
            }
            self.user_session.set_user_data(user3, self.user_info, expired_with_refresh)
        
        # Run cleanup
        self.user_session.cleanup_expired_sessions()
        
        # Check results
        self.assertNotIn(user1, self.user_session.user_sessions)  # Removed (no token manager)
        self.assertNotIn(user2, self.user_session.user_sessions)  # Removed (no tokens)
        self.assertIn(user3, self.user_session.user_sessions)     # Kept (has refresh token)
        
        # Verify storage deletes
        self.mock_storage_manager.delete.assert_has_calls([
            call(user1),
            call(user2)
        ], any_order=True)


if __name__ == "__main__":
    pytest.main(["-xvs", __file__])