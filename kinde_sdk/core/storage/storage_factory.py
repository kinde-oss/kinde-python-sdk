from typing import Dict, Any, Optional, Type
from .storage_interface import StorageInterface
from .memory_storage import MemoryStorage
from .local_storage import LocalStorage
from kinde_sdk.core.framework.framework_factory import FrameworkFactory

class StorageFactory:
    _framework_factories = {}
    
    @classmethod
    def register_framework_factory(cls, framework: str, factory_class: Type) -> None:
        """
        Register a framework-specific storage factory.
        
        Args:
            framework (str): The framework name (e.g., 'fastapi', 'flask')
            factory_class (Type): The storage factory class for the framework
        """
        cls._framework_factories[framework] = factory_class
    
    @classmethod
    def create_storage(cls, config: Dict[str, Any], request: Optional[Any] = None) -> StorageInterface:
        """
        Create a storage backend based on the provided configuration and framework detection.

        Args:
            config (Dict[str, Any]): Configuration dictionary containing storage settings.
            request (Optional[Any]): The request object from the framework (if available)

        Returns:
            StorageInterface: An instance of the requested storage backend.
        """
        # If a specific storage type is requested, use that
        storage_type = config.get("type")
        if storage_type:
            if storage_type == "memory":
                return MemoryStorage()
            elif storage_type == "local_storage":
                return LocalStorage()
            else:
                raise ValueError(f"Unsupported storage type: {storage_type}")
        
        # If no specific type, try to use the framework factory
        framework = FrameworkFactory.create_framework()
        framework_name = framework.get_name()
        
        if framework_name in cls._framework_factories:
            factory_class = cls._framework_factories[framework_name]
            return factory_class.create_storage(request, config)
        
        # Default to memory storage if no framework factory registered
        return MemoryStorage()