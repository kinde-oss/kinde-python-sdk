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

        # Logging settings
        self.logger = logging.getLogger("kinde_sdk")
        self.logger.setLevel(logging.INFO)

        # Authentication properties
        self.verify_ssl = True
        self.proxy = None
        self.proxy_headers = None

        # Create OAuth session
        self.session = OAuth2Session(
            client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri
        )

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
        """
        Get the login URL for user authentication.
        """
        return self._get_auth_url(GrantType.AUTHORIZATION_CODE, state=state)

    # def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
    #     """
    #     Exchange the authorization code for an access token.
    #     """
    #     data = {
    #         "grant_type": GrantType.AUTHORIZATION_CODE.value,
    #         "code": code,
    #         "redirect_uri": self.redirect_uri,
    #         "client_id": self.client_id,
    #         "client_secret": self.client_secret,
    #     }
    #     response = requests.post(self.token_url, data=data)
    #     response.raise_for_status()  # Raise an error for non-2xx responses
    #     return response.json()

    # def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
    #     """
    #     Refresh the access token.
    #     """
    #     data = {
    #         "grant_type": "refresh_token",
    #         "refresh_token": refresh_token,
    #         "client_id": self.client_id,
    #         "client_secret": self.client_secret,
    #     }
    #     response = requests.post(self.token_url, data=data)
    #     response.raise_for_status()
    #     return response.json()

    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        Retrieve user information.
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{self.host}/oauth/userinfo", headers=headers)
        response.raise_for_status()
        return response.json()

    def logout(self, redirect_url: str) -> str:
        """
        Get logout URL.
        """
        params = {
            "client_id": self.client_id,
            "logout_uri": redirect_url,
        }
        return f"{self.logout_url}?{urlencode(params)}"
