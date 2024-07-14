import unittest
from unittest.mock import patch, MagicMock
from kinde_sdk.kinde_api_client import KindeApiClient, GrantType
from kinde_sdk import __version__
from urllib.parse import urlparse, parse_qs

class TestKindeApiClient(unittest.TestCase):

    def setUp(self):
        self.domain = "https://example.kinde.com"
        self.callback_url = "https://example.com/callback"
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        self.mock_oauth2_session_patcher = patch("kinde_sdk.kinde_api_client.OAuth2Session")
        self.mock_oauth2_session = self.mock_oauth2_session_patcher.start()
        self.mock_oauth2_session.return_value.create_authorization_url.return_value = ("https://example.com/auth", "test_state")

    def _create_kinde_client(self, grant_type, code_verifier=None):
        return KindeApiClient(
            domain=self.domain,
            callback_url=self.callback_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type=grant_type,
            code_verifier = code_verifier
        )   

    def tearDown(self):
        self.mock_oauth2_session_patcher.stop()

    def test_initialization(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        self.assertEqual(client.domain, self.domain)
        self.assertEqual(client.client_id, self.client_id)
        self.mock_oauth2_session.assert_called_once()

    def test_initialization_invalid_grant_type(self):
        with self.assertRaises(ValueError):
            self._create_kinde_client("INVALID_GRANT")

    def test_get_login_url(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        login_url = client.get_login_url()
        self.assertEqual(login_url, "https://example.com/auth")

    def test_get_login_url_additional_params(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        login_url = client.get_login_url({
            "auth_url_params": {
                "test": "val"
            }
        })
        self.assertEqual(login_url, "https://example.com/auth?test=val")

    def test_get_register_url(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        register_url = client.get_register_url()
        self.assertEqual(register_url, "https://example.com/auth&start_page=registration")

    def test_logout(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        redirect_to = "https://example.com"
        logout_url = client.logout(redirect_to)
        self.assertEqual(logout_url, f"{self.domain}/logout?redirect={redirect_to}")

    def test_get_claim(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        with patch.object(KindeApiClient, '_decode_token_if_needed'):
            client._KindeApiClient__decoded_tokens = {
                "access_token": {"test_key": "test_value"}
            }
            claim = client.get_claim("test_key")
            self.assertEqual(claim, {"name": "test_key", "value": "test_value"})

    def test_get_boolean_flag(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        with patch.object(KindeApiClient, 'get_claim') as mock_get_claim:
            mock_get_claim.return_value = {"value": {"test_flag": {"v": True, "t": "b"}}}
            flag_value = client.get_boolean_flag("test_flag")
            self.assertTrue(flag_value)

    def test_get_boolean_flag_not_exist(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        with patch.object(KindeApiClient, 'get_claim') as mock_get_claim:
            mock_get_claim.return_value = {"value": {}}
            flag_value = client.get_boolean_flag("non_existent_flag", default_value=False)
            self.assertFalse(flag_value)

    def test_fetch_token_client_credentials(self):
        client = self._create_kinde_client(GrantType.CLIENT_CREDENTIALS)
        self.mock_oauth2_session.return_value.fetch_token.return_value = {"access_token": "test_token"}
        client.fetch_token()
        self.mock_oauth2_session.return_value.fetch_token.assert_called_once()

    def test_fetch_token_authorization_code(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        self.mock_oauth2_session.return_value.fetch_token.return_value = {"access_token": "test_token"}
        client.fetch_token(authorization_response="https://example.com/callback?code=test_code")
        self.mock_oauth2_session.return_value.fetch_token.assert_called_once()

    @patch('kinde_sdk.kinde_api_client.ApiClient.call_api')
    def test_super_call_api_with_correct_args(self, mock_super_call_api):
        client = self._create_kinde_client(GrantType.CLIENT_CREDENTIALS)
        client._get_or_refresh_access_token = MagicMock()

        test_args = ("test_arg1", "test_arg2")
        test_kwargs = {"test_kwarg1": "hello", "test_kwarg2": "world"}
        client.call_api(*test_args, **test_kwargs)

        mock_super_call_api.assert_called_once_with(*test_args, **test_kwargs)

    def test_get_user_organization_uses_correct_key(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        with patch.object(KindeApiClient, '_decode_token_if_needed'):
            client._KindeApiClient__decoded_tokens = {
                "access_token": {"org_code": {"value":"hello"}}
            }
            org_claim = client.get_organization()
            self.assertEqual(org_claim, {'org_code': {'value': 'hello'}})

    @patch.object(KindeApiClient, 'get_claim')
    def test_get_permissions(self, mock_get_claim):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)

        def mock_get_claim_side_effect(key):
            if key == "org_code":
                return {"value": "org123"}
            elif key == "permissions":
                return {"value": ["read", "write", "delete"]}
        
        mock_get_claim.side_effect = mock_get_claim_side_effect

        result = client.get_permissions()

        expected_result = {
            "org_code": "org123",
            "permissions": ["read", "write", "delete"]
        }
        self.assertEqual(result, expected_result)

        mock_get_claim.assert_any_call("org_code")
        mock_get_claim.assert_any_call("permissions")
        self.assertEqual(mock_get_claim.call_count, 2)

    def test_fetch_token_headers_with_authorization_code(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        self.mock_oauth2_session.return_value.fetch_token.return_value = {"access_token": "test_token"}
        client.fetch_token(authorization_response="https://example.com/callback?code=test_code")

        self.mock_oauth2_session.return_value.fetch_token.assert_called_with(
            'https://example.kinde.com/oauth2/token',
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Kinde-SDK": "/".join(("Python", __version__)),
            },
            authorization_response='https://example.com/callback?code=test_code'
        )

    def test_fetch_token_headers_with_PKCE(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE_WITH_PKCE, code_verifier='1234')
        self.mock_oauth2_session.return_value.fetch_token.return_value = {"access_token": "test_token"}
        client.fetch_token(authorization_response="https://example.com/callback?code=test_code")

        call_kwargs = self.mock_oauth2_session.return_value.fetch_token.call_args[1]
        self.assertIn('code_verifier', call_kwargs)
        self.assertEqual(call_kwargs['code_verifier'], '1234')



class TestKindeApiClientAdditional(unittest.TestCase):
    def setUp(self):
        self.domain = "https://example.kinde.com"
        self.callback_url = "https://example.com/callback"
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"

    def _create_kinde_client(self, grant_type, code_verifier=None):
        return KindeApiClient(
            domain=self.domain,
            callback_url=self.callback_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type=grant_type,
            code_verifier = code_verifier
        )
            
    def test_get_login_url_state(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        login_url = client.get_login_url(state="hello")

        url_parts = urlparse(login_url)
        query = parse_qs(url_parts.query)

        self.assertEqual(query['state'][0], "hello")

    def test_get_register_url_state(self):
        client = self._create_kinde_client(GrantType.AUTHORIZATION_CODE)
        register_url = client.get_register_url(state="regis")
        
        url_parts = urlparse(register_url)
        query = parse_qs(url_parts.query)

        self.assertEqual(query['state'][0], "regis")
        self.assertEqual(query['start_page'][0], "registration")

if __name__ == '__main__':
    unittest.main()