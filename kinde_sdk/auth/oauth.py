import os
import requests
import logging
from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, urlparse
import hashlib
import base64
import secrets

from .user_session import UserSession
from .storage_factory import StorageFactory
from .config_loader import load_config
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
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        auth_url: Optional[str] = None,
        token_url: Optional[str] = None,
        logout_url: Optional[str] = None,
        userinfo_url: Optional[str] = None,
        config_file: Optional[str] = None,  #  config_file optional
        storage_config: Optional[Dict[str, Any]] = None,  # Add storage_config parameter
        audience: Optional[str] = None,
        host: Optional[str] = None,
        state: Optional[str] = None,
    ):
        """Initialize the OAuth client."""
        # Fetch values from environment variables if not provided
        self.client_id = client_id or os.getenv("KINDE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("KINDE_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or os.getenv("KINDE_REDIRECT_URI")
        self.auth_url = auth_url or os.getenv("KINDE_AUTH_URL")
        self.token_url = token_url or os.getenv("KINDE_TOKEN_URL")
        self.logout_url = logout_url or os.getenv("KINDE_LOGOUT_URL")
        self.userinfo_url = userinfo_url or os.getenv("KINDE_USERINFO_URL")
        self.host = host or os.getenv("KINDE_HOST", "https://app.kinde.com")
        self.audience = audience or os.getenv("KINDE_AUDIENCE")
        self.state = state
        
        # Validate required configurations
        if not self.client_id:
            raise KindeConfigurationException("Client ID is required.")
        if not self.client_secret:
            raise KindeConfigurationException("Client secret is required.")
        if not self.redirect_uri:
            raise KindeConfigurationException("Redirect URI is required.")
        if not self.auth_url:
            raise KindeConfigurationException("Auth URL is required.")
        if not self.token_url:
            raise KindeConfigurationException("Token URL is required.")
        if not self.logout_url:
            raise KindeConfigurationException("Logout URL is required.")
        if not self.userinfo_url:
            raise KindeConfigurationException("Userinfo URL is required.")

        # Load configuration and create the appropriate storage backend
        if config_file:
            config = load_config(config_file)
            storage_config = config.get("storage", {"type": "memory"})  # Default to "memory"
        elif storage_config is None:
            storage_config = {"type": "memory"}  # Default to in-memory storage if no config is provided
        storage = StorageFactory.create_storage(storage_config)

        self.session_manager = UserSession(storage=storage)

        # Logging settings
        self.logger = logging.getLogger("kinde_sdk")
        self.logger.setLevel(logging.INFO)

        # Authentication properties
        self.verify_ssl = True
        self.proxy = None
        self.proxy_headers = None

    def code_exchange(self, user_id: str, auth_code: str) -> None:
        """Exchange authorization code for tokens and store in session."""
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

        user_info = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "token_url": self.token_url,
        }
        self.session_manager.set_user_data(user_id, user_info, token_data)

    def get_login_url(self, state: Optional[str] = None, scope: Optional[List[str]] = None, login_type: Optional[str] = None) -> str:
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
            "scope": " ".join(scope) if scope else "openid profile email",
            "state": state or "",
        }
        if login_type:
            params["login_type"] = login_type
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
            "scope": " ".join(scope) if scope else "openid profile email",
            "state": state or "",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        return f"{self.auth_url}?{urlencode(params)}"

    def get_user_details(self, user_id: str) -> Dict[str, Any]:
        """Retrieve user information using the stored token."""
        token_manager = self.session_manager.user_sessions.get(user_id, {}).get("token_manager")
        if not token_manager:
            raise KindeRetrieveException("User not authenticated")

        access_token = token_manager.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.userinfo_url, headers=headers)
        response.raise_for_status()
        return response.json()

    def logout(self, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate the logout URL.

        Args:
            params (Optional[Dict[str, Any]]): A dictionary of query parameters to include in the logout URL.
                                            Supported keys: state, post_logout_redirect_uri.

        Returns:
            str: The logout URL.
        """
        # Default parameters
        default_params = {
            "client_id": self.client_id,
            "logout_uri": self.redirect_uri,
            "state": self.state or "",
        }

        # Merge default parameters with user-provided parameters
        if params:
            if "state" in params:
                default_params["state"] = params["state"]
            if "post_logout_redirect_uri" in params:
                default_params["post_logout_redirect_uri"] = params["post_logout_redirect_uri"]

        return f"{self.logout_url}?{urlencode(default_params)}"

    def generate_pkce_code_verifier(self) -> str:
        """Generate a PKCE code verifier."""
        return secrets.token_urlsafe(32)

    def generate_pkce_code_challenge(self, code_verifier: str) -> str:
        """Generate a PKCE code challenge from the verifier."""
        code_challenge = hashlib.sha256(code_verifier.encode()).digest()
        return base64.urlsafe_b64encode(code_challenge).decode().rstrip("=")

    def get_tokens_for_core(self, user_id: str) -> Optional[Dict[str, str]]:
        """
        Retrieve tokens for the core module.

        Args:
            user_id (str): The ID of the user whose tokens are being retrieved.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing the access token and refresh token (if available).
                                      Returns None if the user is not authenticated or the session is invalid.
        """
        session = self.session_manager.storage.get(user_id)
        if not session:
            return None

        token_manager = session.get("token_manager")
        if not token_manager:
            return None

        access_token = token_manager.get_access_token()
        if not access_token:
            return None

        tokens = {
            "access_token": access_token,
        }

        refresh_token = token_manager.tokens.get("refresh_token")
        if refresh_token:
            tokens["refresh_token"] = refresh_token

        return tokens

    # def login(self, params: Optional[Dict[str, Any]] = None) -> str:
    #     """
    #     Generate the login URL for user authentication.

    #     Args:
    #         params (Optional[Dict[str, Any]]): A dictionary of query parameters to include in the login URL.
    #                                           Supported keys: org_code, org_name, is_create_org, auth_url_params.

    #     Returns:
    #         str: The login URL.
    #     """
    #     # Default parameters
    #     default_params = {
    #         "client_id": self.client_id,
    #         "response_type": "code",
    #         "redirect_uri": self.redirect_uri,
    #         "scope": "openid profile email",  # Default scope
    #     }

    #     # Merge default parameters with user-provided parameters
    #     if params:
    #         # Handle organization-specific parameters
    #         if "org_code" in params:
    #             default_params["org_code"] = params["org_code"]
    #         if "org_name" in params:
    #             default_params["org_name"] = params["org_name"]
    #         if "is_create_org" in params:
    #             default_params["is_create_org"] = "true" if params["is_create_org"] else "false"

    #         # Handle additional auth URL parameters
    #         if "auth_url_params" in params and isinstance(params["auth_url_params"], dict):
    #             default_params.update(params["auth_url_params"])

    #     return f"{self.auth_url}?{urlencode(default_params)}"

    # def register(self, params: Optional[Dict[str, Any]] = None) -> str:
    #     """
    #     Generate the registration URL for user sign-up.

    #     Args:
    #         params (Optional[Dict[str, Any]]): A dictionary of query parameters to include in the registration URL.
    #                                           Supported keys: org_code, org_name, is_create_org, auth_url_params.

    #     Returns:
    #         str: The registration URL.
    #     """
    #     # Default parameters
    #     default_params = {
    #         "client_id": self.client_id,
    #         "response_type": "code",
    #         "redirect_uri": self.redirect_uri,
    #         "scope": "openid profile email",  # Default scope
    #     }

    #     # Merge default parameters with user-provided parameters
    #     if params:
    #         # Handle organization-specific parameters
    #         if "org_code" in params:
    #             default_params["org_code"] = params["org_code"]
    #         if "org_name" in params:
    #             default_params["org_name"] = params["org_name"]
    #         if "is_create_org" in params:
    #             default_params["is_create_org"] = "true" if params["is_create_org"] else "false"

    #         # Handle additional auth URL parameters
    #         if "auth_url_params" in params and isinstance(params["auth_url_params"], dict):
    #             default_params.update(params["auth_url_params"])

    #     return f"{self.auth_url}/register?{urlencode(default_params)}"


    def _get_auth_url(self, prompt: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Helper method to generate the authentication URL for login or registration.

        Args:
            prompt (Optional[str]): Set to "create" for registration.
            params (Optional[Dict[str, Any]]): A dictionary of query parameters to include in the URL.
                                            Supported keys: org_code, org_name, is_create_org, auth_url_params.

        Returns:
            str: The authentication URL.
        """
        # Default parameters
        default_params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": "openid profile email",  # Default scope
        }

        # Add prompt if provided (used for registration)
        if prompt:
            default_params["prompt"] = prompt

        # Merge default parameters with user-provided parameters
        if params:
            # Handle organization-specific parameters
            if "org_code" in params:
                default_params["org_code"] = params["org_code"]
            if "org_name" in params:
                default_params["org_name"] = params["org_name"]
            if "is_create_org" in params:
                default_params["is_create_org"] = "true" if params["is_create_org"] else "false"

            # Handle additional auth URL parameters
            if "auth_url_params" in params and isinstance(params["auth_url_params"], dict):
                default_params.update(params["auth_url_params"])

        return f"{self.auth_url}?{urlencode(default_params)}"

    def login(self, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate the login URL for user authentication.

        Args:
            params (Optional[Dict[str, Any]]): A dictionary of query parameters to include in the login URL.
                                            Supported keys: org_code, org_name, is_create_org, auth_url_params.

        Returns:
            str: The login URL.
        """
        return self._get_auth_url(params=params)

    def register(self, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate the registration URL for user sign-up.

        Args:
            params (Optional[Dict[str, Any]]): A dictionary of query parameters to include in the registration URL.
                                            Supported keys: org_code, org_name, is_create_org, auth_url_params.

        Returns:
            str: The registration URL.
        """
        return self._get_auth_url(prompt="create", params=params)
    

    """
    Example usage for login and register.
    # Login URL
    login_url = oauth_client.login(params={"org_code": "12345"})
    print(login_url)  # Output: https://auth.kinde.com?client_id=...&response_type=code&...

    # Registration URL
    register_url = oauth_client.register(params={"org_code": "12345"})
    print(register_url)  # Output: https://auth.kinde.com?client_id=...&response_type=code&...&prompt=create
    
    """