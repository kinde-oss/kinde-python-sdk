from .framework_interface import FrameworkInterface

class NullFramework(FrameworkInterface):
    """
    A null implementation of the FrameworkInterface.
    This implementation does nothing and is used when no framework is detected or specified.
    """
    
    def get_name(self) -> str:
        """
        Get the name of the framework.
        
        Returns:
            str: The name of the null framework
        """
        return "null"
    
    def get_description(self) -> str:
        """
        Get a description of the framework.
        
        Returns:
            str: A description of the null framework
        """
        return "A null framework implementation that does nothing. Used when no framework is detected or specified."
    
    def start(self) -> None:
        """
        Start the framework.
        This is a no-op in the null implementation.
        """
        pass
    
    def stop(self) -> None:
        """
        Stop the framework.
        This is a no-op in the null implementation.
        """
        pass 