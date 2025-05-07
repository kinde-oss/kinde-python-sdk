from typing import Dict, Any
from fastapi import Request
from kinde_sdk.core.storage.storage_interface import StorageInterface
from kinde_sdk.core.storage.storage_factory import StorageFactory
from .fastapi_storage import FastAPIStorage

class FastAPIStorageFactory:
    """
    Factory class for creating FastAPI storage instances.
    """
    
    @staticmethod
    def create_storage(request: Request, config: Dict[str, Any] = None) -> StorageInterface:
        """
        Create a FastAPI storage instance.
        
        Args:
            request (Request): The FastAPI request object that contains the session.
            config (Dict[str, Any], optional): Configuration dictionary. Not used in this implementation
                but kept for consistency with other storage factories.
                
        Returns:
            StorageInterface: A FastAPI storage instance.
        """
        return FastAPIStorage(request)

# Register the FastAPI storage factory
StorageFactory.register_framework_factory("fastapi", FastAPIStorageFactory) 