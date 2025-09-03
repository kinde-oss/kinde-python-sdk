"""
Route Protection Middleware for Kinde Python SDK.

This module provides automatic route protection middleware that integrates with popular
Python web frameworks (Flask, FastAPI, etc.) to enforce role-based and permission-based
access control before requests reach route handlers.

Features:
- Framework-agnostic base middleware class
- Flask-specific middleware implementation  
- FastAPI-specific middleware implementation
- Customizable error handling
- Skip patterns for public routes
- Integration with OAuth route protection configuration

Usage:

Flask:
    from kinde_sdk.auth import OAuth
    from kinde_sdk.auth.route_middleware import FlaskRouteProtectionMiddleware
    
    app = Flask(__name__)
    oauth = OAuth(framework="flask", app=app, route_protection_file="routes.yaml")
    
    middleware = FlaskRouteProtectionMiddleware(
        oauth, 
        skip_patterns=["/health", "/public/*"]
    )
    app.before_request(middleware.before_request)

FastAPI:
    from kinde_sdk.auth import OAuth
    from kinde_sdk.auth.route_middleware import FastAPIRouteProtectionMiddleware
    
    app = FastAPI()
    oauth = OAuth(framework="fastapi", app=app, route_protection_file="routes.yaml")
    
    app.add_middleware(
        FastAPIRouteProtectionMiddleware,
        oauth_client=oauth,
        skip_patterns=["/health", "/docs"]
    )
"""

import logging
import asyncio
from typing import Optional, Any, Dict, Callable, List, Union, Tuple
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class RouteProtectionMiddleware(ABC):
    """
    Abstract base class for route protection middleware.
    
    This class provides the core logic for route protection that can be implemented
    by framework-specific middleware classes.
    """
    
    def __init__(
        self, 
        oauth_client: Any,
        error_handler: Optional[Callable] = None,
        skip_patterns: Optional[List[str]] = None
    ):
        """
        Initialize route protection middleware.
        
        Args:
            oauth_client: OAuth client instance with route protection configured
            error_handler: Optional custom error handler function
            skip_patterns: Optional list of path patterns to skip protection (e.g., ["/health", "/public/*"])
        """
        self.oauth_client = oauth_client
        self.error_handler = error_handler or self._default_error_handler
        self.skip_patterns = skip_patterns or []
        self._logger = logging.getLogger("kinde_sdk.route_middleware")
    
    @abstractmethod
    def _default_error_handler(self, reason: str, **kwargs) -> Any:
        """
        Default error handler for access denied responses.
        Must be implemented by framework-specific subclasses.
        """
        pass
    
    @abstractmethod
    def _get_request_info(self, request: Any) -> Tuple[str, str]:
        """
        Extract path and method from framework-specific request object.
        Must be implemented by framework-specific subclasses.
        
        Returns:
            Tuple of (path, method)
        """
        pass
    
    async def validate_request_access(self, request: Any) -> Optional[Any]:
        """
        Core validation logic that can be used by framework-specific implementations.
        
        Args:
            request: Framework-specific request object
            
        Returns:
            None if access granted, error response if denied
        """
        # Check if route protection is enabled
        if not hasattr(self.oauth_client, 'is_route_protection_enabled') or not self.oauth_client.is_route_protection_enabled():
            return None
        
        # Extract request information
        path, method = self._get_request_info(request)
        
        # Check skip patterns
        if self._should_skip_protection(path):
            self._logger.debug(f"Skipping protection for {method} {path} (matches skip pattern)")
            return None
        
        try:
            # Validate route access
            if hasattr(self.oauth_client, 'validate_route_access'):
                result = await self.oauth_client.validate_route_access(path, method)
            else:
                self._logger.warning("OAuth client does not support route protection")
                return None
            
            if not result.get("allowed", False):
                reason = result.get("reason", "Access denied")
                self._logger.info(f"Access denied for {method} {path}: {reason}")
                return self.error_handler(reason, path=path, method=method, result=result)
            
        except (AttributeError, KeyError, TypeError) as e:
            self._logger.exception("Error during route protection validation")
            # Fail closed - deny access if validation fails
            return self.error_handler(f"Route protection validation failed: {e!s}", path=path, method=method)
        except Exception as e:
            self._logger.exception("Unexpected error during route protection validation")
            return self.error_handler(f"Route protection validation failed: {e!s}", path=path, method=method)
        
        return None
    
    def _should_skip_protection(self, path: str) -> bool:
        """
        Check if the given path matches any skip patterns.
        
        Args:
            path: Request path to check
            
        Returns:
            True if protection should be skipped for this path
        """
        for pattern in self.skip_patterns:
            if self._path_matches_pattern(path, pattern):
                return True
        return False
    
    def _path_matches_pattern(self, path: str, pattern: str) -> bool:
        """
        Check if a path matches a skip pattern.
        
        Supports simple wildcards:
        - "/public/*" matches "/public/info", "/public/docs/api", etc.
        - "/health" matches exactly "/health"
        
        Args:
            path: Request path
            pattern: Skip pattern
            
        Returns:
            True if path matches pattern
        """
        # Normalize paths but preserve root '/'
        if path != '/':
            path = path.rstrip('/')
        if pattern != '/':
            pattern = pattern.rstrip('/')
        
        # Exact match
        if pattern == path:
            return True
        
        # Wildcard match
        if pattern.endswith('/*'):
            pattern_prefix = pattern[:-2]  # Remove /*
            # Ensure we're matching a path segment boundary
            return path == pattern_prefix or path.startswith(pattern_prefix + '/')
        
        return False


