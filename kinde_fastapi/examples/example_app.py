from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from .session import InMemorySessionMiddleware
from pathlib import Path
import os
from dotenv import load_dotenv
import logging
from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth import claims, feature_flags, permissions

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
        return f"""
        <html>
            <body>
                <h1>Welcome, {user.get('email', 'User')}!</h1>
                <p>claims: {await claims.get_all_claims()}</p>
                <p>feature flags: {await feature_flags.get_all_flags()}</p>
                <p>permissions: {await permissions.get_permissions()}</p>
                <p>You are logged in.</p>
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000) 