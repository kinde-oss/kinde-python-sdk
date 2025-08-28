"""
Smart OAuth client that automatically chooses between sync and async implementations
based on the execution context.
"""

import asyncio
import warnings
from typing import Dict, Any, Optional
from .base_oauth import BaseOAuth
from .oauth import OAuth
from .async_oauth import AsyncOAuth

class SmartOAuth(BaseOAuth):
    """
    Smart OAuth client that automatically adapts to sync or async contexts.
    
    This client provides a unified interface that works in both sync and async environments.
    It automatically detects the execution context and uses the appropriate implementation.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize both sync and async OAuth clients."""
        self._sync_oauth = OAuth(*args, **kwargs)
        self._async_oauth = AsyncOAuth(*args, **kwargs)
        self._context_warning_shown = False
    
    def _is_async_context(self) -> bool:
        """Check if we're running in an async context."""
        try:
            asyncio.get_running_loop()
            return True
        except RuntimeError:
            return False
    
    def _warn_async_context(self, method_name: str):
        """Warn when using sync method in async context."""
        if not self._context_warning_shown:
            warnings.warn(
                f"Using sync method '{method_name}' in async context. "
                f"Consider using '{method_name}_async' for better performance.",
                DeprecationWarning,
                stacklevel=3
            )
            self._context_warning_shown = True
    
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated."""
        if self._is_async_context():
            self._warn_async_context("is_authenticated")
        return self._sync_oauth.is_authenticated()
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get user information synchronously."""
        if self._is_async_context():
            self._warn_async_context("get_user_info")
        return self._sync_oauth.get_user_info()
    
    async def get_user_info_async(self) -> Dict[str, Any]:
        """Get user information asynchronously."""
        return await self._async_oauth.get_user_info_async()
    
    def get_tokens(self, user_id: str) -> Dict[str, Any]:
        """Get tokens for a user."""
        if self._is_async_context():
            self._warn_async_context("get_tokens")
        return self._sync_oauth.get_tokens(user_id)
    
    async def generate_auth_url(
        self,
        route_type=None,
        login_options: Dict[str, Any] = None,
        disable_url_sanitization: bool = False
    ) -> Dict[str, Any]:
        """Generate authentication URL."""
        return await self._async_oauth.generate_auth_url(
            route_type=route_type,
            login_options=login_options,
            disable_url_sanitization=disable_url_sanitization
        )
    
    async def login(self, login_options: Dict[str, Any] = None) -> str:
        """Generate login URL."""
        return await self._async_oauth.login(login_options)
    
    async def register(self, login_options: Dict[str, Any] = None) -> str:
        """Generate registration URL."""
        return await self._async_oauth.register(login_options)
    
    async def logout(self, user_id: Optional[str] = None, logout_options: Dict[str, Any] = None) -> str:
        """Generate logout URL."""
        return await self._async_oauth.logout(user_id, logout_options)
    
    async def handle_redirect(self, code: str, user_id: str, state: Optional[str] = None) -> Dict[str, Any]:
        """Handle OAuth redirect."""
        return await self._async_oauth.handle_redirect(code, user_id, state)
    
    # Delegate other properties and methods to the sync implementation
    def __getattr__(self, name):
        """Delegate unknown attributes to the sync OAuth instance."""
        return getattr(self._sync_oauth, name)

# Factory function for creating the appropriate OAuth client
def create_oauth_client(async_mode: bool = None, *args, **kwargs) -> BaseOAuth:
    """
    Factory function to create the appropriate OAuth client.
    
    Args:
        async_mode: If True, creates AsyncOAuth. If False, creates OAuth.
                   If None, creates SmartOAuth that adapts automatically.
        *args, **kwargs: Arguments to pass to the OAuth constructor
    
    Returns:
        BaseOAuth: The appropriate OAuth client
    """
    if async_mode is True:
        return AsyncOAuth(*args, **kwargs)
    elif async_mode is False:
        return OAuth(*args, **kwargs)
    else:
        return SmartOAuth(*args, **kwargs)
