from typing import Optional, Dict, Any
from fastapi import Request, Depends
from fastapi.responses import RedirectResponse
from kinde_sdk.auth.oauth import OAuth
from .storage.fastapi_storage_factory import FastAPIStorageFactory

class KindeFastAPI:
    """
    FastAPI integration for Kinde authentication.
    """
    
    def __init__(
        self,
        framework: Optional[str] = "fastapi",
    ):
        """
        Initialize the Kinde FastAPI integration.
        
        Args:
            client_id (str): Your Kinde client ID.
            client_secret (str): Your Kinde client secret.
            redirect_uri (str): The redirect URI for your application.
            auth_url (str): The Kinde authorization URL.
            token_url (str): The Kinde token URL.
            logout_url (str): The Kinde logout URL.
            audience (Optional[str]): The audience for your application.
            host (Optional[str]): The Kinde host URL.
        """
        # Create a storage factory that can be used by the OAuth class
        self.storage_factory = FastAPIStorageFactory()
        
        # Initialize OAuth with the FastAPI storage factory
        self.oauth = OAuth(
            framework=framework,
            storage_factory=self.storage_factory,  # Pass the storage factory to OAuth
        )
        
    def get_login_url(self, request: Request, state: Optional[str] = None) -> str:
        """
        Get the login URL for user authentication.
        
        Args:
            request (Request): The FastAPI request object.
            state (Optional[str]): Optional state parameter for the OAuth flow.
            
        Returns:
            str: The login URL.
        """
        # Pass the request to the storage factory
        self.storage_factory.request = request
        return self.oauth.get_login_url(state)
        
    def get_logout_url(self, request: Request) -> str:
        """
        Get the logout URL.
        
        Args:
            request (Request): The FastAPI request object.
            
        Returns:
            str: The logout URL.
        """
        # Pass the request to the storage factory
        self.storage_factory.request = request
        return self.oauth.logout(request.session.get("user_id"))
        
    def get_user_info(self, request: Request) -> Dict[str, Any]:
        """
        Get the user information from the session.
        
        Args:
            request (Request): The FastAPI request object.
            
        Returns:
            Dict[str, Any]: The user information.
            
        Raises:
            ValueError: If the user is not authenticated.
        """
        # Pass the request to the storage factory
        self.storage_factory.request = request
        user_id = request.session.get("user_id")
        if not user_id:
            raise ValueError("User not authenticated")
            
        return self.oauth.get_user_info(user_id)
        
    def is_authenticated(self, request: Request) -> bool:
        """
        Check if the user is authenticated.
        
        Args:
            request (Request): The FastAPI request object.
            
        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return "user_id" in request.session
        
    def login_required(self, request: Request) -> None:
        """
        Check if the user is authenticated and redirect to login if not.
        
        Args:
            request (Request): The FastAPI request object.
            
        Returns:
            RedirectResponse: A redirect to the login page if the user is not authenticated.
        """
        if not self.is_authenticated(request):
            return RedirectResponse(url=self.get_login_url(request)) 