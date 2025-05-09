from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pathlib import Path
import os
from dotenv import load_dotenv

from kinde_sdk.auth.oauth import OAuth

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Kinde FastAPI Example")

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
    if kinde_oauth.is_authenticated(request):
        user = kinde_oauth.get_user_info(request)
        return f"""
        <html>
            <body>
                <h1>Welcome, {user.get('email', 'User')}!</h1>
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
    uvicorn.run(app, host="localhost", port=5000) 