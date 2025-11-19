
from typing import Dict, Optional
from .storage_interface import StorageInterface

class MemoryStorage(StorageInterface):
    def __init__(self):
        self._storage = {}
        self._flat_storage = []

    def get(self, key: str) -> Optional[Dict]:
        """
        Retrieve data associated with the given key.
        
        Args:
            key (str): The key to retrieve data for.
            
        Returns:
            Optional[Dict]: The stored data or None if not found.
        """
        return self._storage.get(key)

    def set(self, key: str, value: Dict) -> None:
        """
        Store data associated with the given key.
        
        Args:
            key (str): The key to store the data under.
            value (Dict): The data to store.
        """
        self._storage[key] = value

    def set_flat(self, data: str) -> None:
        """
        Store data associated with the given key.
        
        Args:
            key (str): The key to store the data under.
            value (Dict): The data to store.
        """
        self._flat_storage = data

    def delete(self, key: str) -> None:
        """
        Delete data associated with the given key.
        
        Args:
            key (str): The key to delete data for.
        """
        if key in self._storage:
            del self._storage[key]