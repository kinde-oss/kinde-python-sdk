from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from kinde_sdk.core.framework.framework_context import FrameworkContext

class FrameworkMiddleware(BaseHTTPMiddleware):
    """
    Middleware that sets the current request in the framework context.
    This allows framework-specific storage implementations to access the current request
    without needing to pass it through the entire call chain.
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process the request and set it in the framework context.
        
        Args:
            request (Request): The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            Response: The response from the next middleware or route handler
        """
        # Set the request in the context
        FrameworkContext.set_request(request)
        try:
            # Process the request
            response = await call_next(request)
            return response
        finally:
            # Clean up the context
            FrameworkContext.clear_request() 