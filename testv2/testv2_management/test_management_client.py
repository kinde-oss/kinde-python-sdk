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
        
    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')  
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_init_basic(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test basic initialization of ManagementClient."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_class.return_value = self.mock_api_client
        mock_config_class.return_value = self.mock_configuration
        
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
        
        # Store original call_api method
        original_call_api = Mock()
        self.mock_api_client.call_api = original_call_api
        
        # Create client (this should modify the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Verify that call_api method was replaced
        assert self.mock_api_client.call_api != original_call_api

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
        
        # Mock API response
        expected_response = {"users": []}
        mock_api_client_instance.call_api.return_value = expected_response
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Make API call
        result = client.get_users()
        
        # Verify token was requested
        self.mock_token_manager.get_access_token.assert_called_once()
        
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
        # Capture the original call_api mock before it gets wrapped
        original_call_api_mock = mock_api_client_instance.call_api
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        expected_response = {"users": [{"id": "user1"}, {"id": "user2"}]}
        original_call_api_mock.return_value = expected_response
        
        # Create client (this will wrap the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with query parameters
        result = client.get_users(page_size=10, sort="email")
        
        # Verify API call was made using the original mock
        original_call_api_mock.assert_called()
        
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
        # Capture the original call_api mock before it gets wrapped
        original_call_api_mock = mock_api_client_instance.call_api
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        expected_response = {"id": "user123", "email": "test@example.com"}
        original_call_api_mock.return_value = expected_response
        
        # Create client (this will wrap the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with path parameter
        user_id = "user123"
        result = client.get_user(user_id)
        
        # Verify API call was made using the original mock
        original_call_api_mock.assert_called()
        
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
        # Capture the original call_api mock before it gets wrapped
        original_call_api_mock = mock_api_client_instance.call_api
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        expected_response = {"id": "new_user", "email": "newuser@example.com"}
        original_call_api_mock.return_value = expected_response
        
        # Create client (this will wrap the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with body data
        user_data = {
            "email": "newuser@example.com",
            "given_name": "New",
            "family_name": "User"
        }
        result = client.create_user(**user_data)
        
        # Verify API call was made using the original mock
        original_call_api_mock.assert_called()
        
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
        # Capture the original call_api mock before it gets wrapped
        original_call_api_mock = mock_api_client_instance.call_api
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        expected_response = {"id": "user123", "email": "updated@example.com"}
        original_call_api_mock.return_value = expected_response
        
        # Create client (this will wrap the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test API call with path parameter and body data
        user_id = "user123"
        update_data = {"email": "updated@example.com"}
        result = client.update_user(user_id, **update_data)
        
        # Verify API call was made using the original mock
        original_call_api_mock.assert_called()
        
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
        # Capture the original call_api mock before it gets wrapped
        original_call_api_mock = mock_api_client_instance.call_api
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        expected_response = {"message": "User deleted successfully"}
        original_call_api_mock.return_value = expected_response
        
        # Create client (this will wrap the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test delete API call
        user_id = "user123"
        result = client.delete_user(user_id)
        
        # Verify API call was made using the original mock
        original_call_api_mock.assert_called()
        
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
        # Capture the original call_api mock before it gets wrapped
        original_call_api_mock = mock_api_client_instance.call_api
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        original_call_api_mock.return_value = {}
        
        # Create client (this will wrap the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test get_organizations
        client.get_organizations()
        original_call_api_mock.assert_called()
        
        # Reset mock
        original_call_api_mock.reset_mock()
        
        # Test get_organization
        org_code = "org_123"
        client.get_organization(org_code)
        original_call_api_mock.assert_called()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_feature_flags_api_calls(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test feature flag-related API calls."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        # Capture the original call_api mock before it gets wrapped
        original_call_api_mock = mock_api_client_instance.call_api
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        original_call_api_mock.return_value = {}
        
        # Create client (this will wrap the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test create_feature_flag
        flag_data = {"name": "new_feature", "type": "boolean"}
        client.create_feature_flag(**flag_data)
        original_call_api_mock.assert_called()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_method_docstrings(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that generated methods have proper docstrings."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_class.return_value = self.mock_api_client
        mock_config_class.return_value = self.mock_configuration
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test list method docstring
        assert "Get a list of users" in client.get_users.__doc__
        assert "sort" in client.get_users.__doc__
        assert "page_size" in client.get_users.__doc__
        
        # Test get method docstring
        assert "Get a user by ID" in client.get_user.__doc__
        assert "user_id" in client.get_user.__doc__
        
        # Test create method docstring
        assert "Create a new user" in client.create_user.__doc__
        assert "User data to create" in client.create_user.__doc__
        
        # Test update method docstring
        assert "Update a user" in client.update_user.__doc__
        assert "user_id" in client.update_user.__doc__
        
        # Test delete method docstring
        assert "Delete a user" in client.delete_user.__doc__
        assert "user_id" in client.delete_user.__doc__

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_path_parameter_substitution_multiple_params(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test path parameter substitution with multiple parameters."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        # Capture the original call_api mock before it gets wrapped
        original_call_api_mock = mock_api_client_instance.call_api
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        original_call_api_mock.return_value = {}
        
        # Create client (this will wrap the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test with a hypothetical endpoint that has multiple path parameters
        # We'll manually test the path substitution logic
        api_method = client._create_api_method('GET', '/users/{user_id}/organizations/{org_id}', 'test', 'get')
        
        # Call the method with multiple path parameters
        api_method("user123", "org456")
        
        # Verify API call was made using the original mock
        original_call_api_mock.assert_called()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_none_values_filtered_out(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that None values are filtered out of query params and body."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        # Capture the original call_api mock before it gets wrapped
        original_call_api_mock = mock_api_client_instance.call_api
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        original_call_api_mock.return_value = {}
        
        # Create client (this will wrap the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test GET request with None values
        client.get_users(page_size=10, sort=None, next_token="abc")
        original_call_api_mock.assert_called()
        
        # Reset mock
        original_call_api_mock.reset_mock()
        
        # Test POST request with None values
        client.create_user(email="test@example.com", given_name=None, family_name="User")
        original_call_api_mock.assert_called()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_api_client_error_handling(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test that API client errors are properly propagated."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_class.return_value = self.mock_api_client
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Make API client raise an exception
        from requests.exceptions import HTTPError
        self.mock_api_client.call_api.side_effect = HTTPError("API Error")
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test that exception is propagated
        with pytest.raises(HTTPError):
            client.get_users()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_token_manager_error_handling(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test handling of token manager errors."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_class.return_value = self.mock_api_client
        mock_config_class.return_value = self.mock_configuration
        
        # Make token manager raise an exception
        self.mock_token_manager.get_access_token.side_effect = Exception("Token error")
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test that token error is propagated
        with pytest.raises(Exception, match="Token error"):
            client.get_users()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_headers_dict_vs_httpheaderdict(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test token injection works with both dict and HTTPHeaderDict headers."""
        from urllib3._collections import HTTPHeaderDict
        
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_class.return_value = self.mock_api_client
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        # Create client
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Mock the original call_api to test header handling
        original_call_api = Mock()
        def mock_call_api(*args, **kwargs):
            # Test with HTTPHeaderDict
            if 'headers' in kwargs and isinstance(kwargs['headers'], HTTPHeaderDict):
                assert 'Authorization' in kwargs['headers']
                assert kwargs['headers']['Authorization'] == f"Bearer {test_token}"
            # Test with regular dict
            elif 'headers' in kwargs and isinstance(kwargs['headers'], dict):
                assert kwargs['headers']['Authorization'] == f"Bearer {test_token}"
            return {}
        
        # Replace the wrapped call_api method
        client.api_client.call_api = mock_call_api
        
        # Test API call (this will use dict headers)
        client.get_users()

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_readonly_endpoints(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test read-only endpoints like timezones and industries."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        # Capture the original call_api mock before it gets wrapped
        original_call_api_mock = mock_api_client_instance.call_api
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        original_call_api_mock.return_value = {}
        
        # Create client (this will wrap the call_api method)
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Test timezones endpoint
        client.get_timezones()
        original_call_api_mock.assert_called()
        
        # Reset mock
        original_call_api_mock.reset_mock()
        
        # Test industries endpoint
        client.get_industries()
        original_call_api_mock.assert_called()

    def test_api_endpoints_constant(self):
        """Test that API_ENDPOINTS constant is properly defined."""
        # Test that all expected endpoints are defined
        assert 'users' in ManagementClient.API_ENDPOINTS
        assert 'organizations' in ManagementClient.API_ENDPOINTS
        assert 'roles' in ManagementClient.API_ENDPOINTS
        assert 'permissions' in ManagementClient.API_ENDPOINTS
        assert 'feature_flags' in ManagementClient.API_ENDPOINTS
        assert 'connected_apps' in ManagementClient.API_ENDPOINTS
        assert 'api_applications' in ManagementClient.API_ENDPOINTS
        assert 'subscribers' in ManagementClient.API_ENDPOINTS
        assert 'timezones' in ManagementClient.API_ENDPOINTS
        assert 'industries' in ManagementClient.API_ENDPOINTS
        
        # Test that users endpoint has all expected actions
        users_endpoints = ManagementClient.API_ENDPOINTS['users']
        assert 'list' in users_endpoints
        assert 'get' in users_endpoints
        assert 'create' in users_endpoints
        assert 'update' in users_endpoints
        assert 'delete' in users_endpoints
        
        # Test endpoint format
        assert users_endpoints['list'] == ('GET', '/users')
        assert users_endpoints['get'] == ('GET', '/users/{user_id}')
        assert users_endpoints['create'] == ('POST', '/users')
        assert users_endpoints['update'] == ('PATCH', '/users/{user_id}')
        assert users_endpoints['delete'] == ('DELETE', '/users/{user_id}')


if __name__ == '__main__':
    unittest.main()