from typing import Dict, Any, Optional
import logging
from .oauth import OAuth

class Claims:
    def __init__(self):
        self._logger = logging.getLogger("kinde_sdk")
        self._logger.setLevel(logging.INFO)
        self._oauth = None

    def _get_oauth(self) -> OAuth:
        """Get the OAuth instance using singleton pattern."""
        if not self._oauth:
            self._oauth = OAuth.get_instance()
        return self._oauth

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
        oauth = self._get_oauth()
        if not oauth.is_authenticated():
            return {
                "name": claim_name,
                "value": None
            }

        user_id = oauth._framework.get_user_id()
        token_manager = oauth._session_manager.get_token_manager(user_id)
        
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
        oauth = self._get_oauth()
        if not oauth.is_authenticated():
            return {}

        user_id = oauth._framework.get_user_id()
        token_manager = oauth._session_manager.get_token_manager(user_id)
        
        if not token_manager:
            return {}

        return token_manager.get_claims()

# Create a singleton instance
claims = Claims() 