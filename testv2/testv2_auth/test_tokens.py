import pytest
from unittest.mock import Mock, patch
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.auth.tokens import tokens

@pytest.fixture
def mock_framework():
    framework = Mock()
    framework.get_user_id.return_value = "user_123"
    return framework

@pytest.fixture
def mock_framework_factory(mock_framework):
    with patch('kinde_sdk.core.framework.framework_factory.FrameworkFactory.get_framework_instance') as mock:
        mock.return_value = mock_framework
        yield mock

@pytest.fixture
def mock_token_manager():
    token_manager = Mock()
    token_manager.get_claims.return_value = {
        "aud": ["api.yourapp.com"],
        "given_name": "John",
        "family_name": "Doe",
        "email": "john.doe@example.com",
        "org_code": "org_123"
    }
    return token_manager

@pytest.fixture
def mock_session_manager(mock_token_manager):
    session_manager = Mock(spec=UserSession)
    session_manager.get_token_manager.return_value = mock_token_manager
    return session_manager

class TestTokens:
    @pytest.mark.asyncio
    async def test_get_token_manager_when_available(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        """Test get_token_manager when token manager is available"""
        with patch.object(tokens, '_session_manager', mock_session_manager):
            result = tokens.get_token_manager()
            
            assert result == mock_token_manager

    @pytest.mark.asyncio
    async def test_get_token_manager_when_not_available(self, mock_framework_factory, mock_session_manager):
        """Test get_token_manager when token manager is not available"""
        mock_session_manager.get_token_manager.return_value = None
        
        with patch.object(tokens, '_session_manager', mock_session_manager):
            result = tokens.get_token_manager()
            
            assert result is None

    @pytest.mark.asyncio
    async def test_get_user_id_when_available(self, mock_framework_factory):
        """Test get_user_id when user ID is available"""
        mock_framework = Mock()
        mock_framework.get_user_id.return_value = "user_123"
        mock_framework_factory.return_value = mock_framework
        
        result = tokens.get_user_id()
        
        assert result == "user_123"

    @pytest.mark.asyncio
    async def test_get_user_id_when_not_available(self, mock_framework_factory):
        """Test get_user_id when user ID is not available"""
        tokens._framework = None  # Reset singleton cache
        mock_framework_factory.return_value = None
        
        result = tokens.get_user_id()
        
        assert result is None

    @pytest.mark.asyncio
    async def test_is_authenticated_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        """Test is_authenticated when user is authenticated"""
        with patch.object(tokens, '_session_manager', mock_session_manager):
            result = tokens.is_authenticated()
            
            assert result is True

    @pytest.mark.asyncio
    async def test_is_authenticated_when_not_authenticated(self, mock_framework_factory, mock_session_manager):
        """Test is_authenticated when user is not authenticated"""
        mock_session_manager.get_token_manager.return_value = None
        
        with patch.object(tokens, '_session_manager', mock_session_manager):
            result = tokens.is_authenticated()
            
            assert result is False

    @pytest.mark.asyncio
    async def test_get_token_info_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        """Test get_token_info when user is authenticated with tokens"""
        mock_token_manager.tokens = {
            "access_token": "access_token_value",
            "id_token": "id_token_value",
            "refresh_token": "refresh_token_value"
        }
        
        with patch.object(tokens, '_session_manager', mock_session_manager):
            result = tokens.get_token_info()
            
            assert result["isAuthenticated"] is True
            assert result["userId"] == "user_123"
            assert result["hasAccessToken"] is True
            assert result["hasIdToken"] is True
            assert result["hasRefreshToken"] is True

    @pytest.mark.asyncio
    async def test_get_token_info_when_not_authenticated(self, mock_framework_factory):
        """Test get_token_info when user is not authenticated"""
        mock_framework_factory.return_value = None
        
        result = tokens.get_token_info()
        
        assert result["isAuthenticated"] is False
        assert result["userId"] is None
        assert result["hasAccessToken"] is False
        assert result["hasIdToken"] is False
        assert result["hasRefreshToken"] is False

    @pytest.mark.asyncio
    async def test_get_token_info_partial_tokens(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        """Test get_token_info with only some tokens available"""
        mock_token_manager.tokens = {
            "access_token": "access_token_value"
        }
        
        with patch.object(tokens, '_session_manager', mock_session_manager):
            result = tokens.get_token_info()
            
            assert result["isAuthenticated"] is True
            assert result["userId"] == "user_123"
            assert result["hasAccessToken"] is True
            assert result["hasIdToken"] is False
            assert result["hasRefreshToken"] is False 