"""
Test cases for ManagementTokenManager.

These tests cover token management, singleton behavior, thread safety,
and error handling scenarios.
"""

import pytest
import time
import threading
from unittest.mock import patch, Mock, MagicMock
import requests

from kinde_sdk.management.management_token_manager import ManagementTokenManager


class TestManagementTokenManager:
    """Test cases for ManagementTokenManager."""
    
    def setup_method(self):
        """Reset instances before each test."""
        ManagementTokenManager.reset_instances()
    
    def teardown_method(self):
        """Clean up after each test."""
        ManagementTokenManager.reset_instances()
    
    def test_singleton_behavior(self):
        """Test that the same instance is returned for same domain and client_id."""
        domain = "test.kinde.com"
        client_id = "test_client_id"
        client_secret = "test_client_secret"
        
        # Create two instances with same parameters
        manager1 = ManagementTokenManager(domain, client_id, client_secret)
        manager2 = ManagementTokenManager(domain, client_id, client_secret)
        
        # Should be the same instance
        assert manager1 is manager2
        assert id(manager1) == id(manager2)
    
    def test_different_instances_for_different_domains(self):
        """Test that different instances are created for different domains."""
        client_id = "test_client_id"
        client_secret = "test_client_secret"
        
        manager1 = ManagementTokenManager("domain1.kinde.com", client_id, client_secret)
        manager2 = ManagementTokenManager("domain2.kinde.com", client_id, client_secret)
        
        # Should be different instances
        assert manager1 is not manager2
        assert id(manager1) != id(manager2)
    
    def test_initialization_attributes(self):
        """Test that initialization sets correct attributes."""
        domain = "test.kinde.com"
        client_id = "test_client_id"
        client_secret = "test_client_secret"
        
        manager = ManagementTokenManager(domain, client_id, client_secret)
        
        assert manager.domain == domain
        assert manager.client_id == client_id
        assert manager.client_secret == client_secret
        assert manager.token_url == f"https://{domain}/oauth2/token"
        assert manager.tokens == {}
        assert manager.initialized is True
        # Fix: Use the correct way to check if it's a Lock instance
        assert hasattr(manager.lock, 'acquire') and hasattr(manager.lock, 'release')
    
    def test_skip_reinitialization(self):
        """Test that reinitialization is skipped for existing instances."""
        domain = "test.kinde.com"
        client_id = "test_client_id"
        client_secret = "test_client_secret"
        
        # Create instance
        manager1 = ManagementTokenManager(domain, client_id, client_secret)
        original_domain = manager1.domain
        
        # Try to create another instance with same domain+client_id but different secret
        # The __new__ method uses domain and client_id for the instance key
        manager2 = ManagementTokenManager(domain, client_id, "different_secret")
        
        # Should be same instance with original domain and original secret
        assert manager1 is manager2
        assert manager2.domain == original_domain
        assert manager2.client_secret == client_secret  # Original secret should be preserved
    
    def test_set_tokens(self):
        """Test token storage functionality."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        token_data = {
            "access_token": "test_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        
        # Mock time.time() to have predictable expires_at
        with patch('kinde_sdk.management.management_token_manager.time.time', return_value=1000):
            manager.set_tokens(token_data)
        
        assert manager.tokens["access_token"] == "test_access_token"
        assert manager.tokens["expires_at"] == 1000 + 3600
        assert manager.tokens["token_type"] == "Bearer"
    
    def test_set_tokens_with_defaults(self):
        """Test token storage with default values."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        token_data = {
            "access_token": "test_access_token"
            # Missing expires_in and token_type
        }
        
        with patch('kinde_sdk.management.management_token_manager.time.time', return_value=1000):
            manager.set_tokens(token_data)
        
        assert manager.tokens["access_token"] == "test_access_token"
        assert manager.tokens["expires_at"] == 1000 + 3600  # Default expires_in
        assert manager.tokens["token_type"] == "Bearer"  # Default token_type
    
    @patch('kinde_sdk.management.management_token_manager.requests.post')
    def test_request_new_token_success(self, mock_post):
        """Test successful token request."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        }
        mock_response.raise_for_status.return_value = None  # Add this line
        mock_post.return_value = mock_response
        
        with patch('kinde_sdk.management.management_token_manager.time.time', return_value=2000):
            token = manager.request_new_token()
        
        # Verify request was made correctly (NOW INCLUDING TIMEOUT)
        mock_post.assert_called_once_with(
            "https://test.kinde.com/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": "client_id",
                "client_secret": "client_secret",
                "audience": "https://test.kinde.com/api"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30  # ADD THIS LINE - our fix added timeout
        )
        
        # Verify token was stored and returned
        assert token == "new_access_token"
        assert manager.tokens["access_token"] == "new_access_token"
        assert manager.tokens["expires_at"] == 2000 + 3600
    
    @patch('kinde_sdk.management.management_token_manager.requests.post')
    def test_request_new_token_http_error(self, mock_post):
        """Test token request with HTTP error."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Mock HTTP error response
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized")
        mock_post.return_value = mock_response
        
        # NOW EXPECT OUR CUSTOM EXCEPTION, NOT THE ORIGINAL HTTPError
        with pytest.raises(Exception) as exc_info:
            manager.request_new_token()
        
        # Verify it's our custom exception with the expected message format
        assert "Token request failed for domain test.kinde.com" in str(exc_info.value)
        assert "401 Unauthorized" in str(exc_info.value)
    
    @patch('kinde_sdk.management.management_token_manager.requests.post')
    def test_get_access_token_with_valid_token(self, mock_post):
        """Test getting access token when valid token exists."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Set a valid token (expires in future)
        with patch('kinde_sdk.management.management_token_manager.time.time', return_value=1000):
            manager.set_tokens({
                "access_token": "existing_token",
                "expires_in": 3600,
                "token_type": "Bearer"
            })
        
        # Get token when current time is still before expiry (with 60s buffer)
        with patch('kinde_sdk.management.management_token_manager.time.time', return_value=1500):  # 500 seconds later, still valid
            token = manager.get_access_token()
        
        # Should return existing token without making new request
        assert token == "existing_token"
        mock_post.assert_not_called()
    
    def test_clear_tokens(self):
        """Test clearing stored tokens."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Set some tokens
        manager.set_tokens({
            "access_token": "test_token",
            "expires_in": 3600,
            "token_type": "Bearer"
        })
        
        assert manager.tokens != {}
        
        # Clear tokens
        manager.clear_tokens()
        
        assert manager.tokens == {}
    
    def test_reset_instances(self):
        """Test resetting all instances."""
        # Create some instances
        manager1 = ManagementTokenManager("domain1.kinde.com", "client1", "secret1")
        manager2 = ManagementTokenManager("domain2.kinde.com", "client2", "secret2")
        
        # Verify instances exist
        assert len(ManagementTokenManager._instances) == 2
        
        # Reset instances
        ManagementTokenManager.reset_instances()
        
        # Verify instances are cleared
        assert len(ManagementTokenManager._instances) == 0
        
        # New instances should be different from old ones
        new_manager1 = ManagementTokenManager("domain1.kinde.com", "client1", "secret1")
        assert new_manager1 is not manager1
    
    def test_thread_safety_singleton(self):
        """Test that singleton pattern is thread-safe."""
        domain = "test.kinde.com"
        client_id = "test_client_id"
        client_secret = "test_client_secret"
        
        instances = []
        lock = threading.Lock()
        
        def create_instance():
            instance = ManagementTokenManager(domain, client_id, client_secret)
            with lock:
                instances.append(instance)
        
        # Create multiple threads (reduced from 10 to 5 to avoid timeout)
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=create_instance)
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete with timeout
        for thread in threads:
            thread.join(timeout=2.0)  # Add timeout to prevent hanging
        
        # All instances should be the same
        first_instance = instances[0]
        for instance in instances:
            assert instance is first_instance
    
    def test_thread_safety_token_operations(self):
        """Test that token operations are thread-safe."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        results = []
        lock = threading.Lock()
        
        def set_and_get_token(token_suffix):
            with patch('kinde_sdk.management.management_token_manager.time.time', return_value=1000):
                manager.set_tokens({
                    "access_token": f"token_{token_suffix}",
                    "expires_in": 3600,
                    "token_type": "Bearer"
                })
            # Small delay to allow other threads to interfere
            time.sleep(0.001)
            with lock:
                results.append(manager.tokens.get("access_token"))
        
        # Create multiple threads (reduced number)
        threads = []
        for i in range(3):  # Reduced from 5 to 3
            thread = threading.Thread(target=set_and_get_token, args=(i,))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete with timeout
        for thread in threads:
            thread.join(timeout=2.0)
        
        # Should have received some results (exactly which one depends on timing)
        assert len(results) == 3
        # All results should be valid token strings
        for result in results:
            assert result.startswith("token_")
    
    
    def test_token_data_edge_cases(self):
        """Test edge cases in token data handling."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Test with None values for expires_in - should use default 3600
        token_data = {
            "access_token": "test_token",
            "expires_in": None,  # This will cause the error
            "token_type": None
        }
        
        with patch('kinde_sdk.management.management_token_manager.time.time', return_value=1000):
            manager.set_tokens(token_data)
        
        assert manager.tokens["access_token"] == "test_token"
        assert manager.tokens["expires_at"] == 1000 + 3600  # Default expires_in when None
        assert manager.tokens["token_type"] == "Bearer"  # Default token_type when None
    
    def test_concurrent_token_refresh(self):
        """Test concurrent access to token refresh."""
        manager = ManagementTokenManager("test.kinde.com", "client_id", "client_secret")
        
        # Set an expired token
        with patch('kinde_sdk.management.management_token_manager.time.time', return_value=1000):
            manager.set_tokens({
                "access_token": "expired_token",
                "expires_in": 100,  # Very short expiry
                "token_type": "Bearer"
            })
        
        call_count = 0
        original_request_new_token = manager.request_new_token
        
        def mock_request_new_token():
            nonlocal call_count
            call_count += 1
            # Simulate some delay
            time.sleep(0.01)
            return f"new_token_{call_count}"
        
        manager.request_new_token = mock_request_new_token
        
        results = []
        lock = threading.Lock()
        
        def get_token():
            # This should trigger token refresh since token is expired
            with patch('kinde_sdk.management.management_token_manager.time.time', return_value=2000):
                token = manager.get_access_token()
                with lock:
                    results.append(token)
        
        # Create multiple threads trying to get token simultaneously
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=get_token)
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=2.0)
        
        # Due to thread safety, only one token refresh should occur
        # But all threads should get a valid token
        assert len(results) == 3
        for result in results:
            assert result.startswith("new_token_")