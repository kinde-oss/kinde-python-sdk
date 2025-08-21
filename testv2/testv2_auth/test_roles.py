import pytest
from unittest.mock import Mock, patch
from kinde_sdk.auth.api_options import ApiOptions
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.auth import roles

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
        "roles": [
            {
                "id": "role_1",
                "key": "admin",
                "name": "Administrator",
                "description": "Full system access",
                "is_default_role": False
            },
            {
                "id": "role_2", 
                "key": "user",
                "name": "User",
                "description": "Standard user access",
                "is_default_role": True
            }
        ],
        "org_code": "org_123"
    }
    return token_manager

@pytest.fixture
def mock_session_manager(mock_token_manager):
    session_manager = Mock(spec=UserSession)
    session_manager.get_token_manager.return_value = mock_token_manager
    return session_manager

class TestRoles:
    @pytest.mark.asyncio
    async def test_get_role_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(roles, '_session_manager', mock_session_manager):
            result = await roles.get_role("admin")
            
            assert result["id"] == "role_1"
            assert result["key"] == "admin"
            assert result["name"] == "Administrator"
            assert result["description"] == "Full system access"
            assert result["is_default_role"] is False
            assert result["isGranted"] is True

    @pytest.mark.asyncio
    async def test_get_role_when_not_authenticated(self, mock_framework_factory):
        mock_framework_factory.return_value = None
        
        result = await roles.get_role("admin")
        
        assert result["id"] is None
        assert result["key"] == "admin"
        assert result["name"] is None
        assert result["description"] is None
        assert result["is_default_role"] is False
        assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_role_when_token_manager_not_available(self, mock_framework_factory, mock_session_manager):
        mock_session_manager.get_token_manager.return_value = None
        
        with patch.object(roles, '_session_manager', mock_session_manager):
            result = await roles.get_role("admin")
            
            assert result["id"] is None
            assert result["key"] == "admin"
            assert result["name"] is None
            assert result["description"] is None
            assert result["is_default_role"] is False
            assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_role_when_role_not_found(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(roles, '_session_manager', mock_session_manager):
            result = await roles.get_role("super_admin")
            
            assert result["id"] is None
            assert result["key"] == "super_admin"
            assert result["name"] is None
            assert result["description"] is None
            assert result["is_default_role"] is False
            assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_roles_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch.object(roles, '_session_manager', mock_session_manager):
            result = await roles.get_roles()
            
            assert result["orgCode"] == "org_123"
            assert len(result["roles"]) == 2
            
            # Check admin role
            admin_role = next((role for role in result["roles"] if role.get('key') == 'admin'), None)
            assert admin_role is not None
            assert admin_role['id'] == "role_1"
            assert admin_role['name'] == "Administrator"
            assert admin_role['description'] == "Full system access"
            assert admin_role['is_default_role'] is False
            
            # Check user role
            user_role = next((role for role in result["roles"] if role.get('key') == 'user'), None)
            assert user_role is not None
            assert user_role['id'] == "role_2"
            assert user_role['name'] == "User"
            assert user_role['description'] == "Standard user access"
            assert user_role['is_default_role'] is True

    @pytest.mark.asyncio
    async def test_get_roles_when_not_authenticated(self, mock_framework_factory):
        mock_framework_factory.return_value = None
        
        result = await roles.get_roles()
        
        assert result["orgCode"] is None
        assert result["roles"] == []

    @pytest.mark.asyncio
    async def test_get_roles_when_token_manager_not_available(self, mock_framework_factory, mock_session_manager):
        mock_session_manager.get_token_manager.return_value = None
        
        with patch.object(roles, '_session_manager', mock_session_manager):
            result = await roles.get_roles()
            
            assert result["orgCode"] is None
            assert result["roles"] == []

    @pytest.mark.asyncio
    async def test_get_roles_when_no_roles_in_claims(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        mock_token_manager.get_claims.return_value = {
            "org_code": "org_123"
        }
        
        with patch.object(roles, '_session_manager', mock_session_manager):
            result = await roles.get_roles()
            
            assert result["orgCode"] == "org_123"
            assert result["roles"] == []

    @pytest.mark.asyncio
    async def test_get_role_force_api_true_granted(self):
        mock_result = {
            "id": "role_1",
            "key": "admin",
            "name": "Administrator",
            "description": "Full system access",
            "is_default_role": False,
            "isGranted": True
        }
        with patch.object(roles, "_call_account_api", return_value=mock_result):
            options = ApiOptions(force_api=True)
            result = await roles.get_role("admin", options)
            assert result["id"] == "role_1"
            assert result["key"] == "admin"
            assert result["name"] == "Administrator"
            assert result["description"] == "Full system access"
            assert result["is_default_role"] is False
            assert result["isGranted"] is True

    @pytest.mark.asyncio
    async def test_get_role_force_api_true_not_granted(self):
        mock_result = {
            "id": None,
            "key": "super_admin",
            "name": None,
            "description": None,
            "is_default_role": False,
            "isGranted": False
        }
        with patch.object(roles, "_call_account_api", return_value=mock_result):
            options = ApiOptions(force_api=True)
            result = await roles.get_role("super_admin", options)
            assert result["id"] is None
            assert result["key"] == "super_admin"
            assert result["name"] is None
            assert result["description"] is None
            assert result["is_default_role"] is False
            assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_role_force_api_true_no_roles(self):
        mock_result = {
            "id": None,
            "key": "admin",
            "name": None,
            "description": None,
            "is_default_role": False,
            "isGranted": False
        }
        with patch.object(roles, "_call_account_api", return_value=mock_result):
            options = ApiOptions(force_api=True)
            result = await roles.get_role("admin", options)
            assert result["id"] is None
            assert result["key"] == "admin"
            assert result["name"] is None
            assert result["description"] is None
            assert result["is_default_role"] is False
            assert result["isGranted"] is False      
            
    @pytest.mark.asyncio
    async def test_get_role_force_api_false_granted(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        options = ApiOptions(force_api=False)
        with patch.object(roles, '_session_manager', mock_session_manager):
            result = await roles.get_role("admin", options)
            assert result["id"] == "role_1"
            assert result["key"] == "admin"
            assert result["name"] == "Administrator"
            assert result["description"] == "Full system access"
            assert result["is_default_role"] is False
            assert result["isGranted"] is True

    @pytest.mark.asyncio
    async def test_get_role_force_api_false_not_granted(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        options = ApiOptions(force_api=False)
        with patch.object(roles, '_session_manager', mock_session_manager):
            result = await roles.get_role("super_admin", options)
            assert result["id"] is None
            assert result["key"] == "super_admin"
            assert result["name"] is None
            assert result["description"] is None
            assert result["is_default_role"] is False
            assert result["isGranted"] is False

    @pytest.mark.asyncio
    async def test_get_role_force_api_false_no_roles(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        mock_token_manager.get_claims.return_value = {
            "org_code": "org_123"
        }
        options = ApiOptions(force_api=False)
        with patch.object(roles, '_session_manager', mock_session_manager):
            result = await roles.get_role("admin", options)
            assert result["id"] is None
            assert result["key"] == "admin"
            assert result["name"] is None
            assert result["description"] is None
            assert result["is_default_role"] is False
            assert result["isGranted"] is False
