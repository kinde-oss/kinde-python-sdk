from typing import Dict, Optional, Any
from .storage_interface import StorageInterface
from ..framework.framework_context import FrameworkContext

class FrameworkAwareStorage(StorageInterface):
    """
    Base class for framework-aware storage implementations.
    This class provides common functionality for accessing framework-specific sessions
    through the FrameworkContext.
    """
    
    def __init__(self):
        """Initialize the framework-aware storage."""
        self._session = None
        
    def _get_session(self) -> Optional[Any]:
        """
        Get the current session from the framework context.
        
        Returns:
            Optional[Any]: The current session object, or None if not available
        """
        request = FrameworkContext.get_request()
        if not request:
            return None
            
        # Framework-specific session access
        if hasattr(request, 'session'):  # FastAPI
            return request.session
        elif hasattr(request, 'environ'):  # Flask
            return request.environ.get('flask.session')
        return None
        
    def get(self, key: str) -> Optional[Dict]:
        """
        Retrieve data from the session.
        
        Args:
            key (str): The key to retrieve data for
            
        Returns:
            Optional[Dict]: The stored data or None if not found
        """
        session = self._get_session()
        return session.get(key) if session else None
        
    def set(self, key: str, value: Dict) -> None:
        """
        Store data in the session.
        
        Args:
            key (str): The key to store data under
            value (Dict): The data to store
        """
        session = self._get_session()
        if session:
            session[key] = value
            
    def delete(self, key: str) -> None:
        """
        Delete data from the session.
        
        Args:
            key (str): The key to delete data for
        """
        session = self._get_session()
        if session and key in session:
            del session[key]
            
    def set_flat(self, value: str) -> None:
        """
        Store flat data in the session.
        
        Args:
            value (str): The data to store
        """
        session = self._get_session()
        if session:
            session["_flat_data"] = value 