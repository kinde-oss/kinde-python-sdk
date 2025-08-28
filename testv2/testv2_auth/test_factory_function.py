"""
Tests for the factory function that creates OAuth clients.
"""

import pytest
from unittest.mock import patch, Mock
from kinde_sdk.auth.smart_oauth import create_oauth_client
from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.async_oauth import AsyncOAuth
from kinde_sdk.auth.smart_oauth import SmartOAuth

class TestCreateOAuthClientFactory:
    """Test the factory function for creating OAuth clients."""
    
    def test_create_sync_client_explicit(self):
        """Test creating explicit sync client with async_mode=False."""
        with patch('kinde_sdk.auth.smart_oauth.OAuth') as mock_sync_class:
            mock_instance = Mock(spec=OAuth)
            mock_sync_class.return_value = mock_instance
            
            client = create_oauth_client(
                async_mode=False,
                client_id="test_client_id",
                client_secret="test_client_secret",
                redirect_uri="https://test.com/callback"
            )
            
            # Should create sync client
            mock_sync_class.assert_called_once_with(
                client_id="test_client_id",
                client_secret="test_client_secret",
                redirect_uri="https://test.com/callback"
            )
            assert client == mock_instance
    
    def test_create_async_client_explicit(self):
        """Test creating explicit async client with async_mode=True."""
        with patch('kinde_sdk.auth.smart_oauth.AsyncOAuth') as mock_async_class:
            mock_instance = Mock(spec=AsyncOAuth)
            mock_async_class.return_value = mock_instance
            
            client = create_oauth_client(
                async_mode=True,
                client_id="test_client_id",
                client_secret="test_client_secret",
                redirect_uri="https://test.com/callback"
            )
            
            # Should create async client
            mock_async_class.assert_called_once_with(
                client_id="test_client_id",
                client_secret="test_client_secret",
                redirect_uri="https://test.com/callback"
            )
            assert client == mock_instance
    
    def test_create_smart_client_default(self):
        """Test creating smart client when async_mode is None (default)."""
        with patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            mock_instance = Mock(spec=SmartOAuth)
            mock_smart_class.return_value = mock_instance
            
            client = create_oauth_client(
                client_id="test_client_id",
                client_secret="test_client_secret",
                redirect_uri="https://test.com/callback"
            )
            
            # Should create smart client
            mock_smart_class.assert_called_once_with(
                client_id="test_client_id",
                client_secret="test_client_secret",
                redirect_uri="https://test.com/callback"
            )
            assert client == mock_instance
    
    def test_create_smart_client_explicit_none(self):
        """Test creating smart client with explicit async_mode=None."""
        with patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            mock_instance = Mock(spec=SmartOAuth)
            mock_smart_class.return_value = mock_instance
            
            client = create_oauth_client(
                async_mode=None,
                client_id="test_client_id",
                client_secret="test_client_secret",
                redirect_uri="https://test.com/callback"
            )
            
            # Should create smart client
            mock_smart_class.assert_called_once_with(
                client_id="test_client_id",
                client_secret="test_client_secret",
                redirect_uri="https://test.com/callback"
            )
            assert client == mock_instance
    
    def test_factory_passes_all_arguments(self):
        """Test that factory passes all arguments correctly to all client types."""
        test_args = {
            'client_id': "test_client_id",
            'client_secret': "test_client_secret",
            'redirect_uri': "https://test.com/callback",
            'framework': "fastapi",
            'host': "https://custom.kinde.com",
            'audience': "api.example.com"
        }
        
        # Test sync client
        with patch('kinde_sdk.auth.smart_oauth.OAuth') as mock_sync_class:
            create_oauth_client(async_mode=False, **test_args)
            sync_call_args = mock_sync_class.call_args[1]
            for key, value in test_args.items():
                assert sync_call_args[key] == value
        
        # Test async client
        with patch('kinde_sdk.auth.smart_oauth.AsyncOAuth') as mock_async_class:
            create_oauth_client(async_mode=True, **test_args)
            async_call_args = mock_async_class.call_args[1]
            for key, value in test_args.items():
                assert async_call_args[key] == value
        
        # Test smart client
        with patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            create_oauth_client(async_mode=None, **test_args)
            smart_call_args = mock_smart_class.call_args[1]
            for key, value in test_args.items():
                assert smart_call_args[key] == value
    
    def test_factory_with_minimal_arguments(self):
        """Test factory with minimal required arguments."""
        with patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            create_oauth_client(client_id="test_client_id")
            
            # Should pass only the provided argument
            call_args = mock_smart_class.call_args[1]
            assert call_args['client_id'] == "test_client_id"
            assert 'client_secret' not in call_args
            assert 'redirect_uri' not in call_args
    
    def test_factory_with_optional_arguments(self):
        """Test factory with optional arguments."""
        optional_args = {
            'framework': "flask",
            'app': Mock(),
            'storage_config': {"type": "memory"},
            'audience': "api.example.com",
            'state': "random_state"
        }
        
        with patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            create_oauth_client(
                client_id="test_client_id",
                **optional_args
            )
            
            call_args = mock_smart_class.call_args[1]
            assert call_args['client_id'] == "test_client_id"
            for key, value in optional_args.items():
                assert call_args[key] == value
    
    def test_factory_returns_correct_types(self):
        """Test that factory returns the correct client types."""
        # Test sync client
        with patch('kinde_sdk.auth.smart_oauth.OAuth') as mock_sync_class:
            mock_sync_instance = Mock(spec=OAuth)
            mock_sync_class.return_value = mock_sync_instance
            
            client = create_oauth_client(async_mode=False, client_id="test")
            assert isinstance(client, Mock)  # Mock doesn't preserve spec in this context
            assert client == mock_sync_instance
        
        # Test async client
        with patch('kinde_sdk.auth.smart_oauth.AsyncOAuth') as mock_async_class:
            mock_async_instance = Mock(spec=AsyncOAuth)
            mock_async_class.return_value = mock_async_instance
            
            client = create_oauth_client(async_mode=True, client_id="test")
            assert isinstance(client, Mock)  # Mock doesn't preserve spec in this context
            assert client == mock_async_instance
        
        # Test smart client
        with patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            mock_smart_instance = Mock(spec=SmartOAuth)
            mock_smart_class.return_value = mock_smart_instance
            
            client = create_oauth_client(client_id="test")
            assert isinstance(client, Mock)  # Mock doesn't preserve spec in this context
            assert client == mock_smart_instance
    
    def test_factory_handles_boolean_values_correctly(self):
        """Test that factory handles boolean values correctly."""
        # Test with explicit True
        with patch('kinde_sdk.auth.smart_oauth.AsyncOAuth') as mock_async_class:
            create_oauth_client(async_mode=True, client_id="test")
            mock_async_class.assert_called_once()
        
        # Test with explicit False
        with patch('kinde_sdk.auth.smart_oauth.OAuth') as mock_sync_class:
            create_oauth_client(async_mode=False, client_id="test")
            mock_sync_class.assert_called_once()
        
        # Test with None (should default to smart client)
        with patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            create_oauth_client(async_mode=None, client_id="test")
            mock_smart_class.assert_called_once()
        
        # Test without async_mode parameter (should default to smart client)
        with patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            create_oauth_client(client_id="test")
            mock_smart_class.assert_called_once()
    
    def test_factory_error_handling(self):
        """Test that factory handles errors from client constructors."""
        # Test sync client constructor error
        with patch('kinde_sdk.auth.smart_oauth.OAuth') as mock_sync_class:
            mock_sync_class.side_effect = Exception("Sync client error")
            
            with pytest.raises(Exception, match="Sync client error"):
                create_oauth_client(async_mode=False, client_id="test")
        
        # Test async client constructor error
        with patch('kinde_sdk.auth.smart_oauth.AsyncOAuth') as mock_async_class:
            mock_async_class.side_effect = Exception("Async client error")
            
            with pytest.raises(Exception, match="Async client error"):
                create_oauth_client(async_mode=True, client_id="test")
        
        # Test smart client constructor error
        with patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            mock_smart_class.side_effect = Exception("Smart client error")
            
            with pytest.raises(Exception, match="Smart client error"):
                create_oauth_client(client_id="test")

