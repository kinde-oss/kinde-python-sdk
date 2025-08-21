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
        if options and options.force_api:
            return await self._call_account_api(role_key)
        
        token_manager = self._get_token_manager()
        if not token_manager:
            return {
                "id": None,
                "key": role_key,
                "name": None,
                "description": None,
                "is_default_role": False,
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
        if options and options.force_api:
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
        roles_api = RolesApi()
        response = roles_api.get_user_roles()
        roles_data = getattr(response, "data", None)
        
        if roles_data is None:
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
                "isGranted": False
            }
        
        org_code = getattr(roles_data, "org_code", None)
        
        # Extract role information from the response
        if hasattr(roles_data, "roles") and roles_data.roles:
            roles = []
            for role in roles_data.roles:
                if hasattr(role, 'key') and role.key:
                    role_info = {
                        "id": getattr(role, 'id', None),
                        "key": role.key,
                        "name": getattr(role, 'name', None),
                        "description": getattr(role, 'description', None),
                        "is_default_role": getattr(role, 'is_default_role', False)
                    }
                    roles.append(role_info)
        else:
            roles = []
        
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
                "isGranted": True
            }
        else:
            return {
                "id": None,
                "key": role_key,
                "name": None,
                "description": None,
                "is_default_role": False,
                "isGranted": False
            }

# Create a singleton instance
roles = Roles()