# core/storage/storage_manager.py
import threading
import uuid
import time
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
        self._device_id = None
        self._storage_type = "memory"  # Default storage type

    def initialize(self, config: Dict[str, Any] = None, device_id: Optional[str] = None, storage: Optional[StorageInterface] = None):
        """
        Initialize the storage with the provided configuration.
        
        Args:
            config (Dict[str, Any], optional): Configuration dictionary for storage.
                If None, defaults to in-memory storage.
            device_id (str, optional): A unique identifier for the current device/session.
                If None, a random identifier will be generated.
            storage (StorageInterface, optional): A pre-configured storage instance.
                If provided, this will be used instead of creating a new one.
        """
        with self._lock:
            if config is None:
                config = {"type": "memory"}
                
            # Set storage type
            self._storage_type = config.get("type", "memory")
                
            # Clear any existing storage first
            self._storage = None
            
            # Use provided storage or create new one
            if storage is not None:
                self._storage = storage
            else:
                self._storage = StorageFactory.create_storage(config)
            
            # Set or generate device ID
            if device_id:
                self._device_id = device_id
            elif not self._device_id:
                # Generate a persistent device ID if none provided
                self._device_id = str(uuid.uuid4())
                
            # Store the device ID in storage for persistence
            self._storage.set("_device_id", {"value": self._device_id, "timestamp": time.time()})

    def get_device_id(self) -> str:
        """
        Get the current device ID.
        
        Returns:
            str: The current device ID
        """
        if not self._device_id:
            # Try to load from storage
            stored_device = self.get("_device_id")
            if stored_device and "value" in stored_device:
                self._device_id = stored_device["value"]
            else:
                # Generate a new device ID
                self._device_id = str(uuid.uuid4())
                self.setItems("_device_id", {"value": self._device_id, "timestamp": time.time()})
                
        return self._device_id
    
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

    @property
    def storage_type(self) -> str:
        """
        Get the current storage type.
        
        Returns:
            str: The current storage type
        """
        return self._storage_type

    def _get_namespaced_key(self, key: str) -> str:
        """
        Create a namespaced key that includes the device ID to prevent
        session clashes between same user on different devices.
        
        Args:
            key (str): The original key
            
        Returns:
            str: A namespaced key including device ID
        """
        device_id = self.get_device_id()
        
        # If the key is for the device ID itself, don't namespace it
        if key == "_device_id":
            return key
            
        # Special handling for keys that should be global (shared across devices)
        if key.startswith("global:"):
            return key
            
        # For user-specific but device-independent storage (like OAuth state)
        if key.startswith("user:"):
            return key
            
        # For device-specific user data (default)
        return f"device:{device_id}:{key}"
    
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
            
        namespaced_key = self._get_namespaced_key(key)
        return self._storage.get(namespaced_key)

    def setItems(self, key: str, value: Dict) -> None:
        """
        Store data in storage.
        
        Args:
            key (str): The key to store under.
            value (Dict): The data to store.
        """
        if self._storage is None:
            self.initialize()
            
        namespaced_key = self._get_namespaced_key(key)
        self._storage.set(namespaced_key, value)


    def set(self, access_token : str) -> None:
        """
        Store data in storage.
        
        Args:
            key (str): The key to store under.
            value (Dict): The data to store.
        """
        if self._storage is None:
            self.initialize()
            
        # namespaced_key = self._get_namespaced_key(key)
        self._storage.set_flat(access_token)


    def delete(self, key: str) -> None:
        """
        Delete data from storage by key.
        
        Args:
            key (str): The key to delete.
        """
        if self._storage is None:
            self.initialize()
            
        namespaced_key = self._get_namespaced_key(key)
        self._storage.delete(namespaced_key)

    def clear_device_data(self) -> None:
        """
        Clear all data associated with the current device.
        Useful for complete logout/reset scenarios.
        
        Note: This is implementation dependent and works best with
        storage backends that support prefix-based operations.
        """
        if self._storage is None:
            return
            
        device_id = self.get_device_id()
        prefix = f"device:{device_id}:"
        
        # This is a naive implementation for storage that doesn't support prefix operations
        # For more efficient implementations, extend StorageInterface with prefix operations
        
        # Note: This implementation works with memory storage as a fallback
        # but won't be efficient for all storage types
        if hasattr(self._storage, "clear_prefix"):
            # If the storage implementation supports prefix clearing
            self._storage.clear_prefix(prefix)
        else:
            # Fallback implementation - less efficient
            if hasattr(self._storage, "_storage") and isinstance(self._storage._storage, dict):
                keys_to_delete = [k for k in self._storage._storage.keys() if k.startswith(prefix)]
                for k in keys_to_delete:
                    self._storage.delete(k)

    def reset(self):
        """Reset the storage manager - useful for testing"""
        with self._lock:
            self._storage = None
            self._device_id = None
            self.initialize({"type": "memory"})