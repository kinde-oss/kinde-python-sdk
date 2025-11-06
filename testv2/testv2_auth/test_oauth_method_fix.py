"""
Tests to verify the OAuth method signature fix.

This test file verifies that OAuth.is_authenticated() and OAuth.get_user_info()
methods do not accept a request parameter, fixing the bug where framework
implementations were passing a parameter these methods don't accept.

The fix ensures:
1. OAuth.is_authenticated() accepts no parameters beyond self
2. OAuth.get_user_info() accepts no parameters beyond self
3. These methods can be called without parameters
4. Passing extra parameters raises TypeError
"""
import unittest
from unittest.mock import Mock, patch
import inspect
from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.core.exceptions import KindeConfigurationException


class TestOAuthMethodSignatures(unittest.TestCase):
    """Test OAuth method signatures match what framework code expects."""

    def setUp(self):
        """Set up test fixtures."""
        self.env_patcher = patch.dict('os.environ', {
            'KINDE_CLIENT_ID': 'test_client_id',
            'KINDE_CLIENT_SECRET': 'test_client_secret',
            'KINDE_REDIRECT_URI': 'http://localhost:8000/callback',
            'KINDE_HOST': 'https://test.kinde.com'
        })
        self.env_patcher.start()

    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()

    @patch('kinde_sdk.auth.oauth.requests.get')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    def test_is_authenticated_signature_has_no_parameters(self, mock_framework_factory, mock_storage_factory, mock_get):
        """
        Test that is_authenticated() accepts no parameters beyond self.
        
        This prevents the bug where FastAPI/Flask were passing request parameter.
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
        
        oauth = OAuth(framework=None)
        sig = inspect.signature(oauth.is_authenticated)
        params = list(sig.parameters.keys())
        
        # Should have no parameters (self is implicit)
        self.assertEqual(len(params), 0,
                        f"is_authenticated() should accept no parameters, found: {params}")

    @patch('kinde_sdk.auth.oauth.requests.get')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    def test_get_user_info_signature_has_no_parameters(self, mock_framework_factory, mock_storage_factory, mock_get):
        """
        Test that get_user_info() accepts no parameters beyond self.
        
        This prevents the bug where FastAPI/Flask were passing request parameter.
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
        
        oauth = OAuth(framework=None)
        sig = inspect.signature(oauth.get_user_info)
        params = list(sig.parameters.keys())
        
        # Should have no parameters (self is implicit)
        self.assertEqual(len(params), 0,
                        f"get_user_info() should accept no parameters, found: {params}")

    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.requests.get')
    def test_is_authenticated_rejects_extra_parameters(self, mock_get, mock_framework_factory, mock_storage_factory):
        """
        Test that passing extra parameters to is_authenticated() raises TypeError.
        
        This ensures if someone accidentally adds request parameter back,
        the test will catch it.
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
        
        oauth = OAuth(framework=None)
        
        # Passing a parameter should raise TypeError
        with self.assertRaises(TypeError) as context:
            oauth.is_authenticated("unexpected_parameter")
        
        # Verify error message mentions positional arguments
        self.assertIn("positional argument", str(context.exception).lower())

    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.requests.get')
    def test_get_user_info_rejects_extra_parameters(self, mock_get, mock_framework_factory, mock_storage_factory):
        """
        Test that passing extra parameters to get_user_info() raises TypeError.
        
        This ensures if someone accidentally adds request parameter back,
        the test will catch it.
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
        
        oauth = OAuth(framework=None)
        
        # Passing a parameter should raise TypeError
        with self.assertRaises(TypeError) as context:
            oauth.get_user_info("unexpected_parameter")
        
        # Verify error message mentions positional arguments
        self.assertIn("positional argument", str(context.exception).lower())


if __name__ == '__main__':
    unittest.main()

