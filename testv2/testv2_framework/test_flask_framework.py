import unittest
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, call
from flask import Flask
from kinde_flask.framework.flask_framework import FlaskFramework
from kinde_sdk.auth.oauth import OAuth


class BaseFlaskFrameworkTest(unittest.TestCase):
    """Base test class with common setUp/tearDown logic for all Flask framework tests."""
    
    def setUp(self):
        """Set up test fixtures. Subclasses can override to customize behavior."""
        # Store original env vars - snapshot ALL env vars
        self.original_env = dict(os.environ)
        
        # Track created frameworks for cleanup
        self.created_frameworks = []
    
    def tearDown(self):
        """Clean up after tests."""
        # Clean up any framework-created session directories
        for framework in self.created_frameworks:
            if hasattr(framework, 'app') and framework.app:
                session_dir = framework.app.config.get('SESSION_FILE_DIR')
                if session_dir and os.path.exists(session_dir):
                    shutil.rmtree(session_dir, ignore_errors=True)
        
        # Clean up test session directory if it exists
        if hasattr(self, 'test_session_dir') and os.path.exists(self.test_session_dir):
            shutil.rmtree(self.test_session_dir, ignore_errors=True)
        
        # Clean up session directory from setUp if it exists
        if hasattr(self, '_setup_session_dir'):
            session_dir = os.environ.get('SESSION_FILE_DIR')
            if session_dir and os.path.exists(session_dir):
                shutil.rmtree(session_dir, ignore_errors=True)
        
        # Remove any env vars added during test and restore original state
        current_keys = set(os.environ.keys())
        original_keys = set(self.original_env.keys())
        
        # Remove keys that were added during the test
        for key in current_keys - original_keys:
            del os.environ[key]
        
        # Restore original values
        for key, value in self.original_env.items():
            os.environ[key] = value


class TestFlaskFramework(BaseFlaskFrameworkTest):
    """Test cases for FlaskFramework configuration."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        
        # Clear specific keys for clean test environment
        for key in ['SECRET_KEY', 'SESSION_TYPE', 'SESSION_FILE_DIR']:
            if key in os.environ:
                del os.environ[key]
        
        # Create a temporary directory for test sessions
        self.test_session_dir = tempfile.mkdtemp(prefix='test_flask_sessions_')
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.logger')
    def test_secret_key_auto_generation_with_warning(self, mock_logger, _mock_session):
        """Test that SECRET_KEY is auto-generated with a warning when not set."""
        # Ensure SECRET_KEY is not set
        if 'SECRET_KEY' in os.environ:
            del os.environ['SECRET_KEY']
        
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
        # Verify SECRET_KEY was set
        self.assertIsNotNone(framework.app.config.get('SECRET_KEY'))
        self.assertGreater(len(framework.app.config['SECRET_KEY']), 0)
        
        # Verify warning was logged
        mock_logger.warning.assert_any_call(
            "SECRET_KEY not set. Generated a random key for this session. "
            "Set SECRET_KEY environment variable for production use."
        )
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.logger')
    def test_secret_key_from_environment(self, mock_logger, _mock_session):
        """Test that SECRET_KEY is read from environment variable."""
        test_secret = "my_test_secret_key_12345"
        os.environ['SECRET_KEY'] = test_secret
        
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
        # Verify SECRET_KEY was set from env
        self.assertEqual(framework.app.config['SECRET_KEY'], test_secret)
        
        # Verify no warning was logged for SECRET_KEY
        warning_calls = [call for call in mock_logger.warning.call_args_list 
                        if 'SECRET_KEY' in str(call)]
        self.assertEqual(len(warning_calls), 0)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_session_type_default(self, _mock_session):
        """Test that SESSION_TYPE defaults to 'filesystem'."""
        if 'SESSION_TYPE' in os.environ:
            del os.environ['SESSION_TYPE']
        
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
        self.assertEqual(framework.app.config['SESSION_TYPE'], 'filesystem')
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_session_type_from_environment(self, _mock_session):
        """Test that SESSION_TYPE is read from environment variable."""
        os.environ['SESSION_TYPE'] = 'test-session-type'
        
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
        self.assertEqual(framework.app.config['SESSION_TYPE'], 'test-session-type')
    
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
        self.assertGreaterEqual(mock_chmod.call_count, 1)
        first_call = mock_chmod.call_args_list[0]
        self.assertEqual(first_call, call(test_temp_dir, 0o700))
        
        # Verify SESSION_FILE_DIR was set
        self.assertEqual(framework.app.config['SESSION_FILE_DIR'], test_temp_dir)
        
        # Verify warning was logged
        mock_logger.warning.assert_any_call(
            f"SESSION_FILE_DIR not set. Using temporary directory: {test_temp_dir}. "
            "Set SESSION_FILE_DIR environment variable for production use."
        )

    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.logger')
    def test_session_file_dir_from_environment(self, mock_logger, _mock_session):
        """Test that SESSION_FILE_DIR is read from environment variable."""
        os.environ['SESSION_FILE_DIR'] = self.test_session_dir
        
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
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
        self.created_frameworks.append(framework)
        
        # Verify Session was called with the app
        mock_session.assert_called_once_with(framework.app)
        
        # Verify debug log was written
        mock_logger.debug.assert_called_with("Flask-Session initialized with server-side storage")
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_session_permanent_is_false(self, _mock_session):
        """Test that SESSION_PERMANENT is set to False."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
        self.assertFalse(framework.app.config['SESSION_PERMANENT'])


