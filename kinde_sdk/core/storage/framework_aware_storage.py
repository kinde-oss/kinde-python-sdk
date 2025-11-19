from typing import Dict, Optional, Any
from .storage_interface import StorageInterface
from ..framework.framework_context import FrameworkContext
import logging

class FrameworkAwareStorage(StorageInterface):
    """
    Base class for framework-aware storage implementations.
    This class provides common functionality for accessing framework-specific sessions
    through the FrameworkContext.
    """
    
    def __init__(self):
        """Initialize the framework-aware storage."""
        self._session = None
        self._logger = logging.getLogger(__name__)
        
    def _get_session(self) -> Optional[Any]:
        """
        Get the current session from the framework context.
        
        Returns:
            Optional[Any]: The current session object, or None if not available
        """
        request = FrameworkContext.get_request()
        if not request:
            self._logger.warning("No request found in context")
            return None
            
        # Framework-specific session access
        if hasattr(request, 'session'):  # FastAPI
            self._logger.debug("FastAPI session found")
            return request.session
        elif hasattr(request, 'environ'):  # Flask
            self._logger.debug("Flask session found")
            from flask import session
            return session
        self._logger.warning("No session found")
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
        if session is not None:
            value = session.get(key)
            self._logger.debug(f"Getting key '{key}' from session: {value}")
            return value
        return None
        
    def set(self, key: str, value: Dict) -> None:
        """
        Store data in the session.
        
        Args:
            key (str): The key to store data under
            value (Dict): The data to store
        """
        session = self._get_session()
        if session is not None:
            self._logger.debug(f"Setting key '{key}' in session with value: {value}")
            session[key] = value
            # Mark session as modified for Flask
            if hasattr(session, 'modified'):
                session.modified = True
                self._logger.debug(f"Marked session as modified after setting '{key}'")
            
    def delete(self, key: str) -> None:
        """
        Delete data from the session.
        
        Args:
            key (str): The key to delete data for
        """
        session = self._get_session()
        if session and key in session:
            self._logger.debug(f"Deleting key '{key}' from session")
            del session[key]
            # Mark session as modified for Flask
            if hasattr(session, 'modified'):
                session.modified = True
                self._logger.debug(f"Marked session as modified after deleting '{key}'")
            
    def set_flat(self, value: str) -> None:
        """
        Store flat data in the session.
        
        Args:
            value (str): The data to store
        """
        session = self._get_session()
        if session is not None:
            self._logger.debug(f"Setting flat data in session: {value}")
            session["_flat_data"] = value
            # Mark session as modified for Flask
            if hasattr(session, 'modified'):
                session.modified = True
                self._logger.debug("Marked session as modified after setting flat data") 