import pytest
from unittest.mock import Mock, patch
from kinde_sdk.auth import OAuth
from kinde_sdk.auth.feature_flags import FeatureFlag
from kinde_sdk.auth import feature_flags

@pytest.fixture
def mock_oauth():
    with patch('kinde_sdk.auth.oauth.OAuth.get_instance') as mock:
        oauth = Mock(spec=OAuth)
        oauth.is_authenticated.return_value = True
        oauth._framework = Mock()
        oauth._framework.get_user_id.return_value = "test_user_id"
        oauth._session_manager = Mock()
        mock.return_value = oauth
        yield oauth

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

class TestFeatureFlags:
    @pytest.mark.asyncio
    async def test_get_flag_string_when_authenticated(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await feature_flags.get_flag("theme")
        
        assert isinstance(result, FeatureFlag)
        #assert result.code == "theme"
        assert result.type == "string"
        assert result.value == "pink"
        assert result.is_default is False

    @pytest.mark.asyncio
    async def test_get_flag_boolean_when_authenticated(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await feature_flags.get_flag("is_dark_mode")
        
        assert isinstance(result, FeatureFlag)
        #assert result.code == "is_dark_mode"
        assert result.type == "boolean"
        assert result.value is True
        assert result.is_default is False

    @pytest.mark.asyncio
    async def test_get_flag_integer_when_authenticated(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await feature_flags.get_flag("competitions_limit")
        
        assert isinstance(result, FeatureFlag)
        #assert result.code == "competitions_limit"
        assert result.type == "integer"
        assert result.value == 5
        assert result.is_default is False

    @pytest.mark.asyncio
    async def test_get_flag_when_not_authenticated(self, mock_oauth):
        mock_oauth.is_authenticated.return_value = False
        
        result = await feature_flags.get_flag("theme", default_value="light")
        
        assert isinstance(result, FeatureFlag)
        #assert result.code == "theme"
        assert result.type == "string"
        assert result.value == "pink"
        assert result.is_default is False

    @pytest.mark.asyncio
    async def test_get_flag_when_token_manager_not_available(self, mock_oauth):
        mock_oauth._session_manager.get_token_manager.return_value = None
        
        result = await feature_flags.get_flag("theme", default_value="light")
        
        assert isinstance(result, FeatureFlag)
        #assert result.code == "theme"
        assert result.type == "string"
        assert result.value == "pink"
        assert result.is_default is False

    @pytest.mark.asyncio
    async def test_get_flag_when_flag_not_found(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await feature_flags.get_flag("non_existent_flag", default_value=False)
        
        assert isinstance(result, FeatureFlag)
        #assert result.code == "non_existent_flag"
        assert result.type == "unknown"
        assert result.value is False
        assert result.is_default is True

    @pytest.mark.asyncio
    async def test_get_all_flags_when_authenticated(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await feature_flags.get_all_flags()
        
        assert isinstance(result, dict)
        assert len(result) == 3
        
        theme_flag = result["theme"]
        assert isinstance(theme_flag, FeatureFlag)
        #assert theme_flag.code == "theme"
        assert theme_flag.type == "string"
        assert theme_flag.value == "pink"
        
        dark_mode_flag = result["is_dark_mode"]
        assert isinstance(dark_mode_flag, FeatureFlag)
        #assert dark_mode_flag.code == "is_dark_mode"
        assert dark_mode_flag.type == "boolean"
        assert dark_mode_flag.value is True
        
        limit_flag = result["competitions_limit"]
        assert isinstance(limit_flag, FeatureFlag)
        #assert limit_flag.code == "competitions_limit"
        assert limit_flag.type == "integer"
        assert limit_flag.value == 5

    @pytest.mark.asyncio
    async def test_get_all_flags_when_not_authenticated(self, mock_oauth):
        mock_oauth.is_authenticated.return_value = False
        
        result = await feature_flags.get_all_flags()
        
        assert isinstance(result, dict)
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_get_all_flags_when_token_manager_not_available(self, mock_oauth):
        mock_oauth._session_manager.get_token_manager.return_value = None
        
        result = await feature_flags.get_all_flags()
        
        assert isinstance(result, dict)
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_get_all_flags_when_no_feature_flags_in_claims(self, mock_oauth, mock_token_manager):
        mock_token_manager.get_claims.return_value = {}
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await feature_flags.get_all_flags()
        
        assert isinstance(result, dict)
        assert len(result) == 3 