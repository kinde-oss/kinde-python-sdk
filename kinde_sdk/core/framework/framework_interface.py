from abc import ABC, abstractmethod
from typing import Any, Optional

class FrameworkInterface(ABC):
    """
    Interface for framework implementations.
    This interface defines the contract that all framework implementations must follow.
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the framework.
        
        Returns:
            str: The name of the framework (e.g., 'fastapi', 'flask', 'django')
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get a description of the framework.
        
        Returns:
            str: A description of the framework and its capabilities
        """
        pass
    
    @abstractmethod
    def start(self) -> None:
        """
        Start the framework.
        This method should initialize any necessary framework components.
        """
        pass
    
    @abstractmethod
    def stop(self) -> None:
        """
        Stop the framework.
        This method should clean up any framework resources.
        """
        pass
    
    @abstractmethod
    def get_app(self) -> Any:
        """
        Get the framework application instance.
        
        Returns:
            Any: The framework application instance
        """
        pass
    
    @abstractmethod
    def get_request(self) -> Optional[Any]:
        """
        Get the current request object.
        
        Returns:
            Optional[Any]: The current request object, or None if not available
        """
        pass

    @abstractmethod
    def get_user_id(self) -> Optional[str]:
        """
        Get the user ID from the current request.
        
        Returns:
            Optional[str]: The user ID, or None if not available
        """
        pass
    
    @abstractmethod
    def can_auto_detect(self) -> bool:
        """
        Check if this framework can be auto-detected.
        
        Returns:
            bool: True if the framework can be auto-detected, False otherwise
        """
        return False 