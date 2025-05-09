from typing import Optional, Dict, Any
from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from kinde_sdk.core.framework.framework_interface import FrameworkInterface
from kinde_sdk.auth.oauth import OAuth
from ..middleware.framework_middleware import FrameworkMiddleware
import os
import uuid
import logging

logger = logging.getLogger(__name__)

class FastAPIFramework(FrameworkInterface):
    """
    FastAPI framework implementation.
    This class provides FastAPI-specific functionality and integration.
    """
    
    def __init__(self, app: Optional[FastAPI] = None):
        """
        Initialize the FastAPI framework.
        
        Args:
            app (Optional[FastAPI]): The FastAPI application instance.
                If not provided, a new instance will be created.
        """
        self.app = app or FastAPI()
        self._initialized = False
        self._oauth = None
    
    def get_name(self) -> str:
        """
        Get the name of the framework.
        
        Returns:
            str: The name of the framework
        """
        return "fastapi"
    
    def get_description(self) -> str:
        """
        Get a description of the framework.
        
        Returns:
            str: A description of the framework
        """
        return "FastAPI framework implementation for Kinde authentication"
    
    def start(self) -> None:
        """
        Start the framework.
        This method initializes any necessary FastAPI components and registers Kinde routes.
        """
        if not self._initialized:
            # Add session middleware with proper configuration
            self.app.add_middleware(
                SessionMiddleware,
                secret_key=os.getenv("SECRET_KEY", "your-secret-key"),
                #session_cookie="kinde_session",
                max_age=3600,  # 1 hour
                same_site="lax",  # Protect against CSRF
                https_only=False,  # Set to True in production
                path="/"  # Ensure cookie is available for all paths
            )
            
            # Add framework middleware
            self.app.add_middleware(FrameworkMiddleware)
            
            # Register Kinde routes
            self._register_kinde_routes()
            
            self._initialized = True
    
    def stop(self) -> None:
        """
        Stop the framework.
        This method cleans up any FastAPI resources.
        """
        if self._initialized:
            self._initialized = False
    
    def get_app(self) -> FastAPI:
        """
        Get the FastAPI application instance.
        
        Returns:
            FastAPI: The FastAPI application instance
        """
        return self.app
    
    def get_request(self) -> Optional[Request]:
        """
        Get the current request object.
        
        Returns:
            Optional[Request]: The current FastAPI request object, if available
        """
        from kinde_sdk.core.framework.framework_context import FrameworkContext
        return FrameworkContext.get_request()
    
    def set_oauth(self, oauth: OAuth) -> None:
        """
        Set the OAuth instance for this framework.
        
        Args:
            oauth (OAuth): The OAuth instance
        """
        self._oauth = oauth
    
    def _register_kinde_routes(self) -> None:
        """
        Register all Kinde-specific routes with the FastAPI application.
        """
        # Helper function to get current user
        async def get_current_user(request: Request):
            if not self._oauth.is_authenticated(request):
                return None
            try:
                return self._oauth.get_user_info(request)
            except ValueError:
                return None
        
        # Login route
        @self.app.get("/login")
        async def login(request: Request):
            """Redirect to Kinde login page."""
            request.session["testvalue"] = "123"
            return RedirectResponse(url=await self._oauth.login())
        
        # Callback route
        @self.app.get("/callback")
        async def callback(request: Request, code: str, state: Optional[str] = None):
            """Handle the OAuth callback from Kinde."""
            try:
                # Generate a unique user ID for the session
                user_id = request.session.get("user_id") or str(uuid.uuid4())
                
                # Use OAuth's handle_redirect method to process the callback
                result = await self._oauth.handle_redirect(code, user_id, state)
                
                # Store user ID in session
                request.session["user_id"] = user_id
                
                # Create response with explicit session cookie settings
                response = RedirectResponse(url="/")
                response.set_cookie(
                    key="kinde_session",
                    value=request.cookies.get("kinde_session", ""),
                    max_age=3600,
                    httponly=True,
                    samesite="lax"
                )
                return response
            except Exception as e:
                logger.error(f"Authentication failed: {str(e)}")
                return HTMLResponse(f"Authentication failed: {str(e)}")
        
        # Logout route
        @self.app.get("/logout")
        async def logout(request: Request):
            """Logout the user and redirect to Kinde logout page."""
            request.session.clear()
            return RedirectResponse(url=await self._oauth.logout())
        
        # Register route
        @self.app.get("/register")
        async def register(request: Request):
            """Redirect to Kinde registration page."""
            return RedirectResponse(url=await self._oauth.register())
        
        # User info route
        @self.app.get("/user")
        async def get_user(request: Request):
            """Get the current user's information."""
            if not self._oauth.is_authenticated(request):
                return RedirectResponse(url=await self._oauth.login())
            return self._oauth.get_user_info(request)
    
    def can_auto_detect(self) -> bool:
        """
        Check if this framework can be auto-detected.
        
        Returns:
            bool: True if FastAPI is installed and available
        """
        try:
            import fastapi
            return True
        except ImportError:
            return False 