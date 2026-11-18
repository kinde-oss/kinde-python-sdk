"""
Async OAuth implementation that provides async versions of all OAuth operations.
This ensures consistency for async applications.
"""

import asyncio
from typing import Dict, Any, List, Optional, Union
from .base_oauth import BaseOAuth
from .oauth import OAuth
from kinde_sdk.core.helpers import get_user_details
from kinde_sdk.core.exceptions import KindeConfigurationException

class AsyncOAuth(BaseOAuth):
    """
    Async OAuth implementation that wraps the existing OAuth class
    and provides async versions of all methods.
    """
    
    def __init__(self, *args, **kwargs):
        """Initialize with the same parameters as the sync OAuth class."""
        self._sync_oauth = OAuth(*args, **kwargs)
    
    def is_authenticated(self) -> bool:
        """Check if the user is authenticated (sync method)."""
        return self._sync_oauth.is_authenticated()
    
    async def get_user_info_async(self) -> Dict[str, Any]:
        """
        Get user information asynchronously.
        
        Returns:
            Dict[str, Any]: The user information
            
        Raises:
            KindeConfigurationException: If no user ID is found in session
        """
        # Get user ID from framework
        user_id = self._sync_oauth._framework.get_user_id()
        if not user_id:
            raise KindeConfigurationException("No user ID found in session")
            
        # Get token manager for the user
        token_manager = self._sync_oauth._session_manager.get_token_manager(user_id)
        if not token_manager:
            raise KindeConfigurationException("No token manager found for user")
        
        # Use the async helper function
        user_details = await get_user_details(
            userinfo_url=self._sync_oauth.userinfo_url,
            token_manager=token_manager,
            logger=self._sync_oauth._logger
        )
            
        return user_details
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get user information synchronously (maintains backward compatibility).
        This method will work in both sync and async contexts.
        """
        return self._sync_oauth.get_user_info()
    
    def get_tokens(self, user_id: str) -> Dict[str, Any]:
        """Get tokens for a user (sync method)."""
        return self._sync_oauth.get_tokens(user_id)
    
    async def generate_auth_url(
        self,
        route_type=None,
        login_options: Dict[str, Any] = None,
        disable_url_sanitization: bool = False
    ) -> Dict[str, Any]:
        """Generate authentication URL asynchronously."""
        return await self._sync_oauth.generate_auth_url(
            route_type=route_type,
            login_options=login_options,
            disable_url_sanitization=disable_url_sanitization
        )
    
    async def login(self, login_options: Dict[str, Any] = None) -> str:
        """Generate login URL asynchronously."""
        return await self._sync_oauth.login(login_options)
    
    async def register(self, login_options: Dict[str, Any] = None) -> str:
        """Generate registration URL asynchronously."""
        return await self._sync_oauth.register(login_options)
    
    async def logout(self, user_id: Optional[str] = None, logout_options: Dict[str, Any] = None) -> str:
        """Generate logout URL asynchronously."""
        return await self._sync_oauth.logout(user_id, logout_options)
    
    async def handle_redirect(
        self,
        code: Optional[str],
        user_id: Optional[str],
        state: Optional[str] = None,
        error: Optional[str] = None,
        error_description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Handle OAuth redirect asynchronously."""
        if error:
            return await self._sync_oauth.handle_redirect(
                code, user_id, state, error=error, error_description=error_description
            )
        return await self._sync_oauth.handle_redirect(code, user_id, state)

    async def step_up(
        self,
        acr: Optional[Union[str, List[str]]] = None,
        max_age: Optional[int] = None,
        login_options: Optional[Dict[str, Any]] = None,
        post_login_redirect_url: Optional[str] = None,
    ) -> str:
        """Generate the URL for a step-up authentication request asynchronously."""
        return await self._sync_oauth.step_up(
            acr=acr,
            max_age=max_age,
            login_options=login_options,
            post_login_redirect_url=post_login_redirect_url,
        )

    def get_authentication_context(self) -> Dict[str, Any]:
        """Get the acr, amr and auth_time of the current session (sync method)."""
        return self._sync_oauth.get_authentication_context()

    def has_authentication_context(
        self,
        acr: Optional[Union[str, List[str]]] = None,
        max_age: Optional[int] = None,
    ) -> bool:
        """Check whether the current session meets a required authentication context (sync method)."""
        return self._sync_oauth.has_authentication_context(acr=acr, max_age=max_age)

    def is_step_up_supported(self) -> bool:
        """Check whether the Kinde environment supports step-up authentication (sync method)."""
        return self._sync_oauth.is_step_up_supported()
    
    # Delegate other properties and methods to the sync implementation
    def __getattr__(self, name):
        """Delegate unknown attributes to the sync OAuth instance."""
        return getattr(self._sync_oauth, name)
