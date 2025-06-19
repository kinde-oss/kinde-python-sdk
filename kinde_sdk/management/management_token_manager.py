"""
Token manager for the Kinde Management API.

This module provides token management for the Kinde Management API using client credentials flow.
"""

import time
import requests
import threading
from typing import Any, Dict, Optional
import importlib.metadata
import sys

class SDKTracker:
    """Handles SDK tracking header generation for Kinde Python SDK."""
    
    # SDK Package name for version detection
    SDK_PACKAGE_NAME = "kinde-python-sdk"
    
    # Framework detection mapping
    FRAMEWORK_DETECTION = {
        'django': 'Django',
        'flask': 'Flask', 
        'fastapi': 'FastAPI',
        'starlette': 'Starlette',
        'tornado': 'Tornado',
        'pyramid': 'Pyramid',
        'bottle': 'Bottle',
        'cherrypy': 'CherryPy',
        'falcon': 'Falcon',
        'sanic': 'Sanic',
        'quart': 'Quart',
        'aiohttp': 'aiohttp'
    }
    
    @classmethod
    def get_sdk_version(cls) -> str:
        """Get the installed SDK version."""
        try:
            return importlib.metadata.version(cls.SDK_PACKAGE_NAME)
        except importlib.metadata.PackageNotFoundError:
            # Fallback for development/testing
            return "2.0.0-dev"
    
    @classmethod
    def get_python_version(cls) -> str:
        """Get the Python version in format: major.minor.micro"""
        version_info = sys.version_info
        return f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    
    @classmethod
    def detect_framework(cls) -> Optional[str]:
        """
        Detect the web framework being used.
        
        Returns:
            str: Framework name if detected, None otherwise
        """
        for module_name, framework_name in cls.FRAMEWORK_DETECTION.items():
            try:
                importlib.import_module(module_name)
                return framework_name
            except ImportError:
                continue
        return None
    
    @classmethod
    def generate_tracking_header(cls, framework: Optional[str] = None) -> str:
        """
        Generate the Kinde-SDK tracking header value.
        
        Args:
            framework: Optional framework name to override auto-detection
            
        Returns:
            str: Header value in format: Python-[framework]/[SDK_VERSION]/[PYTHON_VERSION]/python
                 or Python/[SDK_VERSION] if no framework detected
        """
        sdk_version = cls.get_sdk_version()
        python_version = cls.get_python_version()
        
        # Use provided framework or auto-detect
        detected_framework = framework or cls.detect_framework()
        
        if detected_framework:
            # Format: Python-[framework]/[SDK_VERSION]/[PYTHON_VERSION]/python
            return f"Python-{detected_framework}/{sdk_version}/{python_version}/python"
        else:
            # Format: Python/[SDK_VERSION] (when no framework detected)
            return f"Python/{sdk_version}"
    
    @classmethod
    def get_tracking_headers(cls, framework: Optional[str] = None) -> Dict[str, str]:
        """
        Get the complete headers dict including tracking header.
        
        Args:
            framework: Optional framework name to override auto-detection
            
        Returns:
            dict: Headers dictionary with Kinde-SDK header
        """
        return {
            "Kinde-SDK": cls.generate_tracking_header(framework)
        }


class ManagementTokenManager:
    """
    Token manager for the Kinde Management API.
    Uses client credentials grant type to obtain access tokens.
    """
    _instances = {}
    _lock = threading.RLock()  # Add a lock for thread safety

    # SDK tracking configuration
    SDK_PACKAGE_NAME = "kinde-python-sdk"
    FRAMEWORK_DETECTION = {
        'django': 'Django',
        'flask': 'Flask', 
        'fastapi': 'FastAPI'
    }

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

    def _get_sdk_version(self) -> str:
        """Get the installed SDK version."""
        try:
            return importlib.metadata.version(self.SDK_PACKAGE_NAME)
        except importlib.metadata.PackageNotFoundError:
            # Fallback for development/testing
            return "2.0.0-dev"

    def _get_python_version(self) -> str:
        """Get the Python version in format: major.minor.micro"""
        version_info = sys.version_info
        return f"{version_info.major}.{version_info.minor}.{version_info.micro}"

    def _detect_framework(self) -> Optional[str]:
        """
        Detect the web framework being used.
        
        Returns:
            str: Framework name if detected, None otherwise
        """
        for module_name, framework_name in self.FRAMEWORK_DETECTION.items():
            try:
                importlib.import_module(module_name)
                return framework_name
            except ImportError:
                continue
        return None

    def _generate_tracking_header(self, framework: Optional[str] = None) -> str:
        """
        Generate the Kinde-SDK tracking header value.
        
        Format: [SDK Used]/[Version of SDK]/[Version of language]/python
        
        Args:
            framework: Optional framework name to override auto-detection
            
        Returns:
            str: Header value in 4-segment format as per client specification
        """
        sdk_version = self._get_sdk_version()
        python_version = self._get_python_version()
        
        # Use provided framework or auto-detect
        detected_framework = framework or self._detect_framework()
        
        if detected_framework:
            # Format: Python-[framework]/[SDK_VERSION]/[PYTHON_VERSION]/python
            return f"Python-{detected_framework}/{sdk_version}/{python_version}/python"
        else:
            # Format: Python/[SDK_VERSION]/[PYTHON_VERSION]/python (FIXED - now 4 segments)
            return f"Python/{sdk_version}/{python_version}/python"

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
        """Use client credentials to get a new access token with tracking headers."""
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": f"https://{self.domain}/api"
        }
            
        # Base headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        # Add SDK tracking header as per specification
        # This is required for analytics and support purposes
        # Format: [SDK Used]/[Version of SDK]/[Version of language]/python
        headers["Kinde-SDK"] = self._generate_tracking_header()
        
        # Add timeout to prevent hanging on network issues
        try:
            response = requests.post(
                self.token_url, 
                data=data, 
                headers=headers,  # Now includes tracking headers
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