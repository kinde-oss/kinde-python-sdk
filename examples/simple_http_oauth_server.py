#!/usr/bin/env python3
"""
Simple HTTP OAuth Server for Local Testing

This is a minimal HTTP server that demonstrates the Kinde OAuth flow
without any framework dependencies. It's perfect for local testing
and development.

Features:
- Simple HTTP server using Python's built-in http.server
- OAuth login/logout flows
- Session management using KindeSessionManagement (clean API)
- No external dependencies beyond the Kinde SDK
- Easy to run and test locally
- Automatically loads .env file if present

Usage:
1. Create a .env file with your Kinde credentials (or set environment variables)
2. Run: python simple_http_oauth_server.py
3. Open http://localhost:5000 in your browser
4. Test the OAuth flow

Environment Variables (can be in .env file or environment):
- KINDE_CLIENT_ID: Your Kinde application client ID
- KINDE_CLIENT_SECRET: Your Kinde application client secret
- KINDE_REDIRECT_URI: http://localhost:5000/callback
- KINDE_HOST: Your Kinde domain (e.g., https://your-domain.kinde.com)
- KINDE_AUDIENCE: Your API audience (optional)

Note on OAuth Methods:
This example uses the proper login() and register() methods with KindeSessionManagement
for clean session management. The SDK now supports both:
- Framework-based usage (Flask, FastAPI) - automatic session management
- Standalone usage (serverless, Lambda) - manual session management with KindeSessionManagement
"""

import os
import json
import asyncio
import uuid
import urllib.parse
import logging
import html
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, Optional
from pathlib import Path

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded .env file from: {env_path}")
    else:
        # Also try loading from current directory
        current_env = Path('.env')
        if current_env.exists():
            load_dotenv(current_env)
            print(f"✅ Loaded .env file from: {current_env.absolute()}")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")

