from typing import Optional, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from kinde_sdk.auth.oauth import OAuth

from .framework_interface import FrameworkInterface

class NullFramework(FrameworkInterface):
    """
    A null implementation of the FrameworkInterface.
    This implementation does nothing and is used when no framework is detected or specified.
    """
    
    def __init__(self):
        """Initialize the null framework."""
        self._oauth = None
    
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
        return "A null framework implementation that does nothing. Used when no framework is detected or specified."
    
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
        
    def set_oauth(self, oauth: 'OAuth') -> None:
        """
        Set the OAuth instance for this framework.
        
        Args:
            oauth (OAuth): The OAuth instance
        """
        self._oauth = oauth 