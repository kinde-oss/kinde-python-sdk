# core/storage/storage_manager.py
import threading
from typing import Dict, Any, Optional
from .storage_factory import StorageFactory
from .storage_interface import StorageInterface

class StorageManager:
    _instance = None
    _lock = threading.Lock()  # Lock for thread safety
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(StorageManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        # Initialize only once
        if self._initialized:
            return
            
        self._storage = None
        self._initialized = True

    def initialize(self, config: Dict[str, Any] = None):
        """
        Initialize the storage with the provided configuration.
        
        Args:
            config (Dict[str, Any], optional): Configuration dictionary for storage.
                If None, defaults to in-memory storage.
        """
        with self._lock:
            if config is None:
                config = {"type": "memory"}
                
            self._storage = StorageFactory.create_storage(config)

    @property
    def storage(self) -> Optional[StorageInterface]:
        """
        Get the configured storage instance.
        
        Returns:
            StorageInterface: The configured storage instance, or None if not initialized.
        """
        if self._storage is None:
            # Auto-initialize with default memory storage if not set
            self.initialize()
            
        return self._storage

    def get(self, key: str) -> Optional[Dict]:
        """
        Retrieve data from storage by key.
        
        Args:
            key (str): The key to retrieve.
            
        Returns:
            Optional[Dict]: The stored data or None if not found.
        """
        if self._storage is None:
            self.initialize()
            
        return self._storage.get(key)

    def set(self, key: str, value: Dict) -> None:
        """
        Store data in storage.
        
        Args:
            key (str): The key to store under.
            value (Dict): The data to store.
        """
        if self._storage is None:
            self.initialize()
            
        self._storage.set(key, value)

    def delete(self, key: str) -> None:
        """
        Delete data from storage by key.
        
        Args:
            key (str): The key to delete.
        """
        if self._storage is None:
            self.initialize()
            
        self._storage.delete(key)