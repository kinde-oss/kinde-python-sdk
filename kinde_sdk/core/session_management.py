"""
Kinde Session Management

This module provides a user-friendly interface for session management when using
the Kinde SDK in standalone mode (without a web framework). It wraps access to
the NullFramework behind a more intuitive API.
"""

from typing import Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from kinde_sdk.core.framework.null_framework import NullFramework

logger = logging.getLogger(__name__)


class KindeSessionManagement:
    """
    A user-friendly interface for session management in standalone Kinde SDK usage.
    
    This class provides a clean API for managing user sessions when using the Kinde SDK
    without a web framework. It wraps the NullFramework functionality behind a more
    intuitive interface.
    
    Note: This class can only be used when the SDK is running in standalone mode
    (without a web framework). If a framework like FastAPI or Flask is being used,
    this class will raise an exception to prevent misuse.
    """
    
    def __init__(self):
        """
        Initialize the Kinde session management.
        
        Raises:
            RuntimeError: If the SDK is not running in standalone mode (NullFramework not active)
        """
        self._logger = logging.getLogger(__name__)
        self._null_framework = self._get_null_framework()
        
        if not self._null_framework:
            raise RuntimeError(
                "KindeSessionManagement can only be used in standalone mode. "
                "When using a web framework (FastAPI, Flask, etc.), session management "
                "is handled automatically by the framework. Please use the framework's "
                "built-in session management instead."
            )
    
    def _get_null_framework(self) -> Optional['NullFramework']:
        """
        Get the current NullFramework instance if it's active.
        
        Returns:
            Optional[NullFramework]: The NullFramework instance if active, None otherwise
        """
        try:
            from kinde_sdk.core.framework.null_framework import NullFramework
            from kinde_sdk.core.framework.framework_factory import FrameworkFactory
            
            # First, try to get the framework instance from FrameworkFactory
            current_framework = FrameworkFactory.get_framework_instance()
            
            # Check if it's a NullFramework instance
            if current_framework and isinstance(current_framework, NullFramework):
                return current_framework
            
            # If not found in FrameworkFactory, try to get it from the NullFramework singleton
            # This handles the case where OAuth creates NullFramework directly
            try:
                null_framework = NullFramework()
                # Check if this is actually being used (has been initialized)
                if hasattr(null_framework, '_initialized') and null_framework._initialized:
                    return null_framework
            except Exception:
                pass
            
            return None
            
        except Exception as e:
            self._logger.debug(f"Could not get NullFramework: {e}")
            return None
    
    def get_user_id(self) -> Optional[str]:
        """
        Get the current user ID from the session.
        
        Returns:
            Optional[str]: The current user ID, or None if not set
        """
        if not self._null_framework:
            raise RuntimeError("Session management is not available in this context")
        
        return self._null_framework.get_user_id()
    
    def set_user_id(self, user_id: str) -> None:
        """
        Set the current user ID for the session.
        
        This method allows you to set the current user session, which is useful
        for applications that need to manage multiple user sessions or when
        integrating with custom session management systems.
        
        Args:
            user_id (str): The user ID to set as current
            
        Raises:
            RuntimeError: If session management is not available in this context
            ValueError: If user_id is empty or None
        """
        if not self._null_framework:
            raise RuntimeError("Session management is not available in this context")
        
        if not user_id or not user_id.strip():
            raise ValueError("user_id cannot be empty or None")
        
        self._null_framework.set_user_id(user_id)
        self._logger.debug(f"Set user ID: {user_id}")
    
    def clear_user_id(self) -> None:
        """
        Clear the current user ID from the session.
        
        This method removes the current user session, effectively logging out
        the user from the current context.
        
        Raises:
            RuntimeError: If session management is not available in this context
        """
        if not self._null_framework:
            raise RuntimeError("Session management is not available in this context")
        
        self._null_framework.clear_user_id()
        self._logger.debug("Cleared user ID from session")
    
    def is_user_logged_in(self) -> bool:
        """
        Check if a user is currently logged in.
        
        Returns:
            bool: True if a user is logged in, False otherwise
        """
        if not self._null_framework:
            raise RuntimeError("Session management is not available in this context")
        
        user_id = self._null_framework.get_user_id()
        return user_id is not None and user_id.strip() != ""
    
    def get_session_info(self) -> dict:
        """
        Get information about the current session.
        
        Returns:
            dict: A dictionary containing session information
            
        Raises:
            RuntimeError: If session management is not available in this context
        """
        if not self._null_framework:
            raise RuntimeError("Session management is not available in this context")
        
        user_id = self._null_framework.get_user_id()
        
        return {
            "user_id": user_id,
            "is_logged_in": user_id is not None and user_id.strip() != "",
            "framework": "standalone",
            "session_type": "null_framework"
        }
    
    def __repr__(self) -> str:
        """Return a string representation of the session management object."""
        if not self._null_framework:
            return "KindeSessionManagement(unavailable - not in standalone mode)"
        
        user_id = self._null_framework.get_user_id()
        status = "logged_in" if user_id else "not_logged_in"
        return f"KindeSessionManagement(user_id={user_id}, status={status})"
