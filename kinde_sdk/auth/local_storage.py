# local_storage.py
from typing import Dict, Optional
import json
from .storage_interface import StorageInterface

class LocalStorage(StorageInterface):
    def __init__(self):
        # In a browser environment, `localStorage` is available globally.
        # For testing in a non-browser environment, you can mock this.
        self.storage = localStorage

    def get(self, key: str) -> Optional[Dict]:
        """Retrieve data associated with the given key."""
        data = self.storage.getItem(key)
        return json.loads(data) if data else None

    def set(self, key: str, value: Dict) -> None:
        """Store data associated with the given key."""
        self.storage.setItem(key, json.dumps(value))

    def delete(self, key: str) -> None:
        """Delete data associated with the given key."""
        self.storage.removeItem(key)