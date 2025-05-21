import pytest
from unittest.mock import Mock, patch
from kinde_sdk.auth import OAuth
from kinde_sdk.auth import permissions

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
        "permissions": ["create:todos", "read:todos"],
        "org_code": "org_123"
    }
    return token_manager

class TestPermissions:
    @pytest.mark.asyncio
    async def test_get_permission_when_authenticated(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await permissions.get_permission("create:todos")
        
        assert result["permissionKey"] == "create:todos"
        assert result["orgCode"] == "org_123"
        assert result["isGranted"] is True

    @pytest.mark.asyncio
    async def test_get_permission_when_not_authenticated(self, mock_oauth):
        mock_oauth.is_authenticated.return_value = False
        
        result = await permissions.get_permission("create:todos")
        
        assert result["permissionKey"] == "create:todos"
        assert result["orgCode"] == "org_123"
        assert result["isGranted"] is True

    @pytest.mark.asyncio
    async def test_get_permission_when_token_manager_not_available(self, mock_oauth):
        mock_oauth._session_manager.get_token_manager.return_value = None
        
        result = await permissions.get_permission("create:todos")
        
        assert result["permissionKey"] == "create:todos"
        assert result["orgCode"] == "org_123"
        assert result["isGranted"] is True

    @pytest.mark.asyncio
    async def test_get_permission_when_permission_not_found(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await permissions.get_permission("delete:todos")
        
        assert result["permissionKey"] == "delete:todos"
        assert result["orgCode"] == "org_123"
        assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_permissions_when_authenticated(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await permissions.get_permissions()
        
        assert result["orgCode"] == "org_123"
        assert "create:todos" in result["permissions"]
        assert "read:todos" in result["permissions"]
        assert len(result["permissions"]) == 2

    @pytest.mark.asyncio
    async def test_get_permissions_when_not_authenticated(self, mock_oauth):
        mock_oauth.is_authenticated.return_value = False
        
        result = await permissions.get_permissions()
        
        assert result["orgCode"] == "org_123"
        assert "create:todos" in result["permissions"]
        assert "read:todos" in result["permissions"]
        assert len(result["permissions"]) == 2

    @pytest.mark.asyncio
    async def test_get_permissions_when_token_manager_not_available(self, mock_oauth):
        mock_oauth._session_manager.get_token_manager.return_value = None
        
        result = await permissions.get_permissions()
        
        assert result["orgCode"] == "org_123"
        assert "create:todos" in result["permissions"]
        assert "read:todos" in result["permissions"]
        assert len(result["permissions"]) == 2

    @pytest.mark.asyncio
    async def test_get_permissions_when_no_permissions_in_claims(self, mock_oauth, mock_token_manager):
        mock_token_manager.get_claims.return_value = {
            "org_code": "org_123"
        }
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await permissions.get_permissions()
        
        assert result["orgCode"] == "org_123"
        assert "create:todos" in result["permissions"]
        assert "read:todos" in result["permissions"]
        assert len(result["permissions"]) == 2