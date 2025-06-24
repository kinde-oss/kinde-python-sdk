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
            'list': ('GET', '/users'),
            'get': ('GET', '/users/{user_id}'),
            'create': ('POST', '/users'),
            'update': ('PATCH', '/users/{user_id}'),
            'delete': ('DELETE', '/users/{user_id}'),
        },
        
        # Organizations API
        'organizations': {
            'list': ('GET', '/organizations'),
            'get': ('GET', '/organizations/{org_code}'),
            'create': ('POST', '/organizations'),
            'update': ('PATCH', '/organizations/{org_code}'),
            'delete': ('DELETE', '/organizations/{org_code}'),
        },
        
        # Roles API
        'roles': {
            'list': ('GET', '/roles'),
            'get': ('GET', '/roles/{role_id}'),
            'create': ('POST', '/roles'),
            'update': ('PATCH', '/roles/{role_id}'),
            'delete': ('DELETE', '/roles/{role_id}'),
        },

        # Permissions API
        'permissions': {
            'list': ('GET', '/permissions'),
            'get': ('GET', '/permissions/{permission_id}'),
            'create': ('POST', '/permissions'),
            'update': ('PATCH', '/permissions/{permission_id}'),
            'delete': ('DELETE', '/permissions/{permission_id}'),
        },
        
        # Feature Flags API
        'feature_flags': {
            'list': ('GET', '/feature_flags'),
            'get': ('GET', '/feature_flags/{feature_flag_id}'),
            'create': ('POST', '/feature_flags'),
            'update': ('PATCH', '/feature_flags/{feature_flag_id}'),
            'delete': ('DELETE', '/feature_flags/{feature_flag_id}'),
        },

        # Connected Apps API
        'connected_apps': {
            'list': ('GET', '/connected_apps'),
            'get': ('GET', '/connected_apps/{app_id}'),
        },

        # API Applications API
        'api_applications': {
            'list': ('GET', '/api/applications'),
            'get': ('GET', '/api/applications/{app_id}'),
            'create': ('POST', '/api/applications'),
            'update': ('PATCH', '/api/applications/{app_id}'),
            'delete': ('DELETE', '/api/applications/{app_id}'),
        },

        # Subscribers API
        'subscribers': {
            'list': ('GET', '/subscribers'),
            'get': ('GET', '/subscribers/{subscriber_id}'),
        },

        # Timezones API
        'timezones': {
            'list': ('GET', '/timezones'),
        },

        # Industries API
        'industries': {
            'list': ('GET', '/industries'),
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
            resource_singular = resource[:-1] if resource.endswith('s') else resource
            
            for action, (method, path) in endpoints.items():
                # Create method name based on action and resource
                if action == 'list':
                    method_name = f"get_{resource}"
                elif action == 'get':
                    method_name = f"get_{resource_singular}"
                else:
                    method_name = f"{action}_{resource_singular}"
                
                # Create the method
                api_method = self._create_api_method(method, path, resource, action)
                
                # Set the method on the class
                setattr(self, method_name, api_method)
    
    def _create_api_method(self, http_method: str, path: str, resource: str, action: str) -> Callable:
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
            
            # Handle query params or body data based on HTTP method
            query_params = None
            body = None
            
            if http_method in ('GET', 'DELETE'):
                query_params = {k: v for k, v in kwargs.items() if v is not None}
            else:
                body = {k: v for k, v in kwargs.items() if v is not None}
            
            # FIXED: Use param_serialize to properly construct the full URL with host
            # Handle query parameters by appending them to the path
            final_path = formatted_path
            if query_params and http_method in ('GET', 'DELETE'):
                query_string = '&'.join([f"{k}={v}" for k, v in query_params.items() if v is not None])
                if query_string:
                    separator = '&' if '?' in final_path else '?'
                    final_path = f"{final_path}{separator}{query_string}"
            
            # Use param_serialize to get the proper URL with host
            method, url, header_params, body, post_params = self.api_client.param_serialize(
                method=http_method,
                resource_path=formatted_path,  # Use original path, not with query params
                query_params=query_params if http_method in ('GET', 'DELETE') else None,
                header_params={},
                body=body if http_method not in ('GET', 'DELETE') else None
            )
            
            # Add the authorization token to headers
            token = self.token_manager.get_access_token()
            header_params['Authorization'] = f"Bearer {token}"
            
            # Call the REST client directly with the constructed URL
            response = self.api_client.rest_client.request(
                method=http_method,
                url=url,
                headers=header_params,
                body=body if http_method not in ('GET', 'DELETE') else None,
                post_params=post_params,
                _request_timeout=None
            )
            
            # Use the API client's response_deserialize to properly handle the response
            # First read the response data
            response.read()
            
            # Then deserialize it
            api_response = self.api_client.response_deserialize(response, {})
            
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