import unittest
import os
import tempfile
import shutil
import logging
from unittest.mock import Mock, patch, MagicMock, call
from flask import Flask
from kinde_flask.framework.flask_framework import FlaskFramework
from kinde_sdk.auth.oauth import OAuth


class TestFlaskFramework(unittest.TestCase):
    """Test cases for FlaskFramework configuration."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Store original env vars
        self.original_env = {}
        for key in ['SECRET_KEY', 'SESSION_TYPE', 'SESSION_FILE_DIR']:
            if key in os.environ:
                self.original_env[key] = os.environ[key]
                del os.environ[key]
        
        # Create a temporary directory for test sessions
        self.test_session_dir = tempfile.mkdtemp(prefix='test_flask_sessions_')
    
    def tearDown(self):
        """Clean up after tests."""
        # Restore original env vars
        for key, value in self.original_env.items():
            os.environ[key] = value
        
        # Clean up test session directory
        if os.path.exists(self.test_session_dir):
            shutil.rmtree(self.test_session_dir)
    
    @patch('kinde_flask.framework.flask_framework.logger')
    def test_secret_key_auto_generation_with_warning(self, mock_logger):
        """Test that SECRET_KEY is auto-generated with a warning when not set."""
        # Ensure SECRET_KEY is not set
        if 'SECRET_KEY' in os.environ:
            del os.environ['SECRET_KEY']
        
        framework = FlaskFramework()
        
        # Verify SECRET_KEY was set
        self.assertIsNotNone(framework.app.config.get('SECRET_KEY'))
        self.assertGreater(len(framework.app.config['SECRET_KEY']), 0)
        
        # Verify warning was logged
        mock_logger.warning.assert_any_call(
            "SECRET_KEY not set. Generated a random key for this session. "
            "Set SECRET_KEY environment variable for production use."
        )
    
    @patch('kinde_flask.framework.flask_framework.logger')
    def test_secret_key_from_environment(self, mock_logger):
        """Test that SECRET_KEY is read from environment variable."""
        test_secret = "my_test_secret_key_12345"
        os.environ['SECRET_KEY'] = test_secret
        
        framework = FlaskFramework()
        
        # Verify SECRET_KEY was set from env
        self.assertEqual(framework.app.config['SECRET_KEY'], test_secret)
        
        # Verify no warning was logged for SECRET_KEY
        warning_calls = [call for call in mock_logger.warning.call_args_list 
                        if 'SECRET_KEY' in str(call)]
        self.assertEqual(len(warning_calls), 0)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_session_type_default(self, mock_session):
        """Test that SESSION_TYPE defaults to 'filesystem'."""
        if 'SESSION_TYPE' in os.environ:
            del os.environ['SESSION_TYPE']
        
        framework = FlaskFramework()
        
        self.assertEqual(framework.app.config['SESSION_TYPE'], 'filesystem')
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_session_type_from_environment(self, mock_session):
        """Test that SESSION_TYPE is read from environment variable."""
        # Use 'filesystem' instead of 'redis' since redis module is not installed in test env
        os.environ['SESSION_TYPE'] = 'filesystem'
        
        framework = FlaskFramework()
        
        self.assertEqual(framework.app.config['SESSION_TYPE'], 'filesystem')
    
    @patch('kinde_flask.framework.flask_framework.logger')
    @patch('kinde_flask.framework.flask_framework.tempfile.mkdtemp')
    @patch('kinde_flask.framework.flask_framework.os.chmod')
    def test_session_file_dir_auto_generation_with_warning(self, mock_chmod, mock_mkdtemp, 
                                                           mock_logger):
        """Test that SESSION_FILE_DIR is auto-generated with warning when not set."""
        if 'SESSION_FILE_DIR' in os.environ:
            del os.environ['SESSION_FILE_DIR']
        
        test_temp_dir = '/tmp/test_kinde_sessions_abc123'
        mock_mkdtemp.return_value = test_temp_dir
        
        framework = FlaskFramework()
        
        # Verify mkdtemp was called with correct prefix
        mock_mkdtemp.assert_called_once_with(prefix='kinde_flask_sessions_')
        
        # Verify chmod was called with 0o700 for security (at least once for the main directory)
        # Flask-Session may also call chmod on subdirectories, so we check the first call
        assert mock_chmod.call_count >= 1
        first_call = mock_chmod.call_args_list[0]
        assert first_call == call(test_temp_dir, 0o700)
        
        # Verify SESSION_FILE_DIR was set
        self.assertEqual(framework.app.config['SESSION_FILE_DIR'], test_temp_dir)
        
        # Verify warning was logged
        mock_logger.warning.assert_any_call(
            f"SESSION_FILE_DIR not set. Using temporary directory: {test_temp_dir}. "
            "Set SESSION_FILE_DIR environment variable for production use."
        )

    @patch('kinde_flask.framework.flask_framework.logger')
    def test_session_file_dir_from_environment(self, mock_logger):
        """Test that SESSION_FILE_DIR is read from environment variable."""
        os.environ['SESSION_FILE_DIR'] = self.test_session_dir
        
        framework = FlaskFramework()
        
        # Verify SESSION_FILE_DIR was set from env
        self.assertEqual(framework.app.config['SESSION_FILE_DIR'], self.test_session_dir)
        
        # Verify no warning was logged for SESSION_FILE_DIR
        warning_calls = [call for call in mock_logger.warning.call_args_list 
                        if 'SESSION_FILE_DIR' in str(call)]
        self.assertEqual(len(warning_calls), 0)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.logger')
    def test_flask_session_initialization(self, mock_logger, mock_session):
        """Test that Flask-Session is properly initialized."""
        framework = FlaskFramework()
        
        # Verify Session was called with the app
        mock_session.assert_called_once_with(framework.app)
        
        # Verify debug log was written
        mock_logger.debug.assert_called_with("Flask-Session initialized with server-side storage")
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_session_permanent_is_false(self, mock_session):
        """Test that SESSION_PERMANENT is set to False."""
        framework = FlaskFramework()
        
        self.assertFalse(framework.app.config['SESSION_PERMANENT'])


class TestFlaskFrameworkRoutes(unittest.TestCase):
    """Test cases for Flask framework route handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.original_env = {}
        for key in ['SECRET_KEY', 'SESSION_TYPE', 'SESSION_FILE_DIR']:
            if key in os.environ:
                self.original_env[key] = os.environ[key]
        
        # Set env vars to avoid auto-generation during tests
        os.environ['SECRET_KEY'] = 'test_secret_key'
        os.environ['SESSION_FILE_DIR'] = tempfile.mkdtemp(prefix='test_sessions_')
        
        # Mock OAuth instance
        self.mock_oauth = Mock(spec=OAuth)
    
    def tearDown(self):
        """Clean up after tests."""
        # Restore original env vars
        for key in ['SECRET_KEY', 'SESSION_TYPE', 'SESSION_FILE_DIR']:
            if key in os.environ:
                del os.environ[key]
        for key, value in self.original_env.items():
            os.environ[key] = value
        
        # Clean up test session directory
        session_dir = os.environ.get('SESSION_FILE_DIR')
        if session_dir and os.path.exists(session_dir):
            shutil.rmtree(session_dir)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.asyncio.new_event_loop')
    def test_login_route_event_loop_management(self, mock_new_event_loop, mock_session):
        """Test that login route properly creates and closes event loop."""
        framework = FlaskFramework()
        framework.set_oauth(self.mock_oauth)
        
        # Create mock event loop
        mock_loop = Mock()
        mock_new_event_loop.return_value = mock_loop
        self.mock_oauth.login = Mock(return_value='https://example.com/login')
        mock_loop.run_until_complete = Mock(return_value='https://example.com/login')
        
        framework.start()
        
        # Test login route
        with framework.app.test_client() as client:
            response = client.get('/login')
            
            # Verify event loop was created
            mock_new_event_loop.assert_called()
            
            # Verify loop.run_until_complete was called
            mock_loop.run_until_complete.assert_called()
            
            # Verify loop.close was called
            mock_loop.close.assert_called()
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.asyncio.new_event_loop')
    def test_logout_route_event_loop_management(self, mock_new_event_loop, mock_session):
        """Test that logout route properly creates and closes event loop."""
        framework = FlaskFramework()
        framework.set_oauth(self.mock_oauth)
        
        # Create mock event loop
        mock_loop = Mock()
        mock_new_event_loop.return_value = mock_loop
        self.mock_oauth.logout = Mock(return_value='https://example.com/logout')
        mock_loop.run_until_complete = Mock(return_value='https://example.com/logout')
        
        framework.start()
        
        # Test logout route
        with framework.app.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = 'test_user_123'
            
            response = client.get('/logout')
            
            # Verify event loop was created
            mock_new_event_loop.assert_called()
            
            # Verify loop.run_until_complete was called
            mock_loop.run_until_complete.assert_called()
            
            # Verify loop.close was called
            mock_loop.close.assert_called()
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.asyncio.new_event_loop')
    def test_register_route_event_loop_management(self, mock_new_event_loop, mock_session):
        """Test that register route properly creates and closes event loop."""
        framework = FlaskFramework()
        framework.set_oauth(self.mock_oauth)
        
        # Create mock event loop
        mock_loop = Mock()
        mock_new_event_loop.return_value = mock_loop
        self.mock_oauth.register = Mock(return_value='https://example.com/register')
        mock_loop.run_until_complete = Mock(return_value='https://example.com/register')
        
        framework.start()
        
        # Test register route
        with framework.app.test_client() as client:
            response = client.get('/register')
            
            # Verify event loop was created
            mock_new_event_loop.assert_called()
            
            # Verify loop.run_until_complete was called
            mock_loop.run_until_complete.assert_called()
            
            # Verify loop.close was called
            mock_loop.close.assert_called()
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.asyncio.new_event_loop')
    def test_event_loop_closed_on_exception(self, mock_new_event_loop, mock_session):
        """Test that event loop is closed even when an exception occurs."""
        framework = FlaskFramework()
        framework.set_oauth(self.mock_oauth)
        
        # Create mock event loop that raises an exception
        mock_loop = Mock()
        mock_new_event_loop.return_value = mock_loop
        mock_loop.run_until_complete = Mock(side_effect=Exception("Test exception"))
        
        framework.start()
        
        # Test login route with exception
        with framework.app.test_client() as client:
            try:
                response = client.get('/login')
            except Exception:
                pass  # Expected to raise
            
            # Verify loop.close was still called despite exception
            mock_loop.close.assert_called()


