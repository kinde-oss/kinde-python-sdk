import time
import requests
import threading
from typing import Dict, Optional

class TokenManager:
    _instances = {}
    _lock = threading.Lock()  # Add a lock for thread safety

    def __new__(cls, user_id, *args, **kwargs):
        """
        Ensure only one instance per user.
        """
        with cls._lock:
            if user_id not in cls._instances:
                cls._instances[user_id] = super(TokenManager, cls).__new__(cls)
                cls._instances[user_id].__init__(user_id, *args, **kwargs)
            return cls._instances[user_id]

    def __init__(self, user_id, client_id, client_secret, token_url):
        if hasattr(self, "initialized"):  # Prevent re-initialization
            return
        self.user_id = user_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.tokens = {}  # Store tokens (access/refresh)
        self.lock = threading.Lock()  # Add a lock for thread safety
        self.initialized = True

    def set_tokens(self, access_token, refresh_token, expires_in):
        """ Store tokens with expiration. """
        with self.lock:
            self.tokens = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": time.time() + expires_in,
            }

    def exchange_code_for_token(self, code):
        """
        Exchange an authorization code for an access token.
        """
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        token_data = response.json()
        self.set_tokens(
            token_data["access_token"],
            token_data["refresh_token"],
            token_data.get("expires_in", 3600),
        )
        return self.tokens["access_token"]

    def get_access_token(self):
        """ Get a valid access token. Refresh if expired. """
        if self.tokens and time.time() < self.tokens["expires_at"]:
            return self.tokens["access_token"]
        elif self.tokens.get("refresh_token"):
            return self.refresh_access_token()
        else:
            raise ValueError("No valid tokens available")

    def refresh_access_token(self):
        """ Use the refresh token to get a new access token. """
        if "refresh_token" not in self.tokens:
            raise ValueError("No refresh token available")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.tokens["refresh_token"],
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        token_data = response.json()
        self.set_tokens(
            token_data["access_token"],
            token_data["refresh_token"],
            token_data.get("expires_in", 3600),
        )
        return self.tokens["access_token"]

    def revoke_token(self):
        """ Revoke the current access token. """
        if "access_token" not in self.tokens:
            raise ValueError("No access token to revoke")

        data = {
            "token": self.tokens["access_token"],
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post(f"{self.token_url}/revoke", data=data)
        response.raise_for_status()
        self.tokens = {}  # Clear stored tokens
