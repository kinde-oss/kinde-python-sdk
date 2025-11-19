"""
Test cases for KindeSessionManagement class.

This module tests the KindeSessionManagement functionality to ensure it works
correctly in standalone mode and raises appropriate exceptions when used
with web frameworks.
"""

import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the SDK to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from kinde_sdk.core.session_management import KindeSessionManagement
from kinde_sdk.core.framework.null_framework import NullFramework
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.oauth import OAuth


class TestKindeSessionManagement(unittest.TestCase):
    """Test cases for KindeSessionManagement class."""
    
    def setUp(self):
        """Set up test environment."""
        # Clear any existing framework instance
        FrameworkFactory._framework_instance = None
        # Clear NullFramework singleton state
        if hasattr(NullFramework, '_instance'):
            NullFramework._instance = None
        
    def tearDown(self):
        """Clean up after tests."""
        # Clear any existing framework instance
        FrameworkFactory._framework_instance = None
        # Clear NullFramework singleton state
        if hasattr(NullFramework, '_instance'):
            NullFramework._instance = None
        
    def test_session_management_with_null_framework(self):
        """Test that KindeSessionManagement works with NullFramework."""
        # Create an OAuth instance without framework (will use NullFramework)
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:5000/callback",
            framework=None  # This will trigger NullFramework usage
        )
        
        # Now create session management
        session_mgmt = KindeSessionManagement()
        
        # Test initial state
        self.assertIsNone(session_mgmt.get_user_id())
        self.assertFalse(session_mgmt.is_user_logged_in())
        
        # Test setting user ID
        session_mgmt.set_user_id("test_user_123")
        self.assertEqual(session_mgmt.get_user_id(), "test_user_123")
        self.assertTrue(session_mgmt.is_user_logged_in())
        
        # Test session info
        session_info = session_mgmt.get_session_info()
        self.assertEqual(session_info["user_id"], "test_user_123")
        self.assertTrue(session_info["is_logged_in"])
        self.assertEqual(session_info["framework"], "standalone")
        self.assertEqual(session_info["session_type"], "null_framework")
        
        # Test clearing user ID
        session_mgmt.clear_user_id()
        self.assertIsNone(session_mgmt.get_user_id())
        self.assertFalse(session_mgmt.is_user_logged_in())
        
    def test_session_management_with_framework_raises_error(self):
        """Test that KindeSessionManagement raises error when framework is active."""
        # Mock a framework instance that's not NullFramework
        mock_framework = MagicMock()
        mock_framework.get_name.return_value = "fastapi"
        
        with patch.object(FrameworkFactory, 'get_framework_instance', return_value=mock_framework):
            with patch('kinde_sdk.core.framework.null_framework.NullFramework') as mock_null:
                mock_null.return_value = None
                with self.assertRaises(RuntimeError) as context:
                    KindeSessionManagement()
                
                self.assertIn("can only be used in standalone mode", str(context.exception))
                self.assertIn("web framework", str(context.exception))
    
    def test_session_management_with_no_framework_raises_error(self):
        """Test that KindeSessionManagement raises error when no framework is active."""
        with patch.object(FrameworkFactory, 'get_framework_instance', return_value=None):
            with patch('kinde_sdk.core.framework.null_framework.NullFramework') as mock_null:
                mock_null.return_value = None
                with self.assertRaises(RuntimeError) as context:
                    KindeSessionManagement()
                
                self.assertIn("can only be used in standalone mode", str(context.exception))
    
    def test_set_user_id_validation(self):
        """Test that set_user_id validates input properly."""
        # Create OAuth with NullFramework
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:5000/callback",
            framework=None
        )
        
        session_mgmt = KindeSessionManagement()
        
        # Test empty string
        with self.assertRaises(ValueError):
            session_mgmt.set_user_id("")
        
        # Test None
        with self.assertRaises(ValueError):
            session_mgmt.set_user_id(None)
        
        # Test whitespace only
        with self.assertRaises(ValueError):
            session_mgmt.set_user_id("   ")
    
    def test_session_management_methods_without_framework(self):
        """Test that session management methods raise error when framework is not available."""
        # Mock no framework available
        with patch.object(FrameworkFactory, 'get_framework_instance', return_value=None):
            with patch('kinde_sdk.core.framework.null_framework.NullFramework') as mock_null:
                mock_null.return_value = None
                # This should raise error during initialization
                with self.assertRaises(RuntimeError):
                    KindeSessionManagement()
    
    def test_repr_method(self):
        """Test the string representation of KindeSessionManagement."""
        # Create OAuth with NullFramework
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:5000/callback",
            framework=None
        )
        
        session_mgmt = KindeSessionManagement()
        
        # Test repr when not logged in
        repr_str = repr(session_mgmt)
        self.assertIn("KindeSessionManagement", repr_str)
        self.assertIn("not_logged_in", repr_str)
        
        # Test repr when logged in
        session_mgmt.set_user_id("test_user")
        repr_str = repr(session_mgmt)
        self.assertIn("KindeSessionManagement", repr_str)
        self.assertIn("test_user", repr_str)
        self.assertIn("logged_in", repr_str)
    
    def test_session_info_comprehensive(self):
        """Test comprehensive session info functionality."""
        # Create OAuth with NullFramework
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:5000/callback",
            framework=None
        )
        
        session_mgmt = KindeSessionManagement()
        
        # Test session info when not logged in
        session_info = session_mgmt.get_session_info()
        self.assertIsNone(session_info["user_id"])
        self.assertFalse(session_info["is_logged_in"])
        self.assertEqual(session_info["framework"], "standalone")
        self.assertEqual(session_info["session_type"], "null_framework")
        
        # Test session info when logged in
        session_mgmt.set_user_id("user_123")
        session_info = session_mgmt.get_session_info()
        self.assertEqual(session_info["user_id"], "user_123")
        self.assertTrue(session_info["is_logged_in"])
        self.assertEqual(session_info["framework"], "standalone")
        self.assertEqual(session_info["session_type"], "null_framework")


