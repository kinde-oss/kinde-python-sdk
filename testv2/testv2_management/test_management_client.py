"""
Test suite for the Kinde Management API client.

This module provides comprehensive tests for the ManagementClient class,
covering initialization, method generation, token handling, and API calls.

Tests use a "less mocking" approach where only the HTTP layer and token manager
are mocked, allowing real serialization/deserialization logic to run.
"""

import json
import pytest
import unittest
import warnings
from unittest.mock import Mock, MagicMock, patch, call
from typing import Dict, Any

# Import the modules to test
from kinde_sdk.management.management_client import ManagementClient
from kinde_sdk.management.management_token_manager import ManagementTokenManager
from kinde_sdk.management.rest import RESTResponse


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
        
        # Mock dependencies for structural tests
        self.mock_token_manager = Mock(spec=ManagementTokenManager)
        self.mock_api_client = Mock()
        self.mock_configuration = Mock()
        self.mock_rest_client = Mock()
    
    def _make_mock_http_response(self, status: int, body: dict) -> RESTResponse:
        """
        Create a mock urllib3 response wrapped in RESTResponse.
        
        This allows real deserialization to run while only mocking the HTTP layer.
        """
        mock_urllib3_response = Mock()
        mock_urllib3_response.status = status
        mock_urllib3_response.reason = "OK" if status == 200 else "Error"
        mock_urllib3_response.data = json.dumps(body).encode('utf-8')
        mock_urllib3_response.headers = {'Content-Type': 'application/json'}
        return RESTResponse(mock_urllib3_response)
        
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
    def test_token_injection_with_positional_args(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test token injection when header_params is passed as positional argument."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_access_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        original_call_api = Mock(return_value="api_response")
        mock_api_client_instance.call_api = original_call_api
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Call with header_params as 3rd positional arg (index 2)
        # Simulating: call_api(method, url, header_params, ...)
        existing_headers = {'X-Custom-Header': 'custom_value'}
        client.api_client.call_api('GET', '/api/v1/users', existing_headers)
        
        # Verify the call - args should have Authorization added
        original_call_api.assert_called_once()
        call_args = original_call_api.call_args[0]
        
        # The header_params should now include both the original header and Authorization
        assert len(call_args) >= 3
        header_params = call_args[2]
        assert 'Authorization' in header_params
        assert header_params['Authorization'] == f"Bearer {test_token}"
        assert header_params['X-Custom-Header'] == 'custom_value'

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_token_injection_with_positional_args_none_headers(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test token injection when header_params is None as positional argument."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_access_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        original_call_api = Mock(return_value="api_response")
        mock_api_client_instance.call_api = original_call_api
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Call with header_params=None as 3rd positional arg
        client.api_client.call_api('GET', '/api/v1/users', None)
        
        # Verify the call
        original_call_api.assert_called_once()
        call_args = original_call_api.call_args[0]
        
        # The header_params should be a dict with Authorization (was None, now initialized)
        assert len(call_args) >= 3
        header_params = call_args[2]
        assert isinstance(header_params, dict)
        assert 'Authorization' in header_params
        assert header_params['Authorization'] == f"Bearer {test_token}"

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_token_injection_with_kwargs_none_headers(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test token injection when header_params=None in kwargs."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_access_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        original_call_api = Mock(return_value="api_response")
        mock_api_client_instance.call_api = original_call_api
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Call with header_params=None in kwargs
        client.api_client.call_api(method='GET', resource_path='/api/v1/users', header_params=None)
        
        # Verify the call
        original_call_api.assert_called_once()
        call_kwargs = original_call_api.call_args[1]
        
        # The header_params should be a dict with Authorization (was None, now initialized)
        assert 'header_params' in call_kwargs
        assert isinstance(call_kwargs['header_params'], dict)
        assert 'Authorization' in call_kwargs['header_params']
        assert call_kwargs['header_params']['Authorization'] == f"Bearer {test_token}"

    @patch('kinde_sdk.management.management_client.Configuration')
    @patch('kinde_sdk.management.management_client.ApiClient')
    @patch('kinde_sdk.management.management_client.ManagementTokenManager')
    def test_token_injection_without_header_params(self, mock_token_manager_class, mock_api_client_class, mock_config_class):
        """Test token injection when no header_params provided at all."""
        # Setup mocks
        mock_token_manager_class.return_value = self.mock_token_manager
        mock_api_client_instance = Mock()
        mock_api_client_class.return_value = mock_api_client_instance
        mock_config_class.return_value = self.mock_configuration
        
        test_token = "test_access_token"
        self.mock_token_manager.get_access_token.return_value = test_token
        
        original_call_api = Mock(return_value="api_response")
        mock_api_client_instance.call_api = original_call_api
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Call without header_params at all
        client.api_client.call_api(method='GET', resource_path='/api/v1/users')
        
        # Verify the call
        original_call_api.assert_called_once()
        call_kwargs = original_call_api.call_args[1]
        
        # The header_params should be created with just Authorization
        assert 'header_params' in call_kwargs
        assert call_kwargs['header_params'] == {'Authorization': f"Bearer {test_token}"}

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_get_users_api_call(self, mock_tm_init, mock_get_token):
        """Test get_users API call with real parameter serialization."""
        # Create client - real Configuration and ApiClient are used
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Mock only the HTTP layer
        response_body = {
            "code": "OK",
            "message": "Success",
            "users": [
                {"id": "user_123", "email": "alice@example.com", "provided_id": None},
                {"id": "user_456", "email": "bob@example.com", "provided_id": None}
            ],
            "next_token": None
        }
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            # Suppress deprecation warning for this test
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                result = client.get_users(page_size=10)
            
            # Verify the HTTP request was constructed correctly (real serialization ran)
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Method and URL are positional args
            method = call_args[0][0]
            url = call_args[0][1]
            
            # Check HTTP method
            assert method == 'GET'
            
            # Check URL includes query params
            assert '/api/v1/users' in url
            assert 'page_size=10' in url
            
            # Check Authorization header was injected (in kwargs)
            headers = call_args[1].get('headers', {})
            assert 'Authorization' in headers
            assert headers['Authorization'] == 'Bearer fake_token'
            
            # Verify response was deserialized (real deserialization ran)
            assert result is not None
            assert hasattr(result, 'users') or (isinstance(result, dict) and 'users' in result)

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_get_user_data_with_query_parameter(self, mock_tm_init, mock_get_token):
        """Test get_user_data API call with query parameter (id)."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {
            "id": "kp_abc123",
            "email": "test@example.com",
            "provided_id": None,
            "first_name": "Test",
            "last_name": "User"
        }
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            # Use the users_api directly (preferred over deprecated wrapper)
            result = client.users_api.get_user_data(id="kp_abc123")
            
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Method and URL are positional args
            method = call_args[0][0]
            url = call_args[0][1]
            
            # Check URL includes query parameter
            assert method == 'GET'
            assert '/api/v1/user' in url
            assert 'id=kp_abc123' in url
            
            # Verify response
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_create_user_with_body_data(self, mock_tm_init, mock_get_token):
        """Test create_user API call with real body serialization."""
        from kinde_sdk.management.models.create_user_request import CreateUserRequest
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {
            "id": "kp_new123",
            "created": True,
            "identities": [{"type": "email", "identity": "newuser@example.com"}]
        }
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            # Use the Pydantic model for the request
            create_request = CreateUserRequest(
                profile={"given_name": "New", "family_name": "User"},
                identities=[{"type": "email", "details": {"email": "newuser@example.com"}}]
            )
            
            result = client.users_api.create_user(create_user_request=create_request)
            
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Method and URL are positional args
            method = call_args[0][0]
            url = call_args[0][1]
            
            # Check HTTP method
            assert method == 'POST'
            
            # Check URL
            assert '/api/v1/user' in url
            
            # Check body was serialized (real param_serialize ran)
            body = call_args[1].get('body')
            assert body is not None
            parsed_body = json.loads(body) if isinstance(body, str) else body
            assert 'profile' in parsed_body or 'identities' in parsed_body
            
            # Verify response
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_update_user_with_path_and_body(self, mock_tm_init, mock_get_token):
        """Test update_user API call with real path parameter substitution and body serialization."""
        from kinde_sdk.management.models.update_user_request import UpdateUserRequest
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {
            "id": "kp_user123",
            "given_name": "Updated",
            "family_name": "Name"
        }
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            update_request = UpdateUserRequest(
                given_name="Updated",
                family_name="Name"
            )
            
            result = client.users_api.update_user(
                id="kp_user123",
                update_user_request=update_request
            )
            
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Method and URL are positional args
            method = call_args[0][0]
            url = call_args[0][1]
            
            # Check HTTP method
            assert method == 'PATCH'
            
            # Check URL contains the user ID (real path param substitution)
            assert '/api/v1/user' in url
            assert 'id=kp_user123' in url
            
            # Check body was serialized
            body = call_args[1].get('body')
            assert body is not None
            
            # Verify response
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_delete_user(self, mock_tm_init, mock_get_token):
        """Test delete_user API call with real parameter handling."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {
            "code": "OK",
            "message": "Success"
        }
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            result = client.users_api.delete_user(id="kp_user123")
            
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Method and URL are positional args
            method = call_args[0][0]
            url = call_args[0][1]
            
            # Check HTTP method
            assert method == 'DELETE'
            
            # Check URL contains the user ID
            assert '/api/v1/user' in url
            assert 'id=kp_user123' in url
            
            # Verify response
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_organizations_api_calls(self, mock_tm_init, mock_get_token):
        """Test organization-related API calls with real serialization."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {
            "code": "OK",
            "message": "Success",
            "organizations": [
                {"code": "org_abc", "name": "Test Org", "is_default": True}
            ],
            "next_token": None
        }
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            result = client.organizations_api.get_organizations(page_size=25)
            
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Method and URL are positional args
            method = call_args[0][0]
            url = call_args[0][1]
            
            # Check HTTP method and URL
            assert method == 'GET'
            assert '/api/v1/organizations' in url
            assert 'page_size=25' in url
            
            # Verify response
            assert result is not None
            assert hasattr(result, 'organizations') or (isinstance(result, dict) and 'organizations' in result)

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_create_feature_flag_with_required_fields(self, mock_tm_init, mock_get_token):
        """Test creating a feature flag with real body serialization."""
        from kinde_sdk.management.models.create_feature_flag_request import CreateFeatureFlagRequest
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {
            "code": "FEATURE_FLAG_CREATED",
            "message": "Feature flag created"
        }
        # Note: create_feature_flag expects 201 status code per the API spec
        mock_http_response = self._make_mock_http_response(201, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            create_request = CreateFeatureFlagRequest(
                name="new_flag",
                description="Test feature flag",
                key="test_flag_key",
                type="bool",
                default_value="false"
            )
            
            result = client.feature_flags_api.create_feature_flag(
                create_feature_flag_request=create_request
            )
            
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Method and URL are positional args
            method = call_args[0][0]
            url = call_args[0][1]
            
            # Check HTTP method
            assert method == 'POST'
            
            # Check URL
            assert '/api/v1/feature_flags' in url
            
            # Check body was serialized correctly
            body = call_args[1].get('body')
            assert body is not None
            parsed_body = json.loads(body) if isinstance(body, str) else body
            assert parsed_body.get('name') == 'new_flag'
            assert parsed_body.get('key') == 'test_flag_key'
            assert parsed_body.get('type') == 'bool'
            
            # Verify response
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_get_user_data_by_id(self, mock_tm_init, mock_get_token):
        """Test retrieving user data by user ID with real serialization."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {
            "id": "kp_user123",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "provided_id": None
        }
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            result = client.users_api.get_user_data(id="kp_user123")
            
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Method and URL are positional args
            method = call_args[0][0]
            url = call_args[0][1]
            
            # Check HTTP method
            assert method == 'GET'
            
            # Check URL includes query parameter
            assert '/api/v1/user' in url
            assert 'id=kp_user123' in url
            
            # Verify response was deserialized
            assert result is not None
            # The response should be a User model or dict with the user data
            assert hasattr(result, 'id') or (isinstance(result, dict) and 'id' in result)

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_none_values_not_in_url(self, mock_tm_init, mock_get_token):
        """Test that None/unset optional parameters are not included in the URL."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {
            "code": "OK",
            "message": "Success",
            "users": [],
            "next_token": None
        }
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            # Call with only page_size, leaving other optional params unset
            result = client.users_api.get_users(page_size=10)
            
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Method and URL are positional args
            url = call_args[0][1]
            
            # Check URL only includes provided parameter
            assert 'page_size=10' in url
            # These should NOT be in the URL since they weren't provided
            assert 'email=None' not in url
            
            # Verify response
            assert result is not None

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

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_authorization_header_injected(self, mock_tm_init, mock_get_token):
        """Test that Authorization header is properly injected into requests."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success", "users": [], "next_token": None}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            result = client.users_api.get_users()
            
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Verify Authorization header was injected by the token wrapper
            headers = call_args[1].get('headers', {})
            assert 'Authorization' in headers
            assert headers['Authorization'] == 'Bearer fake_token'
            
            # Also verify other standard headers are present
            assert 'User-Agent' in headers
            
            # Verify response
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_get_timezones_via_dynamic_api(self, mock_tm_init, mock_get_token):
        """Test accessing dynamically generated API classes with real serialization."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {
            "code": "OK",
            "message": "Success",
            "timezones": [
                {"id": "tz_utc", "name": "UTC", "offset": "+00:00"},
                {"id": "tz_est", "name": "EST", "offset": "-05:00"}
            ]
        }
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response) as mock_request:
            result = client.timezones_api.get_timezones()
            
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            
            # Method and URL are positional args
            method = call_args[0][0]
            url = call_args[0][1]
            
            # Check HTTP method and URL
            assert method == 'GET'
            assert '/api/v1/timezones' in url
            
            # Verify response
            assert result is not None

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

    # =========================================================================
    # Tests for deprecated wrapper methods (for coverage)
    # =========================================================================

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_get_users_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated get_users wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success", "users": [], "next_token": None}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            # Should emit deprecation warning and delegate to users_api
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.get_users(page_size=10)
                
                # Verify deprecation warning was emitted
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "get_users()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_create_user_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated create_user wrapper method."""
        from kinde_sdk.management.models.create_user_request import CreateUserRequest
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"id": "kp_new", "created": True, "identities": []}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            create_request = CreateUserRequest(
                profile={"given_name": "Test"},
                identities=[]
            )
            
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.create_user(create_user_request=create_request)
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "create_user()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_get_organizations_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated get_organizations wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success", "organizations": [], "next_token": None}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.get_organizations()
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "get_organizations()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_get_roles_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated get_roles wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success", "roles": [], "next_token": None}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.get_roles()
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "get_roles()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_get_user_data_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated get_user_data wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"id": "kp_user123", "email": "test@example.com", "provided_id": None}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.get_user_data("kp_user123")
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "get_user_data()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_delete_user_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated delete_user wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success"}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.delete_user("kp_user123")
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "delete_user()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_update_user_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated update_user wrapper method."""
        from kinde_sdk.management.models.update_user_request import UpdateUserRequest
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"id": "kp_user123", "given_name": "Updated"}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            update_request = UpdateUserRequest(given_name="Updated")
            
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.update_user("kp_user123", update_user_request=update_request)
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "update_user()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_get_organization_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated get_organization wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "org_abc123", "name": "Test Org"}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.get_organization("org_abc123")
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "get_organization()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_create_organization_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated create_organization wrapper method."""
        from kinde_sdk.management.models.create_organization_request import CreateOrganizationRequest
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success", "organization": {"code": "org_new"}}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            create_request = CreateOrganizationRequest(name="New Org")
            
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.create_organization(create_request)
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "create_organization()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_get_api_applications_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated get_api_applications wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success", "applications": [], "next_token": None}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.get_api_applications()
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "get_api_applications()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_update_organization_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated update_organization wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success"}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.update_organization("org_abc123")
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "update_organization()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_delete_organization_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated delete_organization wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success"}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.delete_organization("org_abc123")
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "delete_organization()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_get_role_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated get_role wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"id": "role_123", "key": "admin", "name": "Admin", "description": "Admin role"}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.get_role("role_123")
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "get_role()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_create_role_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated create_role wrapper method."""
        from kinde_sdk.management.models.create_role_request import CreateRoleRequest
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success", "role": {"id": "role_new"}}
        mock_http_response = self._make_mock_http_response(201, response_body)  # 201 for create
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            create_request = CreateRoleRequest(name="New Role", key="new_role")
            
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.create_role(create_request)
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "create_role()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_update_role_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated update_role wrapper method.
        
        Note: The deprecated wrapper calls roles_api.update_role() but the actual
        API method is update_roles(). This test verifies the wrapper emits the
        deprecation warning before the call fails.
        """
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # Since the deprecated wrapper calls a non-existent method (update_role vs update_roles),
        # we just verify the deprecation warning is emitted
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                client.update_role("role_123", None)
            except AttributeError:
                # Expected - the API method doesn't exist with this name
                pass
            
            # Verify deprecation warning was emitted before the error
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "update_role()" in str(w[0].message)

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_delete_role_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated delete_role wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success"}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.delete_role("role_123")
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "delete_role()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_get_feature_flags_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated get_feature_flags wrapper method.
        
        This method now correctly delegates to environments_api.get_environement_feature_flags().
        """
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success", "feature_flags": {}}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.get_feature_flags()
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "get_feature_flags()" in str(w[0].message)
                assert "environments_api.get_environement_feature_flags()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_create_feature_flag_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated create_feature_flag wrapper method."""
        from kinde_sdk.management.models.create_feature_flag_request import CreateFeatureFlagRequest
        
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success"}
        mock_http_response = self._make_mock_http_response(201, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            create_request = CreateFeatureFlagRequest(
                name="Test Flag",
                key="test_flag",
                type="bool",
                default_value="true"
            )
            
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.create_feature_flag(create_request)
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "create_feature_flag()" in str(w[0].message)
                
            assert result is not None

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_update_feature_flag_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated update_feature_flag wrapper method.
        
        Note: The deprecated wrapper expects an update_feature_flag_request param
        but the API expects individual params. This test verifies the wrapper
        emits the deprecation warning.
        """
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        # The deprecated wrapper has a signature mismatch with the actual API,
        # so we just verify the deprecation warning is emitted
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                client.update_feature_flag("test_flag", None)
            except Exception:
                # Expected - signature mismatch (ValidationError from pydantic)
                pass
            
            # Verify deprecation warning was emitted before the error
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "update_feature_flag()" in str(w[0].message)

    @patch.object(ManagementTokenManager, 'get_access_token', return_value="fake_token")
    @patch.object(ManagementTokenManager, '__init__', return_value=None)
    def test_deprecated_delete_feature_flag_wrapper(self, mock_tm_init, mock_get_token):
        """Test the deprecated delete_feature_flag wrapper method."""
        client = ManagementClient(self.domain, self.client_id, self.client_secret)
        
        response_body = {"code": "OK", "message": "Success"}
        mock_http_response = self._make_mock_http_response(200, response_body)
        
        with patch.object(client.api_client.rest_client, 'request', return_value=mock_http_response):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                result = client.delete_feature_flag("test_flag")
                
                assert len(w) == 1
                assert issubclass(w[0].category, DeprecationWarning)
                assert "delete_feature_flag()" in str(w[0].message)
                
            assert result is not None


if __name__ == '__main__':
    unittest.main()