from typing import Dict, Any, Optional
from .base_auth import BaseAuth

class Claims(BaseAuth):
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