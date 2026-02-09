"""
Kinde FastAPI Example Application

This example demonstrates how to use the Kinde OAuth client in a FastAPI application.
The OAuth class automatically registers authentication routes and handles the OAuth flow.

Key Features Demonstrated:
- Simple OAuth setup with FastAPI
- Automatic route registration (/login, /logout, /callback, /register, /user)
- Authentication status checking
- User information retrieval

Usage:
1. Set up your environment variables in a .env file:
   - KINDE_CLIENT_ID=your_client_id
   - KINDE_CLIENT_SECRET=your_client_secret
   - KINDE_REDIRECT_URI=http://localhost:8000/callback
   - KINDE_HOST=https://your-domain.kinde.com
   
2. Run from the SDK root directory:
   python -m uvicorn kinde_fastapi.examples.example_app:app --reload --port 8000
   
3. Visit http://localhost:8000

Available Routes (automatically registered):
- /login - Redirects to Kinde login
- /logout - Logs out the user
- /callback - Handles OAuth callback
- /register - Redirects to Kinde registration
- /user - Returns user information (redirects to login if not authenticated)
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from .session import InMemorySessionMiddleware
import os
from dotenv import load_dotenv
import logging
from kinde_sdk.auth.oauth import OAuth

logger = logging.getLogger(__name__)

# Load environment variables from .env file located alongside this script
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Initialize FastAPI app
app = FastAPI(title="Kinde FastAPI Example")

# Add session middleware with proper configuration
# This is required for storing session data between requests
app.add_middleware(
    InMemorySessionMiddleware,
    max_age=3600,  # 1 hour
    https_only=False
)

# Initialize Kinde OAuth with FastAPI framework
# This automatically registers /login, /logout, /callback, /register, /user routes
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
        try:
            user = kinde_oauth.get_user_info()
            return f"""
            <html>
                <body>
                    <h1>Welcome, {user.get('email', 'User')}!</h1>
                    <p>You are logged in.</p>
                    <h3>User Information:</h3>
                    <ul>
                        <li><strong>Email:</strong> {user.get('email', 'N/A')}</li>
                        <li><strong>Name:</strong> {user.get('given_name', '')} {user.get('family_name', '')}</li>
                        <li><strong>ID:</strong> {user.get('sub', 'N/A')}</li>
                    </ul>
                    <hr>
                    <p><a href="/user">View Full User Info (JSON)</a></p>
                    <p><a href="/logout">Logout</a></p>
                </body>
            </html>
            """
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return f"""
            <html>
                <body>
                    <h1>Error</h1>
                    <p>Failed to get user information: {str(e)}</p>
                    <a href="/logout">Logout</a>
                </body>
            </html>
            """
    
    return """
    <html>
        <body>
            <h1>Welcome to the Kinde FastAPI Example</h1>
            <p>You are not logged in.</p>
            <p>This example demonstrates Kinde OAuth integration with FastAPI.</p>
            <p><a href="/login">Login</a> | <a href="/register">Register</a></p>
        </body>
    </html>
    """


@app.get("/protected")
async def protected_route():
    """
    Example of a protected route that requires authentication.
    """
    if not kinde_oauth.is_authenticated():
        return {"error": "Not authenticated", "redirect": "/login"}
    
    user = kinde_oauth.get_user_info()
    return {
        "message": "This is a protected route",
        "user": user.get('email')
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
