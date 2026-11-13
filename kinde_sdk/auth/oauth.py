import hmac
import os
import requests
import logging
import time
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlencode

from .user_session import UserSession
from kinde_sdk.core.storage.storage_manager import StorageManager
from kinde_sdk.core.storage.storage_factory import StorageFactory
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from .config_loader import load_config
from .enums import IssuerRouteTypes, PromptTypes
from .login_options import LoginOptions
from kinde_sdk.core.helpers import generate_random_string, generate_pkce_pair, get_user_details as helper_get_user_details, get_user_details_sync
from kinde_sdk.core.exceptions import (
    KindeConfigurationException,
    KindeLoginException,
    KindeTokenException,
    KindeRetrieveException,
    KindeCallbackError,
    CALLBACK_ERRORS,
)
from .step_up import (
    authentication_context_from_claims,
    discovery_supports_step_up,
    has_authentication_context as _has_authentication_context,
    normalize_acr_values,
    normalize_max_age,
    normalize_step_up_auth_param,
    prompt_includes_none,
    strongest_acr,
)

# Seconds to wait before fetching the OpenID discovery document again after a
# failed fetch. Checks that run on every request wait longer than step_up(),
# which cannot go ahead without the document.
_DISCOVERY_RETRY_SECONDS = 60
_STEP_UP_DISCOVERY_RETRY_SECONDS = 5

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
        force_api: bool = False,
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
        self.force_api = force_api
        
        # Validate required configurations
        if not self.client_id:
            raise KindeConfigurationException("Client ID is required.")
        
        # OpenID discovery document, cached by _fetch_openid_configuration()
        self._openid_configuration = None
        self._openid_configuration_tried_at = 0.0

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
            # Use null framework for standalone usage
            self._initialize_null_framework(storage_config)

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
        
        # Initialize storage manager with the framework-specific storage. The
        # device id is part of every session key, so it must be the same in
        # every worker process: a generated one would hide a session stored by
        # one worker from all the others.
        self._storage_manager.initialize(
            config={"type": self.framework},
            device_id=self._framework.get_name(),
            storage=self._storage,
        )

    def _initialize_null_framework(self, storage_config: Dict[str, Any]) -> None:
        """
        Initialize the null framework for standalone usage.
        This sets up the null framework and its associated storage.
        """
        from kinde_sdk.core.framework.null_framework import NullFramework
        
        # Create null framework instance (singleton)
        self._framework = NullFramework()
        
        # Set the OAuth instance in the framework
        self._framework.set_oauth(self)
        
        # Start the framework (no-op for null framework)
        self._framework.start()
        
        # Create storage using provided config (defaulting to memory)
        storage_type = (storage_config or {}).get("type", "memory") if isinstance(storage_config, dict) else "memory"
        self._storage = StorageFactory.create_storage({**({"type": storage_type}), **(storage_config or {})})

        # Initialize storage manager with explicit device_id
        self._storage_manager.initialize(
            config={"type": storage_type},
            device_id=self._framework.get_name(),
            storage=self._storage,
        )

    def is_authenticated(self) -> bool:
        """
        Check if the user is authenticated using the session manager.
        
        Returns:
            bool: True if the user is authenticated, False otherwise
        """
        # Get user ID from framework
        self._logger.debug(f"self._framework: {self._framework}")
        user_id = self._framework.get_user_id()
        self._logger.debug(f"user_id: {user_id}")
        if not user_id:
            self._logger.debug("No user ID found in session")
            return False
            
        # Check authentication using session manager
        self._logger.debug(f"self._session_manager: {self._session_manager}")
        return self._session_manager.is_authenticated(user_id)

    def get_user_info(self) -> Dict[str, Any]:
        """
        Get the user information from the session.
        
        Returns:
            Dict[str, Any]: The user information
            
        Raises:
            KindeConfigurationException: If no user ID is found in session
        """
        # Get user ID from framework
        self._logger.debug(f"Retrieve the user id")
        user_id = self._framework.get_user_id()
        if not user_id:
            raise KindeConfigurationException("No user ID found in session")
            
        # Get token manager for the user
        self._logger.debug(f"User id: {user_id} retrieve the token for the user id")
        token_manager = self._session_manager.get_token_manager(user_id)
        if not token_manager:
            raise KindeConfigurationException("No token manager found for user")
        
        user_details = get_user_details_sync(
            userinfo_url=self.userinfo_url,
            token_manager=token_manager,
            logger=self._logger
        )
            
        # Get claims from token manager
        self._logger.info(f"Get the claims from the token manager {user_details}")
        return user_details

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

            # Keep the document for is_step_up_supported()
            if isinstance(config, dict):
                self._openid_configuration = config
            
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
            # Step-up authentication params
            LoginOptions.ACR_VALUES: "acr_values",
            LoginOptions.MAX_AGE: "max_age",
            # Registration params
            LoginOptions.PLAN_INTEREST: "plan_interest",
            LoginOptions.PRICING_TABLE_KEY: "pricing_table_key",
            # Invitation params
            LoginOptions.INVITATION_CODE: "invitation_code",
            LoginOptions.IS_INVITATION: "is_invitation",
            # Re-authentication support
            LoginOptions.SUPPORT_RE_AUTH: "supports_reauth",
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
                elif option_key == LoginOptions.IS_INVITATION:
                    # Only add is_invitation if it's truthy
                    if login_options[option_key]:
                        search_params[param_key] = "true"
                elif option_key == LoginOptions.ACR_VALUES:
                    # "mfa" / "phr" or a list of them, sent space-separated
                    search_params[param_key] = normalize_acr_values(login_options[option_key])
                elif option_key == LoginOptions.MAX_AGE:
                    # Rejected unless a non-negative int: Kinde reads a malformed
                    # max_age as "re-authenticate", which would hide the bug
                    search_params[param_key] = str(normalize_max_age(login_options[option_key]))
                else:
                    # Use string representation for query params
                    search_params[param_key] = str(login_options[option_key])
        
        # Handle invitation code: automatically set is_invitation to "true" when invitation_code is present
        if LoginOptions.INVITATION_CODE in login_options and login_options[LoginOptions.INVITATION_CODE]:
            if LoginOptions.IS_INVITATION not in login_options or not login_options[LoginOptions.IS_INVITATION]:
                search_params["is_invitation"] = "true"
        
        # Add additional auth parameters
        if LoginOptions.AUTH_PARAMS in login_options and isinstance(login_options[LoginOptions.AUTH_PARAMS], dict):
            for key, value in login_options[LoginOptions.AUTH_PARAMS].items():
                if key in (LoginOptions.ACR_VALUES, LoginOptions.MAX_AGE):
                    # Never send an unset or malformed step-up parameter
                    value = normalize_step_up_auth_param(key, value)
                    if value is None:
                        continue
                # Convert all values to strings for URL parameters
                search_params[key] = str(value) if value is not None else ""
        
        # Generate state if not provided
        state = login_options.get(LoginOptions.STATE, generate_random_string(32))
        search_params["state"] = state
        self._session_manager.storage_manager.setItems("user:state", {"value": state})
        
        # Generate nonce if not provided
        nonce = login_options.get(LoginOptions.NONCE, generate_random_string(16))
        search_params["nonce"] = nonce
        self._session_manager.storage_manager.setItems("user:nonce", {"value": nonce})
        
        # Handle PKCE
        code_verifier = ""
        if login_options.get(LoginOptions.CODE_CHALLENGE):
            search_params["code_challenge"] = login_options[LoginOptions.CODE_CHALLENGE]
        else:
            # Generate PKCE pair
            pkce_data = await generate_pkce_pair(52)  # Use 52 chars to match JS implementation
            code_verifier = pkce_data["code_verifier"]
            search_params["code_challenge"] = pkce_data["code_challenge"]
            self._session_manager.storage_manager.setItems("user:code_verifier", {"value": code_verifier})
        
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
                - pricing_table_key: Optional string indicating the pricing table key
                - acr_values: Required authentication context, "mfa" or "phr" (or a list)
                - max_age: Maximum age of the last authentication, in seconds (non-negative int)
                - auth_params: Additional auth parameters
                
        Returns:
            Login URL
        """
        if login_options is None:
            login_options = {}

        # Add support for re-authentication
        login_options[LoginOptions.SUPPORT_RE_AUTH] = "true"

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
                - pricing_table_key: Optional string indicating the pricing table key
                - acr_values: Required authentication context, "mfa" or "phr" (or a list)
                - max_age: Maximum age of the last authentication, in seconds (non-negative int)
                - auth_params: Additional auth parameters
                
        Returns:
            Registration URL
        """
        if login_options is None:
            login_options = {}

        # Add support for re-authentication
        login_options[LoginOptions.SUPPORT_RE_AUTH] = "true"
        
        # Set prompt to 'create' for registration if not specified
        if not login_options.get("prompt"):
            login_options["prompt"] = PromptTypes.CREATE.value
        
        auth_url_data = await self.generate_auth_url(
            route_type=IssuerRouteTypes.REGISTER,
            login_options=login_options
        )
        return auth_url_data["url"]
    
    async def step_up(
        self,
        acr: Optional[Union[str, List[str]]] = None,
        max_age: Optional[int] = None,
        login_options: Optional[Dict[str, Any]] = None,
        post_login_redirect_url: Optional[str] = None,
    ) -> str:
        """
        Generate the URL for a step-up authentication request (RFC 9470).

        Ask Kinde for a stronger or more recent authentication before a
        sensitive action. Kinde collects only what is missing, and the user
        keeps their session. This is a normal interactive login with
        ``acr_values`` and/or ``max_age``: redirect the user to the returned
        URL. The current tokens stay in place until the callback replaces them.

        Args:
            acr: Required context, ``"mfa"`` or ``"phr"`` (or a list of them).
            max_age: Maximum age of the last authentication, in seconds.
                ``0`` forces a fresh verification.
            login_options: The usual login options (see ``login()``).
            post_login_redirect_url: Where the framework's callback route sends
                the user afterwards. Defaults to the current page for GET
                requests. Ignored without a framework integration.

        Returns:
            The authorization URL.

        Raises:
            ValueError: If neither ``acr`` nor ``max_age`` is requested, a value
                is invalid, or ``prompt=none`` is passed (including through
                ``auth_params``). Kinde can't collect a factor without a screen.
            KindeConfigurationException: If the environment doesn't advertise
                step-up in its discovery document. Kinde would ignore
                ``acr_values`` and ``max_age`` there, so nothing is sent. To
                force a fresh sign-in on such an environment, use ``login()``
                with ``prompt=login``.
            KindeRetrieveException: If the discovery document could not be
                fetched, so support is unknown. This is temporary: the fetch
                is retried, at most once every few seconds.
        """
        options = dict(login_options) if login_options else {}
        auth_params = options.get(LoginOptions.AUTH_PARAMS)
        auth_params = dict(auth_params) if isinstance(auth_params, dict) else {}

        if acr is not None:
            options[LoginOptions.ACR_VALUES] = acr
        if max_age is not None:
            options[LoginOptions.MAX_AGE] = max_age

        # Kinde cannot collect a factor without showing a screen
        if prompt_includes_none(options.get(LoginOptions.PROMPT)) or prompt_includes_none(auth_params.get("prompt")):
            raise ValueError("step_up() cannot be used with prompt=none: step-up authentication is interactive")

        # Work out what will be sent. auth_params override the typed options.
        requested_acr = None
        if options.get(LoginOptions.ACR_VALUES) is not None:
            requested_acr = normalize_acr_values(options[LoginOptions.ACR_VALUES])
        passthrough_acr = normalize_step_up_auth_param("acr_values", auth_params.get("acr_values"))
        if passthrough_acr is not None:
            # Kinde silently ignores unrecognised values, which would skip the step-up
            if strongest_acr(passthrough_acr) is None:
                raise ValueError(f"Unsupported acr_values {passthrough_acr!r}. Expected 'mfa' or 'phr'")
            requested_acr = passthrough_acr

        requested_max_age = None
        if options.get(LoginOptions.MAX_AGE) is not None:
            requested_max_age = normalize_max_age(options[LoginOptions.MAX_AGE])
        passthrough_max_age = normalize_step_up_auth_param("max_age", auth_params.get("max_age"))
        if passthrough_max_age is not None:
            requested_max_age = int(passthrough_max_age)

        if requested_acr is None and requested_max_age is None:
            raise ValueError("step_up() requires acr, max_age, or both")

        # Kinde ignores acr_values and max_age unless the environment advertises
        # step-up. Sending them anyway would bring the user back unchanged, and
        # a guard that asks again would redirect in a loop.
        openid_configuration = self._get_openid_configuration(retry_after=_STEP_UP_DISCOVERY_RETRY_SECONDS)
        if openid_configuration is None:
            raise KindeRetrieveException(
                "Could not fetch the OpenID configuration, so it is not known whether this "
                "Kinde environment supports step-up authentication. Try again."
            )
        if not discovery_supports_step_up(openid_configuration):
            raise KindeConfigurationException(
                "Step-up authentication is not supported on this Kinde environment: its discovery "
                "document has no acr_values_supported, so acr_values and max_age would be ignored. "
                "To force a fresh sign-in there, use login() with prompt=login."
            )

        if auth_params or LoginOptions.AUTH_PARAMS in options:
            options[LoginOptions.AUTH_PARAMS] = auth_params

        # Same as login(): add support for re-authentication
        options[LoginOptions.SUPPORT_RE_AUTH] = "true"

        auth_url_data = await self.generate_auth_url(
            route_type=IssuerRouteTypes.LOGIN,
            login_options=options
        )

        # Remember what was asked for, so a callback error can say what was not met
        self._session_manager.storage_manager.setItems("user:step_up", {
            "state": auth_url_data["state"],
            "acr_values": requested_acr,
            "max_age": requested_max_age,
        })

        # Bring the user back to where they were, through the framework's
        # post-login redirect (a no-op without a framework integration)
        remember_redirect = getattr(self._framework, "set_post_login_redirect_url", None)
        if callable(remember_redirect):
            remember_redirect(post_login_redirect_url)

        return auth_url_data["url"]

    def is_step_up_supported(self) -> bool:
        """
        Check whether the Kinde environment supports step-up authentication.

        Reads ``acr_values_supported`` from the OpenID discovery document that
        is fetched when the client is created. If that fetch failed, it is
        retried here, at most once a minute.

        Returns:
            bool: True if step-up is supported. False if it isn't, or while the
            discovery document is unavailable (``step_up()`` tells the two
            apart). Without support, Kinde ignores ``acr_values`` and ``max_age``.
        """
        return discovery_supports_step_up(self._get_openid_configuration())

    def _get_openid_configuration(self, retry_after: float = _DISCOVERY_RETRY_SECONDS) -> Optional[Dict[str, Any]]:
        """
        Return the cached discovery document, or None if it is unavailable.

        A fetch that failed is not repeated until ``retry_after`` seconds have
        passed since the last attempt, so that an unreachable host is not
        waited on by every request.
        """
        config = getattr(self, "_openid_configuration", None)
        if config is not None:
            return config

        now = time.time()
        if now - getattr(self, "_openid_configuration_tried_at", 0.0) < retry_after:
            return None
        self._openid_configuration_tried_at = now

        try:
            response = requests.get(f"{self.host}/.well-known/openid-configuration", timeout=5)
            if response.status_code == 200:
                config = response.json()
                if isinstance(config, dict):
                    self._openid_configuration = config
                    return config
        except Exception as e:
            self._logger.warning(f"Failed to fetch OpenID configuration: {str(e)}")
        return None

    def get_authentication_context(self) -> Dict[str, Any]:
        """
        Get how the current user authenticated, from the session's tokens.

        Returns:
            Dict[str, Any]: ``{"acr": ..., "amr": [...], "auth_time": ...}``
                - acr: ``"mfa"``, ``"phr"``, or None for a single-factor sign-in
                - amr: the methods used (informational only), or ``[]``
                - auth_time: when the user last actively authenticated, in
                  seconds since the epoch, read from the ID token. None if
                  unknown, or if the environment doesn't support step-up
                  (the claim may then be the token's issue time).

            All three are empty when there is no signed-in user.

        Use this for UI decisions. On a server, make security decisions with
        ``has_authentication_context()`` on every request that needs them.
        """
        token_manager = None
        user_id = self._framework.get_user_id()
        if user_id:
            token_manager = self._session_manager.get_token_manager(user_id)
        if not token_manager:
            return authentication_context_from_claims()

        return authentication_context_from_claims(
            id_token_claims=token_manager.get_claims("id_token"),
            access_token_claims=token_manager.get_claims("access_token"),
            trust_auth_time=self.is_step_up_supported(),
        )

    def has_authentication_context(
        self,
        acr: Optional[Union[str, List[str]]] = None,
        max_age: Optional[int] = None,
    ) -> bool:
        """
        Check whether the current user's authentication meets a requirement.

        Args:
            acr: Required context, ``"mfa"`` or ``"phr"``. ``phr`` also meets ``mfa``.
            max_age: Maximum age of the last authentication, in seconds. ``0``
                is almost never met; use a short window such as 60 instead.

        Returns:
            bool: True if the user is signed in and meets the requirement.
            When it returns False, call ``step_up()`` with the same arguments.
            Refreshing tokens never changes the answer.

        Raises:
            ValueError: If ``acr`` or ``max_age`` is not a valid requirement.
        """
        # Validate first, so a mistyped requirement raises instead of returning False
        if acr is not None:
            normalize_acr_values(acr)
        if max_age is not None:
            normalize_max_age(max_age)

        if not self.is_authenticated():
            return False

        return _has_authentication_context(self.get_authentication_context(), acr=acr, max_age=max_age)

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

    async def handle_redirect(
        self,
        code: Optional[str],
        user_id: Optional[str],
        state: Optional[str] = None,
        error: Optional[str] = None,
        error_description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Handle the OAuth redirect and exchange the code for tokens.

        The tokens from the callback replace the session's access, ID and
        refresh tokens, including when the user is already signed in (for
        example after a step-up).
        
        Args:
            code: Authorization code from the redirect
            user_id: User identifier for token storage
            state: State parameter for verification
            error: The ``error`` parameter from the redirect, if any
            error_description: The ``error_description`` parameter from the redirect, if any
            
        Returns:
            Dict with user and token information

        Raises:
            UnmetAuthenticationRequirementsError: The redirect carried
                ``error=unmet_authentication_requirements``. This is final:
                don't retry and don't redirect to login.
            LoginRequiredError: The redirect carried ``error=login_required``.
            KindeCallbackError: The redirect carried any other ``error``.
            KindeLoginException: The state is missing or doesn't match.
        """
        if error:
            self._raise_callback_error(error, error_description, state)

        # Verify state if provided
        if state:
            stored_state = self._session_manager.storage_manager.get("user:state")
            self._logger.warning(f"stored_state: {stored_state}, state: {state}")
            if not stored_state or state != stored_state.get("value"):
                self._logger.error(f"State mismatch: received {state}, stored {stored_state}")
                raise KindeLoginException("Invalid state parameter")
        
        # Get code verifier for PKCE
        code_verifier = None
        stored_code_verifier = self._session_manager.storage_manager.get("user:code_verifier")
        if stored_code_verifier:
            code_verifier = stored_code_verifier.get("value")
            
            # Clean up the used code verifier
            self._session_manager.storage_manager.delete("user:code_verifier")
        
        # Exchange code for tokens
        try:
            token_data = await self.exchange_code_for_tokens(code, code_verifier)
        except Exception as e:
            self._logger.error(f"Token exchange failed: {str(e)}")
            raise KindeTokenException(f"Failed to exchange code for tokens: {str(e)}") from e
        
        # Store tokens
        user_info = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "token_url": self.token_url,
            "redirect_uri": self.redirect_uri,
        }
        
        # Store session data. The new tokens replace all of the stored ones, so
        # nothing issued before this authorization (such as a refresh token from
        # before a step-up) is left behind.
        self._session_manager.set_user_data(user_id, user_info, token_data, replace_tokens=True)
        
        # Get user details using the token
        token_manager = self._session_manager.get_token_manager(user_id)
        if not token_manager:
            raise KindeRetrieveException("Failed to get token manager")
        
        # Set the force_api setting on the token manager
        token_manager.set_force_api(self.force_api)
        
        # This will now throw the exception if it fails, allowing proper error handling
        user_details = await helper_get_user_details(
            userinfo_url=self.userinfo_url,
            token_manager=token_manager,
            logger=self._logger
        )
        
        # Clean up state
        if state:
            self._session_manager.storage_manager.delete("user:state")
        
        # Clean up nonce
        self._session_manager.storage_manager.delete("user:nonce")

        # Clean up the pending step-up request, if any
        self._session_manager.storage_manager.delete("user:step_up")
        
        return {
            "tokens": token_data,
            "user": user_details
        }

    def _raise_callback_error(self, error: str, error_description: Optional[str], state: Optional[str]) -> None:
        """
        Raise the exception for an OAuth error returned to the callback.

        The state is validated first, exactly once: the pending request is
        cleared, so the same error redirect cannot be replayed. Stored tokens
        are not touched, and nothing is retried.
        """
        storage = self._session_manager.storage_manager

        stored_state = storage.get("user:state")
        expected_state = stored_state.get("value") if stored_state else None
        if (
            not state
            or not expected_state
            or not hmac.compare_digest(str(state).encode("utf-8"), str(expected_state).encode("utf-8"))
        ):
            self._logger.error("State mismatch on an error callback")
            raise KindeLoginException("Invalid state parameter")

        # What the step-up request asked for, if this answers one
        pending = storage.get("user:step_up")
        if not isinstance(pending, dict) or pending.get("state") != state:
            pending = {}

        # The authorization response has arrived: this request is finished
        for key in ("user:state", "user:nonce", "user:code_verifier", "user:step_up"):
            storage.delete(key)

        error_class = CALLBACK_ERRORS.get(error)
        if error_class is not None:
            raise error_class(
                error_description,
                state,
                acr_values=pending.get("acr_values"),
                max_age=pending.get("max_age"),
            )
        raise KindeCallbackError(error_description, state, error=error)
    
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
        
        self._logger.debug(f"[Exchange code for tokens] [{self.token_url}] [{data}]")

        response = requests.post(self.token_url, data=data)
        self._logger.debug(f"[Exchange code for tokens] [{response.status_code}] [{response.text}]")
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
            raise ValueError(f"Failed to retrieve tokens: {str(e)}") from e