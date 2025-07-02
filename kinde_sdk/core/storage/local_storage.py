
from typing import Dict, Optional
import json
from .storage_interface import StorageInterface

class LocalStorage(StorageInterface):
    def __init__(self):
        # In a browser environment, `localStorage` is available globally.
        # For testing in a non-browser environment, you can mock this.
        self.storage = {}

    def get(self, key: str) -> Optional[Dict]:
        """
        Retrieve data associated with the given key.
        
        Args:
            key (str): The key to retrieve data for.
            
        Returns:
            Optional[Dict]: The stored data or None if not found.
        """
        data = self.storage.getItem(key)
        return json.loads(data) if data else None

    def set(self, key: str, value: Dict) -> None:
        """
        Store data associated with the given key.
        
        Args:
            key (str): The key to store the data under.
            value (Dict): The data to store.
        """
        self.storage.setItem(key, json.dumps(value))

    def set_flat(self, data: str) -> None:
        """
        Store data associated with the given key.
        
        Args:
            key (str): The key to store the data under.
            value (Dict): The data to store.
        """
        self.storage.set(json.dumps(data))

    def delete(self, key: str) -> None:
        """
        Delete data associated with the given key.
        
        Args:
            key (str): The key to delete data for.
        """
        self.storage.removeItem(key)