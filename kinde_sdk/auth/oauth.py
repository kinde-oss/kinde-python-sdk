from .user_session import UserSession
import requests
import logging
import urllib3
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import hashlib
import base64
import secrets

from .storage_factory import StorageFactory
from .config_loader import load_config
from typing import Dict, Optional

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
        userinfo_url: str,
        config_file: str = "config.yaml",  # Path to the configuration file
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
        self.userinfo_url = userinfo_url
        self.audience = audience
        self.host = host

        # Load configuration and create the appropriate storage backend
        config = load_config(config_file)
        storage_config = config.get("storage", {"type": "memory"})  # Default to "memory"
        storage = StorageFactory.create_storage(storage_config)

        self.session_manager = UserSession(storage= storage)

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
        print("token_data: " + str(token_data))

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
            "scope": " ".join(scope) if scope else "openid profile email offline",
            "state": state or "",
        }
        if audience:
            params["audience"] = audience
        return f"{self.auth_url}?{urlencode(params)}"

        
    # def get_login_url(self, state: Optional[str] = None) -> str:
    #     """ Get the login URL for user authentication. """
    #     params = {
    #         "client_id": self.client_id,
    #         "response_type": "code",
    #         "redirect_uri": self.redirect_uri,
    #         "scope": "openid profile email offline",
    #         "state": state or "",
    #     }
    #     return f"{self.auth_url}?{urlencode(params)}"

    def get_login_url(self, state: Optional[str] = None, scope: Optional[List[str]] = None) -> str:
        """
        Get the login URL for user authentication.

        Args:
            state (Optional[str]): A state parameter for CSRF protection.
            scope (Optional[List[str]]): A list of scopes to request.

        Returns:
            str: The login URL.
        """
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(scope) if scope else "openid profile email",  # Allow custom scope
            "state": state or "",
        }
        return f"{self.auth_url}?{urlencode(params)}"

    def get_login_url_with_pkce(self, state: Optional[str] = None, scope: Optional[List[str]] = None) -> str:
        """
        Get the login URL for PKCE flow.

        Args:
            state (Optional[str]): A state parameter for CSRF protection.
            scope (Optional[List[str]]): A list of scopes to request.

        Returns:
            str: The login URL with PKCE parameters.
        """
        code_verifier = self.generate_pkce_code_verifier()
        code_challenge = self.generate_pkce_code_challenge(code_verifier)

        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(scope) if scope else "openid profile email",  # Allow custom scope
            "state": state or "",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        return f"{self.auth_url}?{urlencode(params)}"


    def get_user_info(self, user_id) -> Dict[str, Any]:
        """ Retrieve user information using the stored token. """
        token_manager = self.session_manager.user_sessions.get(user_id, {}).get("token_manager")
        if not token_manager:
            raise ValueError("User not authenticated")

        access_token = token_manager.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{self.userinfo_url}", headers=headers)
        response.raise_for_status()
        return response.json()

    def logout(self, user_id):
        """
        Get logout URL.
        """
        params = {
            "client_id": self.client_id,
            "logout_uri": self.redirect_uri,
        }
        return f"{self.logout_url}?{urlencode(params)}"

    def generate_pkce_code_verifier(self) -> str:
        """Generate a PKCE code verifier."""
        return secrets.token_urlsafe(32)

    def generate_pkce_code_challenge(self, code_verifier: str) -> str:
        """Generate a PKCE code challenge from the verifier."""
        code_challenge = hashlib.sha256(code_verifier.encode()).digest()
        return base64.urlsafe_b64encode(code_challenge).decode().rstrip("=")

    # def get_login_url_with_pkce(self, state: Optional[str] = None) -> str:
    #     """Get the login URL for PKCE flow."""
    #     code_verifier = self.generate_pkce_code_verifier()
    #     code_challenge = self.generate_pkce_code_challenge(code_verifier)

    #     params = {
    #         "client_id": self.client_id,
    #         "response_type": "code",
    #         "redirect_uri": self.redirect_uri,
    #         "scope": "openid profile email offline",
    #         "state": state or "",
    #         "code_challenge": code_challenge,
    #         "code_challenge_method": "S256",
    #     }
    #     return f"{self.auth_url}?{urlencode(params)}"

    def get_tokens_for_core(self, user_id: str) -> Optional[Dict[str, str]]:
        """
        Retrieve tokens for the core module.

        Args:
            user_id (str): The ID of the user whose tokens are being retrieved.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing the access token and refresh token (if available).
                                      Returns None if the user is not authenticated or the session is invalid.
        """
        # Retrieve the user session from the storage backend
        session = self.session_manager.storage.get(user_id)
        if not session:
            return None  # User session not found

        # Retrieve the TokenManager from the session
        token_manager = session.get("token_manager")
        if not token_manager:
            return None  # TokenManager not found

        # Get the access token
        access_token = token_manager.get_access_token()
        if not access_token:
            return None  # No valid access token

        # Prepare the token dictionary
        tokens = {
            "access_token": access_token,
        }

        # Add the refresh token if available
        refresh_token = token_manager.tokens.get("refresh_token")
        if refresh_token:
            tokens["refresh_token"] = refresh_token

        return tokens