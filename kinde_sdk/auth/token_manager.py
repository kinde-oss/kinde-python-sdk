import time
import requests

class TokenManager:
    def __init__(self, client_id, client_secret, token_url):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.tokens = {}  # Store tokens (access/refresh)

    def set_tokens(self, access_token, refresh_token, expires_in):
        """
        Store tokens and expiration time.
        """
        self.tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": time.time() + expires_in,
        }

    def get_access_token(self):
        """
        Get a valid access token. Refresh if expired.
        """
        if self.tokens and time.time() < self.tokens["expires_at"]:
            return self.tokens["access_token"]
        elif self.tokens.get("refresh_token"):
            return self.refresh_access_token()
        else:
            raise ValueError("No valid tokens available")

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

    def refresh_access_token(self):
        """
        Use the refresh token to get a new access token.
        """
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
        """
        Revoke the current access token.
        """
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
