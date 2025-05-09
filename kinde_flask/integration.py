from typing import Optional, Dict, Any
from flask import Flask, request, redirect, session
from kinde_sdk.auth.oauth import OAuth
from .storage.flask_storage_factory import FlaskStorageFactory
from .middleware.framework_middleware import FrameworkMiddleware

class KindeFlask:
    """
    Flask integration for Kinde authentication.
    """
    
    def __init__(
        self,
        app: Optional[Flask] = None,
        framework: Optional[str] = "flask",
    ):
        """
        Initialize the Kinde Flask integration.
        
        Args:
            app (Optional[Flask]): The Flask application instance.
            framework (Optional[str]): The framework name.
        """
        self.app = app
        if app:
            # Add the framework middleware
            app.before_request(FrameworkMiddleware.before_request)
            app.after_request(FrameworkMiddleware.after_request)
        
        # Create a storage factory that can be used by the OAuth class
        self.storage_factory = FlaskStorageFactory()
        
        # Initialize OAuth with the Flask storage factory
        self.oauth = OAuth(
            framework=framework,
            storage_factory=self.storage_factory,
        )
        
    def get_login_url(self, state: Optional[str] = None) -> str:
        """
        Get the login URL for user authentication.
        
        Args:
            state (Optional[str]): Optional state parameter for the OAuth flow.
            
        Returns:
            str: The login URL.
        """
        return self.oauth.get_login_url(state)
        
    def get_logout_url(self) -> str:
        """
        Get the logout URL.
        
        Returns:
            str: The logout URL.
        """
        return self.oauth.logout()
        
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get the user information from the session.
        
        Returns:
            Dict[str, Any]: The user information.
            
        Raises:
            ValueError: If the user is not authenticated.
        """
        user_id = self._get_user_id()
        if not user_id:
            raise ValueError("User not authenticated")
            
        return self.oauth.get_user_info(user_id)
        
    def is_authenticated(self) -> bool:
        """
        Check if the user is authenticated.
        
        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return self._get_user_id() is not None
        
    def login_required(self) -> redirect:
        """
        Check if the user is authenticated and redirect to login if not.
        
        Returns:
            redirect: A redirect to the login page if the user is not authenticated.
        """
        if not self.is_authenticated():
            return redirect(self.get_login_url())
            
    def _get_user_id(self) -> Optional[str]:
        """
        Get the current user ID from the session.
        
        Returns:
            Optional[str]: The user ID, or None if not authenticated.
        """
        return session.get("user_id")
        
    def _get_current_request(self) -> Optional[request]:
        """
        Get the current request from the framework context.
        
        Returns:
            Optional[request]: The current request, or None if not available.
        """
        from kinde_sdk.core.framework.framework_context import FrameworkContext
        return FrameworkContext.get_request() 