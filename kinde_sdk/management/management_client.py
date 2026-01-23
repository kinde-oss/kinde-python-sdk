"""
Client for the Kinde Management API.

This module provides a client for the Kinde Management API that integrates
with the existing Kinde SDK infrastructure and adds automatic token management
to the generated API classes.
"""

import inspect
import logging
import re
from typing import Optional
import warnings

# Import the api module to dynamically load all API classes
from kinde_sdk.management import api
from kinde_sdk.management.api_client import ApiClient
from kinde_sdk.management.configuration import Configuration
from .management_token_manager import ManagementTokenManager
from .custom_exceptions import KindeTokenException

logger = logging.getLogger("kinde_sdk.management")


class ManagementClient:
    """
    Client for the Kinde Management API.
    
    This client provides access to all Kinde Management API endpoints through
    the auto-generated API classes, with automatic token management.
    
    All API classes are dynamically loaded from the 'api' module and made available
    as snake_case properties. For example:
    - UsersApi -> client.users_api.*
    - OrganizationsApi -> client.organizations_api.*
    - FeatureFlagsApi -> client.feature_flags_api.*
    - etc.
    
    When new API classes are generated from the OpenAPI spec, they will automatically
    be available on this client without any code changes.
    
    Common API properties include:
    - client.users_api.*           - User management
    - client.organizations_api.*   - Organization management
    - client.roles_api.*           - Role management
    - client.permissions_api.*     - Permission management
    - client.feature_flags_api.*   - Feature flag management
    - client.apis_api.*            - API application management
    - client.applications_api.*    - Connected app management
    - client.subscribers_api.*     - Subscriber management
    - client.properties_api.*      - Property management
    - client.webhooks_api.*        - Webhook management
    - client.connections_api.*     - Connection management
    - client.business_api.*        - Business information
    - And more...
    
    Example:
        ```python
        client = ManagementClient(domain, client_id, client_secret)
        
        # Get all users
        users = client.users_api.get_users(page_size=50)
        
        # Create a user
        new_user = client.users_api.create_user(
            create_user_request={'email': 'user@example.com'}
        )
        
        # Get organizations
        orgs = client.organizations_api.get_organizations()
        
        # Access any dynamically loaded API
        timezones = client.timezones_api.get_timezones()
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
        to all outgoing requests. The wrapper handles token acquisition failures
        and ensures existing Authorization headers are not silently overwritten.
        """
        original_call_api = self.api_client.call_api
        
        def call_api_with_token(*args, **kwargs):
            """
            Wrapper that adds authentication token to all API calls.
            
            Raises:
                KindeTokenException: If token acquisition fails or returns a falsy value.
            """
            # Attempt to get the access token with proper error handling
            try:
                token = self.token_manager.get_access_token()
            except Exception as e:
                logger.error(f"Failed to acquire access token: {e}")
                raise KindeTokenException(
                    f"Failed to acquire access token for Management API: {e}"
                ) from e
            
            # Verify the token is valid (not None, empty string, etc.)
            if not token:
                logger.error("Token manager returned a falsy token value")
                raise KindeTokenException(
                    "Failed to acquire access token: token manager returned an invalid token"
                )
            
            # Initialize header_params if not present
            if 'header_params' not in kwargs:
                kwargs['header_params'] = {}
            
            # Check for existing Authorization header and handle appropriately
            if 'Authorization' in kwargs['header_params']:
                existing_auth = kwargs['header_params']['Authorization']
                logger.warning(
                    f"Overwriting existing Authorization header. "
                    f"Existing value: {existing_auth[:20]}... "
                    f"New value: Bearer {token[:20]}..."
                )
            
            # Inject the token into headers
            kwargs['header_params']['Authorization'] = f"Bearer {token}"
            
            # Call the original method
            return original_call_api(*args, **kwargs)
        
        # Replace the call_api method with the robust wrapper
        self.api_client.call_api = call_api_with_token
    
    def _initialize_api_classes(self):
        """
        Dynamically initialize all API classes from the api module.
        
        This method inspects the api module and creates an instance of each
        API class (classes ending with 'Api'), making them available as
        snake_case attributes on this client.
        
        For example:
        - UsersApi -> self.users_api
        - OrganizationsApi -> self.organizations_api
        - FeatureFlagsApi -> self.feature_flags_api
        
        Raises:
            RuntimeError: If API initialization fails or no APIs are found.
        """
        # Track loaded APIs for verification
        loaded_apis = []
        
        # Get all members of the api module
        for name, obj in inspect.getmembers(api):
            # Check if it's a class and ends with 'Api'
            if inspect.isclass(obj) and name.endswith('Api'):
                # Convert class name to snake_case attribute name
                # e.g., UsersApi -> users_api, FeatureFlagsApi -> feature_flags_api
                attr_name = self._class_name_to_snake_case(name)
                
                # Check for attribute collisions with existing ManagementClient attributes
                if hasattr(self, attr_name):
                    logger.warning(
                        f"Attribute '{attr_name}' already exists on ManagementClient, "
                        f"skipping {name}. This may indicate a naming conflict."
                    )
                    continue
                
                # Initialize the API class with error handling
                try:
                    api_instance = obj(api_client=self.api_client)
                except Exception as e:
                    logger.error(f"Failed to initialize {name}: {e}")
                    raise RuntimeError(
                        f"Failed to initialize API class {name}. "
                        f"This may indicate a compatibility issue with the generated API. "
                        f"Error: {e}"
                    ) from e
                
                # Set it as an attribute on this client
                setattr(self, attr_name, api_instance)
                loaded_apis.append(attr_name)
                
                logger.debug(f"Initialized {name} as client.{attr_name}")
        
        # Verify at least some APIs were loaded
        if not loaded_apis:
            raise RuntimeError(
                "No API classes found in kinde_sdk.management.api module. "
                "This may indicate the SDK was not properly installed or generated. "
                "Please verify the installation or regenerate the SDK."
            )
        
        logger.info(f"Loaded {len(loaded_apis)} API classes: {', '.join(sorted(loaded_apis))}")
    
    @staticmethod
    def _class_name_to_snake_case(class_name: str) -> str:
        """
        Convert a class name to snake_case attribute name.
        Handles acronyms intelligently by keeping consecutive uppercase letters together.
        
        Special cases are handled for oddly-named classes generated from the OpenAPI spec
        where the tag naming creates unusual capitalization patterns.
        
        Examples:
        - UsersApi -> users_api
        - FeatureFlagsApi -> feature_flags_api
        - APIsApi -> apis_api (special case - tag "APIs" in spec)
        - MFAApi -> mfa_api (not m_f_a_api or mfaapi)
        - OAuthApi -> oauth_api (not o_auth_api)
        - HTTPSConnectionApi -> https_connection_api
        
        Args:
            class_name: The class name (e.g., 'UsersApi')
            
        Returns:
            Snake case attribute name (e.g., 'users_api')
        """
        # Special cases for oddly-named classes from OpenAPI spec tag naming
        # These arise when spec tags have unusual capitalization (e.g., "APIs" tag)
        special_cases = {
            'APIsApi': 'apis_api',  # From tag "APIs" - would otherwise be "ap_is_api"
        }
        
        if class_name in special_cases:
            return special_cases[class_name]
        
        # Step 1: Insert underscore between sequences of 2+ uppercase letters and 
        # a final uppercase letter followed by lowercase (handles acronym boundaries)
        # e.g., "MFAApi" -> "MFA_Api", "HTTPSConnection" -> "HTTPS_Connection"
        # Note: Requires at least 2 consecutive uppercase to avoid splitting single letters
        s1 = re.sub('([A-Z]{2,})([A-Z][a-z])', r'\1_\2', class_name)
        
        # Step 2: Insert underscore between lowercase (or digit) and uppercase letters
        # e.g., "feature_Flags" -> "feature_Flags" (already has _), "featureFlags" -> "feature_Flags"
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
        
        # Convert to lowercase
        return s2.lower()
    
    # Backwards compatibility: Provide direct method access for common operations
    # These delegate to the appropriate API class methods
    # Note: These methods are deprecated. For full functionality and proper type hints,
    # use the API class methods directly (e.g., client.users_api.get_users())
    
    def get_users(self, **kwargs):
        """
        Get users.
        
        .. deprecated::
            Use :meth:`client.users_api.get_users()` instead.
        
        For full documentation and parameters, see UsersApi.get_users()
        """
        warnings.warn(
            "get_users() is deprecated. Use client.users_api.get_users() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.users_api.get_users(**kwargs)
    
    def get_api_applications(self, **kwargs):
        """
        Get API applications.
        
        .. deprecated::
            Use :meth:`client.applications_api.get_applications()` instead.
        
        For full documentation and parameters, see ApplicationsApi.get_applications()
        """
        warnings.warn(
            "get_api_applications() is deprecated. Use client.applications_api.get_applications() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.applications_api.get_applications(**kwargs)
    
    def get_user_data(self, user_id: str):
        """
        Get user data by ID.
        
        .. deprecated::
            Use :meth:`client.users_api.get_user_data()` instead.
        
        For full documentation and parameters, see UsersApi.get_user_data()
        """
        warnings.warn(
            "get_user_data() is deprecated. Use client.users_api.get_user_data() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.users_api.get_user_data(id=user_id)
    
    def create_user(self, create_user_request=None, **kwargs):
        """
        Create a user.
        
        .. deprecated::
            Use :meth:`client.users_api.create_user()` instead.
        
        For full documentation and parameters, see UsersApi.create_user()
        """
        warnings.warn(
            "create_user() is deprecated. Use client.users_api.create_user() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.users_api.create_user(create_user_request=create_user_request, **kwargs)
    
    def update_user(self, id: str, update_user_request, **kwargs):
        """
        Update a user.
        
        .. deprecated::
            Use :meth:`client.users_api.update_user()` instead.
        
        For full documentation and parameters, see UsersApi.update_user()
        """
        warnings.warn(
            "update_user() is deprecated. Use client.users_api.update_user() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.users_api.update_user(id=id, update_user_request=update_user_request, **kwargs)
    
    def delete_user(self, id: str, **kwargs):
        """
        Delete a user.
        
        .. deprecated::
            Use :meth:`client.users_api.delete_user()` instead.
        
        For full documentation and parameters, see UsersApi.delete_user()
        """
        warnings.warn(
            "delete_user() is deprecated. Use client.users_api.delete_user() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.users_api.delete_user(id=id, **kwargs)
    
    def get_organizations(self, **kwargs):
        """
        Get organizations.
        
        .. deprecated::
            Use :meth:`client.organizations_api.get_organizations()` instead.
        
        For full documentation and parameters, see OrganizationsApi.get_organizations()
        """
        warnings.warn(
            "get_organizations() is deprecated. Use client.organizations_api.get_organizations() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.organizations_api.get_organizations(**kwargs)
    
    def get_organization(self, code: Optional[str] = None, **kwargs):
        """
        Get an organization.
        
        .. deprecated::
            Use :meth:`client.organizations_api.get_organization()` instead.
        
        For full documentation and parameters, see OrganizationsApi.get_organization()
        """
        warnings.warn(
            "get_organization() is deprecated. Use client.organizations_api.get_organization() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.organizations_api.get_organization(code=code, **kwargs)
    
    def create_organization(self, create_organization_request, **kwargs):
        """
        Create an organization.
        
        .. deprecated::
            Use :meth:`client.organizations_api.create_organization()` instead.
        
        For full documentation and parameters, see OrganizationsApi.create_organization()
        """
        warnings.warn(
            "create_organization() is deprecated. Use client.organizations_api.create_organization() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.organizations_api.create_organization(
            create_organization_request=create_organization_request, **kwargs
        )
    
    def update_organization(self, org_code: str, **kwargs):
        """
        Update an organization.
        
        .. deprecated::
            Use :meth:`client.organizations_api.update_organization()` instead.
        
        For full documentation and parameters, see OrganizationsApi.update_organization()
        """
        warnings.warn(
            "update_organization() is deprecated. Use client.organizations_api.update_organization() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.organizations_api.update_organization(org_code=org_code, **kwargs)
    
    def delete_organization(self, org_code: str, **kwargs):
        """
        Delete an organization.
        
        .. deprecated::
            Use :meth:`client.organizations_api.delete_organization()` instead.
        
        For full documentation and parameters, see OrganizationsApi.delete_organization()
        """
        warnings.warn(
            "delete_organization() is deprecated. Use client.organizations_api.delete_organization() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.organizations_api.delete_organization(org_code=org_code, **kwargs)
    
    def get_roles(self, **kwargs):
        """
        Get roles.
        
        .. deprecated::
            Use :meth:`client.roles_api.get_roles()` instead.
        
        For full documentation and parameters, see RolesApi.get_roles()
        """
        warnings.warn(
            "get_roles() is deprecated. Use client.roles_api.get_roles() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.roles_api.get_roles(**kwargs)
    
    def get_role(self, role_id: str):
        """
        Get a role.
        
        .. deprecated::
            Use :meth:`client.roles_api.get_role()` instead.
        
        For full documentation and parameters, see RolesApi.get_role()
        """
        warnings.warn(
            "get_role() is deprecated. Use client.roles_api.get_role() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.roles_api.get_role(role_id=role_id)
    
    def create_role(self, create_role_request=None, **kwargs):
        """
        Create a role.
        
        .. deprecated::
            Use :meth:`client.roles_api.create_role()` instead.
        
        For full documentation and parameters, see RolesApi.create_role()
        """
        warnings.warn(
            "create_role() is deprecated. Use client.roles_api.create_role() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.roles_api.create_role(create_role_request=create_role_request, **kwargs)
    
    def update_role(self, role_id: str, update_role_request=None, **kwargs):
        """
        Update a role.
        
        .. deprecated::
            Use :meth:`client.roles_api.update_role()` instead.
        
        For full documentation and parameters, see RolesApi.update_role()
        """
        warnings.warn(
            "update_role() is deprecated. Use client.roles_api.update_role() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.roles_api.update_role(role_id=role_id, update_role_request=update_role_request, **kwargs)
    
    def delete_role(self, role_id: str):
        """
        Delete a role.
        
        .. deprecated::
            Use :meth:`client.roles_api.delete_role()` instead.
        
        For full documentation and parameters, see RolesApi.delete_role()
        """
        warnings.warn(
            "delete_role() is deprecated. Use client.roles_api.delete_role() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.roles_api.delete_role(role_id=role_id)
    
    def get_feature_flags(self, **kwargs):
        """
        Get feature flags.
        
        .. deprecated::
            Use :meth:`client.feature_flags_api.get_feature_flags()` instead.
        
        For full documentation and parameters, see FeatureFlagsApi.get_feature_flags()
        """
        warnings.warn(
            "get_feature_flags() is deprecated. Use client.feature_flags_api.get_feature_flags() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.feature_flags_api.get_feature_flags(**kwargs)
    
    def create_feature_flag(self, create_feature_flag_request=None, **kwargs):
        """
        Create a feature flag.
        
        .. deprecated::
            Use :meth:`client.feature_flags_api.create_feature_flag()` instead.
        
        For full documentation and parameters, see FeatureFlagsApi.create_feature_flag()
        """
        warnings.warn(
            "create_feature_flag() is deprecated. Use client.feature_flags_api.create_feature_flag() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.feature_flags_api.create_feature_flag(
            create_feature_flag_request=create_feature_flag_request, **kwargs
        )
    
    def update_feature_flag(self, feature_flag_key: str, update_feature_flag_request=None, **kwargs):
        """
        Update a feature flag.
        
        .. deprecated::
            Use :meth:`client.feature_flags_api.update_feature_flag()` instead.
        
        For full documentation and parameters, see FeatureFlagsApi.update_feature_flag()
        """
        warnings.warn(
            "update_feature_flag() is deprecated. Use client.feature_flags_api.update_feature_flag() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.feature_flags_api.update_feature_flag(
            feature_flag_key=feature_flag_key,
            update_feature_flag_request=update_feature_flag_request,
            **kwargs
        )
    
    def delete_feature_flag(self, feature_flag_key: str):
        """
        Delete a feature flag.
        
        .. deprecated::
            Use :meth:`client.feature_flags_api.delete_feature_flag()` instead.
        
        For full documentation and parameters, see FeatureFlagsApi.delete_feature_flag()
        """
        warnings.warn(
            "delete_feature_flag() is deprecated. Use client.feature_flags_api.delete_feature_flag() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self.feature_flags_api.delete_feature_flag(feature_flag_key=feature_flag_key)