class TestFactoryFunctionIntegration:
    """Integration tests for the factory function."""
    
    def test_factory_with_real_client_creation(self):
        """Test factory with real client creation (using mocks for dependencies)."""
        # This test verifies that the factory function works end-to-end
        # by creating actual client instances (with mocked dependencies)
        
        with patch('kinde_sdk.auth.smart_oauth.OAuth') as mock_sync_class, \
             patch('kinde_sdk.auth.smart_oauth.AsyncOAuth') as mock_async_class, \
             patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            
            # Create instances of each client type
            sync_client = create_oauth_client(async_mode=False, client_id="test")
            async_client = create_oauth_client(async_mode=True, client_id="test")
            smart_client = create_oauth_client(client_id="test")
            
            # Verify that each client was created
            assert mock_sync_class.call_count == 1
            assert mock_async_class.call_count == 1
            assert mock_smart_class.call_count == 1
            
            # Verify that the returned clients are the mocked instances
            assert sync_client == mock_sync_class.return_value
            assert async_client == mock_async_class.return_value
            assert smart_client == mock_smart_class.return_value
    
    def test_factory_consistent_behavior(self):
        """Test that factory behaves consistently across multiple calls."""
        with patch('kinde_sdk.auth.smart_oauth.SmartOAuth') as mock_smart_class:
            # Create multiple smart clients with different mock instances
            mock_instance1 = Mock()
            mock_instance2 = Mock()
            mock_instance3 = Mock()
            mock_smart_class.side_effect = [mock_instance1, mock_instance2, mock_instance3]
            
            client1 = create_oauth_client(client_id="test1")
            client2 = create_oauth_client(client_id="test2")
            client3 = create_oauth_client(client_id="test3")
            
            # Each should be a separate instance
            assert client1 != client2
            assert client2 != client3
            assert client1 != client3
            
            # Each should have been created with the correct arguments
            assert mock_smart_class.call_count == 3
            calls = mock_smart_class.call_args_list
            assert calls[0][1]['client_id'] == "test1"
            assert calls[1][1]['client_id'] == "test2"
            assert calls[2][1]['client_id'] == "test3"
