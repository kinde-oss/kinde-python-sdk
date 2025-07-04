from typing import Dict, List, Optional, Any
from .base_auth import BaseAuth

class Permissions(BaseAuth):
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
        token_manager = self._get_token_manager()
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
        token_manager = self._get_token_manager()
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