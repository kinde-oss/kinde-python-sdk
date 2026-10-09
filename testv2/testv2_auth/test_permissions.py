import pytest
from unittest.mock import Mock, patch, AsyncMock
from kinde_sdk.auth.api_options import ApiOptions
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.auth import permissions

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
        "permissions": ["create:todos", "read:todos"],
        "org_code": "org_123"
    }
    token_manager.get_force_api.return_value = False
    return token_manager

@pytest.fixture
def mock_session_manager(mock_token_manager):
    session_manager = Mock(spec=UserSession)
    session_manager.get_token_manager.return_value = mock_token_manager
    return session_manager

class TestPermissions:
    @pytest.mark.asyncio
    async def test_get_permission_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(permissions, '_session_manager', mock_session_manager):
            result = await permissions.get_permission("create:todos")
            
            assert result["permissionKey"] == "create:todos"
            assert result["orgCode"] == "org_123"
            assert result["isGranted"] is True

    @pytest.mark.asyncio
    async def test_get_permission_when_not_authenticated(self, mock_framework_factory):
        mock_framework_factory.return_value = None
        
        result = await permissions.get_permission("create:todos")
        
        assert result["permissionKey"] == "create:todos"
        assert result["orgCode"] is None
        assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_permission_when_token_manager_not_available(self, mock_framework_factory, mock_session_manager):
        mock_session_manager.get_token_manager.return_value = None
        
        with patch.object(permissions, '_session_manager', mock_session_manager):
            result = await permissions.get_permission("create:todos")
            
            assert result["permissionKey"] == "create:todos"
            assert result["orgCode"] is None
            assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_permission_when_permission_not_found(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(permissions, '_session_manager', mock_session_manager):
            result = await permissions.get_permission("delete:todos")
            
            assert result["permissionKey"] == "delete:todos"
            assert result["orgCode"] == "org_123"
            assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_permissions_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(permissions, '_session_manager', mock_session_manager):
            result = await permissions.get_permissions()
            
            assert result["orgCode"] == "org_123"
            assert "create:todos" in result["permissions"]
            assert "read:todos" in result["permissions"]
            assert len(result["permissions"]) == 2

    @pytest.mark.asyncio
    async def test_get_permissions_when_not_authenticated(self, mock_framework_factory):
        mock_framework_factory.return_value = None
        
        result = await permissions.get_permissions()
        
        assert result["orgCode"] is None
        assert result["permissions"] == []

    @pytest.mark.asyncio
    async def test_get_permissions_when_token_manager_not_available(self, mock_framework_factory, mock_session_manager):
        mock_session_manager.get_token_manager.return_value = None
        
        with patch.object(permissions, '_session_manager', mock_session_manager):
            result = await permissions.get_permissions()
            
            assert result["orgCode"] is None
            assert result["permissions"] == []

    @pytest.mark.asyncio
    async def test_get_permissions_when_no_permissions_in_claims(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        mock_token_manager.get_claims.return_value = {
            "org_code": "org_123"
        }
        
        with patch.object(permissions, '_session_manager', mock_session_manager):
            result = await permissions.get_permissions()
            
            assert result["orgCode"] == "org_123"
            assert result["permissions"] == []

    @pytest.mark.asyncio
    async def test_get_permission_force_api_true_granted(self):
        mock_result = {
            "permissionKey": "create:todos",
            "orgCode": "org_123",
            "isGranted": True
        }
        with patch.object(permissions, "_call_account_api", new_callable=AsyncMock, return_value=mock_result):
            options = ApiOptions(force_api=True)
            result = await permissions.get_permission("create:todos", options)
            assert result["permissionKey"] == "create:todos"
            assert result["orgCode"] == "org_123"
            assert result["isGranted"] is True

    @pytest.mark.asyncio
    async def test_get_permission_force_api_true_not_granted(self):
        mock_result = {
            "permissionKey": "create:todos",
            "orgCode": "org_456",
            "isGranted": False
        }
        with patch.object(permissions, "_call_account_api", new_callable=AsyncMock, return_value=mock_result):
            options = ApiOptions(force_api=True)
            result = await permissions.get_permission("create:todos", options)
            assert result["permissionKey"] == "create:todos"
            assert result["orgCode"] == "org_456"
            assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_permission_force_api_true_no_permissions(self):
        mock_result = {
            "permissionKey": "create:todos",
            "orgCode": "org_789",
            "isGranted": False
        }
        with patch.object(permissions, "_call_account_api", new_callable=AsyncMock, return_value=mock_result):
            options = ApiOptions(force_api=True)
            result = await permissions.get_permission("create:todos", options)
            assert result["permissionKey"] == "create:todos"
            assert result["orgCode"] == "org_789"
            assert result["isGranted"] is False      
            
    @pytest.mark.asyncio
    async def test_get_permission_force_api_false_granted(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        options = ApiOptions(force_api=False)
        with patch.object(permissions, '_session_manager', mock_session_manager):
            result = await permissions.get_permission("create:todos", options)
            assert result["permissionKey"] == "create:todos"
            assert result["orgCode"] == "org_123"
            assert result["isGranted"] is True

    @pytest.mark.asyncio
    async def test_get_permission_force_api_false_not_granted(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        options = ApiOptions(force_api=False)
        with patch.object(permissions, '_session_manager', mock_session_manager):
            result = await permissions.get_permission("delete:todos", options)
            assert result["permissionKey"] == "delete:todos"
            assert result["orgCode"] == "org_123"
            assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_permission_force_api_false_no_permissions(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        mock_token_manager.get_claims.return_value = {
            "org_code": "org_123"
        }
        options = ApiOptions(force_api=False)
        with patch.object(permissions, '_session_manager', mock_session_manager):
            result = await permissions.get_permission("create:todos", options)
            assert result["permissionKey"] == "create:todos"
            assert result["orgCode"] == "org_123"
            assert result["isGranted"] is False


class TestPermissionsAccountApiResponse:
    """_call_account_api against the real generated response models."""

    @staticmethod
    def _api_returning(*keys):
        from kinde_sdk.frontend.models import (
            GetUserPermissionsResponse,
            GetUserPermissionsResponseData,
            GetUserPermissionsResponseDataPermissionsInner,
        )
        response = GetUserPermissionsResponse(
            data=GetUserPermissionsResponseData(
                org_code="org_123",
                permissions=[
                    GetUserPermissionsResponseDataPermissionsInner(id=f"perm_{i}", name=key.title(), key=key)
                    for i, key in enumerate(keys)
                ],
            )
        )
        api = Mock()
        api.get_user_permissions.return_value = response
        return api

    @pytest.mark.asyncio
    async def test_granted_permission_is_found_by_key(self):
        api = self._api_returning("create:todos", "read:todos")
        with patch.object(permissions, "_create_authenticated_api_client", return_value=api):
            result = await permissions._call_account_api("create:todos")
        assert result == {"permissionKey": "create:todos", "orgCode": "org_123", "isGranted": True}

    @pytest.mark.asyncio
    async def test_missing_permission_is_not_granted(self):
        api = self._api_returning("read:todos")
        with patch.object(permissions, "_create_authenticated_api_client", return_value=api):
            result = await permissions._call_account_api("delete:todos")
        assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_all_permissions_are_returned_as_keys(self):
        api = self._api_returning("create:todos", "read:todos")
        with patch.object(permissions, "_create_authenticated_api_client", return_value=api):
            result = await permissions._call_account_api()
        assert result == {"orgCode": "org_123", "permissions": ["create:todos", "read:todos"]}

class TestPermissionKey:
    """Account API permissions can be model objects, dicts or plain key strings."""

    @pytest.mark.parametrize("permission, expected", [
        ("read:todos", "read:todos"),
        ({"id": "perm_1", "key": "read:todos"}, "read:todos"),
        (Mock(key="read:todos"), "read:todos"),
        ({"id": "perm_1"}, None),
        (None, None),
    ])
    def test_permission_key(self, permission, expected):
        assert permissions._permission_key(permission) == expected
