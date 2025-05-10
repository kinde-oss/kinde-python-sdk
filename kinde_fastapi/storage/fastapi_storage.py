from typing import Dict, Optional
from kinde_sdk.core.storage.framework_aware_storage import FrameworkAwareStorage
from kinde_sdk.core.storage.framework_aware_storage import FrameworkAwareStorage
from fastapi import Request
from kinde_sdk.core.framework.framework_context import FrameworkContext
import logging

logger = logging.getLogger(__name__)

class FastAPIStorage(FrameworkAwareStorage):
    """
    FastAPI storage implementation that uses FastAPI's session management.
    This implementation stores data in the session using cookies.
    """
    
    def __init__(self):
        """Initialize the FastAPI storage."""
        super().__init__()

    def get(self, key: str) -> Optional[Dict]:
        """
        Retrieve data associated with the given key from the session.
        
        Args:
            key (str): The key to retrieve data for.
            
        Returns:
            Optional[Dict]: The stored data or None if not found.
        """
        session = self._get_session()
        
        if session is None:
            logger.error("No session object found in request")
            return None
            
        return session.get(key)

    def set(self, key: str, value: Dict) -> None:
        """
        Store data associated with the given key in the session.
        
        Args:
            key (str): The key to store the data under.
            value (Dict): The data to store.
        """
        session = self._get_session()
        
        if session is not None:
            session[key] = value
            # Mark session as modified for FastAPI/Starlette
            if hasattr(session, 'modified'):
                session.modified = True

    def set_flat(self, value: str) -> None:
        """
        Store flat data in the session.
        
        Args:
            value (str): The data to store.
        """
        session = self._get_session()
        if session is not None:
            session["_flat_data"] = value
            # Mark session as modified for FastAPI/Starlette
            if hasattr(session, 'modified'):
                session.modified = True

    def delete(self, key: str) -> None:
        """
        Delete data associated with the given key from the session.
        
        Args:
            key (str): The key to delete data for.
        """
        logger.warning(f"Deleting a session key")
        session = self._get_session()
        if session is not None and key in session:
            del session[key]
            # Mark session as modified for FastAPI/Starlette
            if hasattr(session, 'modified'):
                session.modified = True 