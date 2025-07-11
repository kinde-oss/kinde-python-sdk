import pytest
from unittest.mock import Mock, patch
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.auth.feature_flags import FeatureFlag
from kinde_sdk.auth import feature_flags

@pytest.fixture
def mock_framework():
    framework = Mock()
    framework.get_user_id.return_value = "test_user_id"
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
        "feature_flags": {
            "theme": {
                "t": "s",
                "v": "pink"
            },
            "is_dark_mode": {
                "t": "b",
                "v": True
            },
            "competitions_limit": {
                "t": "i",
                "v": 5
            }
        }
    }
    return token_manager

@pytest.fixture
def mock_session_manager(mock_token_manager):
    session_manager = Mock(spec=UserSession)
    session_manager.get_token_manager.return_value = mock_token_manager
    return session_manager

class TestFeatureFlags:
    @pytest.mark.asyncio
    async def test_get_flag_string_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(feature_flags, '_session_manager', mock_session_manager):
            result = await feature_flags.get_flag("theme")
            
            assert isinstance(result, FeatureFlag)
            assert result.type == "string"
            assert result.value == "pink"
            assert result.is_default is False

    @pytest.mark.asyncio
    async def test_get_flag_boolean_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(feature_flags, '_session_manager', mock_session_manager):
            result = await feature_flags.get_flag("is_dark_mode")
            
            assert isinstance(result, FeatureFlag)
            assert result.type == "boolean"
            assert result.value is True
            assert result.is_default is False

    @pytest.mark.asyncio
    async def test_get_flag_integer_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(feature_flags, '_session_manager', mock_session_manager):
            result = await feature_flags.get_flag("competitions_limit")
            
            assert isinstance(result, FeatureFlag)
            assert result.type == "integer"
            assert result.value == 5
            assert result.is_default is False

    @pytest.mark.asyncio
    async def test_get_flag_when_not_authenticated(self, mock_framework_factory):
        mock_framework_factory.return_value = None
        
        result = await feature_flags.get_flag("theme", default_value="light")
        
        assert isinstance(result, FeatureFlag)
        assert result.type == "unknown"
        assert result.value == "light"
        assert result.is_default is True

    @pytest.mark.asyncio
    async def test_get_flag_when_token_manager_not_available(self, mock_framework_factory, mock_session_manager):
        mock_session_manager.get_token_manager.return_value = None
        
        with patch.object(feature_flags, '_session_manager', mock_session_manager):
            result = await feature_flags.get_flag("theme", default_value="light")
            
            assert isinstance(result, FeatureFlag)
            assert result.type == "unknown"
            assert result.value == "light"
            assert result.is_default is True

    @pytest.mark.asyncio
    async def test_get_flag_when_flag_not_found(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(feature_flags, '_session_manager', mock_session_manager):
            result = await feature_flags.get_flag("non_existent_flag", default_value=False)
            
            assert isinstance(result, FeatureFlag)
            assert result.type == "unknown"
            assert result.value is False
            assert result.is_default is True

    @pytest.mark.asyncio
    async def test_get_all_flags_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(feature_flags, '_session_manager', mock_session_manager):
            result = await feature_flags.get_all_flags()
            
            assert isinstance(result, dict)
            assert len(result) == 3
            
            theme_flag = result["theme"]
            assert isinstance(theme_flag, FeatureFlag)
            assert theme_flag.type == "string"
            assert theme_flag.value == "pink"
            
            dark_mode_flag = result["is_dark_mode"]
            assert isinstance(dark_mode_flag, FeatureFlag)
            assert dark_mode_flag.type == "boolean"
            assert dark_mode_flag.value is True
            
            limit_flag = result["competitions_limit"]
            assert isinstance(limit_flag, FeatureFlag)
            assert limit_flag.type == "integer"
            assert limit_flag.value == 5

    @pytest.mark.asyncio
    async def test_get_all_flags_when_not_authenticated(self, mock_framework_factory):
        mock_framework_factory.return_value = None
        
        result = await feature_flags.get_all_flags()
        
        assert isinstance(result, dict)
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_all_flags_when_token_manager_not_available(self, mock_framework_factory, mock_session_manager):
        mock_session_manager.get_token_manager.return_value = None
        
        with patch.object(feature_flags, '_session_manager', mock_session_manager):
            result = await feature_flags.get_all_flags()
            
            assert isinstance(result, dict)
            assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_all_flags_when_no_feature_flags_in_claims(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        mock_token_manager.get_claims.return_value = {}
        
        with patch.object(feature_flags, '_session_manager', mock_session_manager):
            result = await feature_flags.get_all_flags()
            
            assert isinstance(result, dict)
            assert len(result) == 0 