# Import the Kinde SDK
from kinde_sdk import AsyncOAuth, KindeSessionManagement
from kinde_sdk.core.exceptions import KindeConfigurationException

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleOAuthManager:
    """
    Simple OAuth manager for local testing.
    Uses KindeSessionManagement for clean session management.
    """
    
    def __init__(self):
        """Initialize the OAuth manager."""
        self.client_id = os.getenv("KINDE_CLIENT_ID")
        self.client_secret = os.getenv("KINDE_CLIENT_SECRET")
        self.redirect_uri = os.getenv("KINDE_REDIRECT_URI", "http://localhost:5000/callback")
        self.host = os.getenv("KINDE_HOST", "https://app.kinde.com")
        self.audience = os.getenv("KINDE_AUDIENCE")
        
        # Validate required configurations
        if not self.client_id:
            raise KindeConfigurationException("KINDE_CLIENT_ID is required")
        
        # Initialize OAuth client without framework (will use null framework)
        self.oauth = AsyncOAuth(
            framework=None,  # Will use null framework
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            host=self.host,
            audience=self.audience
        )
        
        # Initialize session management using the new KindeSessionManagement API
        # This provides a clean, user-friendly interface for session management
        self.session_mgmt = KindeSessionManagement()
        
        logger.info("Simple OAuth manager initialized successfully")
    
    def create_session(self) -> str:
        """Create a new session."""
        session_id = str(uuid.uuid4())
        return session_id
    
    async def generate_login_url(self, session_id: str) -> str:
        """Generate a login URL."""
        # Set the current user session using KindeSessionManagement
        self.session_mgmt.set_user_id(session_id)
        
        # Use the standard login() method - it will get user_id from the session management
        login_url = await self.oauth.login()
        
        return login_url
    
    async def generate_register_url(self, session_id: str) -> str:
        """Generate a registration URL."""
        # Set the current user session using KindeSessionManagement
        self.session_mgmt.set_user_id(session_id)
        
        # Use the standard register() method - it will get user_id from the session management
        register_url = await self.oauth.register()
        
        return register_url
    
    async def handle_callback(self, session_id: str, code: str, state: Optional[str] = None) -> Dict[str, Any]:
        """Handle OAuth callback."""
        # Set the current user session using KindeSessionManagement
        self.session_mgmt.set_user_id(session_id)
        
        # Handle the redirect using the standard method
        result = await self.oauth.handle_redirect(
            code=code,
            user_id=session_id,
            state=state
        )
        
        return result
    
    def is_authenticated(self, session_id: str) -> bool:
        """Check if session is authenticated."""
        # Set the current user session using KindeSessionManagement
        self.session_mgmt.set_user_id(session_id)
        
        # Use the standard is_authenticated method
        return self.oauth.is_authenticated()
    
    def get_user_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get user information."""
        if not self.is_authenticated(session_id):
            return None
        
        # Set the current user session using KindeSessionManagement
        self.session_mgmt.set_user_id(session_id)
        
        # Use the standard get_user_info method
        try:
            return self.oauth.get_user_info()
        except Exception:
            logger.exception("Failed to get user info")
            return None
    
    async def generate_logout_url(self, session_id: str) -> str:
        """Generate logout URL."""
        # Set the current user session using KindeSessionManagement
        self.session_mgmt.set_user_id(session_id)
        
        # Use the standard logout method
        logout_url = await self.oauth.logout(user_id=session_id)
        
        # Clear the session using KindeSessionManagement
        self.session_mgmt.clear_user_id()
        
        logger.info(f"Generated logout URL and cleared session {session_id}")
        return logout_url


# Global OAuth manager
oauth_manager = None

def get_oauth_manager() -> SimpleOAuthManager:
    """Get or create OAuth manager."""
    global oauth_manager
    if oauth_manager is None:
        oauth_manager = SimpleOAuthManager()
    return oauth_manager


class OAuthHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for OAuth operations."""
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            # Parse URL and query parameters
            parsed_url = urllib.parse.urlparse(self.path)
            path = parsed_url.path
            query_params = urllib.parse.parse_qs(parsed_url.query)
            
            # Flatten query parameters (parse_qs returns lists)
            params = {k: v[0] if v else None for k, v in query_params.items()}

            # Mask sensitive values
            masked_params = dict(params)
            for k in ("code", "state"):
                if masked_params.get(k):
                    masked_params[k] = "[redacted]"

            logger.info("GET %s - Params: %s", path, masked_params)
            
            if path == '/':
                self._handle_home()
            elif path == '/login':
                self._handle_login(params)
            elif path == '/register':
                self._handle_register(params)
            elif path == '/callback':
                self._handle_callback(params)
            elif path == '/user':
                self._handle_user(params)
            elif path == '/logout':
                self._handle_logout(params)
            else:
                self._handle_not_found()
                
        except Exception:
            logger.exception("Error handling request")
            self._send_error_response(500, "Internal server error")
    
    def _handle_home(self):
        """Handle home page."""
        page_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Kinde OAuth Test Server</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                .button { display: inline-block; padding: 10px 20px; margin: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
                .button:hover { background: #0056b3; }
                .info { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }
                .error { background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <h1>🚀 Kinde OAuth Test Server</h1>
            <p>This is a simple HTTP server for testing Kinde OAuth flows locally.</p>
            
            <div class="info">
                <h3>Available Endpoints:</h3>
                <ul>
                    <li><a href="/login" class="button">Login</a> - Start OAuth login flow</li>
                    <li><a href="/register" class="button">Register</a> - Start OAuth registration flow</li>
                    <li><a href="/user" class="button">User Info</a> - View user information (requires login)</li>
                    <li><a href="/logout" class="button">Logout</a> - Logout and clear session</li>
                </ul>
            </div>
            
            <div class="info">
                <h3>Environment Variables Required:</h3>
                <ul>
                    <li><code>KINDE_CLIENT_ID</code> - Your Kinde application client ID</li>
                    <li><code>KINDE_CLIENT_SECRET</code> - Your Kinde application client secret</li>
                    <li><code>KINDE_REDIRECT_URI</code> - http://localhost:5000/callback</li>
                    <li><code>KINDE_HOST</code> - Your Kinde domain</li>
                </ul>
            </div>
        </body>
        </html>
        """
        self._send_html_response(page_html)
    
    def _handle_login(self, _params):
        """Handle login request."""
        try:
            oauth = get_oauth_manager()
            session_id = oauth.create_session()
            login_url = asyncio.run(oauth.generate_login_url(session_id))
            
            # Set session cookie and redirect
            self.send_response(302)
            self.send_header('Location', login_url)
            self.send_header('Set-Cookie', f'session_id={session_id}; HttpOnly; Path=/; SameSite=Lax')
            self.end_headers()
            
        except Exception:
            logger.exception("Login failed")
            self._send_error_response(500, "Login failed")
    
    def _handle_register(self, _params):
        """Handle registration request."""
        try:
            oauth = get_oauth_manager()
            session_id = oauth.create_session()
            register_url = asyncio.run(oauth.generate_register_url(session_id))
            
            # Set session cookie and redirect
            self.send_response(302)
            self.send_header('Location', register_url)
            self.send_header('Set-Cookie', f'session_id={session_id}; HttpOnly; Path=/; SameSite=Lax')
            self.end_headers()
            
        except Exception:
            logger.exception("Registration failed")
            self._send_error_response(500, "Registration failed")
    
    def _handle_callback(self, params):
        """Handle OAuth callback."""
        try:
            code = params.get('code')
            state = params.get('state')
            
            if not code:
                self._send_error_response(400, "Missing authorization code")
                return
            
            # Get session ID from cookie
            session_id = self._get_session_id_from_cookie()
            if not session_id:
                self._send_error_response(400, "No session found")
                return
            
            oauth = get_oauth_manager()
            result = asyncio.run(oauth.handle_callback(session_id, code, state))
            
            # Show success page
            user_info = result['user']
            safe_user_info_json = html.escape(json.dumps(user_info, indent=2))
            page_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Authentication Successful</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                    .success {{ background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .user-info {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .button {{ display: inline-block; padding: 10px 20px; margin: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <h1>✅ Authentication Successful!</h1>
                <div class="success">
                    <p>You have successfully authenticated with Kinde.</p>
                </div>
                
                <div class="user-info">
                    <h3>User Information:</h3>
                    <pre>{safe_user_info_json}</pre>
                </div>
                
                <p>
                    <a href="/user" class="button">View User Info</a>
                    <a href="/logout" class="button">Logout</a>
                    <a href="/" class="button">Home</a>
                </p>
            </body>
            </html>
            """
            self._send_html_response(page_html)
            
        except Exception:
            logger.exception("Authentication failed")
            self._send_error_response(400, "Authentication failed")
    
    def _handle_user(self, _params):
        """Handle user info request."""
        try:
            session_id = self._get_session_id_from_cookie()
            if not session_id:
                self._send_error_response(401, "No session found")
                return
            
            oauth = get_oauth_manager()
            if not oauth.is_authenticated(session_id):
                self._send_error_response(401, "Not authenticated")
                return
            
            user_info = oauth.get_user_info(session_id)
            if not user_info:
                self._send_error_response(404, "User info not found")
                return

            safe_user_info_json = html.escape(json.dumps(user_info, indent=2))
            page_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>User Information</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                    .user-info {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                    .button {{ display: inline-block; padding: 10px 20px; margin: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <h1>👤 User Information</h1>
                
                <div class="user-info">
                    <pre>{safe_user_info_json}</pre>
                </div>
                
                <p>
                    <a href="/logout" class="button">Logout</a>
                    <a href="/" class="button">Home</a>
                </p>
            </body>
            </html>
            """
            self._send_html_response(page_html)
            
        except Exception:
            logger.exception("Failed to get user info")
            self._send_error_response(500, "Failed to get user info")
    
    def _handle_logout(self, _params):
        """Handle logout request."""
        try:
            session_id = self._get_session_id_from_cookie()
            if not session_id:
                self._send_error_response(400, "No session found")
                return
            
            oauth = get_oauth_manager()
            logout_url = asyncio.run(oauth.generate_logout_url(session_id))
            
            # Clear session cookie and redirect
            self.send_response(302)
            self.send_header('Location', logout_url)
            self.send_header('Set-Cookie', 'session_id=; HttpOnly; Path=/; Max-Age=0; SameSite=Lax')
            self.end_headers()
            
        except Exception:
            logger.exception("Logout failed")
            self._send_error_response(500, "Logout failed")
    
    def _handle_not_found(self):
        """Handle 404 errors."""
        self._send_error_response(404, "Page not found")
    
    def _get_session_id_from_cookie(self) -> Optional[str]:
        """Extract session ID from cookie."""
        cookie_header = self.headers.get('Cookie', '')
        if not cookie_header:
            return None
        try:
            import http.cookies as cookies
            jar = cookies.SimpleCookie()
            jar.load(cookie_header)
            if 'session_id' in jar:
                return jar['session_id'].value
        except Exception:
            logger.debug("Failed to parse Cookie header", exc_info=True)
        return None
    
    def _send_html_response(self, html: str, status_code: int = 200):
        """Send HTML response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def _send_error_response(self, status_code: int, message: str):
        """Send error response."""
        escaped_message = html.escape(message)
        page_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error {status_code}</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                .error {{ background: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 10px 20px; margin: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>❌ Error {status_code}</h1>
            <div class="error">
                <p>{escaped_message}</p>
            </div>
            <p><a href="/" class="button">Home</a></p>
        </body>
        </html>
        """
        self._send_html_response(page_html, status_code)
    
    def log_message(self, format, *args):
        """Override to use our logger."""
        logger.info(f"{self.address_string()} - {format % args}")


def main():
    """Main function to start the server."""
    print("🚀 Starting Kinde OAuth Test Server")
    print("="*50)
    
    # Check environment variables
    required_vars = ["KINDE_CLIENT_ID"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("\nYou can set these in two ways:")
        print("\n1. Create a .env file in the project root with:")
        print("   KINDE_CLIENT_ID=your_client_id")
        print("   KINDE_CLIENT_SECRET=your_client_secret")
        print("   KINDE_REDIRECT_URI=http://localhost:5000/callback")
        print("   KINDE_HOST=https://your-domain.kinde.com")
        print("   KINDE_AUDIENCE=your_api_audience  # Optional")
        print("\n2. Or set environment variables:")
        print("   export KINDE_CLIENT_ID=your_client_id")
        print("   export KINDE_CLIENT_SECRET=your_client_secret")
        print("   export KINDE_REDIRECT_URI=http://localhost:5000/callback")
        print("   export KINDE_HOST=https://your-domain.kinde.com")
        print("   export KINDE_AUDIENCE=your_api_audience  # Optional")
        print("\nThen run: python simple_http_oauth_server.py")
        return
    
    try:
        # Test OAuth manager initialization
        get_oauth_manager()
        print("✅ OAuth manager initialized successfully")
        
        # Start HTTP server
        server_address = ('localhost', 5000)
        httpd = HTTPServer(server_address, OAuthHTTPRequestHandler)
        
        print("🌐 Server running at http://localhost:5000")
        print("📋 Available endpoints:")
        print("   GET / - Home page with instructions")
        print("   GET /login - Start OAuth login flow")
        print("   GET /register - Start OAuth registration flow")
        print("   GET /callback - OAuth callback (handled automatically)")
        print("   GET /user - View user information")
        print("   GET /logout - Logout and clear session")
        print("\n🔧 Environment variables:")
        print(f"   KINDE_CLIENT_ID: {os.getenv('KINDE_CLIENT_ID', 'Not set')}")
        print(f"   KINDE_REDIRECT_URI: {os.getenv('KINDE_REDIRECT_URI', 'http://localhost:5000/callback')}")
        print(f"   KINDE_HOST: {os.getenv('KINDE_HOST', 'https://app.kinde.com')}")
        print(f"   KINDE_AUDIENCE: {os.getenv('KINDE_AUDIENCE', 'Not set')}")
        print("\n⏹️  Press Ctrl+C to stop the server")
        
        # Start the server
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception:
        logger.exception("Server error")
        print("❌ Server error")


if __name__ == "__main__":
    main()