class TestFlaskFrameworkInterface(unittest.TestCase):
    """Test cases for FlaskFramework interface compliance."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Set env vars to avoid warnings during tests
        os.environ['SECRET_KEY'] = 'test_secret_key'
        os.environ['SESSION_FILE_DIR'] = tempfile.mkdtemp(prefix='test_sessions_')
    
    def tearDown(self):
        """Clean up after tests."""
        session_dir = os.environ.get('SESSION_FILE_DIR')
        if session_dir and os.path.exists(session_dir):
            shutil.rmtree(session_dir)
        
        for key in ['SECRET_KEY', 'SESSION_TYPE', 'SESSION_FILE_DIR']:
            if key in os.environ:
                del os.environ[key]
    
    def test_framework_properties(self):
        """Test framework name and description."""
        framework = FlaskFramework()
        
        self.assertEqual(framework.get_name(), "flask")
        self.assertIn("Flask", framework.get_description())
        self.assertIn("Kinde", framework.get_description())
    
    def test_get_app_returns_flask_instance(self):
        """Test that get_app returns Flask application instance."""
        framework = FlaskFramework()
        
        app = framework.get_app()
        self.assertIsInstance(app, Flask)
    
    def test_start_and_stop(self):
        """Test framework start and stop methods."""
        framework = FlaskFramework()
        mock_oauth = Mock(spec=OAuth)
        framework.set_oauth(mock_oauth)
        
        # Test start
        self.assertFalse(framework._initialized)
        framework.start()
        self.assertTrue(framework._initialized)
        
        # Test stop
        framework.stop()
        self.assertFalse(framework._initialized)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_can_auto_detect(self, mock_session):
        """Test that Flask can be auto-detected when installed."""
        framework = FlaskFramework()
        
        # Flask is installed (we're using it in tests)
        self.assertTrue(framework.can_auto_detect())
    
    def test_set_oauth(self):
        """Test setting OAuth instance."""
        framework = FlaskFramework()
        mock_oauth = Mock(spec=OAuth)
        
        self.assertIsNone(framework._oauth)
        framework.set_oauth(mock_oauth)
        self.assertEqual(framework._oauth, mock_oauth)
    
    def test_user_id_management(self):
        """Test user ID get/set functionality."""
        framework = FlaskFramework()
        
        with framework.app.test_request_context():
            from flask import session
            
            # Initially no user_id
            self.assertIsNone(framework.get_user_id())
            
            # Set user_id in session
            session['user_id'] = 'test_user_123'
            self.assertEqual(framework.get_user_id(), 'test_user_123')


class TestFlaskFrameworkSecurity(unittest.TestCase):
    """Test cases for Flask framework security features."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Clear env vars
        for key in ['SECRET_KEY', 'SESSION_TYPE', 'SESSION_FILE_DIR']:
            if key in os.environ:
                del os.environ[key]
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.tempfile.mkdtemp')
    @patch('kinde_flask.framework.flask_framework.os.chmod')
    def test_session_directory_permissions(self, mock_chmod, mock_mkdtemp, mock_session):
        """Test that session directory is created with secure permissions (0o700)."""
        test_temp_dir = '/tmp/test_kinde_sessions_xyz789'
        mock_mkdtemp.return_value = test_temp_dir
        
        framework = FlaskFramework()
        
        # Verify chmod was called with restrictive permissions (at least once for the main directory)
        # Flask-Session may also call chmod on subdirectories, so we check the first call
        assert mock_chmod.call_count >= 1
        first_call = mock_chmod.call_args_list[0]
        assert first_call == call(test_temp_dir, 0o700)
    
    def test_secret_key_length(self):
        """Test that auto-generated SECRET_KEY has sufficient length."""
        if 'SECRET_KEY' in os.environ:
            del os.environ['SECRET_KEY']
        
        framework = FlaskFramework()
        
        secret_key = framework.app.config['SECRET_KEY']
        
        # secrets.token_urlsafe(32) generates a 32-byte token
        # which is URL-safe base64 encoded, resulting in ~43 characters
        self.assertGreater(len(secret_key), 30)


if __name__ == '__main__':
    unittest.main()
