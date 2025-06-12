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
    _lock = threading.RLock()  # Add a lock for thread safety

    @classmethod
    def reset_instances(cls):
        """Reset all management token manager instances - useful for testing"""
        with cls._lock:
            cls._instances = {}

    def __new__(cls, domain, *args, **kwargs):
        """
        Ensure only one instance per domain and client_id combination.
        FIXED: Restore original signature to match the original design
        """
        with cls._lock:
            # Extract client_id from args or kwargs
            client_id = args[0] if args else kwargs.get('client_id', '')
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
        self.lock = threading.RLock()  # Add a lock for thread safety
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
        """Use client credentials to get a new access token."""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": f"https://{self.domain}/api"
        }
            
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        # CHANGE 3: Add timeout to prevent hanging on network issues
        try:
            response = requests.post(
                self.token_url, 
                data=data, 
                headers=headers,
                timeout=30  # 30-second timeout
            )
            response.raise_for_status()
            token_data = response.json()
            
            # This call now works because we use RLock
            self.set_tokens(token_data)
            return self.tokens["access_token"]
            
        except requests.exceptions.Timeout:
            raise Exception(f"Token request timed out after 30 seconds for domain {self.domain}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Token request failed for domain {self.domain}: {str(e)}")

    def clear_tokens(self):
        """ Clear stored tokens. """
        with self.lock:
            self.tokens = {}