from typing import Optional, Any, TYPE_CHECKING
import threading
import contextvars

if TYPE_CHECKING:
    from kinde_sdk.auth.oauth import OAuth

from .framework_interface import FrameworkInterface

class NullFramework(FrameworkInterface):
    """
    A null implementation of the FrameworkInterface.
    This implementation provides session management for standalone usage without a web framework.
    Uses a singleton pattern to allow external applications to set the current user session.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(NullFramework, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the null framework."""
        if not hasattr(self, '_initialized'):
            self._oauth = None
            # Use context variables for user_id to avoid race conditions in both threads and async
            self._current_user_id_context = contextvars.ContextVar('current_user_id', default=None)
            self._initialized = True
    
    def get_name(self) -> str:
        """
        Get the name of the framework.
        
        Returns:
            str: The name of the null framework
        """
        return "null"
    
    def get_description(self) -> str:
        """
        Get a description of the framework.
        
        Returns:
            str: A description of the null framework
        """
        return "A null framework implementation that provides session management for standalone usage without a web framework."
    
    def start(self) -> None:
        """
        Start the framework.
        This is a no-op in the null implementation.
        """
        pass
    
    def stop(self) -> None:
        """
        Stop the framework.
        This is a no-op in the null implementation.
        """
        pass
        
    def get_app(self) -> Any:
        """
        Get the framework application instance.
        
        Returns:
            Any: None in the null implementation
        """
        return None
        
    def get_request(self) -> Optional[Any]:
        """
        Get the current request object.
        
        Returns:
            Optional[Any]: None in the null implementation
        """
        return None
        
    def get_user_id(self) -> Optional[str]:
        """
        Get the current user ID from the session.
        
        Returns:
            Optional[str]: The current user ID, or None if not set
        """
        return self._current_user_id_context.get()
    
    def set_user_id(self, user_id: str) -> None:
        """
        Set the current user ID for the session.
        This method allows external applications (like simple HTTP servers) 
        to set the current user session.
        
        Args:
            user_id (str): The user ID to set as current
        """
        self._current_user_id_context.set(user_id)
    
    def clear_user_id(self) -> None:
        """
        Clear the current user ID from the session.
        """
        self._current_user_id_context.set(None)
    
    def set_oauth(self, oauth: 'OAuth') -> None:
        """
        Set the OAuth instance for this framework.
        
        Args:
            oauth (OAuth): The OAuth instance
        """
        self._oauth = oauth
    
    def can_auto_detect(self) -> bool:
        """
        Check if this framework can be auto-detected.
        
        Returns:
            bool: False - null framework is not auto-detected
        """
        return False 