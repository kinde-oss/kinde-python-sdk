from typing import Dict, Type, Optional
from .framework_interface import FrameworkInterface
from .null_framework import NullFramework
from kinde_sdk.framework_detector import FrameworkDetector

class FrameworkFactory:
    """
    Factory class for creating framework instances.
    This factory is responsible for instantiating the appropriate framework implementation
    based on the detected or specified framework.
    """
    
    _framework_registry: Dict[str, Type[FrameworkInterface]] = {}
    
    @classmethod
    def register_framework(cls, framework_name: str, framework_class: Type[FrameworkInterface]) -> None:
        """
        Register a framework implementation.
        
        Args:
            framework_name (str): The name of the framework (e.g., 'fastapi', 'flask')
            framework_class (Type[FrameworkInterface]): The framework implementation class
        """
        cls._framework_registry[framework_name] = framework_class
    
    @classmethod
    def create_framework(cls, framework_name: Optional[str] = None) -> FrameworkInterface:
        """
        Create a framework instance.
        
        Args:
            framework_name (Optional[str]): The name of the framework to create.
                If None, the framework will be auto-detected.
                
        Returns:
            FrameworkInterface: An instance of the requested framework implementation.
                If no framework is specified or detected, returns a NullFramework instance.
        """
        # If framework name is provided, try to create that specific framework
        if framework_name and framework_name in cls._framework_registry:
            return cls._framework_registry[framework_name]()
        
        # If no framework specified, try to detect one
        if not framework_name:
            detector = FrameworkDetector()
            detected_framework = detector.detect_framework(list(cls._framework_registry.keys()))
            if detected_framework and detected_framework in cls._framework_registry:
                return cls._framework_registry[detected_framework]()
        
        # If no framework found or specified, return null framework
        return NullFramework() 