import unittest
import asyncio
import pytest
import time
import os
import inspect
from unittest.mock import patch, MagicMock, AsyncMock, Mock
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


    # -- Invitation code tests --

    def test_generate_auth_url_with_invitation_code(self):
        """invitation_code is included as a query parameter in the auth URL."""
        result = run_async(self.oauth.generate_auth_url(
            login_options={LoginOptions.INVITATION_CODE: "abc123"}
        ))
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["invitation_code"], ["abc123"])

    def test_generate_auth_url_invitation_code_auto_sets_is_invitation(self):
        """is_invitation is automatically set to 'true' when invitation_code is present."""
        result = run_async(self.oauth.generate_auth_url(
            login_options={LoginOptions.INVITATION_CODE: "abc123"}
        ))
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["is_invitation"], ["true"])

    def test_generate_auth_url_invitation_code_with_explicit_is_invitation(self):
        """Explicit is_invitation=True is honoured alongside invitation_code."""
        result = run_async(self.oauth.generate_auth_url(
            login_options={
                LoginOptions.INVITATION_CODE: "abc123",
                LoginOptions.IS_INVITATION: True,
            }
        ))
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["invitation_code"], ["abc123"])
        self.assertEqual(params["is_invitation"], ["true"])

    def test_generate_auth_url_invitation_code_overrides_false_is_invitation(self):
        """invitation_code forces is_invitation='true' even when explicitly set to False."""
        result = run_async(self.oauth.generate_auth_url(
            login_options={
                LoginOptions.INVITATION_CODE: "abc123",
                LoginOptions.IS_INVITATION: False,
            }
        ))
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["is_invitation"], ["true"])

    def test_generate_auth_url_is_invitation_alone(self):
        """is_invitation=True works independently of invitation_code."""
        result = run_async(self.oauth.generate_auth_url(
            login_options={LoginOptions.IS_INVITATION: True}
        ))
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["is_invitation"], ["true"])
        self.assertNotIn("invitation_code", params)

    def test_generate_auth_url_no_invitation_params_by_default(self):
        """Neither invitation_code nor is_invitation appear when not specified."""
        result = run_async(self.oauth.generate_auth_url(login_options={}))
        params = parse_qs(urlparse(result["url"]).query)
        self.assertNotIn("invitation_code", params)
        self.assertNotIn("is_invitation", params)

    def test_generate_auth_url_empty_invitation_code_ignored(self):
        """An empty invitation_code does not add is_invitation."""
        result = run_async(self.oauth.generate_auth_url(
            login_options={LoginOptions.INVITATION_CODE: ""}
        ))
        params = parse_qs(urlparse(result["url"]).query)
        self.assertNotIn("is_invitation", params)

    def test_generate_auth_url_none_invitation_code_ignored(self):
        """invitation_code=None is ignored entirely."""
        result = run_async(self.oauth.generate_auth_url(
            login_options={LoginOptions.INVITATION_CODE: None}
        ))
        params = parse_qs(urlparse(result["url"]).query)
        self.assertNotIn("invitation_code", params)
        self.assertNotIn("is_invitation", params)

    def test_login_passes_invitation_code(self):
        """login() forwards invitation_code to the generated auth URL."""
        url = run_async(self.oauth.login(
            login_options={LoginOptions.INVITATION_CODE: "inv_xyz"}
        ))
        params = parse_qs(urlparse(url).query)
        self.assertEqual(params["invitation_code"], ["inv_xyz"])
        self.assertEqual(params["is_invitation"], ["true"])

    def test_login_without_invitation_code(self):
        """login() without invitation options produces no invitation params."""
        url = run_async(self.oauth.login())
        params = parse_qs(urlparse(url).query)
        self.assertNotIn("invitation_code", params)
        self.assertNotIn("is_invitation", params)

    def test_invitation_code_coexists_with_org_code(self):
        """invitation_code and org_code can be used together."""
        result = run_async(self.oauth.generate_auth_url(
            login_options={
                LoginOptions.INVITATION_CODE: "abc123",
                LoginOptions.ORG_CODE: "org_456",
            }
        ))
        params = parse_qs(urlparse(result["url"]).query)
        self.assertEqual(params["invitation_code"], ["abc123"])
        self.assertEqual(params["is_invitation"], ["true"])
        self.assertEqual(params["org_code"], ["org_456"])