class TestFlaskFrameworkRoutes(BaseFlaskFrameworkTest):
    """Test cases for Flask framework route handling."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        
        # Set env vars to avoid auto-generation during tests
        os.environ['SECRET_KEY'] = 'test_secret_key'
        os.environ['SESSION_FILE_DIR'] = tempfile.mkdtemp(prefix='test_sessions_')
        self._setup_session_dir = True  # Flag for cleanup
        
        # Mock OAuth instance
        self.mock_oauth = Mock(spec=OAuth)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.FlaskFramework._run_async')
    def test_login_route_event_loop_management(self, mock_run_async, _mock_session):
        """Test that login route properly uses _run_async helper."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        framework.set_oauth(self.mock_oauth)
        
        # Mock the OAuth login and _run_async
        self.mock_oauth.login = Mock(return_value='async_login_coro')
        mock_run_async.return_value = 'https://example.com/login'
        
        framework.start()
        
        # Test login route
        with framework.app.test_client() as client:
            response = client.get('/login')
            
            # Verify _run_async was called
            mock_run_async.assert_called_once()
            
            # Verify redirect occurred
            self.assertEqual(response.status_code, 302)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.FlaskFramework._run_async')
    def test_logout_route_event_loop_management(self, mock_run_async, _mock_session):
        """Test that logout route properly uses _run_async helper."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        framework.set_oauth(self.mock_oauth)
        
        # Mock the OAuth logout and _run_async
        self.mock_oauth.logout = Mock(return_value='async_logout_coro')
        mock_run_async.return_value = 'https://example.com/logout'
        
        framework.start()
        
        # Test logout route
        with framework.app.test_client() as client:
            with client.session_transaction() as session:
                session['user_id'] = 'test_user_123'
            
            response = client.get('/logout')
            
            # Verify _run_async was called
            mock_run_async.assert_called_once()
            
            # Verify redirect occurred
            self.assertEqual(response.status_code, 302)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.FlaskFramework._run_async')
    def test_register_route_event_loop_management(self, mock_run_async, _mock_session):
        """Test that register route properly uses _run_async helper."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        framework.set_oauth(self.mock_oauth)
        
        # Mock the OAuth register and _run_async
        self.mock_oauth.register = Mock(return_value='async_register_coro')
        mock_run_async.return_value = 'https://example.com/register'
        
        framework.start()
        
        # Test register route
        with framework.app.test_client() as client:
            response = client.get('/register')
            
            # Verify _run_async was called
            mock_run_async.assert_called_once()
            
            # Verify redirect occurred
            self.assertEqual(response.status_code, 302)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.asyncio.new_event_loop')
    def test_event_loop_closed_on_exception(self, mock_new_event_loop, _mock_session):
        """Test that event loop is closed even when an exception occurs in _run_async."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        framework.set_oauth(self.mock_oauth)
        
        # Create mock event loop that raises an exception
        mock_loop = Mock()
        mock_new_event_loop.return_value = mock_loop
        mock_loop.run_until_complete = Mock(side_effect=Exception("Test exception"))
        self.mock_oauth.login = Mock(return_value='async_login_coro')
        
        framework.start()
        
        # Test login route with exception
        with framework.app.test_client() as client:
            response = client.get('/login')
            self.assertEqual(response.status_code, 500)

            # Verify loop.close was still called despite exception (in _run_async finally block)
            mock_loop.close.assert_called()


class TestFlaskFrameworkInterface(BaseFlaskFrameworkTest):
    """Test cases for FlaskFramework interface compliance."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        
        # Set env vars to avoid warnings during tests
        os.environ['SECRET_KEY'] = 'test_secret_key'
        os.environ['SESSION_FILE_DIR'] = tempfile.mkdtemp(prefix='test_sessions_')
        self._setup_session_dir = True  # Flag for cleanup
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_framework_properties(self, _mock_session):
        """Test framework name and description."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
        self.assertEqual(framework.get_name(), "flask")
        self.assertIn("Flask", framework.get_description())
        self.assertIn("Kinde", framework.get_description())
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_get_app_returns_flask_instance(self, _mock_session):
        """Test that get_app returns Flask application instance."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
        app = framework.get_app()
        self.assertIsInstance(app, Flask)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_start_and_stop(self, _mock_session):
        """Test framework start and stop methods."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
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
    def test_can_auto_detect(self, _mock_session):
        """Test that Flask can be auto-detected when installed."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
        # Flask is installed (we're using it in tests)
        self.assertTrue(framework.can_auto_detect())
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_set_oauth(self, _mock_session):
        """Test setting OAuth instance."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        mock_oauth = Mock(spec=OAuth)
        
        self.assertIsNone(framework._oauth)
        framework.set_oauth(mock_oauth)
        self.assertEqual(framework._oauth, mock_oauth)
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_user_id_management(self, _mock_session):
        """Test user ID get/set functionality."""
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
        with framework.app.test_request_context():
            from flask import session
            
            # Initially no user_id
            self.assertIsNone(framework.get_user_id())
            
            # Set user_id in session
            session['user_id'] = 'test_user_123'
            self.assertEqual(framework.get_user_id(), 'test_user_123')


class TestFlaskFrameworkSecurity(BaseFlaskFrameworkTest):
    """Test cases for Flask framework security features."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        
        # Clear specific env vars for clean test environment
        for key in ['SECRET_KEY', 'SESSION_TYPE', 'SESSION_FILE_DIR']:
            if key in os.environ:
                del os.environ[key]
    
    @patch('kinde_flask.framework.flask_framework.Session')
    @patch('kinde_flask.framework.flask_framework.tempfile.mkdtemp')
    @patch('kinde_flask.framework.flask_framework.os.chmod')
    def test_session_directory_permissions(self, mock_chmod, mock_mkdtemp, _mock_session):
        """Test that session directory is created with secure permissions (0o700)."""
        test_temp_dir = '/tmp/test_kinde_sessions_xyz789'
        mock_mkdtemp.return_value = test_temp_dir
        
        # Framework not tracked since mocks prevent real directory creation
        _framework = FlaskFramework()
        
        # Verify chmod was called with restrictive permissions (at least once for the main directory)
        # Flask-Session may also call chmod on subdirectories, so we check the first call
        self.assertGreaterEqual(mock_chmod.call_count, 1)
        first_call = mock_chmod.call_args_list[0]
        self.assertEqual(first_call, call(test_temp_dir, 0o700))
    
    @patch('kinde_flask.framework.flask_framework.Session')
    def test_secret_key_length(self, _mock_session):
        """Test that auto-generated SECRET_KEY has sufficient length."""
        if 'SECRET_KEY' in os.environ:
            del os.environ['SECRET_KEY']
        
        framework = FlaskFramework()
        self.created_frameworks.append(framework)
        
        secret_key = framework.app.config['SECRET_KEY']
        
        # secrets.token_urlsafe(32) generates a 32-byte token
        # which is URL-safe base64 encoded, resulting in ~43 characters
        self.assertGreater(len(secret_key), 30)


if __name__ == '__main__':
    unittest.main()
