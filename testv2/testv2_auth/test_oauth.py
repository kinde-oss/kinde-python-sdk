import unittest
import asyncio
import pytest
import time
import os
from unittest.mock import patch, MagicMock, AsyncMock
from urllib.parse import urlparse, parse_qs
import requests

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.enums import IssuerRouteTypes, PromptTypes
from kinde_sdk.auth.login_options import LoginOptions
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.core.exceptions import (
    KindeConfigurationException,
    KindeLoginException,
    KindeTokenException,
    KindeRetrieveException,
)

# Helper function to run async tests in unittest
def run_async(coro):
    try:
        # Use the running event loop if available
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # Create a new event loop if none exists
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

class TestOAuthExtended(unittest.TestCase):
    def setUp(self):
        """Set up for each test"""
        # Set up OAuth with minimal required parameters
        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback",
            framework="flask",  # Use a specific framework
            host="https://example.com",
            audience="test_audience"  # Adding audience parameter to test line 94
        )
        
        # Override URLs for testing
        self.oauth.auth_url = "https://example.com/oauth2/auth"
        self.oauth.token_url = "https://example.com/oauth2/token"
        self.oauth.logout_url = "https://example.com/logout"
        self.oauth.userinfo_url = "https://example.com/oauth2/userinfo"
        
        # Setup mocks
        self.setup_mocks()
        
    def tearDown(self):
        """Clean up after each test"""
        # Reset any mocks
        if hasattr(self, 'mock_storage'):
            self.mock_storage.reset_mock()
        if hasattr(self, 'mock_token_manager'):
            self.mock_token_manager.reset_mock()
        if hasattr(self, 'mock_framework'):
            self.mock_framework.reset_mock()
            
        # Reset the OAuth singleton instance
        if hasattr(self, 'oauth'):
            self.oauth = None
            
        # Reset any environment variables that might have been set
        for key in ['KINDE_CLIENT_ID', 'KINDE_CLIENT_SECRET', 'KINDE_REDIRECT_URI', 'KINDE_HOST', 'KINDE_AUDIENCE']:
            if key in os.environ:
                del os.environ[key]
        
    def setup_mocks(self):
        """Set up mocks for the tests"""
        # Mock storage manager
        self.mock_storage = MagicMock()
        
        # Set up storage get to return values
        def mock_get_side_effect(key):
            if key == "state":
                mock = MagicMock()
                mock.get = lambda k: "test_state" if k == "value" else None
                return mock
            elif key == "code_verifier":
                mock = MagicMock()
                mock.get = lambda k: "test_verifier" if k == "value" else None
                return mock
            elif key == "nonce":
                mock = MagicMock()
                mock.get = lambda k: "test_nonce" if k == "value" else None
                return mock
            return None
        
        self.mock_storage.get = MagicMock(side_effect=mock_get_side_effect)
        
        # Mock session manager
        self.mock_session_manager = MagicMock(spec=UserSession)
        self.mock_session_manager.storage_manager = self.mock_storage
        self.oauth._session_manager = self.mock_session_manager
        
        # Mock token manager
        self.mock_token_manager = MagicMock()
        self.mock_token_manager.tokens = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_at": time.time() + 3600
        }
        self.mock_token_manager.get_access_token = MagicMock(return_value="test_access_token")
        self.mock_token_manager.get_id_token = MagicMock(return_value="test_id_token")
        self.mock_token_manager.get_claims = MagicMock(return_value={"sub": "user123", "email": "test@example.com"})
        
        # Make session manager return token manager
        self.mock_session_manager.get_token_manager = MagicMock(return_value=self.mock_token_manager)
        
        # Mock framework
        self.mock_framework = MagicMock()
        self.mock_framework.get_name.return_value = "flask"
        self.mock_framework.get_description.return_value = "Flask framework implementation"
        self.mock_framework.start = MagicMock()
        self.mock_framework.stop = MagicMock()
        self.mock_framework.get_app = MagicMock(return_value=None)
        self.mock_framework.get_request = MagicMock(return_value=None)
        self.mock_framework.get_user_id = MagicMock(return_value="test_user_id")
        self.mock_framework.set_oauth = MagicMock()
        self.mock_framework.can_auto_detect = MagicMock(return_value=True)
        
        # Set the framework in OAuth
        self.oauth._framework = self.mock_framework


if __name__ == "__main__":
    unittest.main()