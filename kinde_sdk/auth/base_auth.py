from typing import Optional, Any
import logging
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession

class BaseAuth:
    """
    Base class for authentication-related functionality that provides
    shared methods for accessing the framework and token manager.
    """
    
    def __init__(self):
        self._logger = logging.getLogger("kinde_sdk")
        self._logger.setLevel(logging.INFO)
        self._framework = None
        self._session_manager = UserSession()

    def _get_framework(self):
        """Get the framework instance using singleton pattern."""
        if not self._framework:
            self._framework = FrameworkFactory.get_framework_instance()
        return self._framework

    def _get_token_manager(self) -> Optional[Any]:
        """
        Get the token manager for the current user.
        
        Returns:
            Optional[Any]: The token manager if available, None otherwise
        """
        framework = self._get_framework()
        if not framework:
            return None

        user_id = framework.get_user_id()
        if not user_id:
            return None

        return self._session_manager.get_token_manager(user_id)

    def _get_force_api_setting(self) -> bool:
        """
        Get the force_api setting from the current user's token manager.
        
        Returns:
            bool: True if force_api is enabled, False otherwise
        """
        token_manager = self._get_token_manager()
        if not token_manager:
            return False
        return token_manager.get_force_api()

    def _create_authenticated_api_client(self, api_class):
        """
        Create an authenticated API client for the current user.
        
        Args:
            api_class: The API class to instantiate (e.g., FeatureFlagsApi, RolesApi, PermissionsApi)
            
        Returns:
            The configured API instance, or None if authentication fails
            
        Raises:
            Exception: If there's an error creating the API client
        """
        # Get the current user's token manager
        token_manager = self._get_token_manager()
        if not token_manager:
            self._logger.error("No token manager available for API call")
            return None
        
        # Get the access token from the token manager
        access_token = token_manager.get_access_token()
        if not access_token:
            self._logger.error("No access token available for API call")
            return None
        
        # Create API client with the user's access token
        from kinde_sdk.frontend.configuration import Configuration
        from kinde_sdk.frontend.api_client import ApiClient
        
        # Create configuration with the access token
        config = Configuration()
        config.access_token = access_token
        
        # Create API client with the configuration
        api_client = ApiClient(configuration=config)
        
        # Create and return the specific API class with the configured client
        return api_class(api_client=api_client) 