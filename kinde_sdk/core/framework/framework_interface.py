from abc import ABC, abstractmethod
from typing import Optional

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