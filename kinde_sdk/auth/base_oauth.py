"""
Base OAuth class that defines the interface for both sync and async operations.
This provides a clear contract for what methods should be available in both contexts.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

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
    async def handle_redirect(self, code: str, user_id: str, state: Optional[str] = None) -> Dict[str, Any]:
        """Handle OAuth redirect."""
        pass
