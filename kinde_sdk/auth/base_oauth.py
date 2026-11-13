"""
Base OAuth class that defines the interface for both sync and async operations.
This provides a clear contract for what methods should be available in both contexts.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union

class BaseOAuth(ABC):
    """
    Abstract base class defining the OAuth interface.
    This ensures consistency between sync and async implementations.
    """
    
    @abstractmethod
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated."""
        pass
    
    @abstractmethod
    def get_user_info(self) -> Dict[str, Any]:
        """Get user information."""
        pass
    
    @abstractmethod
    def get_tokens(self, user_id: str) -> Dict[str, Any]:
        """Get tokens for a user."""
        pass
    
    @abstractmethod
    async def generate_auth_url(
        self,
        route_type: Any = None,
        login_options: Dict[str, Any] = None,
        disable_url_sanitization: bool = False
    ) -> Dict[str, Any]:
        """Generate authentication URL."""
        pass
    
    @abstractmethod
    async def login(self, login_options: Dict[str, Any] = None) -> str:
        """Generate login URL."""
        pass
    
    @abstractmethod
    async def register(self, login_options: Dict[str, Any] = None) -> str:
        """Generate registration URL."""
        pass
    
    @abstractmethod
    async def logout(self, user_id: Optional[str] = None, logout_options: Dict[str, Any] = None) -> str:
        """Generate logout URL."""
        pass
    
    @abstractmethod
    async def handle_redirect(
        self,
        code: Optional[str],
        user_id: Optional[str],
        state: Optional[str] = None,
        error: Optional[str] = None,
        error_description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Handle OAuth redirect."""
        pass

    # Step-up authentication (RFC 9470). These are not abstract, so that
    # existing subclasses keep working.

    async def step_up(
        self,
        acr: Optional[Union[str, List[str]]] = None,
        max_age: Optional[int] = None,
        login_options: Optional[Dict[str, Any]] = None,
        post_login_redirect_url: Optional[str] = None,
    ) -> str:
        """Generate the URL for a step-up authentication request."""
        raise NotImplementedError

    def get_authentication_context(self) -> Dict[str, Any]:
        """Get the acr, amr and auth_time of the current session."""
        raise NotImplementedError

    def has_authentication_context(
        self,
        acr: Optional[Union[str, List[str]]] = None,
        max_age: Optional[int] = None,
    ) -> bool:
        """Check whether the current session meets a required authentication context."""
        raise NotImplementedError

    def is_step_up_supported(self) -> bool:
        """Check whether the Kinde environment supports step-up authentication."""
        raise NotImplementedError
