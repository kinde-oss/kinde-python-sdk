import pytest
from unittest.mock import Mock, patch
from kinde_sdk.auth.base_auth import BaseAuth
from kinde_sdk.auth.feature_flags import FeatureFlags
from kinde_sdk.auth.claims import Claims
from kinde_sdk.auth.permissions import Permissions
from kinde_sdk.auth.tokens import Tokens

class TestBaseAuth:
    def test_base_auth_inheritance(self):
        """Test that all auth classes properly inherit from BaseAuth"""
        assert issubclass(FeatureFlags, BaseAuth)
        assert issubclass(Claims, BaseAuth)
        assert issubclass(Permissions, BaseAuth)
        assert issubclass(Tokens, BaseAuth)

    def test_base_auth_initialization(self):
        """Test that BaseAuth initializes correctly"""
        auth = BaseAuth()
        assert auth._logger is not None
        assert auth._framework is None
        assert auth._session_manager is not None

    @patch('kinde_sdk.core.framework.framework_factory.FrameworkFactory.get_framework_instance')
    def test_get_framework_singleton(self, mock_framework_factory):
        """Test that _get_framework uses singleton pattern"""
        mock_framework = Mock()
        mock_framework_factory.return_value = mock_framework
        
        auth = BaseAuth()
        
        # First call should set the framework
        result1 = auth._get_framework()
        assert result1 == mock_framework
        assert auth._framework == mock_framework
        
        # Second call should return the same instance
        result2 = auth._get_framework()
        assert result2 == mock_framework
        
        # Should only call the factory once
        mock_framework_factory.assert_called_once()

    @patch('kinde_sdk.core.framework.framework_factory.FrameworkFactory.get_framework_instance')
    def test_get_token_manager_with_framework_and_user_id(self, mock_framework_factory):
        """Test _get_token_manager when framework and user_id are available"""
        mock_framework = Mock()
        mock_framework.get_user_id.return_value = "user_123"
        mock_framework_factory.return_value = mock_framework
        
        mock_session_manager = Mock()
        mock_token_manager = Mock()
        mock_session_manager.get_token_manager.return_value = mock_token_manager
        
        auth = BaseAuth()
        auth._session_manager = mock_session_manager
        
        result = auth._get_token_manager()
        
        assert result == mock_token_manager
        mock_framework.get_user_id.assert_called_once()
        mock_session_manager.get_token_manager.assert_called_once_with("user_123")

    @patch('kinde_sdk.core.framework.framework_factory.FrameworkFactory.get_framework_instance')
    def test_get_token_manager_no_framework(self, mock_framework_factory):
        """Test _get_token_manager when framework is not available"""
        mock_framework_factory.return_value = None
        
        auth = BaseAuth()
        result = auth._get_token_manager()
        
        assert result is None

    @patch('kinde_sdk.core.framework.framework_factory.FrameworkFactory.get_framework_instance')
    def test_get_token_manager_no_user_id(self, mock_framework_factory):
        """Test _get_token_manager when user_id is not available"""
        mock_framework = Mock()
        mock_framework.get_user_id.return_value = None
        mock_framework_factory.return_value = mock_framework
        
        auth = BaseAuth()
        result = auth._get_token_manager()
        
        assert result is None 