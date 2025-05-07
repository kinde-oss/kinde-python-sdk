from typing import Dict, Optional
from fastapi import Request
from kinde_sdk.core.storage.storage_interface import StorageInterface

class FastAPIStorage(StorageInterface):
    """
    FastAPI storage implementation that uses FastAPI's session management.
    This implementation stores data in the session using cookies.
    """
    
    def __init__(self, request: Request):
        """
        Initialize the FastAPI storage with a request object.
        
        Args:
            request (Request): The FastAPI request object that contains the session.
        """
        self.request = request
        self._session = request.session

    def get(self, key: str) -> Optional[Dict]:
        """
        Retrieve data associated with the given key from the session.
        
        Args:
            key (str): The key to retrieve data for.
            
        Returns:
            Optional[Dict]: The stored data or None if not found.
        """
        return self._session.get(key)

    def set(self, key: str, value: Dict) -> None:
        """
        Store data associated with the given key in the session.
        
        Args:
            key (str): The key to store the data under.
            value (Dict): The data to store.
        """
        self._session[key] = value

    def set_flat(self, value: str) -> None:
        """
        Store flat data in the session.
        
        Args:
            value (str): The data to store.
        """
        self._session["_flat_data"] = value

    def delete(self, key: str) -> None:
        """
        Delete data associated with the given key from the session.
        
        Args:
            key (str): The key to delete data for.
        """
        if key in self._session:
            del self._session[key] 