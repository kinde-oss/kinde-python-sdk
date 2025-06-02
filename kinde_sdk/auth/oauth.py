import os
import requests
import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlencode, urlparse, quote

from .user_session import UserSession
from kinde_sdk.core.storage.storage_manager import StorageManager
from kinde_sdk.core.storage.storage_factory import StorageFactory
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from .config_loader import load_config
from .enums import GrantType, IssuerRouteTypes, PromptTypes
from .login_options import LoginOptions
from kinde_sdk.core.helpers import generate_random_string, base64_url_encode, generate_pkce_pair, get_user_details as helper_get_user_details
from kinde_sdk.core.exceptions import (
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
        config_file: Optional[str] = None,
        storage_config: Optional[Dict[str, Any]] = None,
        framework: Optional[str] = None,
        audience: Optional[str] = None,
        host: Optional[str] = None,
        state: Optional[str] = None,
        app: Optional[Any] = None,
    ):
        """Initialize the OAuth client."""
        
        # Store original environment variables
        self._original_env = {
            "KINDE_CLIENT_ID": os.getenv("KINDE_CLIENT_ID"),
            "KINDE_CLIENT_SECRET": os.getenv("KINDE_CLIENT_SECRET"),
            "KINDE_REDIRECT_URI": os.getenv("KINDE_REDIRECT_URI"),
            "KINDE_HOST": os.getenv("KINDE_HOST"),
            "KINDE_AUDIENCE": os.getenv("KINDE_AUDIENCE")
        }

        # Fetch values from environment variables if not provided
        self.client_id = client_id or os.getenv("KINDE_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("KINDE_CLIENT_SECRET")
        self.redirect_uri = redirect_uri or os.getenv("KINDE_REDIRECT_URI")
        self.host = host or os.getenv("KINDE_HOST", "https://app.kinde.com")
        self.audience = audience or os.getenv("KINDE_AUDIENCE")
        self.state = state
        self.framework = framework
        self.app = app
        
        # Validate required configurations
        if not self.client_id:
            raise KindeConfigurationException("Client ID is required.")
        
        # Initialize API endpoints
        self._set_api_endpoints()

        # Load configuration
        if config_file:
            self._config = load_config(config_file)
            storage_config = self._config.get("storage", {"type": "memory"})
        elif storage_config is None:
            storage_config = {"type": "memory"}
            self._config = {"storage": storage_config}

        # Create storage manager
        self._storage_manager = StorageManager()
        
        # Initialize framework if specified (this will also set up framework-specific storage)
        if framework:
            self._initialize_framework()
        else:
            # Use configuration-based storage if no framework specified
            self._storage = StorageFactory.create_storage(storage_config)
            self._storage_manager.initialize(config=storage_config, storage=self._storage)

        self._session_manager = UserSession()

        # Logging settings
        self._logger = logging.getLogger("kinde_sdk")
        self._logger.setLevel(logging.INFO)

        # Authentication properties
        self.verify_ssl = True
        self.proxy = None
        self.proxy_headers = None

    def _initialize_framework(self) -> None:
        """
        Initialize the framework-specific components.
        This will set up the framework and its associated storage.
        """
        if not self.framework:
            raise KindeConfigurationException("Framework must be specified for initialization")

        # Get the framework implementation from the factory
        framework_impl = FrameworkFactory.create_framework(
            config={"type": self.framework},
            app=self.app
        )

        # Set the OAuth instance in the framework
        framework_impl.set_oauth(self)

        # Start the framework (this will set up middleware and routes)
        framework_impl.start()

        # Store the framework implementation
        self._framework = framework_impl

        # Create storage using the framework's storage factory
        self._storage = StorageFactory.create_storage({"type": self.framework})
        
        # Initialize storage manager with the framework-specific storage
        self._storage_manager.initialize(config={"type": self.framework, "device_id": self._framework.get_name()}, storage=self._storage)

    def is_authenticated(self) -> bool:
        """
        Check if the user is authenticated using the session manager.
        
        Args:
            request (Optional[Any]): The current request object
            
        Returns:
            bool: True if the user is authenticated, False otherwise
        """
        # Get user ID from framework
        self._logger.warning(f"self._framework: {self._framework}")
        user_id = self._framework.get_user_id()
        self._logger.warning(f"user_id: {user_id}")
        if not user_id:
            self._logger.warning("No user ID found in session")
            return False
            
        # Check authentication using session manager
        self._logger.warning(f"self._session_manager: {self._session_manager}")
        return self._session_manager.is_authenticated(user_id)

    def get_user_info(self) -> Dict[str, Any]:
        """
        Get the user information from the session.
        
        Args:
            request (Optional[Any]): The current request object
            
        Returns:
            Dict[str, Any]: The user information
            
        Raises:
            KindeConfigurationException: If no user ID is found in session
        """
        # Get user ID from framework
        self._logger.warning(f"Retrieve the user id")
        user_id = self._framework.get_user_id()
        if not user_id:
            raise KindeConfigurationException("No user ID found in session")
            
        # Get token manager for the user
        self._logger.warning(f"User id: {user_id} retrieve the token for the user id")
        token_manager = self._session_manager.get_token_manager(user_id)
        if not token_manager:
            raise KindeConfigurationException("No token manager found for user")
            
        # Get claims from token manager
        self._logger.warning(f"Get the claims from the token manager")
        claims = token_manager.get_claims()
        if not claims:
            raise KindeConfigurationException("No user claims found")
        self._logger.warning(f"Return the claims")
        return claims

    def _set_api_endpoints(self):
        """Set API endpoints based on the host URL."""
        # Attempt to fetch OpenID Configuration first
        try:
            self._fetch_openid_configuration()
        except Exception as e:
            self.auth_url = f"{self.host}/oauth2/auth"
            self.token_url = f"{self.host}/oauth2/token"
            self.logout_url = f"{self.host}/logout"
            self.userinfo_url = f"{self.host}/oauth2/userinfo"

    def _fetch_openid_configuration(self):
        """
        Fetch OpenID Configuration and update endpoints accordingly.
        """
        import requests
        
        # Construct the OpenID Configuration URL
        openid_config_url = f"{self.host}/.well-known/openid-configuration"
        
        # Make the request
        response = requests.get(openid_config_url)
        
        if response.status_code == 200:
            config = response.json()
            
            # Update endpoints with the values from the configuration
            self.auth_url = config.get("authorization_endpoint", f"{self.host}/oauth2/auth")
            self.token_url = config.get("token_endpoint", f"{self.host}/oauth2/token")
            self.logout_url = config.get("end_session_endpoint", f"{self.host}/logout")
            self.userinfo_url = config.get("userinfo_endpoint", f"{self.host}/oauth2/userinfo")
            
        else:
            self.auth_url = f"{self.host}/oauth2/auth"
            self.token_url = f"{self.host}/oauth2/token"
            self.logout_url = f"{self.host}/logout"
            self.userinfo_url = f"{self.host}/oauth2/userinfo"

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
            # Registration params
            LoginOptions.PLAN_INTEREST: "plan_interest",
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
        self._session_manager.storage_manager.setItems("state", {"value": state})
        
        # Generate nonce if not provided
        nonce = login_options.get(LoginOptions.NONCE, generate_random_string(16))
        search_params["nonce"] = nonce
        self._session_manager.storage_manager.setItems("nonce", {"value": nonce})
        
        # Handle PKCE
        code_verifier = ""
        if login_options.get(LoginOptions.CODE_CHALLENGE):
            search_params["code_challenge"] = login_options[LoginOptions.CODE_CHALLENGE]
        else:
            # Generate PKCE pair
            pkce_data = await generate_pkce_pair(52)  # Use 52 chars to match JS implementation
            code_verifier = pkce_data["code_verifier"]
            search_params["code_challenge"] = pkce_data["code_challenge"]
            self._session_manager.storage_manager.setItems("code_verifier", {"value": code_verifier})
        
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
                - plan_interest: Optional string indicating the plan of interest
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
                token_manager = self._session_manager.get_token_manager(user_id)
                if token_manager:
                    id_token = token_manager.get_id_token()
                    if id_token:
                        logout_options["id_token_hint"] = id_token
            
            # Perform logout (clear session)
            self._session_manager.logout(user_id)
        
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
            stored_state = self._session_manager.storage_manager.get("state")
            self._logger.warning(f"stored_state: {stored_state}, state: {state}")
            if not stored_state or state != stored_state.get("value"):
                self._logger.error(f"State mismatch: received {state}, stored {stored_state}")
                raise KindeLoginException("Invalid state parameter")
        
        # Get code verifier for PKCE
        code_verifier = None
        stored_code_verifier = self._session_manager.storage_manager.get("code_verifier")
        if stored_code_verifier:
            code_verifier = stored_code_verifier.get("value")
            
            # Clean up the used code verifier
            self._session_manager.storage_manager.delete("code_verifier")
        
        # Exchange code for tokens
        try:
            token_data = await self.exchange_code_for_tokens(code, code_verifier)
        except Exception as e:
            self._logger.error(f"Token exchange failed: {str(e)}")
            raise KindeTokenException(f"Failed to exchange code for tokens: {str(e)}")
        
        # Store tokens
        user_info = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "token_url": self.token_url,
            "redirect_uri": self.redirect_uri,
        }
        
        # Store session data
        self._session_manager.set_user_data(user_id, user_info, token_data)
        
        # Get user details using the token
        token_manager = self._session_manager.get_token_manager(user_id)
        if not token_manager:
            raise KindeRetrieveException("Failed to get token manager")
        
        # This will now throw the exception if it fails, allowing proper error handling
        user_details = await helper_get_user_details(
            userinfo_url=self.userinfo_url,
            token_manager=token_manager,
            logger=self._logger
        )
        
        # Clean up state
        if state:
            self._session_manager.storage_manager.delete("state")
        
        # Clean up nonce
        self._session_manager.storage_manager.delete("nonce")
        
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
        
        self._logger.warning(f"[Exchange code for tokens] [{self.token_url}] [{data}]")

        response = requests.post(self.token_url, data=data)
        self._logger.warning(f"[Exchange code for tokens] [{response.status_code}] [{response.text}]")
        if response.status_code != 200:
            raise KindeTokenException(f"Token exchange failed: {response.text}")
        
        return response.json()

    def get_tokens(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve tokens and related information for a user.
        
        Args:
            user_id: User identifier
                
        Returns:
            Dictionary containing tokens and token information
            
        Raises:
            ValueError: If no tokens are available for the user
        """
        # Get token manager
        token_manager = self._session_manager.get_token_manager(user_id)
        if not token_manager:
            raise ValueError(f"No token manager available for user {user_id}")
        
        # Initialize tokens dictionary
        tokens = {}
        
        try:
            access_token = None
            if "access_token" in token_manager.tokens:
                access_token = token_manager.get_access_token()
                if access_token:
                    tokens["access_token"] = access_token
                else:
                    raise ValueError(f"Invalid access token for user {user_id}")
            else:
                raise ValueError(f"No access token available for user {user_id}")
            
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
            if claims and len(claims) > 0:
                tokens["claims"] = claims
                
            return tokens
        except Exception as e:
            self._logger.error(f"Error retrieving tokens: {str(e)}")
            raise ValueError(f"Failed to retrieve tokens: {str(e)}")