# Flask Integration
try:
    from flask import request as flask_request, jsonify as flask_jsonify
    
    class FlaskRouteProtectionMiddleware(RouteProtectionMiddleware):
        """
        Flask-specific route protection middleware.
        
        Usage:
            middleware = FlaskRouteProtectionMiddleware(oauth_client)
            app.before_request(middleware.before_request)
        """
        
        def _default_error_handler(self, reason: str, **kwargs) -> Any:
            """Default Flask error handler returns JSON response."""
            return flask_jsonify({"error": "Access Denied"}), 403
        
        def _get_request_info(self, request: Any) -> Tuple[str, str]:
            """Extract path and method from Flask request."""
            return request.path, request.method
        
        def before_request(self) -> Optional[Any]:
            """
            Flask before_request handler.
            
            Usage:
                app.before_request(middleware.before_request)
            """
            # Use asyncio.run to handle async validation in sync Flask context
            try:
                # Flask is synchronous, so asyncio.run should be safe here
                # But let's still check for running loops to be extra safe
                try:
                    loop = asyncio.get_running_loop()
                    if loop.is_running():
                        self._logger.warning(
                            "Unexpected: running event loop detected in Flask middleware. "
                            "This may cause issues with route protection."
                        )
                except RuntimeError:
                    # No running loop, which is expected for Flask
                    pass
                    
                return asyncio.run(self.validate_request_access(flask_request))
            except Exception:
                self._logger.exception("Error in Flask route protection")
                return self.error_handler("Route protection error")

except ImportError:
    # Flask not available
    FlaskRouteProtectionMiddleware = None


# FastAPI Integration  
try:
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import JSONResponse
    from starlette.requests import Request as StarletteRequest
    
    class FastAPIRouteProtectionMiddleware(BaseHTTPMiddleware):
        """
        FastAPI/Starlette-specific route protection middleware.
        
        Usage:
            app.add_middleware(
                FastAPIRouteProtectionMiddleware,
                oauth_client=oauth,
                skip_patterns=["/docs", "/openapi.json"]
            )
        """
        
        def __init__(
            self, 
            app, 
            oauth_client: Any,
            error_handler: Optional[Callable] = None,
            skip_patterns: Optional[List[str]] = None
        ):
            super().__init__(app)
            # Create a concrete implementation
            outer_self = self
            class ConcreteProtectionMiddleware(RouteProtectionMiddleware):
                def _default_error_handler(inner_self, reason: str, **kwargs) -> Any:
                    return (error_handler or outer_self._default_error_handler)(reason, **kwargs)
                
                def _get_request_info(inner_self, request: Any) -> Tuple[str, str]:
                    return outer_self._get_request_info(request)
            
            self.protection_middleware = ConcreteProtectionMiddleware(
                oauth_client=oauth_client,
                error_handler=error_handler or self._default_error_handler,
                skip_patterns=skip_patterns
            )
        
        def _default_error_handler(self, reason: str, **kwargs) -> JSONResponse:
            """Default FastAPI error handler."""
            return JSONResponse(
                status_code=403,
                content={"error": "Access Denied"}
            )
        
        def _get_request_info(self, request: StarletteRequest) -> Tuple[str, str]:
            """Extract path and method from FastAPI/Starlette request."""
            return str(request.url.path), request.method
        
        # Override the RouteProtectionMiddleware method to work with FastAPI request objects
        def _get_request_info_for_middleware(self, request: StarletteRequest) -> Tuple[str, str]:
            return str(request.url.path), request.method
        
        # Monkey patch the method for this instance
        def __init_subclass__(cls, **kwargs):
            super().__init_subclass__(**kwargs)
        
        async def dispatch(self, request: StarletteRequest, call_next):
            """FastAPI middleware dispatch method."""
            # Temporarily override the method for this request
            original_get_request_info = self.protection_middleware._get_request_info
            self.protection_middleware._get_request_info = lambda req: self._get_request_info_for_middleware(req)
            
            try:
                # Check route protection
                error_response = await self.protection_middleware.validate_request_access(request)
                if error_response:
                    return error_response
                
                # Continue to next middleware/route handler
                response = await call_next(request)
                return response
                
            finally:
                # Restore original method
                self.protection_middleware._get_request_info = original_get_request_info

except ImportError:
    # FastAPI/Starlette not available
    FastAPIRouteProtectionMiddleware = None


# Generic middleware factory function
def create_route_protection_middleware(
    framework: str,
    oauth_client: Any,
    app: Optional[Any] = None,
    **kwargs
) -> Optional[Any]:
    """
    Factory function to create framework-specific route protection middleware.
    
    Args:
        framework: Framework name ("flask" or "fastapi")
        oauth_client: OAuth client with route protection configured
        app: Framework app instance (required for some frameworks)
        **kwargs: Additional arguments passed to middleware constructor
        
    Returns:
        Framework-specific middleware instance or None if framework not supported
        
    Example:
        middleware = create_route_protection_middleware(
            framework="flask",
            oauth_client=oauth,
            skip_patterns=["/health", "/public/*"]
        )
        
        if middleware:
            app.before_request(middleware.before_request)
    """
    framework = framework.lower()
    
    if framework == "flask" and FlaskRouteProtectionMiddleware:
        return FlaskRouteProtectionMiddleware(oauth_client, **kwargs)
    
    elif framework == "fastapi" and FastAPIRouteProtectionMiddleware:
        if not app:
            raise ValueError("FastAPI middleware requires 'app' parameter")
        # Return class and kwargs for FastAPI's app.add_middleware()
        return {
            "middleware_class": FastAPIRouteProtectionMiddleware,
            "oauth_client": oauth_client,
            **kwargs
        }
    
    else:
        logger.warning(f"Route protection middleware not available for framework: {framework}")
        return None
