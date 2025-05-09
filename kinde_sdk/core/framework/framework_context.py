import threading
from typing import Optional, Any

class FrameworkContext:
    """
    Thread-local context manager for framework-specific request objects.
    This allows framework-specific storage implementations to access the current request
    without needing to pass it through the entire call chain.
    """
    _context = threading.local()
    
    @classmethod
    def set_request(cls, request: Any) -> None:
        """
        Set the current request object in the thread-local context.
        
        Args:
            request (Any): The framework-specific request object
        """
        cls._context.request = request
        
    @classmethod
    def get_request(cls) -> Optional[Any]:
        """
        Get the current request object from the thread-local context.
        
        Returns:
            Optional[Any]: The current request object, or None if not set
        """
        return getattr(cls._context, 'request', None)
        
    @classmethod
    def clear_request(cls) -> None:
        """
        Clear the current request object from the thread-local context.
        """
        if hasattr(cls._context, 'request'):
            delattr(cls._context, 'request') 