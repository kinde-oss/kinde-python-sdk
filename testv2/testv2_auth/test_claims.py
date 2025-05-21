import pytest
from unittest.mock import Mock, patch
from kinde_sdk.auth import OAuth
from kinde_sdk.auth import claims

@pytest.fixture
def mock_oauth():
    with patch('kinde_sdk.auth.claims.OAuth.get_instance') as mock:
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
        "aud": ["api.yourapp.com"],
        "given_name": "John",
        "family_name": "Doe",
        "email": "john.doe@example.com",
        "org_code": "org_123"
    }
    return token_manager

class TestClaims:
    @pytest.mark.asyncio
    async def test_get_claim_when_authenticated(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await claims.get_claim("aud")
        
        assert result["name"] == "aud"
        assert result["value"] == ["api.yourapp.com"]

    @pytest.mark.asyncio
    async def test_get_claim_when_not_authenticated(self, mock_oauth):
        mock_oauth.is_authenticated.return_value = False
        
        result = await claims.get_claim("aud")
        
        assert result["name"] == "aud"
        assert result["value"] == ["api.yourapp.com"]

    @pytest.mark.asyncio
    async def test_get_claim_when_token_manager_not_available(self, mock_oauth):
        mock_oauth._session_manager.get_token_manager.return_value = None
        
        result = await claims.get_claim("aud")
        
        assert result["name"] == "aud"
        assert result["value"] == ["api.yourapp.com"]

    @pytest.mark.asyncio
    async def test_get_claim_when_claim_not_found(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await claims.get_claim("non_existent_claim")
        
        assert result["name"] == "non_existent_claim"
        assert result["value"] is None

    @pytest.mark.asyncio
    async def test_get_claim_with_id_token(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await claims.get_claim("given_name", token_type="id_token")
        
        assert result["name"] == "given_name"
        assert result["value"] == "John"

    @pytest.mark.asyncio
    async def test_get_all_claims_when_authenticated(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await claims.get_all_claims()
        
        assert result["aud"] == ["api.yourapp.com"]
        assert result["given_name"] == "John"
        assert result["family_name"] == "Doe"
        assert result["email"] == "john.doe@example.com"
        assert result["org_code"] == "org_123"

    @pytest.mark.asyncio
    async def test_get_all_claims_when_not_authenticated(self, mock_oauth):
        mock_oauth.is_authenticated.return_value = False
        
        result = await claims.get_all_claims()
        
        assert result["aud"] == ["api.yourapp.com"]
        assert result["given_name"] == "John"
        assert result["family_name"] == "Doe"
        assert result["email"] == "john.doe@example.com"
        assert result["org_code"] == "org_123"

    @pytest.mark.asyncio
    async def test_get_all_claims_when_token_manager_not_available(self, mock_oauth):
        mock_oauth._session_manager.get_token_manager.return_value = None
        
        result = await claims.get_all_claims()
        
        assert result["aud"] == ["api.yourapp.com"]
        assert result["given_name"] == "John"
        assert result["family_name"] == "Doe"
        assert result["email"] == "john.doe@example.com"
        assert result["org_code"] == "org_123"

    @pytest.mark.asyncio
    async def test_get_all_claims_with_id_token(self, mock_oauth, mock_token_manager):
        mock_oauth._session_manager.get_token_manager.return_value = mock_token_manager
        
        result = await claims.get_all_claims(token_type="id_token")
        
        assert result["given_name"] == "John"
        assert result["family_name"] == "Doe"
        assert result["email"] == "john.doe@example.com" 