from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse, PlainTextResponse
from kinde_sdk.core.framework.framework_interface import FrameworkInterface
from kinde_sdk.core.exceptions import (
    CALLBACK_ERRORS,
    KindeCallbackError,
    UnmetAuthenticationRequirementsError,
)
from kinde_sdk.auth.oauth import OAuth
from ..middleware.framework_middleware import FrameworkMiddleware
import os
import uuid
import logging
import base64
import json
from urllib.parse import urlparse, parse_qs
from urllib.parse import urlencode, urlunparse

logger = logging.getLogger(__name__)

class FastAPIFramework(FrameworkInterface):
    """
    FastAPI framework implementation.
    This class provides FastAPI-specific functionality and integration.
    """
    
    def __init__(self, app: Optional[FastAPI] = None):
        """
        Initialize the FastAPI framework.
        
        Args:
            app (Optional[FastAPI]): The FastAPI application instance.
                If not provided, a new instance will be created.
        """
        self.app = app or FastAPI()
        self._initialized = False
        self._oauth = None
        self._logger = logging.getLogger(__name__)
    
    def get_name(self) -> str:
        """
        Get the name of the framework.
        
        Returns:
            str: The name of the framework
        """
        return "fastapi"
    
    def get_description(self) -> str:
        """
        Get a description of the framework.
        
        Returns:
            str: A description of the framework
        """
        return "FastAPI framework implementation for Kinde authentication"
    
    def start(self) -> None:
        """
        Start the framework.
        This method initializes any necessary FastAPI components and registers Kinde routes.
        """
        if not self._initialized:
            # Add framework middleware
            self.app.add_middleware(FrameworkMiddleware)
            
            # Register Kinde routes
            self._register_kinde_routes()

            # Default page for errors the callback hands to the app
            self._register_error_handlers()
            
            self._initialized = True
    
    def stop(self) -> None:
        """
        Stop the framework.
        This method cleans up any FastAPI resources.
        """
        if self._initialized:
            self._initialized = False
    
    def get_app(self) -> FastAPI:
        """
        Get the FastAPI application instance.
        
        Returns:
            FastAPI: The FastAPI application instance
        """
        return self.app
    
    def get_request(self) -> Optional[Request]:
        """
        Get the current request object.
        
        Returns:
            Optional[Request]: The current FastAPI request object, if available
        """
        from kinde_sdk.core.framework.framework_context import FrameworkContext
        return FrameworkContext.get_request()
    
    def get_user_id(self) -> Optional[str]:
        """
        Get the user ID from the current request.
        
        Returns:
            Optional[str]: The user ID, or None if not available
        """
        request = self.get_request()
        if not request:
            return None
        return request.session.get("user_id")
    
    def set_oauth(self, oauth: OAuth) -> None:
        """
        Set the OAuth instance for this framework.
        
        Args:
            oauth (OAuth): The OAuth instance
        """
        self._oauth = oauth
    
    def set_post_login_redirect_url(self, url: Optional[str] = None) -> None:
        """
        Remember where the callback route sends the user after the next
        sign-in or step-up.

        Args:
            url: The URL to return to. If None, the current page is used when
                the current request is a GET. For any other method nothing is
                remembered (a POST is never replayed), and a location left by
                an earlier, abandoned request is cleared.
        """
        request = self.get_request()
        if request is None:
            return
        if url is None:
            if request.method != "GET":
                request.session.pop('post_login_redirect_url', None)
                return
            url = str(request.url)
        request.session['post_login_redirect_url'] = {'url': url}

    def _register_error_handlers(self) -> None:
        """
        Register the default page for callback errors.

        The callback route raises UnmetAuthenticationRequirementsError and
        LoginRequiredError. Handle them with ``@app.exception_handler(...)``.
        This default only applies when the application has no handler of its own.
        """
        if KindeCallbackError not in self.app.exception_handlers:
            self.app.add_exception_handler(KindeCallbackError, self._default_callback_error_page)

    @staticmethod
    async def _default_callback_error_page(request: Request, error: KindeCallbackError):
        """Explain a callback error in plain words. The user stays signed in."""
        if isinstance(error, UnmetAuthenticationRequirementsError):
            message = (
                "We couldn't complete the extra verification needed for this action. "
                "Your account may not have a second sign-in method (such as an "
                "authenticator app) or a passkey set up yet."
            )
            status_code = 403
        else:
            message = "You need to sign in again to continue."
            status_code = 401
        if error.error_description:
            message = f"{message}\n\nDetails: {error.error_description}"
        return PlainTextResponse(message, status_code=status_code)

    def _register_kinde_routes(self) -> None:
        """
        Register all Kinde-specific routes with the FastAPI application.
        """
        # Helper function to get current user
        async def get_current_user():
            if not self._oauth.is_authenticated():
                return None
            try:
                return self._oauth.get_user_info()
            except ValueError:
                return None
        
        # Login route
        @self.app.get("/login")
        async def login(request: Request):
            """Redirect to Kinde login page."""
            # Build login options from query parameters
            login_options = {}
            
            # Check for invitation_code in query parameters
            invitation_code = request.query_params.get('invitation_code')
            if invitation_code:
                login_options['invitation_code'] = invitation_code
            
            url = await self._oauth.login(login_options)
            self._logger.warning(f"[Login] Session is: {request.session}")
            return RedirectResponse(url=url)
        
        # Callback route
        @self.app.get("/callback")
        async def callback(request: Request, code: Optional[str] = None, state: Optional[str] = None):
            """Handle the OAuth callback from Kinde."""
            error = request.query_params.get('error')
            if error and error.lower() == 'login_link_expired':
                reauth_state = request.query_params.get('reauth_state')
                if reauth_state:
                    try:
                        decoded_auth_state = base64.b64decode(reauth_state).decode('utf-8')
                        reauth_dict = json.loads(decoded_auth_state)

                        # Get the redirect URL from config
                        redirect_url = os.getenv("KINDE_REDIRECT_URI")
                        base_url = redirect_url.replace("/callback", "")

                        # Build the login route URL
                        login_route_url = f"{base_url}/login"

                        # Parse and add parameters properly
                        parsed = urlparse(login_route_url)
                        query_dict = parse_qs(parsed.query)

                        # Add reauth parameters
                        for key, value in reauth_dict.items():
                            query_dict[key] = [value]

                        # Build final URL
                        new_query = urlencode(query_dict, doseq=True)
                        login_url = urlunparse((
                            parsed.scheme,
                            parsed.netloc,
                            parsed.path,
                            parsed.params,
                            new_query,
                            parsed.fragment
                        ))

                        return RedirectResponse(login_url)
                    except Exception as ex:
                        return HTMLResponse(f"Error parsing reauth state: {str(ex)}", status_code=400)

            # A step-up the user cannot meet (or login_required after prompt=none)
            # is a final answer. Hand it to the app: the core validates the state
            # and raises the error. Never redirect to login or retry from here.
            if error in CALLBACK_ERRORS:
                assert self._oauth is not None
                try:
                    await self._oauth.handle_redirect(
                        code,
                        request.session.get('user_id'),
                        state,
                        error=error,
                        error_description=request.query_params.get('error_description'),
                    )
                except KindeCallbackError:
                    # The state was valid, so this answers the pending request
                    # and its return location is finished with. A callback
                    # with a wrong state leaves it for the genuine one.
                    request.session.pop('post_login_redirect_url', None)
                    raise
                except Exception as e:
                    return PlainTextResponse(f"Authentication failed: {str(e)}", status_code=400)
                return PlainTextResponse("Authentication failed", status_code=400)

            user_id = request.session.get('user_id') or str(uuid.uuid4())

            try:
                assert self._oauth is not None
                await self._oauth.handle_redirect(code, user_id, state)
            except Exception as e:
                if "State not found" in str(e):
                    return HTMLResponse("Error: State not found. Please check Kinde Python SDK documentation.\n" + str(e), status_code=500)
                raise e

            request.session['user_id'] = user_id

            # Initialize post_login_redirect
            post_login_redirect = request.session.pop('post_login_redirect_url', None)
            if post_login_redirect:
                post_login_redirect = post_login_redirect.get('url', '/')
            else:
                post_login_redirect = '/'

            if not post_login_redirect.startswith('http'):
                post_login_redirect = str(request.base_url).rstrip('/') + post_login_redirect

            parsed = urlparse(post_login_redirect)
            if state:
                query_dict = parse_qs(parsed.query)
                query_dict['state'] = [state]
                new_query = urlencode(query_dict, doseq=True)
                redirect_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
            else:
                redirect_url = post_login_redirect

            return RedirectResponse(redirect_url)
        
        # Logout route
        @self.app.get("/logout")
        async def logout(request: Request):
            """Logout the user and redirect to Kinde logout page."""
            request.session.clear()
            return RedirectResponse(url=await self._oauth.logout())
        
        # Register route
        @self.app.get("/register")
        async def register():
            """Redirect to Kinde registration page."""
            return RedirectResponse(url=await self._oauth.register())
        
        # User info route
        @self.app.get("/user")
        async def get_user():
            """Get the current user's information."""
            if not self._oauth.is_authenticated():
                return RedirectResponse(url=await self._oauth.login())
            return self._oauth.get_user_info()
    
    def can_auto_detect(self) -> bool:
        """
        Check if this framework can be auto-detected.
        
        Returns:
            bool: True if FastAPI is installed and available
        """
        try:
            import fastapi
            _ = fastapi  # Import check only
            return True
        except ImportError:
            return False 