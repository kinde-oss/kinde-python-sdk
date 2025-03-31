import unittest
from unittest.mock import patch, MagicMock, Mock
import json
import base64
import time
import hashlib
import requests
import asyncio
from requests.exceptions import RequestException

# Import the functions to test
from kinde_sdk.core.helpers import (
    generate_random_string,
    base64_url_encode,
    generate_pkce_pair,
    get_user_details,
    decode_jwt,
    is_authenticated,
    get_user_organizations,
    get_organization_details,
    get_organization_users,
    get_user_permissions,
    has_permission,
    get_user_roles,
    has_role,
    get_flag_value,
    get_claim_value,
    is_claim_valid,
    generate_state,
    hash_string,
    get_current_timestamp,
    parse_domain,
    format_api_url,
    is_token_expired,
    sanitize_url
)


class TestHelpers(unittest.TestCase):
    
    def test_generate_random_string(self):
        """Test that generate_random_string produces strings of correct length."""
        # Test default length
        result = generate_random_string()
        # The actual length might be different due to base64 encoding
        # The function uses secrets.token_urlsafe which doesn't guarantee exact length
        self.assertTrue(len(result) >= 32)  # Check it's at least the minimum length
        
        # Test custom length
        custom_length = 64
        result = generate_random_string(custom_length)
        self.assertTrue(len(result) >= 64)  # Check it's at least the minimum length
        
        # Test randomness (two calls should produce different results)
        result1 = generate_random_string()
        result2 = generate_random_string()
        self.assertNotEqual(result1, result2)
    
    def test_base64_url_encode(self):
        """Test base64_url_encode with both string and bytes input."""
        # Test with string input
        test_str = "test string"
        expected = base64.urlsafe_b64encode(test_str.encode('utf-8')).decode('utf-8').replace('=', '')
        result = base64_url_encode(test_str)
        self.assertEqual(result, expected)
        
        # Test with bytes input
        test_bytes = b"test bytes"
        expected = base64.urlsafe_b64encode(test_bytes).decode('utf-8').replace('=', '')
        result = base64_url_encode(test_bytes)
        self.assertEqual(result, expected)

    @patch('kinde_sdk.core.helpers.generate_random_string')
    @patch('kinde_sdk.core.helpers.hashlib.sha256')
    def test_generate_pkce_pair(self, mock_sha256, mock_random_string):
        """Test generate_pkce_pair generates valid verifier and challenge."""
        # Mock the random string and hash
        mock_random_string.return_value = "test_verifier"
        mock_digest = MagicMock()
        mock_digest.digest.return_value = b"hashed_value"
        mock_sha256.return_value = mock_digest
        
        # Call the function (and handle the coroutine)
        result = asyncio.run(generate_pkce_pair(52))
        
        # Check the result
        self.assertEqual(result["code_verifier"], "test_verifier")
        self.assertEqual(
            result["code_challenge"], 
            base64_url_encode(b"hashed_value")
        )
        
        # Verify the mocks were called correctly
        mock_random_string.assert_called_once_with(52)
        mock_sha256.assert_called_once_with(b"test_verifier")
    
    @patch('kinde_sdk.core.helpers.requests.get')
    def test_get_user_details(self, mock_get):
        """Test get_user_details with valid token."""
        # Mock dependencies
        userinfo_url = "https://test.kinde.com/api/v1/user"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "user1", "name": "Test User"}
        mock_get.return_value = mock_response
        
        # Call the function (and handle the coroutine)
        result = asyncio.run(get_user_details(userinfo_url, token_manager, logger))
        
        # Check the result
        self.assertEqual(result, {"id": "user1", "name": "Test User"})
        
        # Verify the mock was called correctly
        mock_get.assert_called_once_with(
            userinfo_url,
            headers={
                "Authorization": "Bearer test_access_token",
                "Accept": "application/json"
            }
        )
    
    def test_decode_jwt(self):
        """Test decode_jwt with a valid token."""
        # Create a mock JWT token
        # Header: {"alg": "HS256", "typ": "JWT"}
        # Payload: {"sub": "1234567890", "name": "John Doe", "iat": 1516239022}
        header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip('=')
        payload = base64.urlsafe_b64encode(json.dumps({"sub": "1234567890", "name": "John Doe", "iat": 1516239022}).encode()).decode().rstrip('=')
        signature = "signature"  # Doesn't matter for this test
        
        token = f"{header}.{payload}.{signature}"
        
        # Call the function
        result = decode_jwt(token)
        
        # Check the result
        self.assertEqual(result["sub"], "1234567890")
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["iat"], 1516239022)
    
    def test_is_authenticated(self):
        """Test is_authenticated with valid and invalid tokens."""
        # Mock token manager with valid token
        token_manager_valid = MagicMock()
        token_manager_valid.get_access_token.return_value = "valid_token"
        
        # Mock token manager with invalid token
        token_manager_invalid = MagicMock()
        token_manager_invalid.get_access_token.return_value = ""
        
        # Mock token manager that raises exception
        token_manager_error = MagicMock()
        token_manager_error.get_access_token.side_effect = Exception("Token error")
        
        # Test valid token
        self.assertTrue(is_authenticated(token_manager_valid))
        
        # Test invalid token
        self.assertFalse(is_authenticated(token_manager_invalid))
        
        # Test exception case
        self.assertFalse(is_authenticated(token_manager_error))
    
    @patch('kinde_sdk.core.helpers.requests.get')
    def test_get_user_organizations(self, mock_get):
        """Test get_user_organizations returns organization list."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "organizations": [
                {"id": "org1", "name": "Org 1"},
                {"id": "org2", "name": "Org 2"}
            ]
        }
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_user_organizations(api_url, token_manager, logger)
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "org1")
        self.assertEqual(result[1]["name"], "Org 2")
        
        # Verify the mock was called correctly
        mock_get.assert_called_once_with(
            f"{api_url}/user/organizations",
            headers={
                "Authorization": "Bearer test_access_token",
                "Accept": "application/json"
            }
        )
    
    @patch('kinde_sdk.core.helpers.requests.get')
    def test_get_organization_details(self, mock_get):
        """Test get_organization_details returns organization details."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        org_code = "org123"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "org123",
            "name": "Test Organization",
            "is_default": True
        }
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_organization_details(api_url, org_code, token_manager, logger)
        
        # Check the result
        self.assertEqual(result["id"], "org123")
        self.assertEqual(result["name"], "Test Organization")
        self.assertTrue(result["is_default"])
        
        # Verify the mock was called correctly
        mock_get.assert_called_once_with(
            f"{api_url}/organization/{org_code}",
            headers={
                "Authorization": "Bearer test_access_token",
                "Accept": "application/json"
            }
        )
    
    @patch('kinde_sdk.core.helpers.requests.get')
    def test_get_organization_users(self, mock_get):
        """Test get_organization_users returns users list."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        org_code = "org123"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "users": [
                {"id": "user1", "name": "User 1"},
                {"id": "user2", "name": "User 2"}
            ]
        }
        mock_get.return_value = mock_response
        
        # Call the function
        result = get_organization_users(api_url, org_code, token_manager, logger)
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "user1")
        self.assertEqual(result[1]["name"], "User 2")
        
        # Verify the mock was called correctly
        mock_get.assert_called_once_with(
            f"{api_url}/organization/{org_code}/users",
            headers={
                "Authorization": "Bearer test_access_token",
                "Accept": "application/json"
            }
        )
    
    @patch('kinde_sdk.core.helpers.requests.get')
    def test_get_user_permissions(self, mock_get):
        """Test get_user_permissions returns permission codes."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "permissions": [
                {"id": "perm1", "code": "read:users"},
                {"id": "perm2", "code": "write:users"}
            ]
        }
        mock_get.return_value = mock_response
        
        # Call the function without org_code
        result = get_user_permissions(api_url, token_manager, logger=logger)
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "read:users")
        self.assertEqual(result[1], "write:users")
        
        # Verify the mock was called correctly
        mock_get.assert_called_once_with(
            f"{api_url}/user/permissions",
            headers={
                "Authorization": "Bearer test_access_token",
                "Accept": "application/json"
            }
        )
        
        # Reset mock and test with org_code
        mock_get.reset_mock()
        org_code = "org123"
        
        # Call the function with org_code
        result = get_user_permissions(api_url, token_manager, org_code, logger)
        
        # Verify the mock was called with org-specific URL
        mock_get.assert_called_once_with(
            f"{api_url}/organization/{org_code}/user/permissions",
            headers={
                "Authorization": "Bearer test_access_token",
                "Accept": "application/json"
            }
        )
    
    @patch('kinde_sdk.core.helpers.get_user_permissions')
    def test_has_permission(self, mock_get_permissions):
        """Test has_permission returns correct boolean."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        logger = MagicMock()
        
        # Set up the mock to return specific permissions
        mock_get_permissions.return_value = ["read:users", "write:users"]
        
        # Test with permission that exists
        result = has_permission("read:users", api_url, token_manager, logger=logger)
        self.assertTrue(result)
        
        # Test with permission that doesn't exist
        result = has_permission("delete:users", api_url, token_manager, logger=logger)
        self.assertFalse(result)
        
        # Test with org_code
        org_code = "org123"
        result = has_permission("read:users", api_url, token_manager, org_code, logger)
        self.assertTrue(result)
        
        # Verify the mock was called correctly
        mock_get_permissions.assert_called_with(api_url, token_manager, org_code, logger)
    
    @patch('kinde_sdk.core.helpers.requests.get')
    def test_get_user_roles(self, mock_get):
        """Test get_user_roles returns roles list."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "roles": [
                {"id": "role1", "code": "admin"},
                {"id": "role2", "code": "user"}
            ]
        }
        mock_get.return_value = mock_response
        
        # Call the function without org_code
        result = get_user_roles(api_url, token_manager, logger=logger)
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["code"], "admin")
        self.assertEqual(result[1]["code"], "user")
        
        # Verify the mock was called correctly
        mock_get.assert_called_once_with(
            f"{api_url}/user/roles",
            headers={
                "Authorization": "Bearer test_access_token",
                "Accept": "application/json"
            }
        )
        
        # Reset mock and test with org_code
        mock_get.reset_mock()
        org_code = "org123"
        
        # Call the function with org_code
        result = get_user_roles(api_url, token_manager, org_code, logger)
        
        # Verify the mock was called with org-specific URL
        mock_get.assert_called_once_with(
            f"{api_url}/organization/{org_code}/user/roles",
            headers={
                "Authorization": "Bearer test_access_token",
                "Accept": "application/json"
            }
        )
    
    @patch('kinde_sdk.core.helpers.get_user_roles')
    def test_has_role(self, mock_get_roles):
        """Test has_role returns correct boolean."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        logger = MagicMock()
        
        # Set up the mock to return specific roles
        mock_get_roles.return_value = [
            {"id": "role1", "code": "admin"},
            {"id": "role2", "code": "user"}
        ]
        
        # Test with role that exists
        result = has_role("admin", api_url, token_manager, logger=logger)
        self.assertTrue(result)
        
        # Test with role that doesn't exist
        result = has_role("editor", api_url, token_manager, logger=logger)
        self.assertFalse(result)
        
        # Test with org_code
        org_code = "org123"
        result = has_role("admin", api_url, token_manager, org_code, logger)
        self.assertTrue(result)
        
        # Verify the mock was called correctly
        mock_get_roles.assert_called_with(api_url, token_manager, org_code, logger)
    
    @patch('kinde_sdk.core.helpers.requests.get')
    def test_get_flag_value(self, mock_get):
        """Test get_flag_value returns correct flag value."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        flag_code = "feature_x"
        default_value = False
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Mock response for active flag
        mock_response_active = MagicMock()
        mock_response_active.json.return_value = {
            "feature_flag": {
                "code": "feature_x",
                "is_active": True,
                "value": True
            }
        }
        
        # Mock response for inactive flag
        mock_response_inactive = MagicMock()
        mock_response_inactive.json.return_value = {
            "feature_flag": {
                "code": "feature_x",
                "is_active": False,
                "value": True
            }
        }
        
        # Test with active flag
        mock_get.return_value = mock_response_active
        result = get_flag_value(api_url, flag_code, default_value, token_manager, logger=logger)
        self.assertTrue(result)
        
        # Test with inactive flag
        mock_get.return_value = mock_response_inactive
        result = get_flag_value(api_url, flag_code, default_value, token_manager, logger=logger)
        self.assertFalse(result)
        
        # Test with org_code
        org_code = "org123"
        mock_get.return_value = mock_response_active
        result = get_flag_value(api_url, flag_code, default_value, token_manager, org_code, logger)
        self.assertTrue(result)
        
        # Verify the mock was called correctly with org-specific URL
        mock_get.assert_called_with(
            f"{api_url}/organization/{org_code}/feature-flags/{flag_code}",
            headers={
                "Authorization": "Bearer test_access_token",
                "Accept": "application/json"
            }
        )
    
    def test_get_claim_value(self):
        """Test get_claim_value returns claim from token."""
        # Mock token manager
        token_manager = MagicMock()
        token_manager.get_claims.return_value = {
            "sub": "user123",
            "roles": ["admin", "user"],
            "email": "test@example.com"
        }
        
        # Test existing claim
        result = get_claim_value(token_manager, "email")
        self.assertEqual(result, "test@example.com")
        
        # Test non-existing claim with default
        result = get_claim_value(token_manager, "phone", "unknown")
        self.assertEqual(result, "unknown")
        
        # Test exception case
        token_manager.get_claims.side_effect = Exception("Token error")
        result = get_claim_value(token_manager, "email", "default@example.com")
        self.assertEqual(result, "default@example.com")
    
    def test_is_claim_valid(self):
        """Test is_claim_valid checks claim value correctly."""
        # Mock token manager
        token_manager = MagicMock()
        token_manager.get_claims.return_value = {
            "sub": "user123",
            "roles": ["admin", "user"],
            "email": "test@example.com"
        }
        
        # Test valid claim
        result = is_claim_valid(token_manager, "email", "test@example.com")
        self.assertTrue(result)
        
        # Test invalid claim
        result = is_claim_valid(token_manager, "email", "wrong@example.com")
        self.assertFalse(result)
        
        # Test non-existing claim
        result = is_claim_valid(token_manager, "phone", "123456789")
        self.assertFalse(result)
        
        # Test exception case
        token_manager.get_claims.side_effect = Exception("Token error")
        result = is_claim_valid(token_manager, "email", "test@example.com")
        self.assertFalse(result)
    
    def test_generate_state(self):
        """Test generate_state produces a valid state string."""
        result = generate_state()
        # The actual length might be different due to base64 encoding
        # Just check that it returns a non-empty string
        self.assertTrue(len(result) > 0)
        
        # Test randomness
        result1 = generate_state()
        result2 = generate_state()
        self.assertNotEqual(result1, result2)
    
    def test_hash_string(self):
        """Test hash_string produces correct SHA-256 hash."""
        test_string = "test string"
        expected = hashlib.sha256(test_string.encode('utf-8')).hexdigest()
        result = hash_string(test_string)
        self.assertEqual(result, expected)
    
    @patch('kinde_sdk.core.helpers.time.time')
    def test_get_current_timestamp(self, mock_time):
        """Test get_current_timestamp returns correct time value."""
        mock_time.return_value = 1616729532.123  # Example timestamp
        result = get_current_timestamp()
        self.assertEqual(result, 1616729532)
    
    def test_parse_domain(self):
        """Test parse_domain extracts domain correctly from URL."""
        # Test HTTP URL
        url = "http://example.com/path/to/resource"
        result = parse_domain(url)
        self.assertEqual(result, "example.com")
        
        # Test HTTPS URL
        url = "https://api.example.org/v1/resource"
        result = parse_domain(url)
        self.assertEqual(result, "api.example.org")
        
        # Test URL with port
        url = "https://localhost:8080/api"
        result = parse_domain(url)
        self.assertEqual(result, "localhost:8080")
        
        # Test invalid URL
        url = "not-a-url"
        result = parse_domain(url)
        self.assertEqual(result, "")
    
    def test_format_api_url(self):
        """Test format_api_url formats API URL correctly."""
        # Test with trailing slash
        host = "https://example.com/"
        result = format_api_url(host)
        self.assertEqual(result, "https://example.com/api")
        
        # Test without trailing slash
        host = "https://example.com"
        result = format_api_url(host)
        self.assertEqual(result, "https://example.com/api")
    
    def test_is_token_expired(self):
        """Test is_token_expired checks expiration correctly."""
        current_time = int(time.time())
        
        # Test expired token
        expires_at = current_time - 10  # Expired 10 seconds ago
        result = is_token_expired(expires_at)
        self.assertTrue(result)
        
        # Test active token
        expires_at = current_time + 120  # Expires in 2 minutes
        result = is_token_expired(expires_at)
        self.assertFalse(result)
        
        # Test token in buffer zone
        expires_at = current_time + 30  # Expires in 30 seconds
        result = is_token_expired(expires_at, buffer_seconds=60)
        self.assertTrue(result)  # Should be considered expired with 60s buffer
    
    def test_sanitize_url(self):
        """Test sanitize_url cleans URL correctly."""
        # Test URL with spaces
        url = " https://example.com/path "
        result = sanitize_url(url)
        self.assertEqual(result, "https://example.com/path")
        
        # Test URL with newlines
        url = "https://example.com/path\n"
        result = sanitize_url(url)
        self.assertEqual(result, "https://example.com/path")
        
        # Test URL with tabs
        url = "\thttps://example.com/path\t"
        result = sanitize_url(url)
        self.assertEqual(result, "https://example.com/path")


if __name__ == "__main__":
    unittest.main()