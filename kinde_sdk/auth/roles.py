from typing import Dict, List, Optional, Any

from .api_options import ApiOptions
from .base_auth import BaseAuth

from kinde_sdk.frontend.api.roles_api import RolesApi

class Roles(BaseAuth):
    async def get_role(
            self, 
            role_key: str,
            options: Optional[ApiOptions] = None
            ) -> Dict[str, Any]:
        """
        Get a specific role for the current user.
        If force_api is True, fetch from API instead of token claims.
        
        Args:
            role_key: The role key to check (e.g. "admin", "user")
            
        Returns:
            Dict containing role details:
            {
                "id": str,
                "key": str,
                "name": str,
                "description": str,
                "is_default_role": bool,
                "isGranted": bool
            }
        """
        # Check SDK-level force_api setting first, then fall back to options parameter
        force_api = self._get_force_api_setting()
        if options and options.force_api:
            force_api = True
        
        if force_api:
            return await self._call_account_api(role_key)
        
        token_manager = self._get_token_manager()
        if not token_manager:
            return {
                "id": None,
                "key": role_key,
                "name": None,
                "description": None,
                "is_default_role": False,
                "orgCode": None,
                "isGranted": False
            }

        claims = token_manager.get_claims()
        roles = claims.get("roles", [])
        org_code = claims.get("org_code")

        # Find the specific role
        role_info = None
        for role in roles:
            if isinstance(role, dict) and role.get('key') == role_key:
                role_info = role
                break

        if role_info:
            return {
                "id": role_info.get('id'),
                "key": role_info.get('key'),
                "name": role_info.get('name'),
                "description": role_info.get('description'),
                "is_default_role": role_info.get('is_default_role', False),
                "orgCode": org_code,
                "isGranted": True
            }
        else:
            return {
                "id": None,
                "key": role_key,
                "name": None,
                "description": None,
                "is_default_role": False,
                "orgCode": org_code,
                "isGranted": False
            }

    async def get_roles(
            self,
            options: Optional[ApiOptions] = None
            ) -> Dict[str, Any]:
        """
        Get all roles for the current user.
        If force_api is True, fetch from API instead of token claims.
        
        Args:
            options: Optional ApiOptions object (deprecated, use SDK-level force_api setting)
        
        Returns:
            Dict containing organization code and list of roles:
            {
                "orgCode": str,
                "roles": List[Dict] where each role has:
                    {
                        "id": str,
                        "key": str,
                        "name": str,
                        "description": str,
                        "is_default_role": bool
                    }
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
                "roles": []
            }

        claims = token_manager.get_claims()
        roles = claims.get("roles", [])
        org_code = claims.get("org_code")

        return {
            "orgCode": org_code,
            "roles": roles
        }
    
    async def _call_account_api(self, role_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Calls the Kinde Account API to get roles.
        If role_key is provided, returns only that role's data.
        Otherwise, returns all roles as a dict.
        """
        try:
            # Create authenticated API client using shared method
            roles_api = self._create_authenticated_api_client(RolesApi)
            if not roles_api:
                if role_key is None:
                    return {"orgCode": None, "roles": []}
                return {
                    "id": None,
                    "key": role_key,
                    "name": None,
                    "description": None,
                    "is_default_role": False,
                    "orgCode": None,
                    "isGranted": False,
                }
            
            response = roles_api.get_user_roles()
        except Exception as e:
            self._logger.error(f"Failed to fetch roles from API: {str(e)}")
            if role_key is None:
                return {
                    "orgCode": None,
                    "roles": []
                }
            return {
                "id": None,
                "key": role_key,
                "name": None,
                "description": None,
                "is_default_role": False,
                "orgCode": None,
                "isGranted": False
            }
        # Support both response.data.* and top-level response.* shapes
        data = getattr(response, "data", None) or response
        org_code = getattr(data, "org_code", getattr(response, "org_code", None))

        raw_roles = getattr(data, "roles", getattr(response, "roles", None)) or []
        roles = []
        for role in raw_roles:
            # SDK model instance
            if hasattr(role, "key") and getattr(role, "key"):
                roles.append({
                    "id": getattr(role, "id", None),
                    "key": getattr(role, "key"),
                    "name": getattr(role, "name", None),
                    "description": getattr(role, "description", None),
                    "is_default_role": getattr(role, "is_default_role", False),
                })
            # Dict payload
            elif isinstance(role, dict) and role.get("key"):
                roles.append({
                    "id": role.get("id"),
                    "key": role.get("key"),
                    "name": role.get("name"),
                    "description": role.get("description"),
                    "is_default_role": role.get("is_default_role", False),
                })
        
        if role_key is None:
            return {
                "orgCode": org_code,
                "roles": roles
            }
        
        # Check if the specific role exists
        role_info = None
        for role in roles:
            if role.get('key') == role_key:
                role_info = role
                break
        
        if role_info:
            return {
                "id": role_info.get('id'),
                "key": role_info.get('key'),
                "name": role_info.get('name'),
                "description": role_info.get('description'),
                "is_default_role": role_info.get('is_default_role', False),
                "orgCode": org_code,
                "isGranted": True
            }
        else:
            return {
                "id": None,
                "key": role_key,
                "name": None,
                "description": None,
                "is_default_role": False,
                "orgCode": org_code,
                "isGranted": False
            }

# Create a singleton instance
roles = Roles()