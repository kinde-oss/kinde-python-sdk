from typing import Optional, Dict, Any, TYPE_CHECKING
from flask import Flask, request, redirect, session
from kinde_sdk.core.framework.framework_interface import FrameworkInterface
from kinde_sdk.auth.oauth import OAuth
from ..middleware.framework_middleware import FrameworkMiddleware
import os
import uuid
import asyncio
import threading
import logging
import nest_asyncio
from flask_session import Session

if TYPE_CHECKING:
    from flask import Request

class FlaskFramework(FrameworkInterface):
    """
    Flask framework implementation.
    This class provides Flask-specific functionality and integration.
    """
    
    def __init__(self, app: Optional[Flask] = None):
        """
        Initialize the Flask framework.
        
        Args:
            app (Optional[Flask]): The Flask application instance.
                If not provided, a new instance will be created.
        """
        self.app = app or Flask(__name__)
        self._initialized = False
        self._oauth = None
        
        # Configure Flask session
        self.app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
        self.app.config['SESSION_TYPE'] = 'filesystem'
        self.app.config['SESSION_PERMANENT'] = False
        
        # Enable nested event loops
        nest_asyncio.apply()
    
    def get_name(self) -> str:
        """
        Get the name of the framework.
        
        Returns:
            str: The name of the framework
        """
        return "flask"
    
    def get_description(self) -> str:
        """
        Get a description of the framework.
        
        Returns:
            str: A description of the framework
        """
        return "Flask framework implementation for Kinde authentication"
    
    def start(self) -> None:
        """
        Start the framework.
        This method initializes any necessary Flask components and registers Kinde routes.
        """
        if not self._initialized:
            # Add framework middleware
            self.app.before_request(FrameworkMiddleware.before_request)
            self.app.after_request(FrameworkMiddleware.after_request)
            
            # Register Kinde routes
            self._register_kinde_routes()
            
            self._initialized = True
    
    def stop(self) -> None:
        """
        Stop the framework.
        This method cleans up any Flask resources.
        """
        if self._initialized:
            self._initialized = False
    
    def get_app(self) -> Flask:
        """
        Get the Flask application instance.
        
        Returns:
            Flask: The Flask application instance
        """
        return self.app
    
    def get_request(self) -> Optional['Request']:
        """
        Get the current request object.
        
        Returns:
            Optional[Request]: The current Flask request object, if available
        """
        from kinde_sdk.core.framework.framework_context import FrameworkContext
        return FrameworkContext.get_request()
    
    def get_user_id(self) -> Optional[str]:
        """
        Get the user ID from the current request.
        
        Returns:
            Optional[str]: The user ID, or None if not available
        """
        session_id = session.get('user_id')
        if not session_id:
            return None
        return session_id
    
    def set_oauth(self, oauth: OAuth) -> None:
        """
        Set the OAuth instance for this framework.
        
        Args:
            oauth (OAuth): The OAuth instance
        """
        self._oauth = oauth
    
    def _register_kinde_routes(self) -> None:
        """
        Register all Kinde-specific routes with the Flask application.
        """
        # Login route
        @self.app.route('/login')
        def login():
            """Redirect to Kinde login page."""
            loop = asyncio.get_event_loop()
            login_url = loop.run_until_complete(self._oauth.login())
            return redirect(login_url)
        

        # Callback route
        @self.app.route('/callback')
        def callback():
            """Handle the OAuth callback from Kinde."""
            try:
                code = request.args.get('code')
                state = request.args.get('state')
                
                if not code:
                    return "Authentication failed: No code provided", 400
                
                # Generate a unique user ID for the session
                user_id = session.get('user_id') or str(uuid.uuid4())
                
                # Use OAuth's handle_redirect method to process the callback
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(self._oauth.handle_redirect(code, user_id, state))
                
                # Store user ID in session
                session['user_id'] = user_id
                
                return redirect('/')
            except Exception as e:
                return f"Authentication failed: {str(e)}", 400
        
        # Logout route
        @self.app.route('/logout')
        def logout():
            """Logout the user and redirect to Kinde logout page."""
            user_id = session.get('user_id')
            session.clear()
            loop = asyncio.get_event_loop()
            logout_url = loop.run_until_complete(self._oauth.logout(user_id))
            return redirect(logout_url)
        
        # Register route
        @self.app.route('/register')
        def register():
            """Redirect to Kinde registration page."""
            loop = asyncio.get_event_loop()
            register_url = loop.run_until_complete(self._oauth.register())
            return redirect(register_url)
        
        # User info route
        @self.app.route('/user')
        def get_user():
            """Get the current user's information."""
            try:
                if not self._oauth.is_authenticated(request):
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        login_url = loop.run_until_complete(self._oauth.login())
                        return redirect(login_url)
                    finally:
                        loop.close()
                
                return self._oauth.get_user_info(request)
            except Exception as e:
                return f"Failed to get user info: {str(e)}", 400
    
    def can_auto_detect(self) -> bool:
        """
        Check if this framework can be auto-detected.
        
        Returns:
            bool: True if Flask is installed and available
        """
        try:
            import flask
            return True
        except ImportError:
            return False 