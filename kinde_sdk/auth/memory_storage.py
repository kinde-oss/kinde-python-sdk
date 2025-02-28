# memory_storage.py
from typing import Dict, Optional
from .storage_interface import StorageInterface

class MemoryStorage(StorageInterface):
    def __init__(self):
        self._storage = {}

    def get(self, key: str) -> Optional[Dict]:
        """Retrieve data associated with the given key."""
        return self._storage.get(key)

    def set(self, key: str, value: Dict) -> None:
        """Store data associated with the given key."""
        self._storage[key] = value

    def delete(self, key: str) -> None:
        """Delete data associated with the given key."""
        if key in self._storage:
            del self._storage[key]