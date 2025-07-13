from typing import Optional, Dict, Any
import urllib.parse
import requests
from .tokens import Tokens
from .utils import generate_random_string, generate_code_challenge
from .session import SessionInterface, InMemorySession

class RedirectRequired(Exception):
    """Custom exception to signal a redirect is needed."""
    def __init__(self, url: str):
        self.url = url
        super().__init__(f"Redirect required to: {url}")

class OAuth:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        host: str,
        scopes: Optional[list] = None,
        session_interface: Optional[SessionInterface] = None,
        callback_path: str = "/kinde_callback",
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        print(f'Configured redirect_uri: {redirect_uri}')  # Debug print
        self.host = host
        self.scopes = scopes or ["openid", "profile", "email", "offline"]
        self.token_endpoint = f"{host}/oauth2/token"
        self.authorize_endpoint = f"{host}/oauth2/auth"
        self.callback_path = callback_path
        self.session = session_interface or InMemorySession()
        self._state = None
        self._code_verifier = None
        self._silent_reauth_attempted = False

    def get_authorize_url(self, additional_params: Optional[Dict[str, str]] = None) -> str:
        """Generate OAuth authorization URL, similar to js-utils generateAuthUrl."""
        # Generate new state and code verifier for each request
        state = generate_random_string()
        code_verifier = generate_random_string()
        
        # Store in session
        self.session.set("code_verifier", code_verifier)
        self.session.set("state", state)
        
        # Also store in instance variables for backward compatibility
        self._state = state
        self._code_verifier = code_verifier
        
        print(f"Generated new state: {state}")
        print(f"Generated new code_verifier: {code_verifier}")
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "state": state,
            "code_challenge": generate_code_challenge(code_verifier),
            "code_challenge_method": "S256",
        }
        if additional_params:
            params.update(additional_params)
        
        return f"{self.authorize_endpoint}?{urllib.parse.urlencode(params)}"

    def get_token(self, code: str) -> Dict[str, str]:
        """Exchange authorization code for tokens."""
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        # Get code verifier from session
        code_verifier = self.session.get("code_verifier")
        print(f"Code verifier from session: {code_verifier}")
        
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": code_verifier,
        }
        response = requests.post(self.token_endpoint, headers=headers, data=data)
        response.raise_for_status()
        tokens_data = response.json()
        Tokens.set_access_token(tokens_data["access_token"])
        if "refresh_token" in tokens_data:
            Tokens.set_refresh_token(tokens_data["refresh_token"])
        return tokens_data

    def refresh_token(self, refresh_token: str) -> Dict[str, str]:
        """Refresh access token using refresh token (silent)."""
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": refresh_token,
        }
        response = requests.post(self.token_endpoint, headers=headers, data=data)
        response.raise_for_status()
        tokens_data = response.json()
        Tokens.set_access_token(tokens_data["access_token"])
        if "refresh_token" in tokens_data:
            Tokens.set_refresh_token(tokens_data["refresh_token"])
        return tokens_data

    def is_authenticated(self) -> bool:
        """Check if the user is authenticated, attempting silent refresh if needed."""
        access_token = Tokens.get_access_token()
        if access_token and Tokens.is_token_valid(access_token):
            return True
        
        # Try silent refresh with refresh token
        refresh_token = Tokens.get_refresh_token()
        if refresh_token:
            try:
                self.refresh_token(refresh_token)
                return True
            except Exception:
                pass  # Refresh failed
        
        return False

    def get_silent_auth_url(self, redirect_uri: Optional[str] = None) -> Optional[str]:
        """Generate URL for silent re-authentication using prompt=none."""
        additional_params = {"prompt": "none"}
        redirect_uri = redirect_uri or self.redirect_uri
        if redirect_uri:
            additional_params["redirect_uri"] = redirect_uri
        try:
            return self.get_authorize_url(additional_params=additional_params)
        except Exception as e:
            print(f"Silent re-auth URL generation failed: {e}")
            return None

    def perform_silent_auth(self, silent_auth_url: str) -> bool:
        """Perform silent auth in background (server-side simulation). 
        Note: This is a placeholder; in a real web app, use client-side JS/iframe for true silence.
        Here, we attempt a server-side request, but it may not fully work without browser context."""
        try:
            # Simulate a background request (not truly silent in Python, but attempts non-interactive)
            response = requests.get(silent_auth_url, allow_redirects=False)
            if response.status_code == 302:  # Redirect indicates success or failure
                location = response.headers.get('Location', '')
                parsed = urllib.parse.urlparse(location)
                query_params = urllib.parse.parse_qs(parsed.query)
                code = query_params.get('code', [None])[0]
                state = query_params.get('state', [None])[0]
                error = query_params.get('error', [None])[0]
                return self.callback_handler(code, error, state)
            return False
        except Exception as e:
            print(f"Silent auth failed: {e}")
            return False

    def callback_handler(self, code: Optional[str] = None, error: Optional[str] = None, state: Optional[str] = None) -> bool:
        """Handle OAuth callback parameters."""
        self._silent_reauth_attempted = False
        
        # Debug state comparison
        stored_state = self.session.get("state")
        print(f"Callback state: {state}")
        print(f"Stored state: {stored_state}")
        
        if state != stored_state:
            print("State mismatch: possible CSRF attack")
            return False
        if error:
            print(f"Callback error: {error}")
            return False
        if not code:
            return False
        
        try:
            tokens_data = self.get_token(code)
            # Clear the state after successful callback
            self.session.set("state", "")
            return True
        except Exception as e:
            print(f"Callback token exchange failed: {e}")
            return False

    def get_user_details(self) -> Dict[str, Any]:
        """Get user details from the userinfo endpoint."""
        if not self.is_authenticated():
            raise ValueError("User is not authenticated")
        access_token = Tokens.get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Try the correct Kinde endpoints
        endpoints = [
            f"{self.host}/oauth2/v2/user_profile",  # Kinde v2 user profile endpoint
            f"{self.host}/oauth2/user_profile",     # Kinde v1 user profile endpoint
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(endpoint, headers=headers)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch user details from {endpoint}: {e}")
                continue
        
        raise ValueError("Could not fetch user details from any endpoint")

    def get_access_token(self) -> Optional[str]:
        """Retrieve the current access token."""
        return Tokens.get_access_token()

    def get_refresh_token(self) -> Optional[str]:
        """Retrieve the current refresh token."""
        return Tokens.get_refresh_token()

"""
def check_auth(self) -> Dict[str, Any]:
    access_token = Tokens.get_access_token()
    if access_token and Tokens.is_token_valid(access_token):
        return {
            'success': True,
            'access_token': access_token,
            'refresh_token': Tokens.get_refresh_token()
        }
    
    refresh_token = Tokens.get_refresh_token()
    if not refresh_token:
        return {'success': False, 'error': 'No refresh token available'}
    
    try:
        tokens_data = self.refresh_token(refresh_token)
        return {
            'success': True,
            'access_token': tokens_data.get('access_token'),
            'refresh_token': tokens_data.get('refresh_token')
        }
    except Exception as e:
        return {'success': False, 'error': f'Refresh failed: {str(e)}'}
"""
from datetime import date
from flask import Flask, url_for, render_template, request, session, jsonify, redirect
from flask_session import Session
from functools import wraps
import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

# Add the local kinde-python-sdk to Python path if needed
sys.path.insert(0, '/Users/brandtkruger/Projects/kinde-python-sdk')

# Load environment variables from .env file
load_dotenv()

# Import kinde_flask to register the Flask framework
import kinde_flask

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth import claims, feature_flags, permissions, tokens
from kinde_sdk.management import ManagementClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize Kinde OAuth with required parameters from environment
kinde_oauth = OAuth(
    client_id=os.getenv('KINDE_CLIENT_ID'),
    client_secret=os.getenv('KINDE_CLIENT_SECRET'),
    redirect_uri=os.getenv('KINDE_REDIRECT_URI'),
    host=os.getenv('KINDE_HOST')
)

def get_authorized_data():
    logger.info("get_authorized_data: Starting authentication check")
    
    if not kinde_oauth.is_authenticated():
        logger.warning("get_authorized_data: User is not authenticated")
        return {}
    
    logger.info("get_authorized_data: User is authenticated, getting user info")
    try:
        user = kinde_oauth.get_user_details()
        logger.info(f"get_authorized_data: User: {user}")
    except Exception as e:
        logger.error(f"Error getting user details: {e}")
        return {}
    
    if not user:
        logger.warning("get_authorized_data: Failed to get user info")
        return {}
    
    logger.info(f"get_authorized_data: Successfully retrieved user info for user ID: {user.get('id', 'unknown')}")
    
    try:
        id_token = tokens.get_token_manager().get_id_token()
        logger.info(f"get_authorized_data: ID token: {id_token}")
        access_token = tokens.get_token_manager().get_access_token()
        logger.info(f"get_authorized_data: Access token: {access_token}")
        claims_data = tokens.get_token_manager().get_claims()
        logger.info(f"get_authorized_data: Claims: {claims_data}")
    except Exception as e:
        logger.error(f"Error getting tokens: {e}")
        id_token = None
        access_token = None
        claims_data = None
    
    user_data = {
        "id": user.get("id"),
        "user_given_name": user.get("given_name"),
        "user_family_name": user.get("family_name"),
        "user_email": user.get("email"),
        "user_picture": user.get("picture"),
    }
    
    logger.info(f"get_authorized_data: Returning user data: {user_data}")
    return user_data


def get_management_client():
    """
    Creates and returns a ManagementClient instance with proper error handling.
    Returns None if environment variables are missing or client creation fails.
    """
    # Validate required environment variables
    required_env_vars = ["KINDE_DOMAIN", "KINDE_MANAGEMENT_CLIENT_ID", "KINDE_MANAGEMENT_CLIENT_SECRET"]
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        return None
    
    try:
        # Initialize ManagementClient with environment variables
        management_client = ManagementClient(
            domain=os.getenv("KINDE_DOMAIN"),
            client_id=os.getenv("KINDE_MANAGEMENT_CLIENT_ID"),
            client_secret=os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET")
        )
        logger.info("ManagementClient created successfully")
        return management_client
        
    except Exception as ex:
        logger.error(f"Failed to create ManagementClient: {ex}")
        return None


@app.route("/test_silent_auth")
def test_silent_auth():
    """
    Test endpoint for silent authentication using iframe approach.
    This provides the same functionality as js-utils silent auth.
    """
    # If already authenticated, redirect to home
    if kinde_oauth.is_authenticated():
        return redirect(url_for('index'))
    
    try:
        # Check if get_silent_auth_url method exists
        if hasattr(kinde_oauth, 'get_silent_auth_url'):
            silent_url = kinde_oauth.get_silent_auth_url(
                redirect_uri=url_for('silent_callback', _external=True)
            )
        else:
            # Fallback to regular authorize URL with prompt=none
            silent_url = kinde_oauth.get_authorize_url(
                additional_params={"prompt": "none"}
            )
        
        # Return HTML page with iframe for silent authentication
        return f'''<!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Silent Authentication</title>
            <meta http-equiv="Content-Security-Policy" content="
                frame-src 'self' https://*.kinde.com;
                script-src 'self' 'unsafe-inline';
                connect-src 'self';
            ">
        </head>
        <body>
            <div id="status">Checking authentication...</div>
            <iframe id="silent-iframe" src="{silent_url}" style="display:none;"></iframe>
            <script>
                let authTimeout = setTimeout(() => {{
                    document.getElementById('status').innerHTML = 'Authentication required - <a href="/login">Please login</a>';
                }}, 10000);
                
                window.addEventListener('message', function(event) {{
                    clearTimeout(authTimeout);
                    
                    if (event.data && typeof event.data === 'string') {{
                        if (event.data.includes('code=')) {{
                            const urlParams = new URLSearchParams(event.data.split('?')[1]);
                            const code = urlParams.get('code');
                            const state = urlParams.get('state');
                            
                            if (code) {{
                                fetch('/exchange_silent_code', {{
                                    method: 'POST',
                                    headers: {{'Content-Type': 'application/json'}},
                                    body: JSON.stringify({{
                                        code: code,
                                        state: state
                                    }})
                                }}).then(response => {{
                                    if (response.ok) {{
                                        document.getElementById('status').innerHTML = 'Authentication successful! Redirecting...';
                                        setTimeout(() => {{
                                            window.location.href = '/';
                                        }}, 1000);
                                    }} else {{
                                        document.getElementById('status').innerHTML = 'Authentication failed - <a href="/login">Please login</a>';
                                    }}
                                }}).catch(error => {{
                                    console.error('Error during token exchange:', error);
                                    document.getElementById('status').innerHTML = 'Authentication error - <a href="/login">Please login</a>';
                                }});
                            }}
                        }} else if (event.data.includes('error=')) {{
                            document.getElementById('status').innerHTML = 'Authentication failed - <a href="/login">Please login</a>';
                        }}
                    }}
                }});
            </script>
        </body>
        </html>'''
        
    except Exception as e:
        logger.error(f"Error generating silent auth URL: {e}")
        return redirect(url_for('login'))


@app.route("/silent_callback")
def silent_callback():
    """
    Handle the silent authentication callback from the iframe.
    """
    try:
        if 'code' in request.args:
            return f'''<!DOCTYPE html>
            <html>
            <head><title>Silent Auth Callback</title></head>
            <body>
                <script>
                    if (window.parent && window.parent !== window) {{
                        window.parent.postMessage(window.location.search, '*');
                    }}
                </script>
            </body>
            </html>'''
        else:
            error = request.args.get('error', 'unknown_error')
            return f'''<!DOCTYPE html>
            <html>
            <head><title>Silent Auth Error</title></head>
            <body>
                <script>
                    if (window.parent && window.parent !== window) {{
                        window.parent.postMessage('error={error}', '*');
                    }}
                </script>
            </body>
            </html>'''
    except Exception as e:
        logger.error(f"Error in silent callback: {e}")
        return f'''<!DOCTYPE html>
        <html>
        <head><title>Silent Auth Error</title></head>
        <body>
            <script>
                if (window.parent && window.parent !== window) {{
                    window.parent.postMessage('error=callback_error', '*');
                }}
            </script>
        </body>
        </html>'''


@app.route("/exchange_silent_code", methods=['POST'])
def exchange_silent_code():
    """
    Exchange the authorization code from silent auth for tokens.
    """
    try:
        data = request.get_json()
        code = data.get('code')
        state = data.get('state')
        
        if not code:
            logger.error("No authorization code received for silent auth")
            return jsonify({'error': 'No authorization code'}), 400
        
        # Use the OAuth client to handle the callback
        success = kinde_oauth.callback_handler(
            code=code,
            state=state
        )
        
        if success:
            logger.info("Silent authentication successful")
            return jsonify({'success': True})
        else:
            logger.error("Silent authentication failed during token exchange")
            return jsonify({'error': 'Authentication failed'}), 400
            
    except Exception as e:
        logger.error(f"Error during silent auth token exchange: {e}")
        return jsonify({'error': 'Server error'}), 500


@app.before_request
def check_auth_before_request():
    """
    Check authentication before each request.
    The SDK should handle token refresh internally.
    """
    # Skip authentication check for these endpoints
    skip_auth_endpoints = [
        'login', 'logout', 'callback', 'silent_callback', 
        'exchange_silent_code', 'test_silent_auth', 'static'
    ]
    
    if request.endpoint in skip_auth_endpoints:
        return
    
    # For protected routes, check if user is authenticated
    if not kinde_oauth.is_authenticated():
        if request.endpoint != 'index':
            return redirect(url_for('test_silent_auth'))


@app.route("/")
def index():
    data = {"current_year": date.today().year}
    template = "logged_out.html"
    if kinde_oauth.is_authenticated():
        user_data = get_authorized_data()
        data.update(user_data)
        template = "home.html"
    return render_template(template, **data)


@app.route("/details")
def get_details():
    template = "logged_out.html"
    data = {"current_year": date.today().year}

    if kinde_oauth.is_authenticated():
        user_data = get_authorized_data()
        data.update(user_data)
        try:
            data["access_token"] = tokens.get_token_manager().get_access_token()
        except Exception as e:
            logger.error(f"Error getting access token: {e}")
            data["access_token"] = None
        template = "details.html"

    return render_template(template, **data)


@app.route("/helpers")
def get_helper_functions():
    template = "logged_out.html"
    data = {"current_year": date.today().year}

    if kinde_oauth.is_authenticated():
        user_data = get_authorized_data()
        data.update(user_data)
        
        try:
            # Handle async calls using event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Get claims
            data["claim"] = loop.run_until_complete(claims.get_all_claims())
            
            # Get feature flags
            flag_result = loop.run_until_complete(feature_flags.get_flag("theme", "red"))
            data["flag"] = flag_result.value if hasattr(flag_result, 'value') else flag_result
            
            bool_flag_result = loop.run_until_complete(feature_flags.get_flag("is_dark_mode", False))
            data["bool_flag"] = bool_flag_result.value if hasattr(bool_flag_result, 'value') else bool_flag_result
            
            str_flag_result = loop.run_until_complete(feature_flags.get_flag("theme", "red"))
            data["str_flag"] = str_flag_result.value if hasattr(str_flag_result, 'value') else str_flag_result
            
            int_flag_result = loop.run_until_complete(feature_flags.get_flag("competitions_limit", 10))
            data["int_flag"] = int_flag_result.value if hasattr(int_flag_result, 'value') else int_flag_result

            org_codes = loop.run_until_complete(claims.get_claim("org_codes","id_token"))
            data["user_organizations"] = org_codes
            
            loop.close()
        except Exception as e:
            logger.error(f"Error retrieving async data: {e}")
            data["claim"] = None
            data["flag"] = "red"
            data["bool_flag"] = False
            data["str_flag"] = "red"
            data["int_flag"] = 10
            data["user_organizations"] = []

        # Get organization data using Management API
        management_client = get_management_client()
        if management_client is not None:
            try:
                all_orgs_response = management_client.get_organizations()
                data["organization"] = all_orgs_response.organizations if hasattr(all_orgs_response, 'organizations') else []
                logger.info(f"Retrieved {len(data['organization'])} total organizations")
            except Exception as org_ex:
                logger.warning(f"Could not retrieve all organizations: {org_ex}")
                data["organization"] = []
        else:
            data["organization"] = []
        
        template = "helpers.html"
    else:
        template = "logged_out.html"

    return render_template(template, **data)


@app.route("/api_demo")
def get_api_demo():
    template = "api_demo.html"
    data = {"current_year": date.today().year}
    
    if kinde_oauth.is_authenticated():
        user_data = get_authorized_data()
        data.update(user_data)
        
        management_client = get_management_client()
        if management_client is None:
            data['is_api_call'] = False
            data['error_message'] = "Failed to initialize management client"
        else:
            try:
                api_response = management_client.get_users()
                logger.info(f"Management API response received: {len(api_response.users) if api_response.users else 0} users")
                data['users'] = [
                    {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'total_sign_ins': int(user.total_sign_ins)
                    }
                    for user in api_response.users
                ]
                data['is_api_call'] = True
            except Exception as ex:
                data['is_api_call'] = False
                logger.error(f"Management API error: {ex}")
                data['error_message'] = str(ex)

    return render_template(template, **data)


@app.route("/login")
def login():
    # Generate login URL and redirect
    login_url = kinde_oauth.get_authorize_url()
    return redirect(login_url)

@app.route("/logout")
def logout():
    # Clear tokens and redirect to logout URL
    tokens.get_token_manager().clear_tokens()
    logout_url = f"{os.getenv('KINDE_HOST')}/logout?redirect={url_for('index', _external=True)}"
    return redirect(logout_url)

@app.route("/callback")
def callback():
    # Handle OAuth callback
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    if error:
        logger.error(f"OAuth callback error: {error}")
        return redirect(url_for('index'))
    
    if not code:
        logger.error("No authorization code received")
        return redirect(url_for('index'))
    
    # Use callback handler
    success = kinde_oauth.callback_handler(code=code, state=state)
    
    if success:
        logger.info("OAuth callback successful")
        return redirect(url_for('index'))
    else:
        logger.error("OAuth callback failed")
        return redirect(url_for('index'))

if __name__ == "__main__":
    # Print SDK version info for debugging
    try:
        import kinde_sdk
        print(f"Using kinde_sdk from: {kinde_sdk.__file__}")
        if hasattr(kinde_sdk, '__version__'):
            print(f"kinde_sdk version: {kinde_sdk.__version__}")
    except Exception as e:
        print(f"Error importing kinde_sdk: {e}")
    
    # Print OAuth configuration for debugging
    print(f"OAuth configured with:")
    print(f"  Client ID: {os.getenv('KINDE_CLIENT_ID')}")
    print(f"  Host: {os.getenv('KINDE_HOST')}")
    print(f"  Redirect URI: {os.getenv('KINDE_REDIRECT_URI')}")
    
    app.run(debug=True, host="0.0.0.0", port=5001)