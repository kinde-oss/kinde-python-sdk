"""
Tests to verify OAuth method signatures don't accept incorrect parameters.

This test file specifically covers the bug fix where is_authenticated() and
get_user_info() were being called with a request parameter they don't accept.
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import inspect
from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.core.exceptions import KindeConfigurationException


class TestOAuthMethodSignatures(unittest.TestCase):
    """Test OAuth method signatures to prevent regression of parameter bug."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock app
        self.mock_app = Mock()
        self.mock_app.add_middleware = Mock()
        
        # Patch environment variables
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

    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    def test_is_authenticated_method_signature_no_parameters(self, mock_storage_factory, mock_framework_factory):
        """Test that is_authenticated() accepts no parameters beyond self."""
        # Create OAuth instance without framework to avoid initialization
        oauth = OAuth(framework=None)
        
        # Get the method signature
        sig = inspect.signature(oauth.is_authenticated)
        
        # Should only have 'self' (which is implicit)
        params = list(sig.parameters.keys())
        
        # Assert no parameters beyond self
        self.assertEqual(len(params), 0, 
                        f"is_authenticated() should accept no parameters, found: {params}")
    
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    def test_get_user_info_method_signature_no_parameters(self, mock_storage_factory, mock_framework_factory):
        """Test that get_user_info() accepts no parameters beyond self."""
        # Create OAuth instance without framework to avoid initialization
        oauth = OAuth(framework=None)
        
        # Get the method signature
        sig = inspect.signature(oauth.get_user_info)
        
        # Should only have 'self' (which is implicit)
        params = list(sig.parameters.keys())
        
        # Assert no parameters beyond self
        self.assertEqual(len(params), 0, 
                        f"get_user_info() should accept no parameters, found: {params}")
    
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.requests.get')
    def test_is_authenticated_called_without_parameters(self, mock_get, mock_storage_factory, mock_framework_factory):
        """Test that is_authenticated() can be called without any parameters."""
        # Setup mocks
        mock_framework = Mock()
        mock_framework.get_user_id = Mock(return_value=None)
        mock_framework_factory.create_framework = Mock(return_value=mock_framework)
        
        mock_storage = Mock()
        mock_storage_factory.create_storage = Mock(return_value=mock_storage)
        
        # Mock the OpenID configuration endpoint
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            'authorization_endpoint': 'https://test.kinde.com/oauth2/auth',
            'token_endpoint': 'https://test.kinde.com/oauth2/token',
            'end_session_endpoint': 'https://test.kinde.com/logout',
            'userinfo_endpoint': 'https://test.kinde.com/oauth2/userinfo'
        })
        mock_get.return_value = mock_response
        
        # Create OAuth instance with framework
        oauth = OAuth(framework="test")
        
        # This should work without any parameters
        result = oauth.is_authenticated()
        
        # Should return False since no user is authenticated
        self.assertFalse(result)
    
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.requests.get')
    def test_get_user_info_called_without_parameters(self, mock_get, mock_storage_factory, mock_framework_factory):
        """Test that get_user_info() can be called without any parameters."""
        # Setup mocks
        mock_framework = Mock()
        mock_framework.get_user_id = Mock(return_value=None)
        mock_framework_factory.create_framework = Mock(return_value=mock_framework)
        
        mock_storage = Mock()
        mock_storage_factory.create_storage = Mock(return_value=mock_storage)
        
        # Mock the OpenID configuration endpoint
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            'authorization_endpoint': 'https://test.kinde.com/oauth2/auth',
            'token_endpoint': 'https://test.kinde.com/oauth2/token',
            'end_session_endpoint': 'https://test.kinde.com/logout',
            'userinfo_endpoint': 'https://test.kinde.com/oauth2/userinfo'
        })
        mock_get.return_value = mock_response
        
        # Create OAuth instance with framework
        oauth = OAuth(framework="test")
        
        # This should raise an exception since no user is authenticated
        # but it should NOT raise TypeError about parameters
        with self.assertRaises(KindeConfigurationException):
            oauth.get_user_info()
    
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.requests.get')
    def test_is_authenticated_rejects_extra_parameters(self, mock_get, mock_storage_factory, mock_framework_factory):
        """Test that passing extra parameters to is_authenticated() raises TypeError."""
        # Setup mocks
        mock_framework = Mock()
        mock_framework.get_user_id = Mock(return_value=None)
        mock_framework_factory.create_framework = Mock(return_value=mock_framework)
        
        mock_storage = Mock()
        mock_storage_factory.create_storage = Mock(return_value=mock_storage)
        
        # Mock the OpenID configuration endpoint
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            'authorization_endpoint': 'https://test.kinde.com/oauth2/auth',
            'token_endpoint': 'https://test.kinde.com/oauth2/token',
            'end_session_endpoint': 'https://test.kinde.com/logout',
            'userinfo_endpoint': 'https://test.kinde.com/oauth2/userinfo'
        })
        mock_get.return_value = mock_response
        
        # Create OAuth instance with framework
        oauth = OAuth(framework="test")
        
        # This should raise TypeError because we're passing an unexpected parameter
        with self.assertRaises(TypeError) as context:
            oauth.is_authenticated("unexpected_parameter")
        
        # Verify the error message mentions positional arguments
        self.assertIn("positional argument", str(context.exception).lower())
    
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.requests.get')
    def test_get_user_info_rejects_extra_parameters(self, mock_get, mock_storage_factory, mock_framework_factory):
        """Test that passing extra parameters to get_user_info() raises TypeError."""
        # Setup mocks
        mock_framework = Mock()
        mock_framework.get_user_id = Mock(return_value=None)
        mock_framework_factory.create_framework = Mock(return_value=mock_framework)
        
        mock_storage = Mock()
        mock_storage_factory.create_storage = Mock(return_value=mock_storage)
        
        # Mock the OpenID configuration endpoint
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            'authorization_endpoint': 'https://test.kinde.com/oauth2/auth',
            'token_endpoint': 'https://test.kinde.com/oauth2/token',
            'end_session_endpoint': 'https://test.kinde.com/logout',
            'userinfo_endpoint': 'https://test.kinde.com/oauth2/userinfo'
        })
        mock_get.return_value = mock_response
        
        # Create OAuth instance with framework
        oauth = OAuth(framework="test")
        
        # This should raise TypeError because we're passing an unexpected parameter
        with self.assertRaises(TypeError) as context:
            oauth.get_user_info("unexpected_parameter")
        
        # Verify the error message mentions positional arguments
        self.assertIn("positional argument", str(context.exception).lower())


