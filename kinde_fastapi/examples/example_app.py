"""
SmartOAuth FastAPI Example Application

This example demonstrates how to use the new SmartOAuth client in a FastAPI application.
SmartOAuth automatically detects the execution context (sync vs async) and uses the
appropriate methods, providing a consistent API across different frameworks.

Key Features Demonstrated:
- Automatic context detection (async in FastAPI)
- Both sync and async method usage
- Warning system for suboptimal usage
- Integration with auth modules (sync and async)
- Factory function usage
- Real-world authentication flow

Usage:
1. Set up your environment variables (see .env.example)
2. Run: python -m uvicorn kinde_fastapi.examples.example_app:app --reload
3. Visit http://localhost:5000
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from .session import InMemorySessionMiddleware
from pathlib import Path
import os
from dotenv import load_dotenv
import logging
from kinde_sdk import SmartOAuth, create_oauth_client
from kinde_sdk.auth import claims, feature_flags, permissions, tokens, async_claims
from kinde_sdk.management import ManagementClient;
from kinde_sdk.management.management_token_manager import ManagementTokenManager
import requests

logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Kinde FastAPI Example")

# Add session middleware with proper configuration
app.add_middleware(
    InMemorySessionMiddleware,
    max_age=3600,  # 1 hour
    https_only=False
)

# Initialize Kinde SmartOAuth with FastAPI framework
# SmartOAuth automatically detects the async context and uses the appropriate methods
kinde_oauth = SmartOAuth(
    framework="fastapi",
    app=app
)

# Alternative: You can also use the factory function
# kinde_oauth = create_oauth_client(
#     async_mode=None,  # None means auto-detect (SmartOAuth)
#     framework="fastapi",
#     app=app
# )

# Example home route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page that shows different content based on authentication status.
    """
    if kinde_oauth.is_authenticated():
        # In FastAPI (async context), SmartOAuth will use async methods automatically
        # You can use either sync or async methods - SmartOAuth will handle the context
        
        # Option 1: Use async methods (recommended in async context)
        user_async = await kinde_oauth.get_user_info_async()
        
        # Use the async version for better performance
        user = user_async

        # Validate environment variables
        domain = os.getenv("KINDE_DOMAIN")
        client_id = os.getenv("KINDE_MANAGEMENT_CLIENT_ID")
        client_secret = os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET")
        
        if not all([domain, client_id, client_secret]):
            return """
            <html>
                <body>
                    <h1>Configuration Error</h1>
                    <p>Missing required environment variables for management client.</p>
                    <a href="/logout">Logout</a>
                </body>
            </html>
            """
        
        management_client = ManagementClient(
            domain=domain,
            client_id=client_id,
            client_secret=client_secret
        )
        try:
            api_response = management_client.get_users()
            user_count = len(api_response.users) if hasattr(api_response, 'users') else 0
        except Exception as e:
            logger.error(f"Failed to fetch users: {e}")
            user_count = 0

        # Demonstrate both sync and async auth module usage
        claims_sync = await claims.get_all_claims()
        claims_async = await async_claims.get_all_claims()
        feature_flags_data = await feature_flags.get_all_flags()
        permissions_data = await permissions.get_permissions()
        access_token = tokens.get_token_manager().get_access_token()

        return f"""
        <html>
            <body>
                <h1>Welcome, {user.get('email')}!</h1>
                <h2>SmartOAuth Demo - FastAPI (Async Context)</h2>
                <p><strong>User Info (async):</strong> {user.get('email')}</p>
                <p><strong>Claims (sync):</strong> {claims_sync}</p>
                <p><strong>Claims (async):</strong> {claims_async}</p>
                <p><strong>Feature Flags:</strong> {feature_flags_data}</p>
                <p><strong>Permissions:</strong> {permissions_data}</p>
                <p><strong>Access Token:</strong> {access_token[:20]}...</p>
                <p><strong>Management Users:</strong> {user_count} user(s) found</p>
                <p><em>Note: SmartOAuth automatically detected the async context and used async methods.</em></p>
                <p>You are logged in.</p>
                <hr>
                <h3>Demo Routes:</h3>
                <ul>
                    <li><a href="/demo_smart_oauth">SmartOAuth Demo (JSON)</a></li>
                    <li><a href="/demo_auth_modules">Auth Modules Demo (JSON)</a></li>
                    <li><a href="/call_management_users">Call Management Users</a></li>
                </ul>
                <hr>
                <a href="/logout">Logout</a>
            </body>
        </html>
        """
    return """
    <html>
        <body>
            <h1>Welcome to the SmartOAuth Example App</h1>
            <p>You are not logged in.</p>
            <p>This example demonstrates SmartOAuth in a FastAPI application.</p>
            <a href="/login">Login with SmartOAuth</a>
        </body>
            </html>
    """

