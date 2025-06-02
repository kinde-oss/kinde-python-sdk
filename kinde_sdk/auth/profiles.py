from typing import Dict, Any, Optional
import logging
import urllib.parse
from urllib.parse import urlparse
import httpx
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession

class Profiles:
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

    async def generate_profile_url(self, domain: str, return_url: str, sub_nav: str) -> Dict[str, str]:
        """
        Generates a URL to the user profile portal.
        
        Args:
            domain: The domain of the Kinde instance
            return_url: URL to redirect to after completing the profile flow
            sub_nav: Sub-navigation section to display
            
        Returns:
            Dict containing the URL to redirect to:
            {
                "url": str
            }
            
        Raises:
            Exception: If active storage is not found
            Exception: If access token is not found
            Exception: If the API request fails
            Exception: If the response contains an invalid URL
        """
        token_manager = self._get_token_manager()
        if not token_manager:
            raise Exception("generate_profile_url: Active storage not found")

        token = token_manager.get_access_token()
        if not token:
            raise Exception("generate_profile_url: Access Token not found")

        sanitized_domain = self._sanitize_url(domain)
        encoded_return_url = urllib.parse.quote(return_url)
        
        url = f"{sanitized_domain}/account_api/v1/portal_link?return_url={encoded_return_url}&sub_nav={sub_nav}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if not response.is_success:
                raise Exception(f"Failed to fetch profile URL: {response.status_code} {response.reason_phrase}")
            
            result = response.json()
            if not result.get("url") or not isinstance(result["url"], str):
                raise Exception("Invalid URL received from API")
            
            try:
                # Validate the URL format
                parsed_url = urlparse(result["url"])
                if not all([parsed_url.scheme, parsed_url.netloc]):
                    raise ValueError("Invalid URL format")
                
                return {"url": result["url"]}
            except Exception as e:
                self._logger.error(f"Error parsing URL: {e}")
                raise Exception(f"Invalid URL format received from API: {result['url']}")

# Create a singleton instance
profiles = Profiles() 