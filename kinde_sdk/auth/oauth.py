from .user_session import UserSession
import requests
import logging
import urllib3
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

import jwt
from jwt import PyJWKClient
from authlib.integrations.requests_client import OAuth2Session
from kinde_sdk.exceptions import (
    KindeConfigurationException,
    KindeLoginException,
    KindeTokenException,
    KindeRetrieveException,
)


class GrantType(Enum):
    CLIENT_CREDENTIALS = "client_credentials"
    AUTHORIZATION_CODE = "authorization_code"
    AUTHORIZATION_CODE_WITH_PKCE = "authorization_code_with_pkce"

class OAuth:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        auth_url: str,
        token_url: str,
        logout_url: str,
        audience: Optional[str] = None,
        host: Optional[str] = "https://app.kinde.com",
    ):
        """Initialize the OAuth client."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url
        self.token_url = token_url
        self.logout_url = logout_url
        self.audience = audience
        self.host = host
        self.session_manager = UserSession()
        
        # Logging settings
        self.logger = logging.getLogger("kinde_sdk")
        self.logger.setLevel(logging.INFO)

        # Authentication properties
        self.verify_ssl = True
        self.proxy = None
        self.proxy_headers = None

    def authenticate_user(self, user_id, auth_code):
        """ Exchange authorization code for tokens and store in session. """
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        token_data = response.json()

        user_info = {"client_id": self.client_id, "client_secret": self.client_secret, "token_url": self.token_url}
        self.session_manager.set_user_data(user_id, user_info, token_data)

    def _get_auth_url(
        self,
        grant_type: GrantType,
        audience: Optional[str] = None,
        scope: Optional[List[str]] = None,
        state: Optional[str] = None,
    ) -> str:
        """
        Internal method to generate an authentication URL.
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(scope) if scope else "openid profile email",
            "state": state or "",
        }
        if audience:
            params["audience"] = audience
        return f"{self.auth_url}?{urlencode(params)}"

        
    def get_login_url(self, state: Optional[str] = None) -> str:
        """ Get the login URL for user authentication. """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "openid profile email",
            "state": state or "",
        }
        return f"{self.auth_url}?{urlencode(params)}"

    def get_user_info(self, user_id) -> Dict[str, Any]:
        """ Retrieve user information using the stored token. """
        token_manager = self.session_manager.user_sessions.get(user_id, {}).get("token_manager")
        if not token_manager:
            raise ValueError("User not authenticated")

        access_token = token_manager.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{self.host}/oauth/userinfo", headers=headers)
        response.raise_for_status()
        return response.json()

    def logout(self, user_id):
        """
        Get logout URL.
        """
        params = {
            "client_id": self.client_id,
            "logout_uri": redirect_url,
        }
        return f"{self.logout_url}?{urlencode(params)}"
