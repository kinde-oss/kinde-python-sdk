from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from .session import InMemorySessionMiddleware
from pathlib import Path
import os
from dotenv import load_dotenv
import logging
from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth import claims, feature_flags, permissions, tokens
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

# Initialize Kinde OAuth with FastAPI framework
kinde_oauth = OAuth(
    framework="fastapi",
    app=app
)

# Example home route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Home page that shows different content based on authentication status.
    """
    if kinde_oauth.is_authenticated():
        user = kinde_oauth.get_user_info()

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

        return f"""
        <html>
            <body>
                <h1>Welcome, {user.get('email')}!</h1>
                <p>claims: {await claims.get_all_claims()}</p>
                <p>feature flags: {await feature_flags.get_all_flags()}</p>
                <p>permissions: {await permissions.get_permissions()}</p>
                <p>tokens: {tokens.get_token_manager().get_access_token()}</p>
                <p>users: {user_count} user(s) found</p>
                <p>You are logged in.</p>
                <a href="/call_management_users">Call Management Users</a>
                <a href="/logout">Logout</a>
            </body>
        </html>
        """
    return """
    <html>
        <body>
            <h1>Welcome to the Example App</h1>
            <p>You are not logged in.</p>
            <a href="/login">Login</a>
        </body>
    </html>
    """

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000) 