"""
Token manager for the Kinde Management API.

This module provides token management for the Kinde Management API using client credentials flow.
"""

import time
import requests
import threading
from typing import Any, Dict, Optional

class ManagementTokenManager:
    """
    Token manager for the Kinde Management API.
    Uses client credentials grant type to obtain access tokens.
    """
    _instances = {}
    _lock = threading.Lock()  # Add a lock for thread safety

    @classmethod
    def reset_instances(cls):
        """Reset all management token manager instances - useful for testing"""
        with cls._lock:
            cls._instances = {}

    def __new__(cls, domain, client_id, client_secret):
        """
        Ensure only one instance per domain and client_id combination.
        """
        with cls._lock:
            instance_key = f"{domain}-{client_id}"
            if instance_key not in cls._instances:
                cls._instances[instance_key] = super(ManagementTokenManager, cls).__new__(cls)
            return cls._instances[instance_key]

    def __init__(self, domain, client_id, client_secret):
        # Skip initialization if already initialized
        if hasattr(self, "initialized") and self.initialized:
            return
            
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = f"https://{domain}/oauth2/token"
        self.tokens = {}  # Store tokens
        self.lock = threading.Lock()  # Add a lock for thread safety
        self.initialized = True

    def set_tokens(self, token_data: Dict[str, Any]):
        """ Store tokens with expiration. """
        with self.lock:
            # Handle None values by using default
            expires_in = token_data.get("expires_in") or 3600
            token_type = token_data.get("token_type") or "Bearer"
            self.tokens = {
            "access_token": token_data.get("access_token"),
            "expires_at": time.time() + expires_in,
            "token_type": token_type
            }

    def get_access_token(self):
        """ Get a valid access token. Request new if expired. """
        with self.lock:
            # Check if token exists and is not expired
            if self.tokens and "access_token" in self.tokens and time.time() < self.tokens.get("expires_at", 0) - 60:
                return self.tokens["access_token"]
                
            # Need to get a new token
            return self.request_new_token()

    def request_new_token(self):
        """ Use client credentials to get a new access token. """
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": f"https://{self.domain}/api"
        }
            
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
            
        response = requests.post(self.token_url, data=data, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        
        self.set_tokens(token_data)
        return self.tokens["access_token"]

    def clear_tokens(self):
        """ Clear stored tokens. """
        with self.lock:
            self.tokens = {}