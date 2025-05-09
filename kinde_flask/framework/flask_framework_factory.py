from typing import Optional
from flask import Flask
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from .flask_framework import FlaskFramework

class FlaskFrameworkFactory:
    """
    Factory class for creating Flask framework instances.
    This factory is responsible for creating and registering Flask framework instances.
    """
    
    @staticmethod
    def create_framework(app: Optional[Flask] = None) -> FlaskFramework:
        """
        Create a Flask framework instance.
        
        Args:
            app (Optional[Flask]): The Flask application instance.
                If not provided, a new instance will be created.
                
        Returns:
            FlaskFramework: A Flask framework instance
        """
        return FlaskFramework(app) 