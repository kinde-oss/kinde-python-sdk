from typing import Dict, Any, Optional
import logging
import urllib.parse
from urllib.parse import urlparse
import httpx
from enum import Enum
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession

class PortalPage(str, Enum):
    """Enum representing the different portal pages available."""
    ORGANIZATION_DETAILS = "organization_details"
    ORGANIZATION_MEMBERS = "organization_members"
    ORGANIZATION_PLAN_DETAILS = "organization_plan_details"
    ORGANIZATION_PAYMENT_DETAILS = "organization_payment_details"
    ORGANIZATION_PLAN_SELECTION = "organization_plan_selection"
    PROFILE = "profile"

class Portals:
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

    def _sanitize_url(self, url: str) -> str:
        """
        Sanitize the URL by ensuring it has a scheme and removing trailing slashes.
        
        Args:
            url: The URL to sanitize
            
        Returns:
            str: The sanitized URL
        """
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')

    async def generate_portal_url(self, domain: str, return_url: str, sub_nav: PortalPage = PortalPage.PROFILE) -> Dict[str, str]:
        """
        Generates a URL to the user portal.
        
        Args:
            domain: The domain of the Kinde instance
            return_url: URL to redirect to after completing the portal flow
            sub_nav: Sub-navigation section to display (defaults to PortalPage.PROFILE)
            
        Returns:
            Dict containing the URL to redirect to:
            {
                "url": URL
            }
            
        Raises:
            Exception: If active storage is not found
            Exception: If access token is not found
            Exception: If return_url is not an absolute URL
            Exception: If the API request fails
            Exception: If the response contains an invalid URL
        """
        token_manager = self._get_token_manager()
        if not token_manager:
            raise Exception("generate_portal_url: Active storage not found")

        token = token_manager.get_access_token()
        if not token:
            raise Exception("generate_portal_url: Access Token not found")

        if not return_url.startswith(('http://', 'https://')):
            raise Exception("generate_portal_url: return_url must be an absolute URL")

        sanitized_domain = self._sanitize_url(domain)
        params = urllib.parse.urlencode({
            'sub_nav': sub_nav.value,
            'return_url': return_url
        })
        
        url = f"{sanitized_domain}/account_api/v1/portal_link?{params}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if not response.is_success:
                raise Exception(f"Failed to fetch portal URL: {response.status_code} {response.reason_phrase}")
            
            result = response.json()
            if not result.get("url") or not isinstance(result["url"], str):
                raise Exception("Invalid URL received from API")
            
            try:
                portal_url = urlparse(result["url"])
                return {"url": result["url"]}
            except Exception as e:
                self._logger.error(f"Error parsing URL: {e}")
                raise Exception(f"Invalid URL format received from API: {result['url']}") from e

# Create a singleton instance
portals = Portals() 