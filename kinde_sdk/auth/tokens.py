from typing import Optional, Any, Dict
from .base_auth import BaseAuth

class Tokens(BaseAuth):
    """
    Tokens wrapper that provides direct access to the token manager
    for SDK consumers who need low-level token access.
    """
    
    def get_token_manager(self) -> Optional[Any]:
        """
        Get the token manager for the current user.
        
        Returns:
            Optional[Any]: The token manager if available, None otherwise
        """
        return self._get_token_manager()
    
    def get_user_id(self) -> Optional[str]:
        """
        Get the current user ID.
        
        Returns:
            Optional[str]: The user ID if available, None otherwise
        """
        framework = self._get_framework()
        if not framework:
            return None
        return framework.get_user_id()
    
    def is_authenticated(self) -> bool:
        """
        Check if the current user is authenticated.
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        token_manager = self._get_token_manager()
        return token_manager is not None
    
    def get_token_info(self) -> Dict[str, Any]:
        """
        Get basic information about the current token state.
        
        Returns:
            Dict containing token information:
            {
                "isAuthenticated": bool,
                "userId": Optional[str],
                "hasAccessToken": bool,
                "hasIdToken": bool,
                "hasRefreshToken": bool
            }
        """
        token_manager = self._get_token_manager()
        framework = self._get_framework()
        
        if not token_manager or not framework:
            return {
                "isAuthenticated": False,
                "userId": None,
                "hasAccessToken": False,
                "hasIdToken": False,
                "hasRefreshToken": False
            }
        
        tokens = token_manager.tokens if hasattr(token_manager, 'tokens') else {}
        
        return {
            "isAuthenticated": True,
            "userId": framework.get_user_id(),
            "hasAccessToken": "access_token" in tokens,
            "hasIdToken": "id_token" in tokens,
            "hasRefreshToken": "refresh_token" in tokens
        }

# Create a singleton instance
tokens = Tokens() 