from typing import Dict, Any, Optional, Type
from .storage_interface import StorageInterface
from .memory_storage import MemoryStorage
from .local_storage import LocalStorage
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
import logging

logger = logging.getLogger(__name__)

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
        logger.warning(f"Registering storage factory: {framework}")
        cls._framework_factories[framework] = factory_class
    
    @classmethod
    def create_storage(cls, config: Dict[str, Any]) -> StorageInterface:
        """
        Create a storage backend based on the provided configuration and framework detection.

        Args:
            config (Dict[str, Any]): Configuration dictionary containing storage settings.

        Returns:
            StorageInterface: An instance of the requested storage backend.
        """
        # If a specific storage type is requested, use that
        storage_type = config.get("type")
        if storage_type:
            # Check if it's a framework-specific storage type
            logger.warning(f"Storage type: {storage_type}")
            logger.warning(f"Framework factories: {cls._framework_factories}")
            if storage_type in cls._framework_factories:
                try:
                    factory_class = cls._framework_factories[storage_type]
                    return factory_class.create_storage(config)
                except Exception as e:
                    logger.warning(f"Failed to create {storage_type} storage, falling back to memory storage: {str(e)}")
                    return MemoryStorage()
            # Handle built-in storage types
            elif storage_type == "memory":
                return MemoryStorage()
            elif storage_type == "local_storage":
                return LocalStorage()
            else:
                logger.warning(f"Unsupported storage type: {storage_type}, falling back to memory storage")
                return MemoryStorage()
        
        # If no specific type, try to use the framework factory
        framework = FrameworkFactory.create_framework()
        framework_name = framework.get_name()
        
        if framework_name in cls._framework_factories:
            factory_class = cls._framework_factories[framework_name]
            return factory_class.create_storage(config)
        
        # If all else fails, use memory storage
        logger.warning("No storage type specified and auto-detection failed, using memory storage")
        return MemoryStorage()