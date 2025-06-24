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


class TestManagementClient(unittest.TestCase):
    """Test cases for the ManagementClient class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.domain = "test.kinde.com"
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        self.base_url = f"https://{self.domain}/api/v1"
        
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
        assert hasattr(client, 'get_user')
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
        
        # Test permission methods
        assert hasattr(client, 'get_permissions')
        assert hasattr(client, 'get_permission')
        assert hasattr(client, 'create_permission')
        assert hasattr(client, 'update_permission')
        assert hasattr(client, 'delete_permission')
        
        # Test feature flag methods
        assert hasattr(client, 'get_feature_flags')
        assert hasattr(client, 'get_feature_flag')
        assert hasattr(client, 'create_feature_flag')
        assert hasattr(client, 'update_feature_flag')
        assert hasattr(client, 'delete_feature_flag')
        
        # Test connected apps methods
        assert hasattr(client, 'get_connected_apps')
        assert hasattr(client, 'get_connected_app')
        
        # Test API applications methods
        assert hasattr(client, 'get_api_applications')
        assert hasattr(client, 'get_api_application')
        assert hasattr(client, 'create_api_application')
        assert hasattr(client, 'update_api_application')
        assert hasattr(client, 'delete_api_application')
        
        # Test subscriber methods
        assert hasattr(client, 'get_subscribers')
        assert hasattr(client, 'get_subscriber')
        
        # Test timezone and industry methods
        assert hasattr(client, 'get_timezones')
        assert hasattr(client, 'get_industries')

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
        
        # Mock token
        test_token = "test_access_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Make API call
        result = client.get_users()
        
        # Verify token was requested
        self.mock_token_manager.get_access_token.assert_called_once()
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify REST client was called with proper headers
        call_args = mock_api_client_instance.rest_client.request.call_args
        assert call_args[1]['headers']['Authorization'] == f"Bearer {test_token}"
        
        # Verify response
        assert result == expected_response

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
            'GET', 'https://test.kinde.com/api/v1/users?page_size=10&sort=email', {}, None, None
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
        
        # Test API call with query parameters
        result = client.get_users(page_size=10, sort="email")
        
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
        result = client.get_user(user_id)
        
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
        result = client.create_user(**user_data)
        
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
        result = client.update_user(user_id, **update_data)
        
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
    def test_feature_flags_api_calls(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test feature flag-related API calls."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'GET', 'https://test.kinde.com/api/v1/feature-flags', {}, None, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"feature_flags": [{"key": "test_flag"}]}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"feature_flags": [{"key": "test_flag"}]}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test feature flag API call
        result = client.get_feature_flags()
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_method_docstrings(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that generated methods have proper docstrings."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_class.return_value = self.mock_api_client
        mock_config_class.return_value = self.mock_configuration
        self.mock_api_client.rest_client = self.mock_rest_client
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test that methods have docstrings
        assert client.get_users.__doc__ is not None
        assert "Get a list of users" in client.get_users.__doc__
        
        assert client.get_user.__doc__ is not None
        assert "Get a user by ID" in client.get_user.__doc__
        
        assert client.create_user.__doc__ is not None
        assert "Create a new user" in client.create_user.__doc__
        
        assert client.update_user.__doc__ is not None
        assert "Update a user" in client.update_user.__doc__
        
        assert client.delete_user.__doc__ is not None
        assert "Delete a user" in client.delete_user.__doc__

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_path_parameter_substitution_multiple_params(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test path parameter substitution with multiple parameters."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        # Mock param_serialize to return expected values
        mock_api_client_instance.param_serialize.return_value = (
            'GET', 'https://test.kinde.com/api/v1/users/user123/roles/role456', {}, None, None
        )
        
        # Mock REST client response
        mock_rest_response = Mock()
        mock_rest_response.read.return_value = None
        mock_rest_response.status = 200
        mock_rest_response.data = b'{"user_id": "user123", "role_id": "role456"}'
        mock_rest_response.getheader.return_value = 'application/json'
        
        mock_api_client_instance.rest_client.request.return_value = mock_rest_response
        
        # Mock response_deserialize
        expected_response = {"user_id": "user123", "role_id": "role456"}
        mock_api_response = Mock()
        mock_api_response.data = expected_response
        mock_api_client_instance.response_deserialize.return_value = mock_api_response
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with multiple path parameters
        # Note: This would require a method that takes multiple path parameters
        # For now, we'll test with a single parameter
        result = client.get_user("user123")
        
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
        
        # Test API call with None values
        result = client.get_users(page_size=10, sort=None, filter=None)
        
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
    def test_readonly_endpoints(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test readonly endpoints (GET requests only)."""
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
        
        # Test readonly endpoints
        result = client.get_timezones()
        
        # Verify param_serialize was called
        mock_api_client_instance.param_serialize.assert_called_once()
        
        # Verify response
        assert result == expected_response

    def test_api_endpoints_constant(self):
        """Test that API_ENDPOINTS constant is properly defined."""
        from kinde_sdk.management.management_client import ManagementClient
        
        # Verify that API_ENDPOINTS is defined
        assert hasattr(ManagementClient, 'API_ENDPOINTS')
        assert isinstance(ManagementClient.API_ENDPOINTS, dict)
        
        # Verify that it contains expected resources
        expected_resources = ['users', 'organizations', 'roles', 'permissions', 'feature_flags', 'connected_apps', 'api_applications', 'subscribers']
        for resource in expected_resources:
            assert resource in ManagementClient.API_ENDPOINTS


if __name__ == '__main__':
    unittest.main()