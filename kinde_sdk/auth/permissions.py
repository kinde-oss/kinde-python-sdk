from typing import Dict, List, Optional, Any
import logging
from .oauth import OAuth

class Permissions:
    def __init__(self):
        self._logger = logging.getLogger("kinde_sdk")
        self._logger.setLevel(logging.INFO)
        self._oauth = None

    def _get_oauth(self) -> OAuth:
        """Get the OAuth instance using singleton pattern."""
        if not self._oauth:
            self._oauth = OAuth.get_instance()
        return self._oauth

    async def get_permission(self, permission_key: str) -> Dict[str, Any]:
        """
        Get a specific permission for the current user.
        
        Args:
            permission_key: The permission key to check (e.g. "create:todos")
            
        Returns:
            Dict containing permission details:
            {
                "permissionKey": str,
                "orgCode": str,
                "isGranted": bool
            }
        """
        oauth = self._get_oauth()
        if not oauth.is_authenticated():
            return {
                "permissionKey": permission_key,
                "orgCode": None,
                "isGranted": False
            }

        user_id = oauth._framework.get_user_id()
        token_manager = oauth._session_manager.get_token_manager(user_id)
        
        if not token_manager:
            return {
                "permissionKey": permission_key,
                "orgCode": None,
                "isGranted": False
            }

        claims = token_manager.get_claims()
        permissions = claims.get("permissions", [])
        org_code = claims.get("org_code")

        return {
            "permissionKey": permission_key,
            "orgCode": org_code,
            "isGranted": permission_key in permissions
        }

    async def get_permissions(self) -> Dict[str, Any]:
        """
        Get all permissions for the current user.
        
        Returns:
            Dict containing organization code and list of permissions:
            {
                "orgCode": str,
                "permissions": List[str]
            }
        """
        oauth = self._get_oauth()
        if not oauth.is_authenticated():
            return {
                "orgCode": None,
                "permissions": []
            }

        user_id = oauth._framework.get_user_id()
        token_manager = oauth._session_manager.get_token_manager(user_id)
        
        if not token_manager:
            return {
                "orgCode": None,
                "permissions": []
            }

        claims = token_manager.get_claims()
        permissions = claims.get("permissions", [])
        org_code = claims.get("org_code")

        return {
            "orgCode": org_code,
            "permissions": permissions
        }

# Create a singleton instance
permissions = Permissions() 