class TestOAuthMethodSignatures(unittest.TestCase):
    """Test OAuth method signatures to verify the fix for incorrect request parameter passing."""

    @patch.dict('os.environ', {
        'KINDE_CLIENT_ID': 'test_client_id',
        'KINDE_CLIENT_SECRET': 'test_client_secret',
        'KINDE_REDIRECT_URI': 'http://localhost:8000/callback',
        'KINDE_HOST': 'https://test.kinde.com'
    })
    @patch('kinde_sdk.auth.oauth.requests.get')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    def test_is_authenticated_signature_has_no_parameters(self, mock_framework_factory, mock_storage_factory, mock_get):
        """
        Test that is_authenticated() accepts no parameters beyond self.
        
        This verifies the fix for the bug where FastAPI/Flask were passing 
        a request parameter that is_authenticated() doesn't accept.
        """
        # Mock OpenID configuration to prevent real network calls
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            'authorization_endpoint': 'https://test.kinde.com/oauth2/auth',
            'token_endpoint': 'https://test.kinde.com/oauth2/token',
            'end_session_endpoint': 'https://test.kinde.com/logout',
            'userinfo_endpoint': 'https://test.kinde.com/oauth2/userinfo'
        })
        mock_get.return_value = mock_response
        
        # Configure factory mocks to prevent blocking during OAuth initialization
        mock_storage_factory.create_storage.return_value = MagicMock()
        mock_framework_factory.create_framework.return_value = None
        
        oauth = OAuth(framework=None)
        sig = inspect.signature(oauth.is_authenticated)
        params = list(sig.parameters.keys())
        
        # Should have no parameters (self is implicit)
        self.assertEqual(len(params), 0,
                        f"is_authenticated() should accept no parameters, found: {params}")

    @patch.dict('os.environ', {
        'KINDE_CLIENT_ID': 'test_client_id',
        'KINDE_CLIENT_SECRET': 'test_client_secret',
        'KINDE_REDIRECT_URI': 'http://localhost:8000/callback',
        'KINDE_HOST': 'https://test.kinde.com'
    })
    @patch('kinde_sdk.auth.oauth.requests.get')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    def test_get_user_info_signature_has_no_parameters(self, mock_framework_factory, mock_storage_factory, mock_get):
        """
        Test that get_user_info() accepts no parameters beyond self.
        
        This verifies the fix for the bug where FastAPI/Flask were passing 
        a request parameter that get_user_info() doesn't accept.
        """
        # Mock OpenID configuration to prevent real network calls
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            'authorization_endpoint': 'https://test.kinde.com/oauth2/auth',
            'token_endpoint': 'https://test.kinde.com/oauth2/token',
            'end_session_endpoint': 'https://test.kinde.com/logout',
            'userinfo_endpoint': 'https://test.kinde.com/oauth2/userinfo'
        })
        mock_get.return_value = mock_response
        
        # Configure factory mocks to prevent blocking during OAuth initialization
        mock_storage_factory.create_storage.return_value = MagicMock()
        mock_framework_factory.create_framework.return_value = None
        
        oauth = OAuth(framework=None)
        sig = inspect.signature(oauth.get_user_info)
        params = list(sig.parameters.keys())
        
        # Should have no parameters (self is implicit)
        self.assertEqual(len(params), 0,
                        f"get_user_info() should accept no parameters, found: {params}")

    @patch.dict('os.environ', {
        'KINDE_CLIENT_ID': 'test_client_id',
        'KINDE_CLIENT_SECRET': 'test_client_secret',
        'KINDE_REDIRECT_URI': 'http://localhost:8000/callback',
        'KINDE_HOST': 'https://test.kinde.com'
    })
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.requests.get')
    def test_is_authenticated_rejects_extra_parameters(self, mock_get, mock_framework_factory, mock_storage_factory):
        """
        Test that passing extra parameters to is_authenticated() raises TypeError.
        
        This ensures if someone accidentally adds request parameter back,
        the test will catch it and prevent regression.
        """
        # Mock OpenID configuration
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            'authorization_endpoint': 'https://test.kinde.com/oauth2/auth',
            'token_endpoint': 'https://test.kinde.com/oauth2/token',
            'end_session_endpoint': 'https://test.kinde.com/logout',
            'userinfo_endpoint': 'https://test.kinde.com/oauth2/userinfo'
        })
        mock_get.return_value = mock_response
        
        # Configure factory mocks to prevent blocking during OAuth initialization
        mock_storage_factory.create_storage.return_value = MagicMock()
        mock_framework_factory.create_framework.return_value = None
        
        oauth = OAuth(framework=None)
        
        # Passing a parameter should raise TypeError
        with self.assertRaises(TypeError) as context:
            oauth.is_authenticated("unexpected_parameter")
        
        # Verify error message mentions positional arguments
        self.assertIn("positional argument", str(context.exception).lower())

    @patch.dict('os.environ', {
        'KINDE_CLIENT_ID': 'test_client_id',
        'KINDE_CLIENT_SECRET': 'test_client_secret',
        'KINDE_REDIRECT_URI': 'http://localhost:8000/callback',
        'KINDE_HOST': 'https://test.kinde.com'
    })
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.requests.get')
    def test_get_user_info_rejects_extra_parameters(self, mock_get, mock_framework_factory, mock_storage_factory):
        """
        Test that passing extra parameters to get_user_info() raises TypeError.
        
        This ensures if someone accidentally adds request parameter back,
        the test will catch it and prevent regression.
        """
        # Mock OpenID configuration
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            'authorization_endpoint': 'https://test.kinde.com/oauth2/auth',
            'token_endpoint': 'https://test.kinde.com/oauth2/token',
            'end_session_endpoint': 'https://test.kinde.com/logout',
            'userinfo_endpoint': 'https://test.kinde.com/oauth2/userinfo'
        })
        mock_get.return_value = mock_response
        
        # Configure factory mocks to prevent blocking during OAuth initialization
        mock_storage_factory.create_storage.return_value = MagicMock()
        mock_framework_factory.create_framework.return_value = None
        
        oauth = OAuth(framework=None)
        
        # Passing a parameter should raise TypeError
        with self.assertRaises(TypeError) as context:
            oauth.get_user_info("unexpected_parameter")
        
        # Verify error message mentions positional arguments
        self.assertIn("positional argument", str(context.exception).lower())


if __name__ == "__main__":
    unittest.main()