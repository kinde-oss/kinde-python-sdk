"""
Client for the Kinde Management API.

This module provides a client for the Kinde Management API that integrates
with the existing Kinde SDK infrastructure.
"""

import logging
from typing import Dict, Any, Optional, List, Union, Callable
from functools import partial

from kinde_sdk.management.configuration import Configuration
from kinde_sdk.management.api_client import ApiClient
from .management_token_manager import ManagementTokenManager

logger = logging.getLogger("kinde_sdk.management")

class ManagementClient:
    """
    Client for the Kinde Management API.
    
    This client provides methods to interact with the Kinde Management API
    for managing users, organizations, roles, permissions, and feature flags.
    """
    
    # Define API endpoints and their methods
    API_ENDPOINTS = {
        # Users API
        'users': {
            'list': ('GET', '/api/v1/users'),
            'get': ('GET', '/api/v1/user'),
            'create': ('POST', '/api/v1/user'),
            'update': ('PATCH', '/api/v1/user', ['id']),
            'delete': ('DELETE', '/api/v1/user'),
        },
        
        # Organizations API
        'organizations': {
            'list': ('GET', '/api/v1/organizations'),
            'get': ('GET', '/api/v1/organization/{org_code}'),
            'create': ('POST', '/api/v1/organization'),
            'update': ('PATCH', '/api/v1/organization/{org_code}'),
            'delete': ('DELETE', '/api/v1/organization/{org_code}'),
        },
        
        # Organization Users API
        'organization_users': {
            'list': ('GET', '/api/v1/organizations/{org_code}/users'),
            'add': ('POST', '/api/v1/organizations/{org_code}/users'),
            'update': ('PATCH', '/api/v1/organizations/{org_code}/users'),
            'remove': ('DELETE', '/api/v1/organizations/{org_code}/users/{user_id}'),
        },
        
        # Organization User Roles API
        'organization_user_roles': {
            'list': ('GET', '/api/v1/organizations/{org_code}/users/{user_id}/roles'),
            'add': ('POST', '/api/v1/organizations/{org_code}/users/{user_id}/roles'),
            'remove': ('DELETE', '/api/v1/organizations/{org_code}/users/{user_id}/roles/{role_id}'),
        },
        
        # Organization User Permissions API
        'organization_user_permissions': {
            'list': ('GET', '/api/v1/organizations/{org_code}/users/{user_id}/permissions'),
            'add': ('POST', '/api/v1/organizations/{org_code}/users/{user_id}/permissions'),
            'remove': ('DELETE', '/api/v1/organizations/{org_code}/users/{user_id}/permissions/{permission_id}'),
        },
        
        # Roles API
        'roles': {
            'list': ('GET', '/api/v1/roles'),
            'get': ('GET', '/api/v1/roles/{role_id}'),
            'create': ('POST', '/api/v1/roles'),
            'update': ('PATCH', '/api/v1/roles/{role_id}'),
            'delete': ('DELETE', '/api/v1/roles/{role_id}'),
        },

        # Permissions API
        'permissions': {
            'list': ('GET', '/api/v1/permissions'),
            'create': ('POST', '/api/v1/permissions'),
            'update': ('PATCH', '/api/v1/permissions/{permission_id}'),
            'delete': ('DELETE', '/api/v1/permissions/{permission_id}'),
        },
        
        # Feature Flags API
        'feature_flags': {
            'create': ('POST', '/api/v1/feature_flags'),
            'update': ('PUT', '/api/v1/feature_flags/{feature_flag_key}'),
            'delete': ('DELETE', '/api/v1/feature_flags/{feature_flag_key}'),
        },

        # Connected Apps API
        'connected_apps': {
            'list': ('GET', '/api/v1/applications'),
            'get': ('GET', '/api/v1/applications/{application_id}'),
            'create': ('POST', '/api/v1/applications'),
            'update': ('PATCH', '/api/v1/applications/{application_id}'),
            'delete': ('DELETE', '/api/v1/applications/{application_id}'),
        },

        # API Applications API
        'api_applications': {
            'list': ('GET', '/api/v1/apis'),
            'get': ('GET', '/api/v1/apis/{api_id}'),
            'create': ('POST', '/api/v1/apis'),
            'delete': ('DELETE', '/api/v1/apis/{api_id}'),
        },

        # Subscribers API
        'subscribers': {
            'list': ('GET', '/api/v1/subscribers'),
            'get': ('GET', '/api/v1/subscribers/{subscriber_id}'),
            'create': ('POST', '/api/v1/subscribers'),
        },

        # Timezones API
        'timezones': {
            'list': ('GET', '/api/v1/timezones'),
        },

        # Industries API
        'industries': {
            'list': ('GET', '/api/v1/industries'),
        },
        
        # Properties API
        'properties': {
            'list': ('GET', '/api/v1/properties'),
            'create': ('POST', '/api/v1/properties'),
            'update': ('PUT', '/api/v1/properties/{property_id}'),
            'delete': ('DELETE', '/api/v1/properties/{property_id}'),
        },
        
        # User Properties API
        'user_properties': {
            'list': ('GET', '/api/v1/users/{user_id}/properties'),
            'update': ('PUT', '/api/v1/users/{user_id}/properties/{property_key}'),
        },
        
        # Organization Properties API
        'organization_properties': {
            'list': ('GET', '/api/v1/organizations/{org_code}/properties'),
            'update': ('PUT', '/api/v1/organizations/{org_code}/properties/{property_key}'),
        },
        
        # Webhooks API
        'webhooks': {
            'list': ('GET', '/api/v1/webhooks'),
            'create': ('POST', '/api/v1/webhooks'),
            'update': ('PATCH', '/api/v1/webhooks/{webhook_id}'),
            'delete': ('DELETE', '/api/v1/webhooks/{webhook_id}'),
        },
        
        # Events API
        'events': {
            'get': ('GET', '/api/v1/events/{event_id}'),
        },
        
        # Event Types API
        'event_types': {
            'list': ('GET', '/api/v1/event_types'),
        },
        
        # Connections API
        'connections': {
            'list': ('GET', '/api/v1/connections'),
            'get': ('GET', '/api/v1/connections/{connection_id}'),
            'create': ('POST', '/api/v1/connections'),
            'update': ('PATCH', '/api/v1/connections/{connection_id}'),
            'delete': ('DELETE', '/api/v1/connections/{connection_id}'),
        },
        
        # Business API
        'business': {
            'get': ('GET', '/api/v1/business'),
            'update': ('PATCH', '/api/v1/business'),
        },
        
        # Environment Feature Flags API
        'environment_feature_flags': {
            'list': ('GET', '/api/v1/environment/feature_flags'),
            'update': ('PATCH', '/api/v1/environment/feature_flags/{feature_flag_key}'),
            'delete': ('DELETE', '/api/v1/environment/feature_flags/{feature_flag_key}'),
        },
        
        # Organization Feature Flags API
        'organization_feature_flags': {
            'list': ('GET', '/api/v1/organizations/{org_code}/feature_flags'),
            'update': ('PATCH', '/api/v1/organizations/{org_code}/feature_flags/{feature_flag_key}'),
            'delete': ('DELETE', '/api/v1/organizations/{org_code}/feature_flags/{feature_flag_key}'),
        },
        
        # User Feature Flags API
        'user_feature_flags': {
            'update': ('PATCH', '/api/v1/users/{user_id}/feature_flags/{feature_flag_key}'),
        },
        
        # User Password API
        'user_password': {
            'update': ('PUT', '/api/v1/users/{user_id}/password'),
        },
        
        # User Refresh Claims API
        'user_refresh_claims': {
            'refresh': ('POST', '/api/v1/users/{user_id}/refresh_claims'),
        },
        'user_identities': {
            'list': ('GET', '/api/v1/users/{user_id}/identities'),
            'create': ('POST', '/api/v1/users/{user_id}/identities'),
        },
        'identities': {
            'get': ('GET', '/api/v1/identities/{identity_id}'),
            'update': ('PATCH', '/api/v1/identities/{identity_id}'),
            'delete': ('DELETE', '/api/v1/identities/{identity_id}'),
        },
    }
    
    # Define response types for each endpoint
    RESPONSE_TYPES = {
        'users': {
            'list': {'200': 'UsersResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'get': {'200': 'User', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'200': 'CreateUserResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'UpdateUserResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'organizations': {
            'list': {'200': 'GetOrganizationsResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'get': {'200': 'GetOrganizationResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'200': 'CreateOrganizationResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'organization_users': {
            'list': {'200': 'GetOrganizationUsersResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'add': {'200': 'AddOrganizationUsersResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'UpdateOrganizationUsersResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'remove': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'organization_user_roles': {
            'list': {'200': 'GetOrganizationsUserRolesResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'add': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'remove': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'organization_user_permissions': {
            'list': {'200': 'GetOrganizationsUserPermissionsResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'add': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'remove': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'roles': {
            'list': {'200': 'GetRolesResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'get': {'200': 'GetRoleResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'201': 'CreateRolesResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'201': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'permissions': {
            'list': {'200': 'GetPermissionsResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'201': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'feature_flags': {
            'create': {'201': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'subscribers': {
            'list': {'200': 'GetSubscribersResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'get': {'200': 'GetSubscriberResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'201': 'CreateSubscriberSuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'api_applications': {
            'list': {'200': 'GetApisResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'get': {'200': 'GetApiResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'200': 'CreateApisResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'connected_apps': {
            'list': {'200': 'GetApplicationsResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'get': {'200': 'GetApplicationResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'201': 'CreateApplicationResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'timezones': {
            'list': {'200': 'GetTimezonesResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'industries': {
            'list': {'200': 'GetIndustriesResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'properties': {
            'list': {'200': 'GetPropertiesResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'201': 'CreatePropertyResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'user_properties': {
            'list': {'200': 'GetPropertyValuesResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'organization_properties': {
            'list': {'200': 'GetPropertyValuesResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'webhooks': {
            'list': {'200': 'GetWebhooksResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'200': 'CreateWebhookResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'UpdateWebhookResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'events': {
            'get': {'200': 'GetEventResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'event_types': {
            'list': {'200': 'GetEventTypesResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'connections': {
            'list': {'200': 'GetConnectionsResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'get': {'200': 'Connection', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'201': 'CreateConnectionResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'business': {
            'get': {'200': 'GetBusinessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'environment_feature_flags': {
            'list': {'200': 'GetEnvironmentFeatureFlagsResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'organization_feature_flags': {
            'list': {'200': 'GetOrganizationFeatureFlagsResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'user_feature_flags': {
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'user_password': {
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'user_refresh_claims': {
            'refresh': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '404': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'user_identities': {
            'list': {'200': 'GetIdentitiesResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'create': {'201': 'CreateIdentityResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
        },
        'identities': {
            'get': {'200': 'Identity', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'update': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
            'delete': {'200': 'SuccessResponse', '400': 'ErrorResponse', '403': 'ErrorResponse', '429': 'ErrorResponse'},
        },
    }
    
    def __init__(self, domain: str, client_id: str, client_secret: str):
        """
        Initialize the management client.
        
        Args:
            domain: Your Kinde domain (e.g., "example.kinde.com")
            client_id: Client ID for the management API
            client_secret: Client secret for the management API
        """
        self.domain = domain
        self.base_url = f"https://{domain}/api/v1"
        self.token_manager = ManagementTokenManager(domain, client_id, client_secret)
        
        # Initialize API client with the correct configuration
        self.configuration = Configuration(host=self.base_url)
        self.api_client = ApiClient(configuration=self.configuration)
        
        # Set up automatic token handling
        self._setup_token_handling()
        
        # Generate dynamic methods
        self._generate_methods()
    
    def _setup_token_handling(self):
        """Set up automatic token refresh for API calls."""
        # Token will be added directly in the API method since we're calling REST client directly
        pass
    
    def _generate_methods(self):
        """Generate dynamic methods for each API endpoint."""
        for resource, endpoints in self.API_ENDPOINTS.items():
            # Handle special cases for singularization
            if resource == 'business':
                resource_singular = 'business'  # Don't remove 's' from 'business'
            else:
                resource_singular = resource[:-1] if resource.endswith('s') else resource
            
            for action, endpoint in endpoints.items():
                if len(endpoint) == 3:
                    method, path, query_keys = endpoint
                else:
                    method, path = endpoint
                    query_keys = ()

                # Create method name based on action and resource
                if action == 'list':
                    method_name = f"get_{resource}"
                elif action == 'get':
                    method_name = f"get_{resource_singular}"
                else:
                    method_name = f"{action}_{resource_singular}"
                
                # Create the method
                api_method = self._create_api_method(method, path, resource, action, query_keys)
                
                # Set the method on the class
                setattr(self, method_name, api_method)
    
    def _create_api_method(self, http_method: str, path: str, resource: str, action: str, query_keys=()) -> Callable:
        """
        Create a dynamic method for an API endpoint.
        
        Args:
            http_method: HTTP method (GET, POST, etc.)
            path: API endpoint path
            resource: API resource name (users, organizations, etc.)
            action: API action (list, get, create, etc.)
            
        Returns:
            A callable method that makes the API request
        """
        # Handle special cases for singularization
        if resource == 'business':
            resource_singular = 'business'  # Don't remove 's' from 'business'
        else:
            resource_singular = resource[:-1] if resource.endswith('s') else resource

        def api_method(*args, **kwargs) -> Dict[str, Any]:
            # Format path with any path parameters from args
            formatted_path = path
            if '{' in path and args:
                param_values = list(args)
                while '{' in formatted_path and param_values:
                    start_idx = formatted_path.find('{')
                    end_idx = formatted_path.find('}')
                    if start_idx >= 0 and end_idx >= 0:
                        formatted_path = formatted_path[:start_idx] + str(param_values.pop(0)) + formatted_path[end_idx + 1:]
            
            # Handle query/body split
            if http_method in ('GET', 'DELETE'):
                query_params = {k: v for k, v in kwargs.items() if v is not None}
                payload = None
            else:
                # Lift ONLY declared query_keys into the query string
                qset = set(query_keys or ())
                query_params = {k: kwargs.pop(k) for k in list(kwargs) if k in qset and kwargs[k] is not None}
                # Remaining kwargs go to JSON body
                payload = {k: v for k, v in kwargs.items() if v is not None}

            # FIXED: Use param_serialize to properly construct the full URL with host
            # Handle query parameters by appending them to the path
            final_path = formatted_path
            if query_params and http_method in ('GET', 'DELETE'):
                query_string = '&'.join([f"{k}={v}" for k, v in query_params.items() if v is not None])
                if query_string:
                    separator = '&' if '?' in final_path else '?'
                    final_path = f"{final_path}{separator}{query_string}"
            
            # Use param_serialize to get the proper URL with host
            # Remove /api/v1 prefix from resource_path since host already includes it
            resource_path_for_serialize = formatted_path.replace('/api/v1', '', 1)
            
            method, url, header_params, serialized_body, post_params = self.api_client.param_serialize(
                method=http_method,
                resource_path=resource_path_for_serialize,  # Use path without /api/v1 prefix
                query_params=query_params or None,
                header_params={},
                body=payload if http_method not in ('GET', 'DELETE') else None
            )

            # Ensure required headers for PATCH/POST/PUT
            if http_method not in ('GET', 'DELETE'):
                header_params.setdefault('Content-Type', 'application/json')
                header_params.setdefault('Accept', 'application/json')

            # Add the authorization token to headers
            token = self.token_manager.get_access_token()
            header_params['Authorization'] = f"Bearer {token}"

            # Call the REST client directly with the constructed URL
            response = self.api_client.rest_client.request(
                method=http_method,
                url=url,
                headers=header_params,
                body=serialized_body if http_method not in ('GET', 'DELETE') else None,
                post_params=post_params,
                _request_timeout=None
            )

            # Use the API client's response_deserialize to properly handle the response
            # First read the response data
            response.read()
            
            # Then deserialize it
            api_response = self.api_client.response_deserialize(response, self.RESPONSE_TYPES[resource][action])
            
            return api_response.data
        
        # Add docstring to the method based on the action and resource
        if action == 'list':
            docstring = f"""
            Get a list of {resource}.
            
            Args:
                **kwargs: Optional arguments to pass to the API.
                    sort (str): Sort {resource} by field. (Optional)
                    page_size (int): Number of results per page. (Optional)
                    next_token (str): Token for the next page of results. (Optional)
                    
            Returns:
                Dict containing {resource} data.
            """
        elif action == 'get':
            param_name = path.split('{')[-1].split('}')[0] if '{' in path else f"{resource_singular}_id"
            docstring = f"""
            Get a {resource_singular} by ID.
            
            Args:
                {param_name}: The ID of the {resource_singular} to get.
                
            Returns:
                Dict containing {resource_singular} data.
            """
        elif action == 'create':
            docstring = f"""
            Create a new {resource_singular}.
            
            Args:
                **kwargs: {resource_singular.capitalize()} data to create.
                
            Returns:
                Dict containing the created {resource_singular}.
            """
        elif action == 'update':
            param_name = path.split('{')[-1].split('}')[0] if '{' in path else f"{resource_singular}_id"
            docstring = f"""
            Update a {resource_singular}.
            
            Args:
                {param_name}: The ID of the {resource_singular} to update.
                **kwargs: {resource_singular.capitalize()} data to update.
                
            Returns:
                Dict containing the updated {resource_singular}.
            """
        elif action == 'delete':
            param_name = path.split('{')[-1].split('}')[0] if '{' in path else f"{resource_singular}_id"
            docstring = f"""
            Delete a {resource_singular}.
            
            Args:
                {param_name}: The ID of the {resource_singular} to delete.
                
            Returns:
                Dict containing the result.
            """
        else:
            docstring = f"""
            {action.capitalize()} {resource}.
            
            Args:
                *args: Positional arguments for path parameters.
                **kwargs: Additional arguments for the API.
                
            Returns:
                Dict containing the API response.
            """
        
        api_method.__doc__ = docstring
        return api_method

# Add backwards compatibility methods for common operations
# These will be deprecated in future versions
for method_name, new_name in [
    ('get_users', 'get_users'),
    ('get_user', 'get_user'),
    ('create_user', 'create_user'),
    ('update_user', 'update_user'),
    ('delete_user', 'delete_user'),
    ('get_organizations', 'get_organizations'),
    ('get_organization', 'get_organization'),
    ('create_organization', 'create_organization'),
    ('update_organization', 'update_organization'),
    ('delete_organization', 'delete_organization'),
    ('get_roles', 'get_roles'),
    ('get_role', 'get_role'),
    ('create_role', 'create_role'),
    ('update_role', 'update_role'),
    ('delete_role', 'delete_role'),
    ('get_feature_flags', 'get_feature_flags'),
    ('create_feature_flag', 'create_feature_flag'),
    ('update_feature_flag', 'update_feature_flag'),
    ('delete_feature_flag', 'delete_feature_flag'),
]:
    pass  # These methods will be created dynamically