import pytest
from unittest.mock import Mock, patch
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.auth import claims

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

class TestClaims:
    @pytest.mark.asyncio
    async def test_get_claim_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch('kinde_sdk.auth.claims.claims._session_manager', mock_session_manager):
            result = await claims.get_claim("aud")
            
            assert result["name"] == "aud"
            assert result["value"] == ["api.yourapp.com"]

    @pytest.mark.asyncio
    async def test_get_claim_when_not_authenticated(self, mock_framework_factory):
        mock_framework_factory.return_value = None
        
        result = await claims.get_claim("aud")
        
        assert result["name"] == "aud"
        assert result["value"] is None

    @pytest.mark.asyncio
    async def test_get_claim_when_token_manager_not_available(self, mock_framework_factory, mock_session_manager):
        mock_session_manager.get_token_manager.return_value = None
        
        with patch('kinde_sdk.auth.claims.claims._session_manager', mock_session_manager):
            result = await claims.get_claim("aud")
            
            assert result["name"] == "aud"
            assert result["value"] is None

    @pytest.mark.asyncio
    async def test_get_claim_when_claim_not_found(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch('kinde_sdk.auth.claims.claims._session_manager', mock_session_manager):
            result = await claims.get_claim("non_existent_claim")
            
            assert result["name"] == "non_existent_claim"
            assert result["value"] is None

    @pytest.mark.asyncio
    async def test_get_claim_with_id_token(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch('kinde_sdk.auth.claims.claims._session_manager', mock_session_manager):
            result = await claims.get_claim("given_name", token_type="id_token")
            
            assert result["name"] == "given_name"
            assert result["value"] == "John"

    @pytest.mark.asyncio
    async def test_get_all_claims_when_authenticated(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch('kinde_sdk.auth.claims.claims._session_manager', mock_session_manager):
            result = await claims.get_all_claims()
            
            assert result["aud"] == ["api.yourapp.com"]
            assert result["given_name"] == "John"
            assert result["family_name"] == "Doe"
            assert result["email"] == "john.doe@example.com"
            assert result["org_code"] == "org_123"

    @pytest.mark.asyncio
    async def test_get_all_claims_when_not_authenticated(self, mock_framework_factory):
        mock_framework_factory.return_value = None
        
        result = await claims.get_all_claims()
        
        assert result == {}

    @pytest.mark.asyncio
    async def test_get_all_claims_when_token_manager_not_available(self, mock_framework_factory, mock_session_manager):
        mock_session_manager.get_token_manager.return_value = None
        
        with patch('kinde_sdk.auth.claims.claims._session_manager', mock_session_manager):
            result = await claims.get_all_claims()
            
            assert result == {}

    @pytest.mark.asyncio
    async def test_get_all_claims_with_id_token(self, mock_framework_factory, mock_session_manager, mock_token_manager):
        with patch('kinde_sdk.auth.claims.claims._session_manager', mock_session_manager):
            result = await claims.get_all_claims(token_type="id_token")
            
            assert result["given_name"] == "John"
            assert result["family_name"] == "Doe"
            assert result["email"] == "john.doe@example.com" 