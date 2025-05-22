from typing import Dict, List, Optional, Any
import logging
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession

class Permissions:
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