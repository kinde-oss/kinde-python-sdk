from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
from dotenv import load_dotenv

from kinde_fastapi import KindeFastAPI

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Kinde FastAPI Example")

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY", "your-secret-key"),  # Get from env or use default
    session_cookie="kinde_session",
    max_age=3600,  # 1 hour
)

# Initialize Kinde FastAPI integration
kinde = KindeFastAPI()

# Set up templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Helper function to get the current user
async def get_current_user(request: Request):
    if not kinde.is_authenticated(request):
        return None
    try:
        return kinde.get_user_info(request)
    except ValueError:
        return None

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user: dict = Depends(get_current_user)):
    """
    Home page that shows different content based on authentication status.
    """
    if user:
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

@app.get("/login")
async def login(request: Request):
    """
    Redirect to Kinde login page.
    """
    return RedirectResponse(url=kinde.get_login_url(request))

@app.get("/callback")
async def callback(request: Request, code: str):
    """
    Handle the OAuth callback from Kinde.
    """
    # In a real application, you would validate the state parameter
    # and handle any errors that might occur during authentication
    
    # Get user info from Kinde
    user_info = kinde.get_user_info(request)
    
    # Store user ID in session
    request.session["user_id"] = user_info.get("id")
    
    return RedirectResponse(url="/")

@app.get("/logout")
async def logout(request: Request):
    """
    Logout the user and redirect to Kinde logout page.
    """
    # Clear the session
    request.session.clear()
    
    # Redirect to Kinde logout
    return RedirectResponse(url=kinde.get_logout_url(request))

@app.get("/protected")
async def protected_route(request: Request, user: dict = Depends(get_current_user)):
    """
    Example of a protected route that requires authentication.
    """
    if not user:
        return RedirectResponse(url=kinde.get_login_url(request))
    
    return {
        "message": "This is a protected route",
        "user": user
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 