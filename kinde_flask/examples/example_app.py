from flask import Flask, render_template_string
import os
from dotenv import load_dotenv

from kinde_sdk.auth.oauth import OAuth

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Kinde OAuth with Flask framework
kinde_oauth = OAuth(
    framework="flask",
    app=app
)

# Example home route
@app.route('/')
def home():
    """
    Home page that shows different content based on authentication status.
    """
    if kinde_oauth.is_authenticated():
        user = kinde_oauth.get_user_info()
        return render_template_string("""
            <html>
                <body>
                    <h1>Welcome, {{ user.email }}!</h1>
                    <p>You are logged in.</p>
                    <a href="/logout">Logout</a>
                </body>
            </html>
        """, user=user)
    return render_template_string("""
        <html>
            <body>
                <h1>Welcome to the Example App</h1>
                <p>You are not logged in.</p>
                <a href="/login">Login</a>
            </body>
        </html>
    """)

if __name__ == '__main__':
    app.run(debug=True) 