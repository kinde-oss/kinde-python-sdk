from typing import Optional, Dict, Any
from fastapi import FastAPI
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from .fastapi_framework import FastAPIFramework

class FastAPIFrameworkFactory:
    """
    Factory class for creating FastAPI framework instances.
    This factory is responsible for creating and registering FastAPI framework instances.
    """
    
    @staticmethod
    def create_framework(app: Optional[FastAPI] = None) -> FastAPIFramework:
        """
        Create a FastAPI framework instance.
        
        Args:
            app (Optional[FastAPI]): The FastAPI application instance.
                If not provided, a new instance will be created.
                
        Returns:
            FastAPIFramework: A FastAPI framework instance
        """
        return FastAPIFramework(app)
