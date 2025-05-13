import contextvars
from typing import Optional, Any

class FrameworkContext:
    """
    Context-local context manager for framework-specific request objects.
    This allows framework-specific storage implementations to access the current request
    without needing to pass it through the entire call chain.
    """
    _context = contextvars.ContextVar('framework_context', default=None)
    
    @classmethod
    def set_request(cls, request: Any) -> None:
        """
        Set the current request object in the context-local storage.
        
        Args:
            request (Any): The framework-specific request object
        """
        cls._context.set(request)
        
    @classmethod
    def get_request(cls) -> Optional[Any]:
        """
        Get the current request object from the context-local storage.
        
        Returns:
            Optional[Any]: The current request object, or None if not set
        """
        return cls._context.get()
        
    @classmethod
    def clear_request(cls) -> None:
        """
        Clear the current request object from the context-local storage.
        """
        cls._context.set(None) 