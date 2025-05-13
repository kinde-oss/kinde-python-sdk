from typing import Optional, Callable
from flask import request, Response, session
from kinde_sdk.core.framework.framework_context import FrameworkContext
import logging

logger = logging.getLogger(__name__)

class FrameworkMiddleware:
    """
    Middleware for handling Flask-specific request/response processing.
    """
    
    @staticmethod
    def before_request() -> None:
        """
        Process the request before it reaches the route handler.
        Sets up the framework context with the current request.
        """
        FrameworkContext.set_request(request)
        
    @staticmethod
    def after_request(response: Response) -> Response:
        """
        Process the response after it leaves the route handler.
        
        Args:
            response (Response): The Flask response object.
            
        Returns:
            Response: The processed response.
        """
        # Clear the framework context
        FrameworkContext.clear_request()
        return response 