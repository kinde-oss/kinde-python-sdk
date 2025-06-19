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