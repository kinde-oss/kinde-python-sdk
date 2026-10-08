from typing import Optional, Any
import logging
import os
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession

class BaseAuth:
    """
    Base class for authentication-related functionality that provides
    shared methods for accessing the framework and token manager.
    """
    
    def __init__(self):
        self._logger = logging.getLogger("kinde_sdk")
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

    @staticmethod
    def _describe_api_error(error: Exception) -> str:
        """Exception type and HTTP status only: API exception messages include the response body."""
        status = getattr(error, "status", None)
        return f"{type(error).__name__} (HTTP {status})" if status else type(error).__name__

    @staticmethod
    def _get_account_api_host(token_manager) -> Optional[str]:
        """
        The Account API lives on the Kinde domain that issued the user's token,
        which also covers custom domains; KINDE_HOST is the fallback.
        """
        claims = token_manager.get_claims() if hasattr(token_manager, "get_claims") else {}
        issuer = claims.get("iss") if isinstance(claims, dict) else None
        host = issuer if isinstance(issuer, str) and issuer.startswith("https://") else os.getenv("KINDE_HOST")
        # The client sends the user's access token, so never use a plain HTTP host
        if not host or not host.startswith("https://"):
            return None
        return host.rstrip("/")

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
        
        host = self._get_account_api_host(token_manager)
        if not host:
            self._logger.error("Cannot determine an HTTPS Kinde host for Account API calls")
            return None

        config = Configuration(host=host)
        config.access_token = access_token
        
        # Create API client with the configuration
        api_client = ApiClient(configuration=config)
        
        # Create and return the specific API class with the configured client
        return api_class(api_client=api_client) 