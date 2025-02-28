# storage_interface.py
from abc import ABC, abstractmethod
from typing import Dict, Optional

class StorageInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Dict]:
        """Retrieve data associated with the given key."""
        pass

    @abstractmethod
    def set(self, key: str, value: Dict) -> None:
        """Store data associated with the given key."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete data associated with the given key."""
        pass