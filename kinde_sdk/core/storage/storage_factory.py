
from typing import Dict, Any
from .storage_interface import StorageInterface
from .memory_storage import MemoryStorage
from .local_storage import LocalStorage

class StorageFactory:
    @staticmethod
    def create_storage(config: Dict[str, Any]) -> StorageInterface:
        """
        Create a storage backend based on the provided configuration.

        Args:
            config (Dict[str, Any]): Configuration dictionary containing storage settings.

        Returns:
            StorageInterface: An instance of the requested storage backend.
        """
        storage_type = config.get("type", "memory")  # Default to "memory" if not specified
        options = config.get("options", {})

        if storage_type == "memory":
            return MemoryStorage()
        elif storage_type == "local_storage":
            return LocalStorage()
        # Add more storage types here as needed
        else:
            raise ValueError(f"Unsupported storage type: {storage_type}")