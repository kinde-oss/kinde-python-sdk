
from abc import ABC, abstractmethod
from typing import Dict, Optional

class StorageInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Dict]:
        """
        Retrieve data associated with the given key.
        
        Args:
            key (str): The key to retrieve data for.
            
        Returns:
            Optional[Dict]: The stored data or None if not found.
        """
        pass

    @abstractmethod
    def set(self, key: str, value: Dict) -> None:
        """
        Store data associated with the given key.
        
        Args:
            key (str): The key to store the data under.
            value (Dict): The data to store.
        """
        pass

    @abstractmethod
    def set_flat(self, value: str) -> None:
        """
        Store data associated with the given key.
        
        Args:
            key (str): The key to store the data under.
            value (Dict): The data to store.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Delete data associated with the given key.
        
        Args:
            key (str): The key to delete data for.
        """
        pass