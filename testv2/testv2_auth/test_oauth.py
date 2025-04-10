import unittest
import pytest
import time
import json
import requests
from unittest.mock import patch, MagicMock, AsyncMock, call
from urllib.parse import urlparse, parse_qs

from kinde_sdk.auth.oauth import OAuth, IssuerRouteTypes, LoginOptions
from kinde_sdk.exceptions import (
    KindeConfigurationException, 
    KindeLoginException,
    KindeTokenException,
    KindeRetrieveException,
)


class TestOAuth(unittest.TestCase):
    def setUp(self):
        """Set up for each test"""
        # Set up OAuth with minimal required parameters
        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback",
            framework="None",
            host="https://example.com"  # Use host parameter instead of individual URLs
        )
        
        # Override URLs for testing
        self.oauth.auth_url = "https://example.com/oauth2/auth"
        self.oauth.token_url = "https://example.com/oauth2/token"
        self.oauth.logout_url = "https://example.com/logout"
        self.oauth.userinfo_url = "https://example.com/oauth2/userinfo"
        
        # Mock the session manager for easier testing
        self.mock_storage = MagicMock()
        self.oauth.session_manager = MagicMock()
        self.oauth.session_manager.storage_manager = self.mock_storage
        
        # Mock token manager
        self.mock_token_manager = MagicMock()
        self.mock_token_manager.tokens = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_at": time.time() + 3600  # 1 hour from now
        }
        self.mock_token_manager.get_access_token.return_value = "test_access_token"
        self.mock_token_manager.get_id_token.return_value = "test_id_token"
        self.mock_token_manager.get_claims.return_value = {"sub": "user123", "email": "test@example.com"}
        
        # Make session manager return our mock token manager
        self.oauth.session_manager.get_token_manager.return_value = self.mock_token_manager

    # Initialize Tests
    def test_init_without_client_id(self):
        """Test initialization without client_id raises exception"""
        with self.assertRaises(KindeConfigurationException):
            OAuth(client_id=None, client_secret="test_client_secret", redirect_uri="http://localhost/callback")

    def test_init_with_config_file(self):
        """Test initialization with config file"""
        mock_config = {"storage": {"type": "redis", "host": "localhost", "port": 6379}}
        
        with patch("kinde_sdk.auth.oauth.load_config", return_value=mock_config) as mock_load_config:
            with patch("kinde_sdk.auth.oauth.StorageManager") as MockStorageManager:
                with patch("kinde_sdk.auth.oauth.UserSession"):
                    storage_manager_instance = MockStorageManager.return_value
                    
                    oauth = OAuth(
                        client_id="test_client_id",
                        config_file="config.json"
                    )
                    
                    mock_load_config.assert_called_once_with("config.json")
                    storage_manager_instance.initialize.assert_called_once_with(
                        {"type": "redis", "host": "localhost", "port": 6379}
                    )

    # Existing login URL test
    @pytest.mark.asyncio
    async def test_login_url(self):
        """Test generating login URL"""
        login_url = await self.oauth.login()
        
        parsed_url = urlparse(login_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/oauth2/auth")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/callback")
        self.assertEqual(query_params["response_type"][0], "code")
        self.assertEqual(query_params["scope"][0], "openid profile email")
        self.assertTrue("state" in query_params)
        self.assertTrue("nonce" in query_params)
        self.assertTrue("code_challenge" in query_params)
        self.assertEqual(query_params["code_challenge_method"][0], "S256")

    # Existing register URL test
    @pytest.mark.asyncio
    async def test_register_url(self):
        """Test generating registration URL"""
        register_url = await self.oauth.register()
        
        parsed_url = urlparse(register_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/oauth2/auth")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/callback")
        self.assertEqual(query_params["prompt"][0], "create")
        self.assertEqual(query_params["response_type"][0], "code")
        self.assertEqual(query_params["scope"][0], "openid profile email")

    # Existing login with options test
    @pytest.mark.asyncio
    async def test_login_with_options(self):
        """Test login with specific options"""
        login_options = {
            LoginOptions.RESPONSE_TYPE: "code",
            LoginOptions.SCOPE: "openid profile email offline_access",
            LoginOptions.STATE: "custom_state",
            LoginOptions.NONCE: "custom_nonce",
            LoginOptions.ORG_CODE: "test_org",
            LoginOptions.IS_CREATE_ORG: True,
            LoginOptions.LANG: "en"
        }
        
        login_url = await self.oauth.login(login_options)
        
        parsed_url = urlparse(login_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["scope"][0], "openid profile email offline_access")
        self.assertEqual(query_params["state"][0], "custom_state")
        self.assertEqual(query_params["nonce"][0], "custom_nonce")
        self.assertEqual(query_params["org_code"][0], "test_org")
        self.assertEqual(query_params["is_create_org"][0], "true")
        self.assertEqual(query_params["lang"][0], "en")

    # New test for empty login options
    @pytest.mark.asyncio
    async def test_login_with_empty_options(self):
        """Test login with empty options dictionary"""
        with patch.object(self.oauth, "generate_auth_url") as mock_gen_url:
            mock_gen_url.return_value = {"url": "https://example.com/oauth2/auth?empty=true"}
            
            # Test with None and empty dict
            await self.oauth.login(None)
            mock_gen_url.assert_called_with(route_type=IssuerRouteTypes.LOGIN, login_options={})
            
            await self.oauth.login({})
            mock_gen_url.assert_called_with(route_type=IssuerRouteTypes.LOGIN, login_options={})

    # Test for code challenge in login options
    @pytest.mark.asyncio
    async def test_generate_auth_url_with_code_challenge(self):
        """Test generate_auth_url with provided code challenge"""
        with patch("kinde_sdk.auth.oauth.generate_random_string") as mock_gen_random:
            mock_gen_random.side_effect = ["test_state", "test_nonce"]
            
            login_options = {
                LoginOptions.CODE_CHALLENGE: "provided_code_challenge",
                LoginOptions.CODE_CHALLENGE_METHOD: "S256"
            }
            
            auth_url_data = await self.oauth.generate_auth_url(login_options=login_options)
            
            # Verify that the provided code challenge was used
            self.assertEqual(auth_url_data["code_challenge"], "provided_code_challenge")
            
            # Verify it's in the URL
            parsed_url = urlparse(auth_url_data["url"])
            query_params = parse_qs(parsed_url.query)
            self.assertEqual(query_params["code_challenge"][0], "provided_code_challenge")
            self.assertEqual(query_params["code_challenge_method"][0], "S256")

    # Test for prompt setting in registration
    @pytest.mark.asyncio
    async def test_register_sets_prompt_create(self):
        """Test that register sets prompt to 'create' if not specified"""
        login_options = {}
        
        with patch.object(self.oauth, "generate_auth_url") as mock_gen_url:
            mock_gen_url.return_value = {"url": "https://example.com/oauth2/auth?prompt=create"}
            
            await self.oauth.register(login_options)
            
            # Check that prompt was set to create
            call_args = mock_gen_url.call_args[1]
            self.assertEqual(call_args["route_type"], IssuerRouteTypes.REGISTER)
            self.assertEqual(call_args["login_options"].get("prompt"), "create")

    # Test framework validation in login
    @pytest.mark.asyncio
    async def test_login_without_framework(self):
        """Test login without framework raises exception"""
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback"
            # framework is missing
        )
        
        with self.assertRaises(KindeConfigurationException):
            await oauth.login()

    # Test framework validation in register
    @pytest.mark.asyncio
    async def test_register_without_framework(self):
        """Test register without framework raises exception"""
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback"
            # framework is missing
        )
        
        with self.assertRaises(KindeConfigurationException):
            await oauth.register()

    # Existing logout URL test
    @pytest.mark.asyncio
    async def test_logout_url(self):
        """Test generating logout URL"""
        logout_url = await self.oauth.logout()
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/logout")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertTrue("redirect_uri" in query_params)

    # Existing logout with options test
    @pytest.mark.asyncio
    async def test_logout_with_options(self):
        """Test logout with specific options"""
        logout_options = {
            "post_logout_redirect_uri": "http://example.com/post-logout",
            "state": "logout_state",
            "id_token_hint": "some_id_token"
        }
        
        logout_url = await self.oauth.logout(logout_options=logout_options)
        
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://example.com/post-logout")
        self.assertEqual(query_params["state"][0], "logout_state")
        self.assertEqual(query_params["id_token_hint"][0], "some_id_token")

    # Test framework validation in logout
    @pytest.mark.asyncio
    async def test_logout_without_framework(self):
        """Test logout without framework raises exception"""
        oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback"
            # framework is missing
        )
        
        with self.assertRaises(KindeConfigurationException):
            await oauth.logout()

    # Test logout with user_id
    @pytest.mark.asyncio
    async def test_logout_with_user_id(self):
        """Test logout with user_id fetches token and clears session"""
        user_id = "user123"
        
        logout_url = await self.oauth.logout(user_id=user_id)
        
        # Verify token manager was accessed
        self.oauth.session_manager.get_token_manager.assert_called_with(user_id)
        # Verify logout was called
        self.oauth.session_manager.logout.assert_called_with(user_id)
        
        # Verify URL
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertTrue("id_token_hint" in query_params)
        self.assertEqual(query_params["id_token_hint"][0], "test_id_token")

    # Existing handle redirect test - but let's update it to use our new mocking approach
    @pytest.mark.asyncio
    async def test_handle_redirect(self):
        """Test handling OAuth redirect"""
        # Set up mocks for state and code verifier
        self.mock_storage.get.side_effect = lambda key: {
            "state": MagicMock(get=lambda k: "test_state" if k == "value" else None),
            "code_verifier": MagicMock(get=lambda k: "test_verifier" if k == "value" else None),
            "nonce": MagicMock(get=lambda k: "test_nonce" if k == "value" else None)
        }.get(key)
        
        # Mock token exchange
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            token_data = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "id_token": "test_id_token",
                "expires_in": 3600
            }
            mock_exchange.return_value = AsyncMock(return_value=token_data)()
            
            # Mock user details retrieval
            with patch("kinde_sdk.auth.oauth.helper_get_user_details") as mock_get_user:
                user_details = {
                    "sub": "user123",
                    "email": "test@example.com",
                    "name": "Test User"
                }
                mock_get_user.return_value = AsyncMock(return_value=user_details)()
                
                # Call the function
                result = await self.oauth.handle_redirect(
                    code="test_code",
                    user_id="user123",
                    state="test_state"
                )
                
                # Verify the token exchange
                mock_exchange.assert_called_once_with("test_code", "test_verifier")
                
                # Verify storage cleanup
                self.mock_storage.delete.assert_has_calls([
                    call("code_verifier"),
                    call("state"),
                    call("nonce")
                ], any_order=True)
                
                # Verify result
                self.assertEqual(result["tokens"], token_data)
                self.assertEqual(result["user"], user_details)

    # Test state validation in handle_redirect
    @pytest.mark.asyncio
    async def test_handle_redirect_invalid_state(self):
        """Test handle_redirect with invalid state"""
        # Make storage return None for state
        self.mock_storage.get.side_effect = lambda key: None if key == "state" else MagicMock()
        
        with self.assertRaises(KindeLoginException):
            await self.oauth.handle_redirect(
                code="test_code",
                user_id="user123",
                state="test_state"
            )
        
        # Test with mismatched state
        self.mock_storage.get.side_effect = lambda key: {
            "state": MagicMock(get=lambda k: "different_state" if k == "value" else None)
        }.get(key)
        
        with self.assertRaises(KindeLoginException):
            await self.oauth.handle_redirect(
                code="test_code",
                user_id="user123",
                state="test_state"
            )

    # Test token exchange error
    @pytest.mark.asyncio
    async def test_handle_redirect_token_exchange_error(self):
        """Test handle_redirect with token exchange error"""
        # Set up mocks for state and code verifier
        self.mock_storage.get.side_effect = lambda key: {
            "state": MagicMock(get=lambda k: "test_state" if k == "value" else None),
            "code_verifier": MagicMock(get=lambda k: "test_verifier" if k == "value" else None)
        }.get(key)
        
        # Mock token exchange to raise an exception
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            mock_exchange.side_effect = Exception("Token exchange failed")
            
            with self.assertRaises(KindeTokenException):
                await self.oauth.handle_redirect(
                    code="test_code",
                    user_id="user123",
                    state="test_state"
                )

    # Test user details error
    @pytest.mark.asyncio
    async def test_handle_redirect_user_details_error(self):
        """Test handle_redirect with user details error"""
        # Set up mocks for state and code verifier
        self.mock_storage.get.side_effect = lambda key: {
            "state": MagicMock(get=lambda k: "test_state" if k == "value" else None),
            "code_verifier": MagicMock(get=lambda k: "test_verifier" if k == "value" else None),
            "nonce": MagicMock(get=lambda k: "test_nonce" if k == "value" else None)
        }.get(key)
        
        # Mock token exchange
        with patch.object(self.oauth, "exchange_code_for_tokens") as mock_exchange:
            token_data = {
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
                "id_token": "test_id_token",
                "expires_in": 3600
            }
            mock_exchange.return_value = AsyncMock(return_value=token_data)()
            
            # Mock user details to raise an exception
            with patch("kinde_sdk.auth.oauth.helper_get_user_details") as mock_get_user:
                mock_get_user.side_effect = Exception("Failed to get user details")
                
                # This should not raise an exception, but return empty user dict
                result = await self.oauth.handle_redirect(
                    code="test_code",
                    user_id="user123",
                    state="test_state"
                )
                
                # Verify empty user dict
                self.assertEqual(result["user"], {})

    # Test exchange_code_for_tokens
    @pytest.mark.asyncio
    async def test_exchange_code_for_tokens(self):
        """Test the exchange_code_for_tokens method"""
        # Mock requests.post
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_in": 3600
        }
        
        with patch("requests.post", return_value=mock_response) as mock_post:
            result = await self.oauth.exchange_code_for_tokens("test_code")
            
            # Verify the call to requests.post
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            self.assertEqual(args[0], self.oauth.token_url)
            self.assertEqual(kwargs["data"]["grant_type"], "authorization_code")
            self.assertEqual(kwargs["data"]["code"], "test_code")
            self.assertEqual(kwargs["data"]["client_id"], "test_client_id")
            self.assertEqual(kwargs["data"]["client_secret"], "test_client_secret")
            
            # Verify result
            self.assertEqual(result["access_token"], "test_access_token")
            self.assertEqual(result["refresh_token"], "test_refresh_token")
            self.assertEqual(result["id_token"], "test_id_token")
            self.assertEqual(result["expires_in"], 3600)

    @pytest.mark.asyncio
    async def test_exchange_code_for_tokens_with_pkce(self):
        """Test exchange_code_for_tokens with PKCE"""
        # Mock requests.post
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "id_token": "test_id_token",
            "expires_in": 3600
        }
        
        code_verifier = "test_code_verifier"
        
        with patch("requests.post", return_value=mock_response) as mock_post:
            result = await self.oauth.exchange_code_for_tokens("test_code", code_verifier)
            
            # Verify the call to requests.post
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            self.assertEqual(kwargs["data"]["code_verifier"], code_verifier)
            
            # Verify result
            self.assertEqual(result["access_token"], "test_access_token")

    @pytest.mark.asyncio
    async def test_exchange_code_for_tokens_error(self):
        """Test exchange_code_for_tokens with error response"""
        # Mock requests.post to return an error
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Invalid grant"
        
        with patch("requests.post", return_value=mock_response) as mock_post:
            with self.assertRaises(KindeTokenException):
                await self.oauth.exchange_code_for_tokens("test_code")

    def test_get_tokens(self):
        """Test retrieving tokens for a user"""
        # Test success case
        result = self.oauth.get_tokens("user123")
        
        # Verify token manager was accessed
        self.oauth.session_manager.get_token_manager.assert_called_with("user123")
        
        # Verify result
        self.assertEqual(result["access_token"], "test_access_token")
        self.assertEqual(result["refresh_token"], "test_refresh_token")
        self.assertEqual(result["id_token"], "test_id_token")
        self.assertTrue("expires_at" in result)
        self.assertTrue("expires_in" in result)
        self.assertEqual(result["claims"]["sub"], "user123")
        self.assertEqual(result["claims"]["email"], "test@example.com")

    def test_get_tokens_no_token_manager(self):
        """Test get_tokens with no token manager"""
        # Make get_token_manager return None
        self.oauth.session_manager.get_token_manager.return_value = None
        
        with self.assertRaises(ValueError) as context:
            self.oauth.get_tokens("user123")
        
        # Check error message
        self.assertTrue("No token manager available for user" in str(context.exception))

    def test_get_tokens_no_access_token(self):
        """Test get_tokens with no access token in tokens"""
        # Remove access_token from tokens
        self.mock_token_manager.tokens = {}
        
        with self.assertRaises(ValueError) as context:
            self.oauth.get_tokens("user123")
        
        # Check error message
        self.assertTrue("No access token available for user" in str(context.exception))

    def test_get_tokens_invalid_access_token(self):
        """Test get_tokens with invalid access token"""
        # Make get_access_token return None
        self.mock_token_manager.get_access_token.return_value = None
        
        with self.assertRaises(ValueError) as context:
            self.oauth.get_tokens("user123")
        
        # Check error message
        self.assertTrue("Invalid access token for user" in str(context.exception))

    def test_get_tokens_error(self):
        """Test get_tokens with an unexpected error"""
        # Make get_access_token raise an exception
        self.mock_token_manager.get_access_token.side_effect = Exception("Unexpected error")
        
        with self.assertRaises(ValueError) as context:
            self.oauth.get_tokens("user123")
        
        # Check error message
        self.assertTrue("Failed to retrieve tokens" in str(context.exception))

if __name__ == "__main__":
    pytest.main(["-xvs", __file__])