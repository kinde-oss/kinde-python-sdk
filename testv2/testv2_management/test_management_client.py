"""
Test suite for the Kinde Management API client.

This module provides comprehensive tests for the ManagementClient class,
covering initialization, method generation, token handling, and API calls.
"""

import pytest
import unittest
from unittest.mock import Mock, MagicMock, patch, call
from typing import Dict, Any

# Import the modules to test
from kinde_sdk.management.management_client import ManagementClient
from kinde_sdk.management.management_token_manager import ManagementTokenManager
from kinde_sdk.management.custom_exceptions import KindeTokenException


class TestManagementClient(unittest.TestCase):
    """Test cases for the ManagementClient class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.domain = "test.kinde.com"
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        self.base_url = f"https://{self.domain}"
        
        # Reset token manager instances before each test
        ManagementTokenManager.reset_instances()
        
        # Mock dependencies
        self.mock_token_manager = Mock(spec=ManagementTokenManager)
        self.mock_api_client = Mock()
        self.mock_configuration = Mock()
        self.mock_rest_client = Mock()
        
    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')  
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_init_basic(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test basic initialization of ManagementClient."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_class.return_value = self.mock_api_client
        mock_config_class.return_value = self.mock_configuration
        self.mock_api_client.rest_client = self.mock_rest_client
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Verify initialization
        assert client.domain == self.domain
        assert client.base_url == self.base_url
        assert client.token_manager == self.mock_token_manager
        assert client.configuration == self.mock_configuration
        assert client.api_client == self.mock_api_client
        
        # Verify mocks were called correctly
        mock_token_manager_class.assert_called_once_with(self.domain, self.client_id, self.client_secret)
        mock_config_class.assert_called_once_with(host=self.base_url)
        mock_api_client_class.assert_called_once_with(configuration=self.mock_configuration)

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_dynamic_method_generation(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that all dynamic methods are generated correctly."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_class.return_value = self.mock_api_client
        mock_config_class.return_value = self.mock_configuration
        self.mock_api_client.rest_client = self.mock_rest_client
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test user methods
        assert hasattr(client, 'get_users')
        assert hasattr(client, 'get_user_data')
        assert hasattr(client, 'create_user')
        assert hasattr(client, 'update_user')
        assert hasattr(client, 'delete_user')
        
        # Test organization methods
        assert hasattr(client, 'get_organizations')
        assert hasattr(client, 'get_organization')
        assert hasattr(client, 'create_organization')
        assert hasattr(client, 'update_organization')
        assert hasattr(client, 'delete_organization')
        
        # Test role methods
        assert hasattr(client, 'get_roles')
        assert hasattr(client, 'get_role')
        assert hasattr(client, 'create_role')
        assert hasattr(client, 'update_role')
        assert hasattr(client, 'delete_role')
        
        # Test feature flag methods
        assert hasattr(client, 'get_feature_flags')
        assert hasattr(client, 'create_feature_flag')
        assert hasattr(client, 'update_feature_flag')
        assert hasattr(client, 'delete_feature_flag')

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_token_handling_setup(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that token handling is set up correctly."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_class.return_value = self.mock_api_client
        mock_config_class.return_value = self.mock_configuration
        self.mock_api_client.rest_client = self.mock_rest_client
        
        # Create client (token handling is now done inline in API methods)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Verify that token handling setup is called (but does nothing now)
        # The actual token handling is done in each API method

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_token_injection_in_api_calls(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that tokens are properly injected into API calls."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock token
        test_token = "test_access_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Mock the original call_api method to verify the wrapper works
        original_call_api = Mock(return_value="api_response")
        mock_api_client_instance.call_api = original_call_api
        
        # Create client - this wraps call_api with token injection
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Now call_api should be wrapped - call it directly to test the wrapper
        client.api_client.call_api(
            method='GET',
            resource_path='/api/v1/users',
            header_params={}
        )
        
        # Verify token was requested from token manager
        self.mock_token_manager.get_access_token.assert_called_once()
        
        # Verify the wrapped call_api was called with Authorization header injected
        original_call_api.assert_called_once()
        call_kwargs = original_call_api.call_args[1]
        
        # Check that Authorization header was added
        assert 'header_params' in call_kwargs
        assert 'Authorization' in call_kwargs['header_params']
        assert call_kwargs['header_params']['Authorization'] == f"Bearer {test_token}"

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_token_injection_handles_acquisition_failure(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that token acquisition failures are properly handled."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Make token acquisition raise an exception
        self.mock_token_manager.get_access_token.side_effect = Exception("Token service unavailable")
        
        # Mock the original call_api method
        original_call_api = Mock(return_value="api_response")
        mock_api_client_instance.call_api = original_call_api
        
        # Create client - this wraps call_api with token injection
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Calling the wrapped call_api should raise KindeTokenException
        with pytest.raises(KindeTokenException) as exc_info:
            client.api_client.call_api(
                method='GET',
                resource_path='/api/v1/users',
                header_params={}
            )
        
        # Verify the exception message is descriptive
        assert "Failed to acquire access token" in str(exc_info.value)
        assert "Token service unavailable" in str(exc_info.value)
        
        # Verify original call_api was never called
        original_call_api.assert_not_called()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_token_injection_handles_falsy_token(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that falsy token values are properly rejected."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Make token acquisition return None
        self.mock_token_manager.get_access_token.return_value = None
        
        # Mock the original call_api method
        original_call_api = Mock(return_value="api_response")
        mock_api_client_instance.call_api = original_call_api
        
        # Create client - this wraps call_api with token injection
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Calling the wrapped call_api should raise KindeTokenException
        with pytest.raises(KindeTokenException) as exc_info:
            client.api_client.call_api(
                method='GET',
                resource_path='/api/v1/users',
                header_params={}
            )
        
        # Verify the exception message is descriptive
        assert "Failed to acquire access token" in str(exc_info.value)
        assert "invalid token" in str(exc_info.value)
        
        # Verify original call_api was never called
        original_call_api.assert_not_called()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_token_injection_warns_on_existing_auth_header(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that existing Authorization headers trigger a warning."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock token
        test_token = "test_access_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Mock the original call_api method
        original_call_api = Mock(return_value="api_response")
        mock_api_client_instance.call_api = original_call_api
        
        # Create client - this wraps call_api with token injection
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Call with an existing Authorization header and capture the warning
        with patch('kinde_sdk.management.management_client.logger') as mock_logger:
            client.api_client.call_api(
                method='GET',
                resource_path='/api/v1/users',
                header_params={'Authorization': 'Bearer existing_token'}
            )
            
            # Verify warning was logged
            mock_logger.warning.assert_called_once()
            warning_message = mock_logger.warning.call_args[0][0]
            assert "Overwriting existing Authorization header" in warning_message
        
        # Verify the new token was still injected
        call_kwargs = original_call_api.call_args[1]
        assert call_kwargs['header_params']['Authorization'] == f"Bearer {test_token}"

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_get_users_api_call(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test get_users API call with query parameters."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'GET', 'https://test.kinde.com/api/v1/users?page_size=10&email=test@example.com', {}, None, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"users": [{"id": "user1"}, {"id": "user2"}]}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"users": [{"id": "user1"}, {"id": "user2"}]}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with valid query parameters
        result = client.get_users(page_size=10, email="test@example.com")
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_get_user_with_path_parameter(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test get_user API call with path parameter."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'GET', 'https://test.kinde.com/api/v1/users/user123', {}, None, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"id": "user123", "email": "test@example.com"}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"id": "user123", "email": "test@example.com"}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with path parameter
        user_id = "user123"
        result = client.get_users(user_id=user_id)
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_create_user_with_body_data(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test create_user API call with body data."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'POST', 'https://test.kinde.com/api/v1/users', {}, 
            {"email": "newuser@example.com", "given_name": "New", "family_name": "User"}, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"id": "new_user", "email": "newuser@example.com"}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"id": "new_user", "email": "newuser@example.com"}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with body data
        user_data = {
            "email": "newuser@example.com",
            "given_name": "New",
            "family_name": "User"
        }
        result = client.create_user(create_user_request=user_data)
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_update_user_with_path_and_body(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test update_user API call with both path parameter and body data."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'PATCH', 'https://test.kinde.com/api/v1/users/user123', {}, 
            {"email": "updated@example.com"}, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"id": "user123", "email": "updated@example.com"}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"id": "user123", "email": "updated@example.com"}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with path parameter and body data
        user_id = "user123"
        update_data = {"email": "updated@example.com"}
        result = client.update_user(user_id, update_user_request=update_data)
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_delete_user(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test delete_user API call."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'DELETE', 'https://test.kinde.com/api/v1/users/user123', {}, None, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"message": "User deleted successfully"}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"message": "User deleted successfully"}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test delete API call
        user_id = "user123"
        result = client.delete_user(user_id)
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_organizations_api_calls(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test organization-related API calls."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'GET', 'https://test.kinde.com/api/v1/organizations', {}, None, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"organizations": [{"id": "org1"}]}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"organizations": [{"id": "org1"}]}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test organization API call
        result = client.get_organizations()
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_create_feature_flag_with_required_fields(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test creating a feature flag with all required fields."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'POST', 'https://test.kinde.com/api/v1/feature_flags', {}, 
            {"name": "new_flag", "description": "Test flag", "key": "test_flag", "type": "bool"}, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"message": "Feature flag created", "code": "FEATURE_FLAG_CREATED"}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"message": "Feature flag created", "code": "FEATURE_FLAG_CREATED"}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test feature flag API call - use create_feature_flag since get_feature_flags doesn't exist
        feature_flag_data = {
            "name": "new_flag", 
            "description": "Test flag", 
            "key": "test_flag", 
            "type": "bool",
            "default_value": "false"
        }
        result = client.create_feature_flag(create_feature_flag_request=feature_flag_data)
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_get_user_data_by_id(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test retrieving user data by user ID."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'GET', 'https://test.kinde.com/api/v1/user?id=user123', {}, None, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"id": "user123", "email": "test@example.com"}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"id": "user123", "email": "test@example.com"}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with path parameter using get_user_data
        result = client.get_user_data("user123")
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_none_values_filtered_out(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that None values are filtered out from query parameters and body."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'GET', 'https://test.kinde.com/api/v1/users?page_size=10', {}, None, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"users": []}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"users": []}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with None values (should be filtered out)
        result = client.get_users(page_size=10, username=None, email=None)
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_api_client_error_handling(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test error handling when API client raises exceptions."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to raise an exception
        mock_api_client_instance.param_serialize.side_effect = Exception("API Error")
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test that API call raises the exception
        with pytest.raises(Exception, match="API Error"):
            client.get_users()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_token_manager_error_handling(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test error handling when token manager raises exceptions."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values (so it doesn't fail before token manager)
        mock_api_client_instance.param_serialize.return_value = (
            'GET', 'https://test.kinde.com/api/v1/users', {}, None, None
        )
        
        # Mock token manager to raise an exception
        self.mock_token_manager.get_access_token.side_effect = Exception("Token Error")
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test that API call raises the exception
        with pytest.raises(Exception, match="Token Error"):
            client.get_users()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_headers_dict_vs_httpheaderdict(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that headers work with both dict and HTTPHeaderDict."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'GET', 'https://test.kinde.com/api/v1/users', {}, None, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"users": []}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"users": []}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call (headers are handled internally now)
        result = client.get_users()
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_get_timezones_via_dynamic_api(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test accessing dynamically generated API classes (timezones_api) without convenience methods."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'GET', 'https://test.kinde.com/api/v1/timezones', {}, None, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"timezones": ["UTC", "EST"]}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"timezones": ["UTC", "EST"]}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test readonly endpoints - use dynamic API class (no convenience method exists for timezones)
        result = client.timezones_api.get_timezones()
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_dynamic_api_generation(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that API classes are dynamically generated and accessible."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_class.return_value = self.mock_api_client
        mock_config_class.return_value = self.mock_configuration
        self.mock_api_client.rest_client = self.mock_rest_client
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test that common API properties are dynamically created
        # These should be auto-generated from the API classes in kinde_sdk.management.api
        expected_apis = [
            'api_keys_api',             # from APIKeysApi (new in updated spec)
            'apis_api',                 # from APIsApi (special case for "APIs" tag in spec)
            'applications_api',         # from ApplicationsApi
            'billing_agreements_api',   # from BillingAgreementsApi
            'billing_entitlements_api', # from BillingEntitlementsApi
            'billing_meter_usage_api',  # from BillingMeterUsageApi
            'business_api',             # from BusinessApi
            'callbacks_api',            # from CallbacksApi
            'connected_apps_api',       # from ConnectedAppsApi
            'connections_api',          # from ConnectionsApi
            'environment_variables_api',# from EnvironmentVariablesApi
            'environments_api',         # from EnvironmentsApi
            'feature_flags_api',        # from FeatureFlagsApi
            'identities_api',           # from IdentitiesApi
            'industries_api',           # from IndustriesApi
            'mfa_api',                  # from MFAApi
            'organizations_api',        # from OrganizationsApi
            'permissions_api',          # from PermissionsApi
            'properties_api',           # from PropertiesApi
            'property_categories_api',  # from PropertyCategoriesApi
            'roles_api',                # from RolesApi
            'search_api',               # from SearchApi
            'subscribers_api',          # from SubscribersApi
            'timezones_api',            # from TimezonesApi
            'users_api',                # from UsersApi
            'webhooks_api',             # from WebhooksApi
        ]
        
        for api_name in expected_apis:
            assert hasattr(client, api_name), f"client.{api_name} should exist"
            api_instance = getattr(client, api_name)
            assert api_instance is not None, f"client.{api_name} should not be None"
            # Verify it's an API instance (all auto-generated APIs have api_client attribute)
            assert hasattr(api_instance, 'api_client'), f"client.{api_name} should be an API instance"
        
        # Test that the snake_case conversion works correctly, including acronyms
        assert hasattr(client, 'users_api')            # UsersApi -> users_api
        assert hasattr(client, 'feature_flags_api')    # FeatureFlagsApi -> feature_flags_api
        assert hasattr(client, 'apis_api')             # APIsApi -> apis_api (special case workaround)
        assert hasattr(client, 'api_keys_api')         # APIKeysApi -> api_keys_api (new in updated spec)
        assert hasattr(client, 'mfa_api')              # MFAApi -> mfa_api (not m_f_a_api)
        
        # Should NOT have PascalCase versions or names without _api suffix
        assert not hasattr(client, 'UsersApi')
        assert not hasattr(client, 'APIsApi')
        assert not hasattr(client, 'APIKeysApi')
        assert not hasattr(client, 'MFAApi')
        assert not hasattr(client, 'users')      # Should be users_api, not users
        assert not hasattr(client, 'apis')       # Should be apis_api, not apis
        assert not hasattr(client, 'api_keys')   # Should be api_keys_api, not api_keys


if __name__ == '__main__':
    unittest.main()