@app.get("/login")
async def login():
    """
    Initiate login with SmartOAuth.
    """
    try:
        # SmartOAuth will automatically use async methods in FastAPI context
        login_url = await kinde_oauth.login()
        return {"login_url": login_url}
    except Exception as e:
        logger.error(f"Login error: {e}")
        return {"error": str(e)}

@app.get("/logout")
async def logout():
    """
    Logout using SmartOAuth.
    """
    try:
        # SmartOAuth will automatically use async methods in FastAPI context
        logout_url = await kinde_oauth.logout()
        return {"logout_url": logout_url}
    except Exception as e:
        logger.error(f"Logout error: {e}")
        return {"error": str(e)}

@app.get("/call_management_users")
async def call_management_users():
    if not kinde_oauth.is_authenticated():
        return {"error": "Not authenticated"}
    
    domain = os.getenv("KINDE_DOMAIN")
    client_id = os.getenv("KINDE_MANAGEMENT_CLIENT_ID")
    client_secret = os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET")
    
    if not all([domain, client_id, client_secret]):
        return {"error": "Missing management credentials"}
    
    try:
        token_manager = ManagementTokenManager(
            domain=domain,
            client_id=client_id,
            client_secret=client_secret
        )
        access_token = token_manager.get_access_token()
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get("http://localhost:8000/management/users", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to call management users: {e}")
        return {"error": str(e)}

@app.get("/demo_smart_oauth")
async def demo_smart_oauth():
    """
    Demonstrate SmartOAuth features in FastAPI context.
    """
    if not kinde_oauth.is_authenticated():
        return {"error": "Not authenticated"}
    
    # Demonstrate different SmartOAuth usage patterns
    results = {}
    
    # 1. Async methods (recommended in async context)
    try:
        user_async = await kinde_oauth.get_user_info_async()
        results["user_async"] = user_async.get('email')
    except Exception as e:
        results["user_async_error"] = str(e)
    
    # 2. Sync methods (will show warning but still work)
    try:
        user_sync = kinde_oauth.get_user_info()
        results["user_sync"] = user_sync.get('email')
    except Exception as e:
        results["user_sync_error"] = str(e)
    
    # 3. Auth URL generation (async)
    try:
        auth_url = await kinde_oauth.generate_auth_url()
        results["auth_url"] = auth_url
    except Exception as e:
        results["auth_url_error"] = str(e)
    
    # 4. Token retrieval
    try:
        tokens_data = kinde_oauth.get_tokens(kinde_oauth._framework.get_user_id())
        results["tokens"] = {
            "has_access_token": bool(tokens_data.get('access_token')),
            "has_refresh_token": bool(tokens_data.get('refresh_token'))
        }
    except Exception as e:
        results["tokens_error"] = str(e)
    
    # 5. Context detection
    results["context_info"] = {
        "is_async_context": kinde_oauth._is_async_context(),
        "framework": "fastapi",
        "authenticated": kinde_oauth.is_authenticated()
    }
    
    return {
        "message": "SmartOAuth Demo Results",
        "results": results,
        "note": "SmartOAuth automatically detected the async context and used appropriate methods."
    }

@app.get("/demo_auth_modules")
async def demo_auth_modules():
    """
    Demonstrate both sync and async auth modules.
    """
    if not kinde_oauth.is_authenticated():
        return {"error": "Not authenticated"}
    
    results = {}
    
    # Sync auth modules
    try:
        results["claims_sync"] = await claims.get_all_claims()
    except Exception as e:
        results["claims_sync_error"] = str(e)
    
    # Async auth modules
    try:
        results["claims_async"] = await async_claims.get_all_claims()
    except Exception as e:
        results["claims_async_error"] = str(e)
    
    try:
        results["feature_flags"] = await feature_flags.get_all_flags()
    except Exception as e:
        results["feature_flags_error"] = str(e)
    
    try:
        results["permissions"] = await permissions.get_permissions()
    except Exception as e:
        results["permissions_error"] = str(e)
    
    return {
        "message": "Auth Modules Demo",
        "results": results,
        "note": "Both sync and async auth modules work in FastAPI context."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000) 