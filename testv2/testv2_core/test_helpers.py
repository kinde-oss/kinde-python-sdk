import unittest
import warnings
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
    get_user_details_sync,
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

    def test_generate_pkce_pair(self):
        """Test generate_pkce_pair generates valid verifier and challenge."""
        # Mock the random string and hash
        with patch('kinde_sdk.core.helpers.generate_random_string') as mock_random_string:
            with patch('kinde_sdk.core.helpers.hashlib.sha256') as mock_sha256:
                mock_random_string.return_value = "test_verifier"
                mock_digest = MagicMock()
                mock_digest.digest.return_value = b"hashed_value"
                mock_sha256.return_value = mock_digest
                
                # Use a loop to run the async function
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

    def test_generate_pkce_pair_error_handling(self):
        """Test error handling in generate_pkce_pair when hashing fails."""
        # Mock the hash function to raise an exception
        with patch('kinde_sdk.core.helpers.hashlib.sha256') as mock_sha256:
            with patch('kinde_sdk.core.helpers.base64_url_encode') as mock_encode:
                mock_sha256.side_effect = Exception("Hash error")
                mock_encode.side_effect = lambda x: f"encoded_{x}"
                
                # Use a loop to run the async function
                result = asyncio.run(generate_pkce_pair(52))
                
                # Should fall back to plain verifier encoding
                self.assertIn("code_verifier", result)
                self.assertIn("code_challenge", result)
                
                # Verify the logger was called
                # Since we're not passing a logger, we need to verify the fallback worked
                self.assertTrue(mock_encode.called)
    
    def test_get_user_details(self):
        """Test get_user_details with valid token."""
        # Mock dependencies
        userinfo_url = "https://test.kinde.com/api/v1/user"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Create the mock for requests.get
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            # Mock response
            mock_response = MagicMock()
            mock_response.json.return_value = {"id": "user1", "name": "Test User"}
            mock_get.return_value = mock_response
            
            # Use a loop to run the async function
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

    def test_get_user_details_token_error(self):
        """Test get_user_details handles token errors."""
        userinfo_url = "https://test.kinde.com/api/v1/user"
        token_manager = MagicMock()
        token_manager.get_access_token.side_effect = ValueError("No token")
        logger = MagicMock()
        
        with self.assertRaises(ValueError):
            asyncio.run(get_user_details(userinfo_url, token_manager, logger))
        
        logger.error.assert_called_with("Token error when retrieving user details: No token")

    def test_get_user_details_request_error_with_json(self):
        """Test get_user_details handles request errors with JSON response."""
        userinfo_url = "https://test.kinde.com/api/v1/user"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response with JSON error data
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"error": "invalid_token", "error_description": "Token is invalid"}
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                asyncio.run(get_user_details(userinfo_url, token_manager, logger))
            
            logger.error.assert_called_with("User details retrieval failed: Token is invalid")

    def test_get_user_details_request_error_without_json(self):
        """Test get_user_details handles request errors without JSON response."""
        userinfo_url = "https://test.kinde.com/api/v1/user"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response that raises an exception when json() is called
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_response.status_code = 500
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                asyncio.run(get_user_details(userinfo_url, token_manager, logger))
            
            logger.error.assert_called_with("User details retrieval failed with status code: 500")
    
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
    
    def test_decode_jwt_invalid_token(self):
        """Test decode_jwt with invalid token formats."""
        # Test missing parts
        with self.assertRaises(ValueError):
            decode_jwt("invalid.token")
        
        # Test invalid base64
        with self.assertRaises(ValueError):
            decode_jwt("header.invalid_payload.signature")
    
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
    
    def test_get_user_organizations(self):
        """Test get_user_organizations returns organization list."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Create a mock for requests.get
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
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

    def test_get_user_organizations_token_error(self):
        """Test get_user_organizations handles token errors."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.side_effect = ValueError("No token")
        logger = MagicMock()
        
        with self.assertRaises(ValueError):
            get_user_organizations(api_url, token_manager, logger)
        
        logger.error.assert_called_with("Token error when retrieving organizations: No token")

    def test_get_user_organizations_request_error_with_json(self):
        """Test get_user_organizations handles request errors with JSON response."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response with JSON error data
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"error": "forbidden", "error_description": "Access denied"}
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                get_user_organizations(api_url, token_manager, logger)
            
            logger.error.assert_called_with("Organizations retrieval failed: Access denied")

    def test_get_user_organizations_request_error_without_json(self):
        """Test get_user_organizations handles request errors without JSON response."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response that raises an exception when json() is called
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_response.status_code = 500
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                get_user_organizations(api_url, token_manager, logger)
            
            logger.error.assert_called_with("Organizations retrieval failed with status code: 500")
    
    def test_get_organization_details(self):
        """Test get_organization_details returns organization details."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        org_code = "org123"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Create a mock for requests.get
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
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

    def test_get_organization_details_token_error(self):
        """Test get_organization_details handles token errors."""
        api_url = "https://test.kinde.com/api"
        org_code = "org123"
        token_manager = MagicMock()
        token_manager.get_access_token.side_effect = ValueError("No token")
        logger = MagicMock()
        
        with self.assertRaises(ValueError):
            get_organization_details(api_url, org_code, token_manager, logger)
        
        logger.error.assert_called_with("Token error when retrieving organization details: No token")

    def test_get_organization_details_request_error_with_json(self):
        """Test get_organization_details handles request errors with JSON response."""
        api_url = "https://test.kinde.com/api"
        org_code = "org123"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response with JSON error data
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"error": "not_found", "error_description": "Organization not found"}
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                get_organization_details(api_url, org_code, token_manager, logger)
            
            logger.error.assert_called_with("Organization details retrieval failed: Organization not found")

    def test_get_organization_details_request_error_without_json(self):
        """Test get_organization_details handles request errors without JSON response."""
        api_url = "https://test.kinde.com/api"
        org_code = "org123"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response that raises an exception when json() is called
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_response.status_code = 404
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                get_organization_details(api_url, org_code, token_manager, logger)
            
            logger.error.assert_called_with("Organization details retrieval failed with status code: 404")
    
    def test_get_organization_users(self):
        """Test get_organization_users returns users list."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        org_code = "org123"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Create a mock for requests.get
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
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

    def test_get_organization_users_token_error(self):
        """Test get_organization_users handles token errors."""
        api_url = "https://test.kinde.com/api"
        org_code = "org123"
        token_manager = MagicMock()
        token_manager.get_access_token.side_effect = ValueError("No token")
        logger = MagicMock()
        
        with self.assertRaises(ValueError):
            get_organization_users(api_url, org_code, token_manager, logger)
        
        logger.error.assert_called_with("Token error when retrieving organization users: No token")

    def test_get_organization_users_request_error_with_json(self):
        """Test get_organization_users handles request errors with JSON response."""
        api_url = "https://test.kinde.com/api"
        org_code = "org123"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response with JSON error data
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"error": "forbidden", "error_description": "Access denied"}
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                get_organization_users(api_url, org_code, token_manager, logger)
            
            logger.error.assert_called_with("Organization users retrieval failed: Access denied")

    def test_get_organization_users_request_error_without_json(self):
        """Test get_organization_users handles request errors without JSON response."""
        api_url = "https://test.kinde.com/api"
        org_code = "org123"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response that raises an exception when json() is called
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_response.status_code = 500
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                get_organization_users(api_url, org_code, token_manager, logger)
            
            logger.error.assert_called_with("Organization users retrieval failed with status code: 500")
    
    def test_get_user_permissions(self):
        """Test get_user_permissions returns permission codes."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Create a mock for requests.get
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
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

    def test_get_user_permissions_token_error(self):
        """Test get_user_permissions handles token errors."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.side_effect = ValueError("No token")
        logger = MagicMock()
        
        with self.assertRaises(ValueError):
            get_user_permissions(api_url, token_manager, logger=logger)
        
        logger.error.assert_called_with("Token error when retrieving user permissions: No token")

    def test_get_user_permissions_request_error_with_json(self):
        """Test get_user_permissions handles request errors with JSON response."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response with JSON error data
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"error": "forbidden", "error_description": "Access denied"}
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                get_user_permissions(api_url, token_manager, logger=logger)
            
            logger.error.assert_called_with("User permissions retrieval failed: Access denied")

    def test_get_user_permissions_request_error_without_json(self):
        """Test get_user_permissions handles request errors without JSON response."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response that raises an exception when json() is called
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_response.status_code = 500
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                get_user_permissions(api_url, token_manager, logger=logger)
            
            logger.error.assert_called_with("User permissions retrieval failed with status code: 500")
    
    def test_get_user_permissions_without_logger(self):
        """Test get_user_permissions when logger is not provided."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        
        # Create a mock for requests.get
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            # Mock response
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "permissions": [
                    {"id": "perm1", "code": "read:users"},
                    {"id": "perm2", "code": "write:users"}
                ]
            }
            mock_get.return_value = mock_response
            
            # Call the function without logger
            result = get_user_permissions(api_url, token_manager)
            
            # Check the result
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0], "read:users")
            self.assertEqual(result[1], "write:users")
    
    def test_has_permission(self):
        """Test has_permission returns correct boolean."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        logger = MagicMock()
        
        # Set up the mock to return specific permissions
        with patch('kinde_sdk.core.helpers.get_user_permissions') as mock_get_permissions:
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

    def test_has_permission_error(self):
        """Test has_permission handles underlying errors."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        logger = MagicMock()
        
        # Test when get_user_permissions raises an exception
        with patch('kinde_sdk.core.helpers.get_user_permissions') as mock_get_perms:
            mock_get_perms.side_effect = Exception("Permission error")
            result = has_permission("perm", api_url, token_manager, logger=logger)
            self.assertFalse(result)
            logger.error.assert_called_with("Error checking permission: Permission error")
    
    def test_get_user_roles(self):
        """Test get_user_roles returns roles list."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Create a mock for requests.get
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
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

    def test_get_user_roles_token_error(self):
        """Test get_user_roles handles token errors."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.side_effect = ValueError("No token")
        logger = MagicMock()
        
        with self.assertRaises(ValueError):
            get_user_roles(api_url, token_manager, logger=logger)
        
        logger.error.assert_called_with("Token error when retrieving user roles: No token")

    def test_get_user_roles_request_error_with_json(self):
        """Test get_user_roles handles request errors with JSON response."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response with JSON error data
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {"error": "forbidden", "error_description": "Access denied"}
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                get_user_roles(api_url, token_manager, logger=logger)
            
            logger.error.assert_called_with("User roles retrieval failed: Access denied")

    def test_get_user_roles_request_error_without_json(self):
        """Test get_user_roles handles request errors without JSON response."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock response that raises an exception when json() is called
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
            mock_response.status_code = 500
            mock_get.side_effect = RequestException(response=mock_response)
            
            with self.assertRaises(RequestException):
                get_user_roles(api_url, token_manager, logger=logger)
            
            logger.error.assert_called_with("User roles retrieval failed with status code: 500")
    
    def test_get_user_roles_without_logger(self):
        """Test get_user_roles when logger is not provided."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        
        # Create a mock for requests.get
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            # Mock response
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "roles": [
                    {"id": "role1", "code": "admin"},
                    {"id": "role2", "code": "user"}
                ]
            }
            mock_get.return_value = mock_response
            
            # Call the function without logger
            result = get_user_roles(api_url, token_manager)
            
            # Check the result
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["code"], "admin")
            self.assertEqual(result[1]["code"], "user")
    
    def test_has_role(self):
        """Test has_role returns correct boolean."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        logger = MagicMock()
        
        # Set up the mock to return specific roles
        with patch('kinde_sdk.core.helpers.get_user_roles') as mock_get_roles:
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

    def test_has_role_error(self):
        """Test has_role handles underlying errors."""
        api_url = "https://test.kinde.com/api"
        token_manager = MagicMock()
        logger = MagicMock()
        
        # Test when get_user_roles raises an exception
        with patch('kinde_sdk.core.helpers.get_user_roles') as mock_get_roles:
            mock_get_roles.side_effect = Exception("Role error")
            result = has_role("admin", api_url, token_manager, logger=logger)
            self.assertFalse(result)
            logger.error.assert_called_with("Error checking role: Role error")
    
    def test_get_flag_value(self):
        """Test get_flag_value returns correct flag value."""
        # Mock dependencies
        api_url = "https://test.kinde.com/api"
        flag_code = "feature_x"
        default_value = False
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Create a mock for requests.get
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            # Mock response for active flag
            mock_response_active = MagicMock()
            mock_response_active.json.return_value = {
                "feature_flag": {
                    "code": "feature_x",
                    "is_active": True,
                    "value": True
                }
            }
            mock_get.return_value = mock_response_active
            
            # Test with active flag
            result = get_flag_value(api_url, flag_code, default_value, token_manager, logger=logger)
            self.assertTrue(result)
            
            # Mock response for inactive flag
            mock_response_inactive = MagicMock()
            mock_response_inactive.json.return_value = {
                "feature_flag": {
                    "code": "feature_x",
                    "is_active": False,
                    "value": True
                }
            }
            mock_get.return_value = mock_response_inactive
            
            # Test with inactive flag
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

    def test_get_flag_value_request_error(self):
        """Test get_flag_value handles request errors."""
        api_url = "https://test.kinde.com/api"
        flag_code = "feature_x"
        default_value = "default"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Create a mock that raises an exception
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_get.side_effect = RequestException("Network error")
            
            # Should return default value on error
            result = get_flag_value(api_url, flag_code, default_value, token_manager, logger=logger)
            self.assertEqual(result, default_value)
            logger.error.assert_called_with("Error retrieving feature flag: Network error")
    
    def test_get_flag_value_without_logger(self):
        """Test get_flag_value without logger."""
        api_url = "https://test.kinde.com/api"
        flag_code = "feature_x"
        default_value = "default"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        
        # Create a mock that raises an exception
        with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
            mock_get.side_effect = RequestException("Network error")
            
            # Should return default value on error without logging
            result = get_flag_value(api_url, flag_code, default_value, token_manager)
            self.assertEqual(result, default_value)
    
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
    
    def test_get_current_timestamp(self):
        """Test get_current_timestamp returns correct time value."""
        with patch('kinde_sdk.core.helpers.time.time') as mock_time:
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
        
        # Test with buffer_seconds=0
        self.assertTrue(is_token_expired(current_time - 1, buffer_seconds=0))
        self.assertFalse(is_token_expired(current_time + 1, buffer_seconds=0))
    
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

    def test_get_user_details_sync_no_event_loop(self):
        """Test get_user_details_sync when no event loop is running (Flask scenario)."""
        # Mock dependencies
        userinfo_url = "https://test.kinde.com/api/v1/user"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Mock asyncio.get_running_loop to raise RuntimeError (no event loop)
        with patch('kinde_sdk.core.helpers.asyncio.get_running_loop') as mock_get_loop:
            with patch('kinde_sdk.core.helpers.asyncio.run') as mock_run:
                with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
                    mock_get_loop.side_effect = RuntimeError("No running event loop")
                    
                    # Mock the async get_user_details function
                    mock_run.return_value = {"id": "user1", "name": "Test User"}
                    
                    result = get_user_details_sync(userinfo_url, token_manager, logger)
                    
                    # Check the result
                    self.assertEqual(result, {"id": "user1", "name": "Test User"})
                    
                    # Verify asyncio.run was called with the async function
                    mock_run.assert_called_once()

    def test_get_user_details_sync_with_event_loop(self):
        """Test get_user_details_sync when event loop is running (FastAPI scenario)."""
        # Mock dependencies
        userinfo_url = "https://test.kinde.com/api/v1/user"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_access_token"
        logger = MagicMock()
        
        # Mock asyncio.get_running_loop to return a mock loop (event loop exists)
        with patch('kinde_sdk.core.helpers.asyncio.get_running_loop') as mock_get_loop:
            with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
                mock_loop = MagicMock()
                mock_get_loop.return_value = mock_loop
                
                # Mock response
                mock_response = MagicMock()
                mock_response.json.return_value = {"id": "user1", "name": "Test User"}
                mock_get.return_value = mock_response
                
                result = get_user_details_sync(userinfo_url, token_manager, logger)
                
                # Check the result
                self.assertEqual(result, {"id": "user1", "name": "Test User"})
                
                # Verify the direct request was made (not asyncio.run)
                mock_get.assert_called_once_with(
                    userinfo_url,
                    headers={
                        "Authorization": "Bearer test_access_token",
                        "Accept": "application/json"
                    }
                )

    def test_get_user_details_sync_token_error(self):
        """Test get_user_details_sync handles token errors."""
        userinfo_url = "https://test.kinde.com/api/v1/user"
        token_manager = MagicMock()
        token_manager.get_access_token.side_effect = ValueError("No token")
        logger = MagicMock()
        
        # Mock asyncio.get_running_loop to raise RuntimeError (no event loop)
        with patch('kinde_sdk.core.helpers.asyncio.get_running_loop') as mock_get_loop:
            mock_get_loop.side_effect = RuntimeError("No running event loop")
            
            with self.assertRaises(ValueError):
                get_user_details_sync(userinfo_url, token_manager, logger)

    def test_get_user_details_sync_request_error(self):
        """Test get_user_details_sync handles request errors."""
        userinfo_url = "https://test.kinde.com/api/v1/user"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Mock asyncio.get_running_loop to return a mock loop (event loop exists)
        with patch('kinde_sdk.core.helpers.asyncio.get_running_loop') as mock_get_loop:
            with patch('kinde_sdk.core.helpers.requests.get') as mock_get:
                mock_loop = MagicMock()
                mock_get_loop.return_value = mock_loop
                
                # Mock response that raises an exception
                mock_response = MagicMock()
                mock_response.raise_for_status.side_effect = RequestException("Network error")
                mock_get.return_value = mock_response
                
                with self.assertRaises(RequestException):
                    get_user_details_sync(userinfo_url, token_manager, logger)

    def test_get_user_details_sync_no_event_loop_with_error(self):
        """Test get_user_details_sync when no event loop and async function raises error."""
        userinfo_url = "https://test.kinde.com/api/v1/user"
        token_manager = MagicMock()
        token_manager.get_access_token.return_value = "test_token"
        logger = MagicMock()
        
        # Mock asyncio.get_running_loop to raise RuntimeError (no event loop)
        with patch('kinde_sdk.core.helpers.asyncio.get_running_loop') as mock_get_loop:
            with patch('kinde_sdk.core.helpers.asyncio.run') as mock_run:
                mock_get_loop.side_effect = RuntimeError("No running event loop")
                
                # Mock asyncio.run to raise an exception
                mock_run.side_effect = ValueError("Token error")
                
                # Suppress the RuntimeWarning about coroutine not being awaited
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", RuntimeWarning)
                    
                    # Test that the exception is properly propagated
                    with self.assertRaises(ValueError) as context:
                        get_user_details_sync(userinfo_url, token_manager, logger)
                    
                    # Verify the error message
                    self.assertEqual(str(context.exception), "Token error")


if __name__ == "__main__":
    unittest.main()