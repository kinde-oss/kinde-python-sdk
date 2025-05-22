from typing import Dict, Any, Optional
import logging
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession

class Claims:
    def __init__(self):
        self._logger = logging.getLogger("kinde_sdk")
        self._logger.setLevel(logging.INFO)
        self._framework = None
        self._session_manager = UserSession()

    def _get_framework(self):
        """Get the framework instance using singleton pattern."""
        if not self._framework:
            self._framework = FrameworkFactory.get_framework_instance()
        return self._framework

    def _get_token_manager(self) -> Optional[Any]:
        """
        Get the token manager for the current user.
        
        Returns:
            Optional[Any]: The token manager if available, None otherwise
        """
        framework = self._get_framework()
        if not framework:
            return None

        user_id = framework.get_user_id()
        if not user_id:
            return None

        return self._session_manager.get_token_manager(user_id)

    async def get_claim(self, claim_name: str, token_type: str = "access_token") -> Dict[str, Any]:
        """
        Get a specific claim from the user's tokens.
        
        Args:
            claim_name: The name of the claim to retrieve (e.g. "aud", "given_name")
            token_type: The type of token to get the claim from ("access_token" or "id_token")
            
        Returns:
            Dict containing claim details:
            {
                "name": str,
                "value": Any
            }
        """
        token_manager = self._get_token_manager()
        if not token_manager:
            return {
                "name": claim_name,
                "value": None
            }

        claims = token_manager.get_claims()
        value = claims.get(claim_name)

        return {
            "name": claim_name,
            "value": value
        }

    async def get_all_claims(self, token_type: str = "access_token") -> Dict[str, Any]:
        """
        Get all claims from the user's tokens.
        
        Args:
            token_type: The type of token to get claims from ("access_token" or "id_token")
            
        Returns:
            Dict containing all claims from the token
        """
        token_manager = self._get_token_manager()
        if not token_manager:
            return {}

        return token_manager.get_claims()

# Create a singleton instance
claims = Claims() 