"""
Client for the Kinde Management API.

This module provides a client for the Kinde Management API that integrates
with the existing Kinde SDK infrastructure.
"""

import logging
import os
import requests
from typing import Dict, Any, Optional, List, Union

from kinde_sdk.configuration import Configuration
from kinde_sdk.api_client import ApiClient
from .management_token_manager import ManagementTokenManager

logger = logging.getLogger("kinde_sdk.management")

class ManagementClient:
    """
    Client for the Kinde Management API.
    
    This client provides methods to interact with the Kinde Management API
    for managing users, organizations, roles, permissions, and feature flags.
    """
    
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
        self.configuration = Configuration(
            host=self.base_url,
        )
        self.api_client = ApiClient(configuration=self.configuration)
        
        # Set up automatic token handling
        self._setup_token_handling()
    
    def _setup_token_handling(self):
        """Set up automatic token refresh for API calls."""
        original_call_api = self.api_client.call_api
        
        def call_api_with_token(*args, **kwargs):
            # Get the current token and add it to the headers
            token = self.token_manager.get_access_token()
            
            # Add or update headers
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            
            if isinstance(kwargs['headers'], dict):
                kwargs['headers']['Authorization'] = f"Bearer {token}"
            else:
                # HTTPHeaderDict case
                kwargs['headers'].update({'Authorization': f"Bearer {token}"})
            
            return original_call_api(*args, **kwargs)
        
        self.api_client.call_api = call_api_with_token
    
    # Users API Methods
    def get_users(self, **kwargs) -> Dict[str, Any]:
        """
        Get a list of users.
        
        Args:
            **kwargs: Optional arguments to pass to the API.
                sort (str): Sort users by field. (Optional)
                page_size (int): Number of results per page. (Optional)
                next_token (str): Token for the next page of results. (Optional)
                
        Returns:
            Dict containing users data.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = "/users"
        method = "GET"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            query_params=params
        )
        
        return response
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get a user by ID.
        
        Args:
            user_id: The ID of the user to get.
            
        Returns:
            Dict containing user data.
        """
        resource_path = f"/users/{user_id}"
        method = "GET"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None
        )
        
        return response
    
    def create_user(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            **kwargs: User data.
                first_name (str): User's first name. (Optional)
                last_name (str): User's last name. (Optional)
                email (str): User's email address.
                is_suspended (bool): Whether the user is suspended. (Optional)
                
        Returns:
            Dict containing the created user.
        """
        data = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = "/users"
        method = "POST"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            body=data
        )
        
        return response
    
    def update_user(self, user_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update a user.
        
        Args:
            user_id: The ID of the user to update.
            **kwargs: User data to update.
                first_name (str): User's first name. (Optional)
                last_name (str): User's last name. (Optional)
                is_suspended (bool): Whether the user is suspended. (Optional)
                
        Returns:
            Dict containing the updated user.
        """
        data = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = f"/users/{user_id}"
        method = "PATCH"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            body=data
        )
        
        return response
    
    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """
        Delete a user.
        
        Args:
            user_id: The ID of the user to delete.
            
        Returns:
            Dict containing the result.
        """
        resource_path = f"/users/{user_id}"
        method = "DELETE"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None
        )
        
        return response
    
    # Organizations API Methods
    def get_organizations(self, **kwargs) -> Dict[str, Any]:
        """
        Get a list of organizations.
        
        Args:
            **kwargs: Optional arguments to pass to the API.
                sort (str): Sort organizations by field. (Optional)
                page_size (int): Number of results per page. (Optional)
                next_token (str): Token for the next page of results. (Optional)
                
        Returns:
            Dict containing organizations data.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = "/organizations"
        method = "GET"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            query_params=params
        )
        
        return response
    
    def get_organization(self, org_code: str) -> Dict[str, Any]:
        """
        Get an organization by code.
        
        Args:
            org_code: The code of the organization to get.
            
        Returns:
            Dict containing organization data.
        """
        resource_path = f"/organizations/{org_code}"
        method = "GET"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None
        )
        
        return response
    
    def create_organization(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new organization.
        
        Args:
            **kwargs: Organization data.
                name (str): Organization name.
                feature_flags (List[Dict]): Feature flags for the organization. (Optional)
                
        Returns:
            Dict containing the created organization.
        """
        data = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = "/organizations"
        method = "POST"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            body=data
        )
        
        return response
    
    def update_organization(self, org_code: str, **kwargs) -> Dict[str, Any]:
        """
        Update an organization.
        
        Args:
            org_code: The code of the organization to update.
            **kwargs: Organization data to update.
                name (str): Organization name. (Optional)
                is_suspended (bool): Whether the organization is suspended. (Optional)
                
        Returns:
            Dict containing the updated organization.
        """
        data = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = f"/organizations/{org_code}"
        method = "PATCH"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            body=data
        )
        
        return response
    
    def delete_organization(self, org_code: str) -> Dict[str, Any]:
        """
        Delete an organization.
        
        Args:
            org_code: The code of the organization to delete.
            
        Returns:
            Dict containing the result.
        """
        resource_path = f"/organizations/{org_code}"
        method = "DELETE"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None
        )
        
        return response
    
    # Roles API Methods
    def get_roles(self, **kwargs) -> Dict[str, Any]:
        """
        Get a list of roles.
        
        Args:
            **kwargs: Optional arguments to pass to the API.
                sort (str): Sort roles by field. (Optional)
                page_size (int): Number of results per page. (Optional)
                next_token (str): Token for the next page of results. (Optional)
                
        Returns:
            Dict containing roles data.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = "/roles"
        method = "GET"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            query_params=params
        )
        
        return response
    
    def get_role(self, role_id: str) -> Dict[str, Any]:
        """
        Get a role by ID.
        
        Args:
            role_id: The ID of the role to get.
            
        Returns:
            Dict containing role data.
        """
        resource_path = f"/roles/{role_id}"
        method = "GET"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None
        )
        
        return response
    
    def create_role(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new role.
        
        Args:
            **kwargs: Role data.
                name (str): Role name.
                description (str): Role description. (Optional)
                key (str): Role key. (Optional)
                is_default_role (bool): Whether this is a default role. (Optional)
                permissions (List[str]): List of permission IDs. (Optional)
                
        Returns:
            Dict containing the created role.
        """
        data = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = "/roles"
        method = "POST"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            body=data
        )
        
        return response
    
    def update_role(self, role_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update a role.
        
        Args:
            role_id: The ID of the role to update.
            **kwargs: Role data to update.
                name (str): Role name. (Optional)
                description (str): Role description. (Optional)
                
        Returns:
            Dict containing the updated role.
        """
        data = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = f"/roles/{role_id}"
        method = "PATCH"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            body=data
        )
        
        return response
    
    def delete_role(self, role_id: str) -> Dict[str, Any]:
        """
        Delete a role.
        
        Args:
            role_id: The ID of the role to delete.
            
        Returns:
            Dict containing the result.
        """
        resource_path = f"/roles/{role_id}"
        method = "DELETE"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None
        )
        
        return response
    
    # Feature Flags API Methods
    def get_feature_flags(self, **kwargs) -> Dict[str, Any]:
        """
        Get a list of feature flags.
        
        Args:
            **kwargs: Optional arguments to pass to the API.
                sort (str): Sort feature flags by field. (Optional)
                page_size (int): Number of results per page. (Optional)
                next_token (str): Token for the next page of results. (Optional)
                
        Returns:
            Dict containing feature flags data.
        """
        params = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = "/feature_flags"
        method = "GET"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            query_params=params
        )
        
        return response
    
    def create_feature_flag(self, **kwargs) -> Dict[str, Any]:
        """
        Create a new feature flag.
        
        Args:
            **kwargs: Feature flag data.
                name (str): Feature flag name.
                description (str): Feature flag description. (Optional)
                key (str): Feature flag key.
                type (str): Feature flag type (boolean, string, integer, number).
                default_value (Any): Default value for the feature flag. (Optional)
                
        Returns:
            Dict containing the created feature flag.
        """
        data = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = "/feature_flags"
        method = "POST"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            body=data
        )
        
        return response
    
    def update_feature_flag(self, feature_flag_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update a feature flag.
        
        Args:
            feature_flag_id: The ID of the feature flag to update.
            **kwargs: Feature flag data to update.
                name (str): Feature flag name. (Optional)
                description (str): Feature flag description. (Optional)
                default_value (Any): Default value for the feature flag. (Optional)
                
        Returns:
            Dict containing the updated feature flag.
        """
        data = {k: v for k, v in kwargs.items() if v is not None}
        resource_path = f"/feature_flags/{feature_flag_id}"
        method = "PATCH"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None,
            body=data
        )
        
        return response
    
    def delete_feature_flag(self, feature_flag_id: str) -> Dict[str, Any]:
        """
        Delete a feature flag.
        
        Args:
            feature_flag_id: The ID of the feature flag to delete.
            
        Returns:
            Dict containing the result.
        """
        resource_path = f"/feature_flags/{feature_flag_id}"
        method = "DELETE"
        
        response = self.api_client.call_api(
            resource_path,
            method,
            auth_settings=['kindeBearerAuth'],
            _return_http_data_only=True,
            _preload_content=True,
            _request_timeout=None
        )
        
        return response