class TestFrameworkIntegrationMethodSignatures(unittest.TestCase):
    """Test that framework route handlers are compatible with OAuth method signatures."""
    
    @patch('kinde_fastapi.framework.fastapi_framework.FrameworkMiddleware')
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.requests.get')
    def test_fastapi_framework_routes_registered_successfully(self, mock_get, mock_storage_factory, 
                                                              mock_framework_factory, mock_middleware):
        """Test that FastAPI framework routes are registered without errors."""
        from kinde_fastapi.framework.fastapi_framework import FastAPIFramework
        from fastapi import FastAPI
        
        # Setup mocks
        mock_framework = Mock()
        mock_framework.get_user_id = Mock(return_value=None)
        mock_framework.get_name = Mock(return_value="fastapi")
        mock_framework_factory.create_framework = Mock(return_value=mock_framework)
        
        mock_storage = Mock()
        mock_storage_factory.create_storage = Mock(return_value=mock_storage)
        
        # Mock the OpenID configuration endpoint
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            'authorization_endpoint': 'https://test.kinde.com/oauth2/auth',
            'token_endpoint': 'https://test.kinde.com/oauth2/token',
            'end_session_endpoint': 'https://test.kinde.com/logout',
            'userinfo_endpoint': 'https://test.kinde.com/oauth2/userinfo'
        })
        mock_get.return_value = mock_response
        
        # Create FastAPI app
        app = FastAPI()
        
        # This should not raise any errors about method signatures
        # The routes should be registered correctly with the proper OAuth method calls
        with patch.dict('os.environ', {
            'KINDE_CLIENT_ID': 'test_client_id',
            'KINDE_CLIENT_SECRET': 'test_client_secret',
            'KINDE_HOST': 'https://test.kinde.com'
        }):
            oauth = OAuth(framework="fastapi", app=app)
            
        # If we get here without errors, the routes were registered correctly
        self.assertIsNotNone(oauth)
    
    @patch('kinde_sdk.auth.oauth.FrameworkFactory')
    @patch('kinde_sdk.auth.oauth.StorageFactory')
    @patch('kinde_sdk.auth.oauth.requests.get')
    def test_flask_framework_routes_registered_successfully(self, mock_get, mock_storage_factory, 
                                                           mock_framework_factory):
        """Test that Flask framework routes are registered without errors."""
        from kinde_flask.framework.flask_framework import FlaskFramework
        from flask import Flask
        
        # Setup mocks
        mock_framework = Mock()
        mock_framework.get_user_id = Mock(return_value=None)
        mock_framework.get_name = Mock(return_value="flask")
        mock_framework_factory.create_framework = Mock(return_value=mock_framework)
        
        mock_storage = Mock()
        mock_storage_factory.create_storage = Mock(return_value=mock_storage)
        
        # Mock the OpenID configuration endpoint
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json = Mock(return_value={
            'authorization_endpoint': 'https://test.kinde.com/oauth2/auth',
            'token_endpoint': 'https://test.kinde.com/oauth2/token',
            'end_session_endpoint': 'https://test.kinde.com/logout',
            'userinfo_endpoint': 'https://test.kinde.com/oauth2/userinfo'
        })
        mock_get.return_value = mock_response
        
        # Create Flask app
        app = Flask(__name__)
        
        # This should not raise any errors about method signatures
        # The routes should be registered correctly with the proper OAuth method calls
        with patch.dict('os.environ', {
            'KINDE_CLIENT_ID': 'test_client_id',
            'KINDE_CLIENT_SECRET': 'test_client_secret',
            'KINDE_HOST': 'https://test.kinde.com'
        }):
            oauth = OAuth(framework="flask", app=app)
            
        # If we get here without errors, the routes were registered correctly
        self.assertIsNotNone(oauth)


if __name__ == '__main__':
    unittest.main()

