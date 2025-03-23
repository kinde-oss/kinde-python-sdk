import os
import requests
import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode, urlparse, quote

from .user_session import UserSession
from .storage_factory import StorageFactory
from .config_loader import load_config
from .enums import GrantType, IssuerRouteTypes, PromptTypes
from .login_options import LoginOptions
from kinde_sdk.core.helpers import generate_random_string, base64_url_encode, generate_pkce_pair, get_user_details as helper_get_user_details
from kinde_sdk.exceptions import (
    KindeConfigurationException,
    KindeLoginException,
    KindeTokenException,
    KindeRetrieveException,
)

class OAuth:
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        config_file: Optional[str] = None,  #  config_file optional
        storage_config: Optional[Dict[str, Any]] = None,  # Add storage_config parameter
        framework: Optional[str] = None,  # Add framework property
        audience: Optional[str] = None,
        host: Optional[str] = None,
        state: Optional[str] = None,
    ):
        """Initialize the OAuth client."""
        # Fetch values from environment variables if not provided
        self.client_id = client_id or os.getenv("KINDE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("KINDE_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or os.getenv("KINDE_REDIRECT_URI")
        self.host = host or os.getenv("KINDE_HOST", "https://app.kinde.com")
        self.audience = audience or os.getenv("KINDE_AUDIENCE")
        self.state = state
        self.framework = framework
        
        # Validate required configurations
        if not self.client_id:
            raise KindeConfigurationException("Client ID is required.")
        

        # Set API endpoints
        self.auth_url = f"{self.host}/oauth2/auth"
        self.token_url = f"{self.host}/oauth2/token"
        self.logout_url = f"{self.host}/logout"
        self.userinfo_url = f"{self.host}/oauth2/userinfo"

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

    async def generate_auth_url(
        self,
        route_type: IssuerRouteTypes = IssuerRouteTypes.LOGIN,
        login_options: Dict[str, Any] = None,
        disable_url_sanitization: bool = False
    ) -> Dict[str, Any]:
        """
        Generate an authentication URL for login or registration.
        
        Args:
            route_type: Type of authentication route (login or register)
            login_options: Dictionary of login options
            disable_url_sanitization: Flag to disable URL sanitization
            
        Returns:
            Dictionary containing URL and security parameters
        """
        if login_options is None:
            login_options = {}
            
        # Define standard login parameters mapping with constants
        login_param_mapping = {
            # Standard OAuth params
            LoginOptions.RESPONSE_TYPE: "response_type", 
            LoginOptions.REDIRECT_URI: "redirect_uri",
            LoginOptions.SCOPE: "scope",
            LoginOptions.AUDIENCE: "audience",
            # Organization params
            LoginOptions.ORG_CODE: "org_code",
            LoginOptions.ORG_NAME: "org_name",
            LoginOptions.IS_CREATE_ORG: "is_create_org",
            # User experience params
            LoginOptions.PROMPT: "prompt",
            LoginOptions.LANG: "lang",
            LoginOptions.LOGIN_HINT: "login_hint",
            LoginOptions.CONNECTION_ID: "connection_id",
            LoginOptions.REDIRECT_URL: "redirect_url",
            LoginOptions.HAS_SUCCESS_PAGE: "has_success_page",
            LoginOptions.WORKFLOW_DEPLOYMENT_ID: "workflow_deployment_id",
        }
        
        # Base search parameters with defaults
        search_params = {
            "client_id": self.client_id,
            "response_type": login_options.get(LoginOptions.RESPONSE_TYPE, "code"),
            "redirect_uri": login_options.get(LoginOptions.REDIRECT_URI, self.redirect_uri),
            "scope": login_options.get(LoginOptions.SCOPE, "openid profile email"),
        }
        
        # Add audience if specified in the instance or options
        if self.audience or login_options.get(LoginOptions.AUDIENCE):
            search_params["audience"] = login_options.get(LoginOptions.AUDIENCE, self.audience)
        
        # Merge all supported params from login_options
        for option_key, param_key in login_param_mapping.items():
            if option_key in login_options and login_options[option_key] is not None:
                # Skip those already handled above
                if option_key in [LoginOptions.RESPONSE_TYPE, LoginOptions.REDIRECT_URI, 
                                 LoginOptions.SCOPE, LoginOptions.AUDIENCE]:
                    continue
                
                # Handle boolean parameters
                if option_key == LoginOptions.IS_CREATE_ORG or option_key == LoginOptions.HAS_SUCCESS_PAGE:
                    search_params[param_key] = "true" if login_options[option_key] else "false"
                else:
                    # Use string representation for query params
                    search_params[param_key] = str(login_options[option_key])
        
        # Add additional auth parameters
        if LoginOptions.AUTH_PARAMS in login_options and isinstance(login_options[LoginOptions.AUTH_PARAMS], dict):
            for key, value in login_options[LoginOptions.AUTH_PARAMS].items():
                # Convert all values to strings for URL parameters
                search_params[key] = str(value) if value is not None else ""
        
        # Generate state if not provided
        state = login_options.get(LoginOptions.STATE, generate_random_string(32))
        search_params["state"] = state
        self.session_manager.storage.set("state", {"value": state})
        
        # Generate nonce if not provided
        nonce = login_options.get(LoginOptions.NONCE, generate_random_string(16))
        search_params["nonce"] = nonce
        self.session_manager.storage.set("nonce", {"value": nonce})
        
        # Handle PKCE
        code_verifier = ""
        if login_options.get(LoginOptions.CODE_CHALLENGE):
            search_params["code_challenge"] = login_options[LoginOptions.CODE_CHALLENGE]
        else:
            # Generate PKCE pair
            pkce_data = await generate_pkce_pair(52)  # Use 52 chars to match JS implementation
            code_verifier = pkce_data["code_verifier"]
            search_params["code_challenge"] = pkce_data["code_challenge"]
            self.session_manager.storage.set("code_verifier", {"value": code_verifier})
        
        # Set code challenge method
        code_challenge_method = login_options.get(LoginOptions.CODE_CHALLENGE_METHOD, "S256")
        search_params["code_challenge_method"] = code_challenge_method
        
        # Set prompt for registration
        if route_type == IssuerRouteTypes.REGISTER and not search_params.get("prompt"):
            search_params["prompt"] = PromptTypes.CREATE.value
        
        # Build URL
        query_string = urlencode(search_params)
        auth_url = f"{self.auth_url}?{query_string}"
        
        return {
            "url": auth_url,
            "state": search_params["state"],
            "nonce": search_params["nonce"],
            "code_challenge": search_params.get("code_challenge", ""),
            "code_verifier": code_verifier,
        }
    
    async def login(self, login_options: Dict[str, Any] = None) -> str:
        """
        Generate login URL with the specified options.
        
        Args:
            login_options: Dictionary of login options including:
                - response_type: OAuth response type (default: 'code')
                - redirect_uri: URI to redirect after login
                - scope: OAuth scopes (default: 'openid profile email')
                - audience: API audience
                - org_code: Organization code
                - org_name: Organization name
                - is_create_org: Whether to create organization
                - prompt: Prompt option
                - lang: Language preference
                - login_hint: Login hint (email)
                - connection_id: Connection identifier
                - redirect_url: URL to redirect after authentication
                - has_success_page: Whether to show success page
                - workflow_deployment_id: Workflow deployment ID
                - auth_params: Additional auth parameters
                
        Returns:
            Login URL
        """
        if not self.framework:
            raise KindeConfigurationException("Framework must be selected")
        
        if login_options is None:
            login_options = {}
        
        auth_url_data = await self.generate_auth_url(
            route_type=IssuerRouteTypes.LOGIN,
            login_options=login_options
        )
        return auth_url_data["url"]
    
    async def register(self, login_options: Dict[str, Any] = None) -> str:
        """
        Generate registration URL with the specified options.
        
        Args:
            login_options: Dictionary of login options including:
                - response_type: OAuth response type (default: 'code')
                - redirect_uri: URI to redirect after registration
                - scope: OAuth scopes (default: 'openid profile email')
                - audience: API audience
                - org_code: Organization code
                - org_name: Organization name
                - is_create_org: Whether to create organization
                - prompt: Prompt option (will be set to 'create' if not specified)
                - lang: Language preference
                - login_hint: Login hint (email)
                - connection_id: Connection identifier
                - redirect_url: URL to redirect after authentication
                - has_success_page: Whether to show success page
                - workflow_deployment_id: Workflow deployment ID
                - auth_params: Additional auth parameters
                
        Returns:
            Registration URL
        """
        if not self.framework:
            raise KindeConfigurationException("Framework must be selected")

        if login_options is None:
            login_options = {}
        
        # Set prompt to 'create' for registration if not specified
        if not login_options.get("prompt"):
            login_options["prompt"] = PromptTypes.CREATE.value
        
        auth_url_data = await self.generate_auth_url(
            route_type=IssuerRouteTypes.REGISTER,
            login_options=login_options
        )
        return auth_url_data["url"]
    
    async def logout(self, user_id: Optional[str] = None, logout_options: Dict[str, Any] = None) -> str:
        """
        Generate the logout URL and clear session if user_id provided.
        
        Args:
            user_id: User identifier to clear session
            logout_options: Dictionary with logout options including:
                - post_logout_redirect_uri: URI to redirect after logout
                - state: State parameter for validation
                - id_token_hint: ID token hint for validation
            
        Returns:
            Logout URL
        """
        if not self.framework:
            raise KindeConfigurationException("Framework must be selected")

        if logout_options is None:
            logout_options = {}
        
        # Clear session if user_id provided
        if user_id:
            # Get ID token before logging out if not provided in options
            if "id_token_hint" not in logout_options and user_id:
                token_manager = self.session_manager.get_token_manager(user_id)
                if token_manager:
                    id_token = token_manager.get_id_token()
                    if id_token:
                        logout_options["id_token_hint"] = id_token
            
            # Perform logout (clear session)
            self.session_manager.logout(user_id)
        
        # Generate logout URL
        params = {
            "client_id": self.client_id,
        }
        
        # Add redirect URI
        redirect_uri = logout_options.get("post_logout_redirect_uri", self.redirect_uri)
        if redirect_uri:
            params["redirect_uri"] = redirect_uri
        
        # Add state if provided
        if "state" in logout_options:
            params["state"] = logout_options["state"]
        
        # Add ID token hint if provided
        if "id_token_hint" in logout_options:
            params["id_token_hint"] = logout_options["id_token_hint"]
        
        # Build logout URL
        query_string = urlencode(params)
        return f"{self.logout_url}?{query_string}"
    
    async def handle_redirect(self, code: str, user_id: str, state: Optional[str] = None) -> Dict[str, Any]:
        """
        Handle the OAuth redirect and exchange the code for tokens.
        
        Args:
            code: Authorization code from the redirect
            user_id: User identifier for token storage
            state: State parameter for verification
            
        Returns:
            Dict with user and token information
        """
        # Verify state if provided
        if state:
            stored_state = self.session_manager.storage.get("state")
            if not stored_state or state != stored_state.get("value"):
                self.logger.error(f"State mismatch: received {state}, stored {stored_state}")
                raise KindeLoginException("Invalid state parameter")
        
        # Get code verifier for PKCE
        code_verifier = None
        stored_code_verifier = self.session_manager.storage.get("code_verifier")
        if stored_code_verifier:
            code_verifier = stored_code_verifier.get("value")
            
            # Clean up the used code verifier
            self.session_manager.storage.delete("code_verifier")
        
        # Exchange code for tokens
        try:
            token_data = await self.exchange_code_for_tokens(code, code_verifier)
        except Exception as e:
            self.logger.error(f"Token exchange failed: {str(e)}")
            raise KindeTokenException(f"Failed to exchange code for tokens: {str(e)}")
        
        # Store tokens
        user_info = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "token_url": self.token_url,
            "redirect_uri": self.redirect_uri,
        }
        
        # Store session data
        self.session_manager.set_user_data(user_id, user_info, token_data)
        
        # Get user details using the token
        try:
            token_manager = self.session_manager.get_token_manager(user_id)
            if token_manager:
                user_details = await helper_get_user_details(
                    userinfo_url=self.userinfo_url,
                    token_manager=token_manager,
                    logger=self.logger
                )
            else:
                user_details = {}
        except Exception as e:
            self.logger.error(f"Failed to get user details: {str(e)}")
            user_details = {}
        
        # Clean up state
        if state:
            self.session_manager.storage.delete("state")
        
        # Clean up nonce
        self.session_manager.storage.delete("nonce")
        
        return {
            "tokens": token_data,
            "user": user_details
        }
    
    async def exchange_code_for_tokens(self, code: str, code_verifier: Optional[str] = None) -> Dict[str, Any]:
        """
        Exchange authorization code for tokens.
        
        Args:
            code: Authorization code
            code_verifier: PKCE code verifier
            
        Returns:
            Dict with token data
        """
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
        }
        
        # Add client secret if available (for non-PKCE flow)
        if self.client_secret:
            data["client_secret"] = self.client_secret
        
        # Add code verifier for PKCE flow
        if code_verifier:
            data["code_verifier"] = code_verifier
        
        response = requests.post(self.token_url, data=data)
        if response.status_code != 200:
            raise KindeTokenException(f"Token exchange failed: {response.text}")
        
        return response.json()
    
    def get_tokens(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve tokens and related information for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary containing tokens and token information or None if not authenticated
        """
        # Get token manager
        token_manager = self.session_manager.get_token_manager(user_id)
        if not token_manager:
            return None
        
        # Initialize tokens dictionary
        tokens = {}
        
        try:
            # Get access token
            access_token = token_manager.get_access_token()
            tokens["access_token"] = access_token
            
            # Get token expiration time
            if "expires_at" in token_manager.tokens:
                tokens["expires_at"] = token_manager.tokens["expires_at"]
                tokens["expires_in"] = max(0, int(token_manager.tokens["expires_at"] - time.time()))
            
            # Add refresh token if available
            if token_manager.tokens.get("refresh_token"):
                tokens["refresh_token"] = token_manager.tokens["refresh_token"]
                
            # Add ID token if available
            if token_manager.tokens.get("id_token"):
                tokens["id_token"] = token_manager.tokens["id_token"]
            
            # Add claims if available
            claims = token_manager.get_claims()
            if claims:
                tokens["claims"] = claims
                
            return tokens
        except Exception as e:
            self.logger.error(f"Error retrieving tokens: {str(e)}")
            return None