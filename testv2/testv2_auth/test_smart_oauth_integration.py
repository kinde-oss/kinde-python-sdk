"""
Integration tests for SmartOAuth that verify it works in real scenarios.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from kinde_sdk.auth.smart_oauth import SmartOAuth
from kinde_sdk.core.exceptions import KindeConfigurationException

@pytest.fixture
def mock_sync_oauth():
    """Mock sync OAuth instance with realistic behavior."""
    mock = Mock()
    mock.is_authenticated.return_value = True
    mock.get_user_info.return_value = {"email": "test@example.com", "name": "Test User"}
    mock.get_tokens.return_value = {"access_token": "test_token"}
    mock.generate_auth_url.return_value = {"url": "https://test.com/auth"}
    mock.login.return_value = "https://test.com/login"
    mock.register.return_value = "https://test.com/register"
    mock.logout.return_value = "https://test.com/logout"
    mock.handle_redirect.return_value = {"tokens": {}, "user": {}}
    return mock

@pytest.fixture
def mock_async_oauth():
    """Mock async OAuth instance with realistic behavior."""
    mock = Mock()
    mock.is_authenticated.return_value = True
    
    # Create async coroutines for async methods using Mock.side_effect
    async def async_get_user_info_async(*args, **kwargs):
        return {"email": "test@example.com", "name": "Test User"}
    
    async def async_generate_auth_url(*args, **kwargs):
        return {"url": "https://test.com/auth"}
    
    async def async_login(*args, **kwargs):
        return "https://test.com/login"
    
    async def async_register(*args, **kwargs):
        return "https://test.com/register"
    
    async def async_logout(*args, **kwargs):
        return "https://test.com/logout"
    
    async def async_handle_redirect(*args, **kwargs):
        return {"tokens": {}, "user": {}}
    
    # Set up the async methods using side_effect to maintain Mock functionality
    mock.get_user_info_async = Mock(side_effect=async_get_user_info_async)
    mock.generate_auth_url = Mock(side_effect=async_generate_auth_url)
    mock.login = Mock(side_effect=async_login)
    mock.register = Mock(side_effect=async_register)
    mock.logout = Mock(side_effect=async_logout)
    mock.handle_redirect = Mock(side_effect=async_handle_redirect)
    
    return mock

@pytest.fixture
def smart_oauth(mock_sync_oauth, mock_async_oauth):
    """Create SmartOAuth instance with mocked dependencies."""
    with patch('kinde_sdk.auth.smart_oauth.OAuth', return_value=mock_sync_oauth), \
         patch('kinde_sdk.auth.smart_oauth.AsyncOAuth', return_value=mock_async_oauth):
        return SmartOAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="https://test.com/callback"
        )

class TestSmartOAuthRealWorldScenarios:
    """Test SmartOAuth in real-world scenarios."""
    
    def test_flask_application_scenario(self, smart_oauth, mock_sync_oauth):
        """Test SmartOAuth in a Flask application scenario (sync context)."""
        # Simulate Flask application usage
        with patch('warnings.warn') as mock_warn:
            # Check authentication
            is_auth = smart_oauth.is_authenticated()
            assert is_auth is True
            
            # Get user info
            user_info = smart_oauth.get_user_info()
            assert user_info == {"email": "test@example.com", "name": "Test User"}
            
            # Get tokens
            tokens = smart_oauth.get_tokens("user_123")
            assert tokens == {"access_token": "test_token"}
            
            # No warnings should be shown in sync context
            mock_warn.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_fastapi_application_scenario(self, smart_oauth, mock_sync_oauth, mock_async_oauth):
        """Test SmartOAuth in a FastAPI application scenario (async context)."""
        # Simulate FastAPI application usage
        with patch('warnings.warn') as mock_warn:
            # Use async methods (preferred in async context)
            user_info_async = await smart_oauth.get_user_info_async()
            assert user_info_async == {"email": "test@example.com", "name": "Test User"}
            
            auth_url = await smart_oauth.generate_auth_url()
            assert auth_url == {"url": "https://test.com/auth"}
            
            login_url = await smart_oauth.login()
            assert login_url == "https://test.com/login"
            
            # Use sync methods (should work but show warnings)
            is_auth = smart_oauth.is_authenticated()
            assert is_auth is True
            
            user_info_sync = smart_oauth.get_user_info()
            assert user_info_sync == {"email": "test@example.com", "name": "Test User"}
            
            # Warning should be shown for sync methods in async context
            assert mock_warn.call_count == 1
    
    @pytest.mark.asyncio
    async def test_mixed_framework_scenario(self, smart_oauth, mock_sync_oauth, mock_async_oauth):
        """Test SmartOAuth in a scenario where both sync and async are used."""
        # Simulate a complex application that uses both sync and async patterns
        
        # Start with sync operations
        is_auth = smart_oauth.is_authenticated()
        assert is_auth is True
        
        # Switch to async operations
        user_info_async = await smart_oauth.get_user_info_async()
        assert user_info_async == {"email": "test@example.com", "name": "Test User"}
        
        auth_url = await smart_oauth.generate_auth_url()
        assert auth_url == {"url": "https://test.com/auth"}
        
        # Back to sync operations
        tokens = smart_oauth.get_tokens("user_123")
        assert tokens == {"access_token": "test_token"}
        
        # More async operations
        logout_url = await smart_oauth.logout("user_123")
        assert logout_url == "https://test.com/logout"
        
        # Verify all methods were called
        mock_sync_oauth.is_authenticated.assert_called_once()
        mock_sync_oauth.get_tokens.assert_called_once_with("user_123")
        mock_async_oauth.get_user_info_async.assert_called_once()
        mock_async_oauth.generate_auth_url.assert_called_once()
        mock_async_oauth.logout.assert_called_once_with("user_123", None)
    
    def test_error_handling_scenario(self, smart_oauth, mock_sync_oauth):
        """Test SmartOAuth error handling in real scenarios."""
        # Configure mock to raise exception
        mock_sync_oauth.is_authenticated.side_effect = KindeConfigurationException("Authentication failed")
        
        # Should propagate the exception
        with pytest.raises(KindeConfigurationException, match="Authentication failed"):
            smart_oauth.is_authenticated()
    
    @pytest.mark.asyncio
    async def test_async_error_handling_scenario(self, smart_oauth, mock_async_oauth):
        """Test SmartOAuth async error handling in real scenarios."""
        # Configure mock to raise exception
        mock_async_oauth.get_user_info_async.side_effect = KindeConfigurationException("User info failed")
        
        # Should propagate the exception
        with pytest.raises(KindeConfigurationException, match="User info failed"):
            await smart_oauth.get_user_info_async()

class TestSmartOAuthContextSwitching:
    """Test SmartOAuth context switching behavior."""
    
    def test_context_detection_accuracy(self, smart_oauth):
        """Test that context detection works accurately."""
        # In sync context
        assert smart_oauth._is_async_context() is False
        
        # In async context
        async def async_function():
            return smart_oauth._is_async_context()
        
        # Run async function
        result = asyncio.run(async_function())
        assert result is True
    
    def test_warning_behavior_in_different_contexts(self, smart_oauth, mock_sync_oauth):
        """Test warning behavior in different contexts."""
        # In sync context - no warnings
        with patch('warnings.warn') as mock_warn:
            smart_oauth.is_authenticated()
            mock_warn.assert_not_called()
        
        # In async context - warnings shown
        async def async_function():
            with patch('warnings.warn') as mock_warn:
                smart_oauth.is_authenticated()
                return mock_warn.call_count
        
        warning_count = asyncio.run(async_function())
        assert warning_count == 1

class TestSmartOAuthPerformance:
    """Test SmartOAuth performance characteristics."""
    
    def test_initialization_performance(self):
        """Test that SmartOAuth initialization is fast."""
        import time
        
        with patch('kinde_sdk.auth.smart_oauth.OAuth'), \
             patch('kinde_sdk.auth.smart_oauth.AsyncOAuth'):
            
            start_time = time.time()
            smart_oauth = SmartOAuth(client_id="test")
            end_time = time.time()
            
            # Initialization should be fast (< 100ms)
            assert (end_time - start_time) < 0.1
    
    def test_method_delegation_performance(self, smart_oauth, mock_sync_oauth):
        """Test that method delegation is fast."""
        import time
        
        # Test sync method performance
        start_time = time.time()
        for _ in range(100):
            smart_oauth.is_authenticated()
        end_time = time.time()
        
        # 100 calls should be fast (< 10ms)
        assert (end_time - start_time) < 0.01
    
    @pytest.mark.asyncio
    async def test_async_method_performance(self, smart_oauth, mock_async_oauth):
        """Test that async method delegation is fast."""
        import time
        
        # Test async method performance
        start_time = time.time()
        for _ in range(10):
            await smart_oauth.get_user_info_async()
        end_time = time.time()
        
        # 10 async calls should be fast (< 100ms)
        assert (end_time - start_time) < 0.1

class TestSmartOAuthMemoryUsage:
    """Test SmartOAuth memory usage characteristics."""
    
    def test_memory_efficiency(self):
        """Test that SmartOAuth doesn't create memory leaks."""
        import gc
        import sys
        
        # Get initial object count
        gc.collect()
        initial_count = len(gc.get_objects())
        
        # Create and destroy many SmartOAuth instances
        with patch('kinde_sdk.auth.smart_oauth.OAuth'), \
             patch('kinde_sdk.auth.smart_oauth.AsyncOAuth'):
            
            for _ in range(100):
                smart_oauth = SmartOAuth(client_id="test")
                del smart_oauth
        
        # Force garbage collection
        gc.collect()
        final_count = len(gc.get_objects())
        
        # Memory usage should be reasonable (not more than 10% increase)
        increase_percentage = ((final_count - initial_count) / initial_count) * 100
        assert increase_percentage < 10

class TestSmartOAuthThreadSafety:
    """Test SmartOAuth thread safety."""
    
    def test_thread_safety(self, smart_oauth, mock_sync_oauth):
        """Test that SmartOAuth is thread-safe."""
        import threading
        import time
        
        results = []
        errors = []
        
        def worker():
            try:
                for _ in range(10):
                    result = smart_oauth.is_authenticated()
                    results.append(result)
                    time.sleep(0.001)  # Small delay
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Should have no errors
        assert len(errors) == 0
        
        # Should have correct number of results
        assert len(results) == 50  # 5 threads * 10 calls each
        
        # All results should be True
        assert all(results)
