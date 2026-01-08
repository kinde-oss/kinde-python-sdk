"""
Client for the Kinde Management API.

This module provides a client for the Kinde Management API that integrates
with the existing Kinde SDK infrastructure and adds automatic token management
to the generated API classes.
"""

import logging
import inspect
import re
import warnings
from typing import Dict, Any, Optional

from kinde_sdk.management.configuration import Configuration
from kinde_sdk.management.api_client import ApiClient
from .management_token_manager import ManagementTokenManager

# Import the api module to dynamically load all API classes
from kinde_sdk.management import api

logger = logging.getLogger("kinde_sdk.management")


class ManagementClient:
    """
    Client for the Kinde Management API.
    
    This client provides access to all Kinde Management API endpoints through
    the auto-generated API classes, with automatic token management.
    
    All API classes are dynamically loaded from the 'api' module and made available
    as snake_case properties. For example:
    - UsersApi -> client.users.*
    - OrganizationsApi -> client.organizations.*
    - FeatureFlagsApi -> client.feature_flags.*
    - etc.
    
    When new API classes are generated from the OpenAPI spec, they will automatically
    be available on this client without any code changes.
    
    Common API properties include:
    - client.users.*           - User management
    - client.organizations.*   - Organization management
    - client.roles.*           - Role management
    - client.permissions.*     - Permission management
    - client.feature_flags.*   - Feature flag management
    - client.apis.*            - API application management
    - client.applications.*    - Connected app management
    - client.subscribers.*     - Subscriber management
    - client.properties.*      - Property management
    - client.webhooks.*        - Webhook management
    - client.connections.*     - Connection management
    - client.business.*        - Business information
    - And more...
    
    Example:
        ```python
        client = ManagementClient(domain, client_id, client_secret)
        
        # Get all users
        users = client.users.get_users(page_size=50)
        
        # Create a user
        new_user = client.users.create_user(
            create_user_request={'email': 'user@example.com'}
        )
        
        # Get organizations
        orgs = client.organizations.get_organizations()
        
        # Access any dynamically loaded API
        billing = client.billing.get_billing_info()
        ```
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
        self.base_url = f"https://{domain}"
        self.token_manager = ManagementTokenManager(domain, client_id, client_secret)
        
        # Initialize API client with the correct configuration
        self.configuration = Configuration(host=self.base_url)
        self.api_client = ApiClient(configuration=self.configuration)
        
        # Set up automatic token injection
        self._setup_token_handling()
        
        # Dynamically initialize all API classes from the api module
        self._initialize_api_classes()
    
    def _setup_token_handling(self):
        """
        Set up automatic token injection for all API calls.
        
        This modifies the API client to automatically add the Bearer token
        to all outgoing requests.
        """
        original_call_api = self.api_client.call_api
        
        def call_api_with_token(*args, **kwargs):
            """Wrapper that adds authentication token to all API calls."""
            # Get the access token
            token = self.token_manager.get_access_token()
            
            # Inject the token into headers
            if 'header_params' not in kwargs:
                kwargs['header_params'] = {}
            kwargs['header_params']['Authorization'] = f"Bearer {token}"
            
            # Call the original method
            return original_call_api(*args, **kwargs)
        
        # Replace the call_api method
        self.api_client.call_api = call_api_with_token
    
    def _initialize_api_classes(self):
        """
        Dynamically initialize all API classes from the api module.
        
        This method inspects the api module and creates an instance of each
        API class (classes ending with 'Api'), making them available as
        snake_case attributes on this client.
        
        For example:
        - UsersApi -> self.users
        - OrganizationsApi -> self.organizations
        - FeatureFlagsApi -> self.feature_flags
        """
        # Get all members of the api module
        for name, obj in inspect.getmembers(api):
            # Check if it's a class and ends with 'Api'
            if inspect.isclass(obj) and name.endswith('Api'):
                # Convert class name to snake_case attribute name
                # e.g., UsersApi -> users, FeatureFlagsApi -> feature_flags
                attr_name = self._class_name_to_snake_case(name)
                
                # Initialize the API class with our configured api_client
                api_instance = obj(api_client=self.api_client)
                
                # Set it as an attribute on this client
                setattr(self, attr_name, api_instance)
                
                logger.debug(f"Initialized {name} as client.{attr_name}")
    
    @staticmethod
    def _class_name_to_snake_case(class_name: str) -> str:
        """
        Convert a class name to snake_case attribute name.
        
        Examples:
        - UsersApi -> users
        - FeatureFlagsApi -> feature_flags
        - APIsApi -> apis
        - MFAApi -> mfa
        
        Args:
            class_name: The class name (e.g., 'UsersApi')
            
        Returns:
            Snake case attribute name (e.g., 'users')
        """
        # Remove the 'Api' suffix
        name = class_name[:-3] if class_name.endswith('Api') else class_name
        
        # Insert underscores before uppercase letters (except at the start)
        # and convert to lowercase
        snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        
        return snake_case
    
    # Backwards compatibility: Provide direct method access for common operations
    # These delegate to the appropriate API class methods
    # Note: These methods are deprecated. For full functionality and proper type hints,
    # use the API class methods directly (e.g., client.users.get_users())
    
    def get_users(self, **kwargs):
        """
        Get users.
        
        .. deprecated::
            Use :meth:`client.users.get_users()` instead.
        
        For full documentation and parameters, see UsersApi.get_users()
        """
        warnings.warn(
            "get_users() is deprecated. Use client.users.get_users() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.users.get_users(**kwargs)
    
    def get_user_data(self, user_id: str):
        """
        Get user data by ID.
        
        .. deprecated::
            Use :meth:`client.users.get_user_data()` instead.
        
        For full documentation and parameters, see UsersApi.get_user_data()
        """
        warnings.warn(
            "get_user_data() is deprecated. Use client.users.get_user_data() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.users.get_user_data(user_id=user_id)
    
    def create_user(self, create_user_request=None, **kwargs):
        """
        Create a user.
        
        .. deprecated::
            Use :meth:`client.users.create_user()` instead.
        
        For full documentation and parameters, see UsersApi.create_user()
        """
        warnings.warn(
            "create_user() is deprecated. Use client.users.create_user() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.users.create_user(create_user_request=create_user_request, **kwargs)
    
    def update_user(self, id: str, update_user_request, **kwargs):
        """
        Update a user.
        
        .. deprecated::
            Use :meth:`client.users.update_user()` instead.
        
        For full documentation and parameters, see UsersApi.update_user()
        """
        warnings.warn(
            "update_user() is deprecated. Use client.users.update_user() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.users.update_user(id=id, update_user_request=update_user_request, **kwargs)
    
    def delete_user(self, id: str, **kwargs):
        """
        Delete a user.
        
        .. deprecated::
            Use :meth:`client.users.delete_user()` instead.
        
        For full documentation and parameters, see UsersApi.delete_user()
        """
        warnings.warn(
            "delete_user() is deprecated. Use client.users.delete_user() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.users.delete_user(id=id, **kwargs)
    
    def get_organizations(self, **kwargs):
        """
        Get organizations.
        
        .. deprecated::
            Use :meth:`client.organizations.get_organizations()` instead.
        
        For full documentation and parameters, see OrganizationsApi.get_organizations()
        """
        warnings.warn(
            "get_organizations() is deprecated. Use client.organizations.get_organizations() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.organizations.get_organizations(**kwargs)
    
    def get_organization(self, code: str = None, **kwargs):
        """
        Get an organization.
        
        .. deprecated::
            Use :meth:`client.organizations.get_organization()` instead.
        
        For full documentation and parameters, see OrganizationsApi.get_organization()
        """
        warnings.warn(
            "get_organization() is deprecated. Use client.organizations.get_organization() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.organizations.get_organization(code=code, **kwargs)
    
    def create_organization(self, create_organization_request, **kwargs):
        """
        Create an organization.
        
        .. deprecated::
            Use :meth:`client.organizations.create_organization()` instead.
        
        For full documentation and parameters, see OrganizationsApi.create_organization()
        """
        warnings.warn(
            "create_organization() is deprecated. Use client.organizations.create_organization() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.organizations.create_organization(
            create_organization_request=create_organization_request, **kwargs
        )
    
    def update_organization(self, org_code: str, **kwargs):
        """
        Update an organization.
        
        .. deprecated::
            Use :meth:`client.organizations.update_organization()` instead.
        
        For full documentation and parameters, see OrganizationsApi.update_organization()
        """
        warnings.warn(
            "update_organization() is deprecated. Use client.organizations.update_organization() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.organizations.update_organization(org_code=org_code, **kwargs)
    
    def delete_organization(self, org_code: str, **kwargs):
        """
        Delete an organization.
        
        .. deprecated::
            Use :meth:`client.organizations.delete_organization()` instead.
        
        For full documentation and parameters, see OrganizationsApi.delete_organization()
        """
        warnings.warn(
            "delete_organization() is deprecated. Use client.organizations.delete_organization() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.organizations.delete_organization(org_code=org_code, **kwargs)
    
    def get_roles(self, **kwargs):
        """
        Get roles.
        
        .. deprecated::
            Use :meth:`client.roles.get_roles()` instead.
        
        For full documentation and parameters, see RolesApi.get_roles()
        """
        warnings.warn(
            "get_roles() is deprecated. Use client.roles.get_roles() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.roles.get_roles(**kwargs)
    
    def get_role(self, role_id: str):
        """
        Get a role.
        
        .. deprecated::
            Use :meth:`client.roles.get_role()` instead.
        
        For full documentation and parameters, see RolesApi.get_role()
        """
        warnings.warn(
            "get_role() is deprecated. Use client.roles.get_role() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.roles.get_role(role_id=role_id)
    
    def create_role(self, create_role_request=None, **kwargs):
        """
        Create a role.
        
        .. deprecated::
            Use :meth:`client.roles.create_role()` instead.
        
        For full documentation and parameters, see RolesApi.create_role()
        """
        warnings.warn(
            "create_role() is deprecated. Use client.roles.create_role() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.roles.create_role(create_role_request=create_role_request, **kwargs)
    
    def update_role(self, role_id: str, update_role_request=None, **kwargs):
        """
        Update a role.
        
        .. deprecated::
            Use :meth:`client.roles.update_role()` instead.
        
        For full documentation and parameters, see RolesApi.update_role()
        """
        warnings.warn(
            "update_role() is deprecated. Use client.roles.update_role() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.roles.update_role(role_id=role_id, update_role_request=update_role_request, **kwargs)
    
    def delete_role(self, role_id: str):
        """
        Delete a role.
        
        .. deprecated::
            Use :meth:`client.roles.delete_role()` instead.
        
        For full documentation and parameters, see RolesApi.delete_role()
        """
        warnings.warn(
            "delete_role() is deprecated. Use client.roles.delete_role() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.roles.delete_role(role_id=role_id)
    
    def get_feature_flags(self, **kwargs):
        """
        Get feature flags.
        
        .. deprecated::
            Use :meth:`client.feature_flags.get_feature_flags()` instead.
        
        For full documentation and parameters, see FeatureFlagsApi.get_feature_flags()
        """
        warnings.warn(
            "get_feature_flags() is deprecated. Use client.feature_flags.get_feature_flags() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.feature_flags.get_feature_flags(**kwargs)
    
    def create_feature_flag(self, create_feature_flag_request=None, **kwargs):
        """
        Create a feature flag.
        
        .. deprecated::
            Use :meth:`client.feature_flags.create_feature_flag()` instead.
        
        For full documentation and parameters, see FeatureFlagsApi.create_feature_flag()
        """
        warnings.warn(
            "create_feature_flag() is deprecated. Use client.feature_flags.create_feature_flag() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.feature_flags.create_feature_flag(
            create_feature_flag_request=create_feature_flag_request, **kwargs
        )
    
    def update_feature_flag(self, feature_flag_key: str, update_feature_flag_request=None, **kwargs):
        """
        Update a feature flag.
        
        .. deprecated::
            Use :meth:`client.feature_flags.update_feature_flag()` instead.
        
        For full documentation and parameters, see FeatureFlagsApi.update_feature_flag()
        """
        warnings.warn(
            "update_feature_flag() is deprecated. Use client.feature_flags.update_feature_flag() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.feature_flags.update_feature_flag(
            feature_flag_key=feature_flag_key,
            update_feature_flag_request=update_feature_flag_request,
            **kwargs
        )
    
    def delete_feature_flag(self, feature_flag_key: str):
        """
        Delete a feature flag.
        
        .. deprecated::
            Use :meth:`client.feature_flags.delete_feature_flag()` instead.
        
        For full documentation and parameters, see FeatureFlagsApi.delete_feature_flag()
        """
        warnings.warn(
            "delete_feature_flag() is deprecated. Use client.feature_flags.delete_feature_flag() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.feature_flags.delete_feature_flag(feature_flag_key=feature_flag_key)
