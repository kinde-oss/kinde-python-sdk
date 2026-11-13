from typing import Optional, TYPE_CHECKING
from flask import Flask, Response, request, redirect, session, has_request_context
from flask_session import Session
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
import asyncio
import logging
import secrets
import tempfile

if TYPE_CHECKING:
    from flask import Request

logger = logging.getLogger(__name__)

class FlaskFramework(FrameworkInterface):
    """
    Flask framework implementation.
    This class provides Flask-specific functionality and integration.
    """
    
    def __init__(self, app: Optional[Flask] = None):
        """
        Initialize the Flask framework.
        
        Args:
            app (Optional[Flask]): The Flask application instance.
                If not provided, a new instance will be created.
        """
        self.app = app or Flask(__name__)
        self._initialized = False
        self._oauth = None
        
        # Configure Flask session for server-side storage
        # This is required because OAuth tokens can exceed cookie size limits (~4KB)
        secret_key = os.getenv('SECRET_KEY')
        if not secret_key:
            secret_key = secrets.token_urlsafe(32)
            logger.warning(
                "SECRET_KEY not set. Generated a random key for this session. "
                "Set SECRET_KEY environment variable for production use."
            )
        self.app.config['SECRET_KEY'] = secret_key
        self.app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE', 'filesystem')
        self.app.config['SESSION_PERMANENT'] = False
        
        session_file_dir = os.getenv('SESSION_FILE_DIR')
        if not session_file_dir:
            # Create a secure temporary directory with restrictive permissions (0700)
            session_file_dir = tempfile.mkdtemp(prefix='kinde_flask_sessions_')
            os.chmod(session_file_dir, 0o700)
            logger.warning(
                f"SESSION_FILE_DIR not set. Using temporary directory: {session_file_dir}. "
                "Set SESSION_FILE_DIR environment variable for production use."
            )
        self.app.config['SESSION_FILE_DIR'] = session_file_dir
        
        # Initialize Flask-Session extension
        # Without this, SESSION_TYPE is ignored and Flask uses client-side cookie sessions
        Session(self.app)
        logger.debug("Flask-Session initialized with server-side storage")
        
    
    def get_name(self) -> str:
        """
        Get the name of the framework.
        
        Returns:
            str: The name of the framework
        """
        return "flask"
    
    def get_description(self) -> str:
        """
        Get a description of the framework.
        
        Returns:
            str: A description of the framework
        """
        return "Flask framework implementation for Kinde authentication"
    
    def start(self) -> None:
        """
        Start the framework.
        This method initializes any necessary Flask components and registers Kinde routes.
        """
        if not self._initialized:
            # Add framework middleware
            self.app.before_request(FrameworkMiddleware.before_request)
            self.app.after_request(FrameworkMiddleware.after_request)
            
            # Register Kinde routes
            self._register_kinde_routes()

            # Default page for errors the callback hands to the app
            self._register_error_handlers()
            
            self._initialized = True
    
    def stop(self) -> None:
        """
        Stop the framework.
        This method cleans up any Flask resources.
        """
        if self._initialized:
            self._initialized = False
    
    def get_app(self) -> Flask:
        """
        Get the Flask application instance.
        
        Returns:
            Flask: The Flask application instance
        """
        return self.app
    
    def get_request(self) -> Optional['Request']:
        """
        Get the current request object.
        
        Returns:
            Optional[Request]: The current Flask request object, if available
        """
        from kinde_sdk.core.framework.framework_context import FrameworkContext
        return FrameworkContext.get_request()
    
    def get_user_id(self) -> Optional[str]:
        """
        Get the user ID from the current request.
        
        Returns:
            Optional[str]: The user ID, or None if not available
        """
        session_id = session.get('user_id')
        if not session_id:
            return None
        return session_id
    
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
        if not has_request_context():
            return
        if url is None:
            if request.method != "GET":
                session.pop('post_login_redirect_url', None)
                return
            url = request.url
        session['post_login_redirect_url'] = {'url': url}

    def _register_error_handlers(self) -> None:
        """
        Register the default page for callback errors.

        The callback route raises UnmetAuthenticationRequirementsError and
        LoginRequiredError. Handle them with ``@app.errorhandler(...)``. This
        default only applies when the application has no handler of its own.
        """
        handlers = self.app.error_handler_spec[None][None]
        if KindeCallbackError not in handlers:
            self.app.register_error_handler(KindeCallbackError, self._default_callback_error_page)

    @staticmethod
    def _default_callback_error_page(error: KindeCallbackError):
        """Explain a callback error in plain words. The user stays signed in."""
        if isinstance(error, UnmetAuthenticationRequirementsError):
            message = (
                "We couldn't complete the extra verification needed for this action. "
                "Your account may not have a second sign-in method (such as an "
                "authenticator app) or a passkey set up yet."
            )
            status = 403
        else:
            message = "You need to sign in again to continue."
            status = 401
        if error.error_description:
            message = f"{message}\n\nDetails: {error.error_description}"
        return Response(message, status=status, mimetype="text/plain")

    @staticmethod
    def _run_async(coro):
        """
        Run an async coroutine in a new event loop, then close it.
        
        This helper ensures consistent event loop handling across all routes.
        Clears the event loop reference before closing to prevent use-after-close issues.
        
        Args:
            coro: The coroutine to run
            
        Returns:
            The result of the coroutine
        """
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            asyncio.set_event_loop(None)
            loop.close()
    
    def _register_kinde_routes(self) -> None:
        """
        Register all Kinde-specific routes with the Flask application.
        """
        # Login route
        @self.app.route('/login')
        def login():
            """Redirect to Kinde login page."""
            # Build login options from query parameters
            login_options = {}
            
            # Check for invitation_code in query parameters
            invitation_code = request.args.get('invitation_code')
            if invitation_code:
                login_options['invitation_code'] = invitation_code
            
            login_url = self._run_async(self._oauth.login(login_options))
            return redirect(login_url)

        # Callback route
        @self.app.route("/callback")
        def callback():
            """Handle the OAuth callback from Kinde."""
            import base64
            import json
            from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
            
            error = request.args.get('error')
            if error and error.lower() == 'login_link_expired':
                reauth_state = request.args.get('reauth_state')
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

                        return redirect(login_url)
                    except Exception as ex:
                        return f"Error parsing reauth state: {str(ex)}", 400

            # A step-up the user cannot meet (or login_required after prompt=none)
            # is a final answer. Hand it to the app: the core validates the state
            # and raises the error. Never redirect to login or retry from here.
            if error in CALLBACK_ERRORS:
                try:
                    self._run_async(self._oauth.handle_redirect(
                        request.args.get('code'),
                        session.get('user_id'),
                        request.args.get('state'),
                        error=error,
                        error_description=request.args.get('error_description'),
                    ))
                except KindeCallbackError:
                    # The state was valid, so this answers the pending request
                    # and its return location is finished with. A callback
                    # with a wrong state leaves it for the genuine one.
                    session.pop('post_login_redirect_url', None)
                    raise
                except Exception as e:
                    return f"Authentication failed: {str(e)}", 400
                return "Authentication failed", 400

            # Read the return location, and drop it only once the callback has
            # been accepted: a callback with a wrong state must not discard it
            post_login_redirect = session.get('post_login_redirect_url')
            if post_login_redirect:
                post_login_redirect = post_login_redirect.get('url', '/')
            else:
                post_login_redirect = '/'

            code = request.args.get('code')
            state = request.args.get('state')
            
            # Validate required code parameter
            if not code:
                return "Authentication failed: Missing authorization code", 400
            
            # Get or generate user_id
            user_id = session.get('user_id', str(uuid.uuid4()))
            session['user_id'] = user_id
            
            # Handle async call to handle_redirect
            try:
                self._run_async(self._oauth.handle_redirect(code, user_id, state))
            except Exception as e:
                return f"Authentication failed: {str(e)}", 400

            session.pop('post_login_redirect_url', None)

            if not post_login_redirect.startswith('http'):
                # Use url_root to get just the scheme and host without the current path
                post_login_redirect = str(request.url_root).rstrip('/') + post_login_redirect

            # After successful authentication, simply redirect to the destination
            return redirect(post_login_redirect)
        
        # Logout route
        @self.app.route('/logout')
        def logout():
            """Logout the user and redirect to Kinde logout page."""
            user_id = session.get('user_id')
            session.clear()
            logout_url = self._run_async(self._oauth.logout(user_id))
            return redirect(logout_url)
        
        # Register route
        @self.app.route('/register')
        def register():
            """Redirect to Kinde registration page."""
            register_url = self._run_async(self._oauth.register())
            return redirect(register_url)
        
        # User info route
        @self.app.route('/user')
        def get_user():
            """Get the current user's information."""
            try:
                if not self._oauth.is_authenticated():
                    login_url = self._run_async(self._oauth.login())
                    return redirect(login_url)
                
                return self._oauth.get_user_info()
            except Exception as e:
                return f"Failed to get user info: {str(e)}", 400
    
    def can_auto_detect(self) -> bool:
        """
        Check if this framework can be auto-detected.
        
        Returns:
            bool: True if Flask is installed and available
        """
        try:
            import flask
            _ = flask  # Import check only
            return True
        except ImportError:
            return False