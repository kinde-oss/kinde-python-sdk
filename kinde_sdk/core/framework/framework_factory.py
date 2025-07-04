"""
Framework Factory for creating framework instances.
"""

from typing import Dict, Type, Optional, Any
import importlib
import pkgutil
import logging
import threading
from .framework_interface import FrameworkInterface
from .null_framework import NullFramework

logger = logging.getLogger(__name__)

class FrameworkFactory:
    """
    Factory class for creating framework instances.
    """
    _frameworks = {}
    _initialized = False
    _framework_instance = None
    _lock = threading.RLock()
    
    @classmethod
    def _discover_frameworks(cls) -> None:
        """
        Auto-discover and register available framework implementations.
        This method looks for installed packages that start with 'kinde_' and
        attempts to import and register their framework implementations.
        """
        if cls._initialized:
            return
            
        logger.info("Discovering frameworks")
        
        # First pass: Look for installed packages
        for _, name, is_pkg in pkgutil.iter_modules():
            if is_pkg and name.startswith('kinde_') and name != 'kinde_sdk':
                try:
                    # Import the package
                    importlib.import_module(name)
                    logger.warning(f"Successfully imported framework package: {name}")
                except ImportError as e:
                    logger.warning(f"Failed to import framework package {name}: {str(e)}")
                except Exception as e:
                    logger.warning(f"Unexpected error importing framework package {name}: {str(e)}")
        
        logger.info(f"Framework registry: {list(cls._frameworks.keys())}")
        cls._initialized = True
    
    @classmethod
    def register_framework(cls, name: str, framework_class: Type[FrameworkInterface]) -> None:
        """
        Register a framework implementation.
        
        Args:
            name: The name of the framework
            framework_class: The framework implementation class
        """
        with cls._lock:
            cls._frameworks[name] = framework_class
            logger.warning(f"Registered framework: {name}")
    
    @classmethod
    def get_framework_instance(cls) -> Optional[FrameworkInterface]:
        """
        Get the current framework instance if it exists.
        
        Returns:
            Optional[FrameworkInterface]: The current framework instance or None if not created yet
        """
        with cls._lock:
            return cls._framework_instance
    
    @classmethod
    def create_framework(cls, config: Dict[str, Any], app: Optional[Any] = None) -> FrameworkInterface:
        """
        Create a framework instance or return existing instance if already created.
        Thread-safe implementation.
        
        Args:
            config: Dictionary containing framework configuration
            app: The application instance (optional)
            
        Returns:
            FrameworkInterface: A framework instance
            
        Raises:
            ValueError: If the framework is not found
        """
        with cls._lock:
            # Return existing instance if it exists
            if cls._framework_instance is not None:
                return cls._framework_instance
                
            # Ensure frameworks are discovered
            cls._discover_frameworks()
            
            framework_type = config.get('type')
            if framework_type is None:
                raise ValueError("Framework type not specified in configuration")
                
            # Try to get the framework class
            framework_class = cls._frameworks.get(framework_type)
            if framework_class is None:
                # If not found, try auto-detection
                for name, impl in cls._frameworks.items():
                    # Create an instance to check auto-detection
                    instance = impl(app)
                    if hasattr(instance, 'can_auto_detect') and instance.can_auto_detect():
                        logger.info(f"Auto-detected framework: {name}")
                        framework_class = impl
                        break
                
                if framework_class is None:
                    raise ValueError(f"Framework not found: {framework_type}")
            
            # Create and store the framework instance
            cls._framework_instance = framework_class(app)
            return cls._framework_instance 