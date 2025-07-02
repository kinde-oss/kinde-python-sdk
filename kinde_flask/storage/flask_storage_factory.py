from typing import Optional, Dict, Any
from flask import session
from kinde_sdk.core.storage.storage_factory import StorageFactory
from kinde_sdk.core.storage.storage_interface import StorageInterface
from kinde_sdk.core.storage.framework_aware_storage import FrameworkAwareStorage
import logging

logger = logging.getLogger(__name__)

class FlaskStorage(FrameworkAwareStorage):
    """
    Flask-specific storage implementation using Flask's session.
    """
    
    def __init__(self):
        """Initialize the Flask storage."""
        super().__init__()
        
    def get(self, key: str) -> Optional[Dict]:
        """
        Get a value from Flask's session.
        
        Args:
            key (str): The key to retrieve.
            
        Returns:
            Optional[Dict]: The value if found, None otherwise.
        """
        session = self._get_session()
        if session is not None:
            value = session.get(key)
            logger.debug(f"Getting key '{key}' from session: {value}")
            return value
        return None
        
    def set(self, key: str, value: Dict) -> None:
        """
        Set a value in Flask's session.
        
        Args:
            key (str): The key to set.
            value (Dict): The value to store.
        """
        session = self._get_session()
        if session is not None:
            session[key] = value
            session.modified = True
        
    def delete(self, key: str) -> None:
        """
        Delete a value from Flask's session.
        
        Args:
            key (str): The key to delete.
        """
        session = self._get_session()
        if session and key in session:
            del session[key]
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
            session.modified = True

class FlaskStorageFactory(StorageFactory):
    """
    Factory for creating Flask-specific storage instances.
    """
    
    @staticmethod
    def create_storage(config: Optional[Dict[str, Any]] = None) -> FlaskStorage:
        """
        Create a Flask storage instance.
        
        Args:
            config (Optional[Dict[str, Any]]): Configuration options.
                Not used in Flask implementation as it uses Flask's session.
                
        Returns:
            FlaskStorage: A Flask storage instance.
        """
        return FlaskStorage()