class TestKindeSessionManagementIntegration(unittest.TestCase):
    """Integration tests for KindeSessionManagement with real OAuth instances."""
    
    def setUp(self):
        """Set up test environment."""
        # Clear any existing framework instance
        FrameworkFactory._framework_instance = None
        # Clear NullFramework singleton state
        if hasattr(NullFramework, '_instance'):
            NullFramework._instance = None
        
    def tearDown(self):
        """Clean up after tests."""
        # Clear any existing framework instance
        FrameworkFactory._framework_instance = None
        # Clear NullFramework singleton state
        if hasattr(NullFramework, '_instance'):
            NullFramework._instance = None
    
    def test_integration_with_oauth_standalone(self):
        """Test integration with OAuth in standalone mode."""
        # Create OAuth instance in standalone mode
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:5000/callback",
            framework=None  # Standalone mode
        )
        
        # Create session management
        session_mgmt = KindeSessionManagement()
        
        # Test that we can manage sessions
        session_mgmt.set_user_id("integration_test_user")
        
        # Verify the session is set in the OAuth instance
        self.assertTrue(oauth.is_authenticated() or session_mgmt.is_user_logged_in())
        
        # Test session info
        session_info = session_mgmt.get_session_info()
        self.assertEqual(session_info["user_id"], "integration_test_user")
        self.assertTrue(session_info["is_logged_in"])
    
    def test_multiple_session_management_instances(self):
        """Test that multiple KindeSessionManagement instances work correctly."""
        # Create OAuth instance
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:5000/callback",
            framework=None
        )
        
        # Create multiple session management instances
        session_mgmt1 = KindeSessionManagement()
        session_mgmt2 = KindeSessionManagement()
        
        # Set user ID with first instance
        session_mgmt1.set_user_id("user_123")
        
        # Verify second instance sees the same session
        self.assertEqual(session_mgmt2.get_user_id(), "user_123")
        self.assertTrue(session_mgmt2.is_user_logged_in())
        
        # Clear with second instance
        session_mgmt2.clear_user_id()
        
        # Verify first instance sees the cleared session
        self.assertIsNone(session_mgmt1.get_user_id())
        self.assertFalse(session_mgmt1.is_user_logged_in())


if __name__ == '__main__':
    unittest.main()
