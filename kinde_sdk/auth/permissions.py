from typing import Dict, List, Optional, Any

from .api_options import ApiOptions
from .base_auth import BaseAuth

from kinde_sdk.frontend.api.permissions_api import PermissionsApi

class Permissions(BaseAuth):
    async def get_permission(
            self, 
            permission_key: str,
            options: Optional[ApiOptions] = None
            ) -> Dict[str, Any]:
        """
        Get a specific permission for the current user.
        
        Args:
            permission_key: The permission key to check (e.g. "create:todos")
            options: Optional ApiOptions object. If provided and force_api=True,
                    fetches permissions from the API instead of token claims.
                    Defaults to None (use token claims).
            
        Returns:
            Dict containing permission details:
            {
                "permissionKey": str,
                "orgCode": Optional[str],  # May be None if user has no associated organization
                "isGranted": bool
            }
        """
        # Check SDK-level force_api setting first, then fall back to options parameter
        force_api = self._get_force_api_setting()
        if options and options.force_api:
            force_api = True
        
        if force_api:
            return await self._call_account_api(permission_key)
        
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

    async def get_permissions(
            self,
            options: Optional[ApiOptions] = None
            ) -> Dict[str, Any]:
        """
        Get all permissions for the current user.
        
        Args:
            options: Optional ApiOptions object. If provided and force_api=True,
                    fetches permissions from the API instead of token claims.
                    Defaults to None (use token claims).
        
        Returns:
            Dict containing organization code and list of permissions:
            {
                "orgCode": Optional[str],  # May be None if user has no associated organization
                "permissions": List[str]
            }
        """
        # Check SDK-level force_api setting first, then fall back to options parameter
        force_api = self._get_force_api_setting()
        if options and options.force_api:
            force_api = True
        
        if force_api:
            return await self._call_account_api()
    
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
    
    async def _call_account_api(self, permission_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Calls the Kinde Account API to get permissions.
        If permission_key is provided, returns only that permission's data.
        Otherwise, returns all permissions as a dict.
        """
        try:
            # Create authenticated API client using shared method
            permissions_api = self._create_authenticated_api_client(PermissionsApi)
            if not permissions_api:
                if permission_key is None:
                    return {"orgCode": None, "permissions": []}
                return {"permissionKey": permission_key, "orgCode": None, "isGranted": False}
            
            response = permissions_api.get_user_permissions()
        except Exception as e:
            # Log error and return empty result
            if hasattr(self, '_logger'):
                self._logger.error(f"Failed to fetch permissions from API: {str(e)}")
            if permission_key is None:
                return {"orgCode": None, "permissions": []}
            return {"permissionKey": permission_key, "orgCode": None, "isGranted": False}
            
        # Handle both direct attributes and response.data envelopes
        if hasattr(response, "data"):
            data = getattr(response, "data")
            permissions = getattr(data, "permissions", []) or []
            org_code = getattr(data, "org_code", None)
        else:
            permissions = getattr(response, "permissions", []) or []
            org_code = getattr(response, "org_code", None)
        
        if permission_key is None:
            return {
                "orgCode": org_code,
                "permissions": permissions
            }
        
        is_granted = permission_key in permissions
        return {
            "permissionKey": permission_key,
            "orgCode": org_code,
            "isGranted": is_granted
        }

# Create a singleton instance
permissions = Permissions() 