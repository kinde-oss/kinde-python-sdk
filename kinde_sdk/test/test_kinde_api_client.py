import jwt
from unittest import TestCase
from unittest.mock import patch

from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import (
    GrantType,
    KindeApiClient,
    KindeConfigurationException,
    KindeRetrieveException,
    KindeTokenException,
)
from kinde_sdk import __version__
from authlib.oauth2.rfc6749 import OAuth2Token


class BaseTestCase(TestCase):
    def setUp(self):
        self.host = "HOST_ADDRESS"
        self.callback_url = "CALLBACK_URL"
        self.client_id = "CLIENT_ID"
        self.client_secret = "CLIENT_SECRET"
        self.login_url = "login_url"
        self.registration_url = f"{self.login_url}&start_page=registration"
        self.create_org_url = f"{self.registration_url}&is_create_org=true"
        self.scope = "openid profile email offline"
        self.state = "state"
        self.fake_access_token = jwt.encode(
            self._get_decoded_token(), "secret", algorithm="HS256"
        )
        self.fake_id_token = jwt.encode(
            self._get_user_details(), "secret", algorithm="HS256"
        )

    def _create_kinde_client(self, auth_session_mock, grant_type, **kwargs):
        auth_session_mock.return_value.create_authorization_url.return_value = [
            self.login_url,
            self.state,
        ]
        configuration = Configuration(host=self.host)
        kinde_client = KindeApiClient(
            configuration=configuration,
            domain=self.host,
            callback_url=self.callback_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type=grant_type,
            **kwargs,
        )
        return kinde_client

    def _get_decoded_token(self):
        return {
            "aud": [],
            "azp": "123456789",
            "exp": 9999999999,
            "feature_flags": {
                "competitions_limit": {"t": "i", "v": 5},
                "is_dark_mode": {"t": "b", "v": True},
                "name": {"t": "s", "v": "pink"},
                "theme": {"t": "s", "v": "pink"},
            },
            "iat": 9999999999,
            "iss": "https://user-dev.au.kinde.com",
            "jti": "12345678-1234-1234-1234-123456789101",
            "org_code": "org_12345678901",
            "permissions": [],
            "scp": ["openid", "profile", "email", "offline"],
            "sub": "kp:1234567890",
        }

    def _get_token(self, params={}):
        return OAuth2Token(
            params={
                "access_token": self.fake_access_token,
                "expires_in": 9999999999,
                "scope": "openid profile email offline",
                "token_type": "bearer",
                "expires_at": 9999999999,
                **params,
            }
        )

    def _get_token_authorization_code(self):
        return self._get_token(
            {"id_token": self.fake_id_token, "refresh_token": "refresh_token"}
        )

    def _get_token_authorization_code_expired(self):
        return self._get_token(
            {
                "expires_in": 1,
                "expires_at": 1,
                "id_token": self.fake_id_token,
                "refresh_token": "refresh_token",
            }
        )

    def _get_token_authorization_code_invalid(self):
        return self._get_token(
            {
                "expires_in": 1,
                "expires_at": 1,
                "id_token": self.fake_id_token,
                "refresh_token": "",
            }
        )

    def _get_user_details(self):
        return {
            "id": 123456789,
            "given_name": "given_name",
            "family_name": "family_name",
            "email": "given_name@example.com",
            "picture": "picture_url",
        }


class TestKindeApiClientClientCredentials(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.grant_type = GrantType.CLIENT_CREDENTIALS

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_create_client(self, auth_session_mock):
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        auth_session_mock.assert_called_with(
            self.client_id,
            self.client_secret,
            redirect_uri=self.callback_url,
            scope="",
            token_endpoint=kinde_client.token_endpoint,
        )
        auth_session_mock.return_value.create_authorization_url.assert_called_with(
            kinde_client.authorization_endpoint
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_fetch_token(self, auth_session_mock):
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        token_endpoint = kinde_client.token_endpoint
        auth_session_mock.return_value.fetch_token.assert_called_with(
            token_endpoint,
            grant_type=GrantType.CLIENT_CREDENTIALS.value,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Kinde-SDK": "/".join(("Python", __version__)),
            },
        )
        self.assertEqual(
            kinde_client.configuration.access_token, self._get_token()["access_token"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_claim(self, auth_session_mock):
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        org_code_expected = {
            "name": "org_code",
            "value": self._get_decoded_token()["org_code"],
        }
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        org_code = kinde_client.get_claim("org_code")
        self.assertEqual(org_code, org_code_expected)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_claim_error(self, auth_session_mock):
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        org_code_expected = {
            "name": "org_code",
            "value": self._get_decoded_token()["org_code"],
        }
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        with self.assertRaises(KindeTokenException):
            kinde_client.get_claim("org_code", "not_exist")

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_flag_success(self, auth_session_mock):
        fake_flag = "theme"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        flag = kinde_client.get_flag(fake_flag)["value"]
        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_flag_not_exist_has_default(self, auth_session_mock):
        fake_flag = "new_feature"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        kinde_client.get_flag(fake_flag, default_value=1)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_flag_wrong_flag_type(self, auth_session_mock):
        fake_flag = "competitions_limit"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_flag(fake_flag, default_value=3, flag_type="s")["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_flag_not_exist_no_default(self, auth_session_mock):
        fake_flag = "new_feature"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_boolean_flag_success(self, auth_session_mock):
        fake_flag = "is_dark_mode"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()
        flag = kinde_client.get_boolean_flag(fake_flag)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_boolean_flag_success_has_default(
        self, auth_session_mock
    ):
        fake_flag = "is_dark_mode"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()
        flag = kinde_client.get_boolean_flag(fake_flag, default_value=False)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_boolean_flag_not_exist_has_default(
        self, auth_session_mock
    ):
        fake_flag = "new_feature"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()
        flag = kinde_client.get_boolean_flag(fake_flag, default_value=False)

        self.assertEqual(flag, False)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_boolean_flag_not_exist_no_default(
        self, auth_session_mock
    ):
        fake_flag = "competitions_limit"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_boolean_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_boolean_flag_wrong_type_has_default(
        self, auth_session_mock
    ):
        fake_flag = "theme"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_boolean_flag(fake_flag, default_value=False)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_string_flag_success(self, auth_session_mock):
        fake_flag = "theme"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()
        flag = kinde_client.get_string_flag(fake_flag)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_string_flag_success_has_default(
        self, auth_session_mock
    ):
        fake_flag = "theme"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()
        flag = kinde_client.get_string_flag(fake_flag, default_value="orange")

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_string_flag_not_exist_has_default(
        self, auth_session_mock
    ):
        fake_flag = "cta_color"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()
        flag = kinde_client.get_string_flag(fake_flag, default_value="blue")

        self.assertEqual(flag, "blue")

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_string_flag_not_exist_no_default(
        self, auth_session_mock
    ):
        fake_flag = "cta_color"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_string_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_string_flag_wrong_type_has_default(
        self, auth_session_mock
    ):
        fake_flag = "is_dark_mode"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_string_flag(fake_flag, default_value=False)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_integer_flag_success(self, auth_session_mock):
        fake_flag = "competitions_limit"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()
        flag = kinde_client.get_integer_flag(fake_flag)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_integer_flag_success_has_default(
        self, auth_session_mock
    ):
        fake_flag = "competitions_limit"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()
        flag = kinde_client.get_integer_flag(fake_flag, default_value=3)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_integer_flag_not_exist_has_default(
        self, auth_session_mock
    ):
        fake_flag = "team_count"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()
        flag = kinde_client.get_integer_flag(fake_flag, default_value=2)

        self.assertEqual(flag, 2)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_integer_flag_not_exist_no_default(
        self, auth_session_mock
    ):
        fake_flag = "team_count"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_integer_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_get_integer_flag_wrong_type_has_default(
        self, auth_session_mock
    ):
        fake_flag = "is_dark_mode"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_integer_flag(fake_flag, default_value=False)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_is_authenticated(
        self, auth_session_mock
    ):
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token()

        is_authenticated = kinde_client.is_authenticated()
        self.assertTrue(is_authenticated)


class TestKindeApiClientAuthorizationCode(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.grant_type = GrantType.AUTHORIZATION_CODE

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_create_client(self, auth_session_mock):
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        auth_session_mock.assert_called_with(
            self.client_id,
            self.client_secret,
            scope=self.scope,
            token_endpoint=kinde_client.token_endpoint,
            redirect_uri=self.callback_url,
        )
        auth_session_mock.return_value.create_authorization_url.assert_called_with(
            kinde_client.authorization_endpoint
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_login(self, auth_session_mock):
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        self.assertEqual(kinde_client.get_login_url(), self.login_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_register(self, auth_session_mock):
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        self.assertEqual(kinde_client.get_register_url(), self.registration_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_create_org(self, auth_session_mock):
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        self.assertEqual(kinde_client.create_org(), self.create_org_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_fetch_token(self, auth_session_mock):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        token_endpoint = kinde_client.token_endpoint
        auth_session_mock.return_value.fetch_token.assert_called_with(
            token_endpoint,
            authorization_response="TEST",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Kinde-SDK": "/".join(("Python", __version__)),
            },
        )
        self.assertEqual(
            kinde_client.configuration.access_token,
            self._get_token_authorization_code()["access_token"],
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_claim(self, auth_session_mock):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        org_code_expected = {
            "name": "org_code",
            "value": self._get_decoded_token()["org_code"],
        }
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        org_code = kinde_client.get_claim("org_code")
        self.assertEqual(org_code, org_code_expected)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_claim_error(self, auth_session_mock):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeTokenException):
            kinde_client.get_claim("org_code", "not_exist")

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_user_details(self, auth_session_mock):
        user_details_key = ["id", "given_name", "family_name", "email", "picture"]
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        user = kinde_client.get_user_details()
        self.assertEqual(list(user.keys()), user_details_key)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_flag_success(self, auth_session_mock):
        fake_flag = "theme"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        flag = kinde_client.get_flag(fake_flag)["value"]
        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_flag_not_exist_has_default(self, auth_session_mock):
        fake_flag = "new_feature"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_flag_wrong_flag_type(self, auth_session_mock):
        fake_flag = "competitions_limit"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_flag(fake_flag, default_value=3, flag_type="s")["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_flag_not_exist_no_default(self, auth_session_mock):
        fake_flag = "new_feature"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_boolean_flag_success(self, auth_session_mock):
        fake_flag = "is_dark_mode"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_boolean_flag(fake_flag)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_boolean_flag_success_has_default(
        self, auth_session_mock
    ):
        fake_flag = "is_dark_mode"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_boolean_flag(fake_flag, default_value=False)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_boolean_flag_not_exist_has_default(
        self, auth_session_mock
    ):
        fake_flag = "new_feature"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_boolean_flag(fake_flag, default_value=False)

        self.assertEqual(flag, False)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_boolean_flag_not_exist_no_default(
        self, auth_session_mock
    ):
        fake_flag = "competitions_limit"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_boolean_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_boolean_flag_wrong_type_has_default(
        self, auth_session_mock
    ):
        fake_flag = "theme"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_boolean_flag(fake_flag, default_value=False)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_string_flag_success(self, auth_session_mock):
        fake_flag = "theme"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_string_flag(fake_flag)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_string_flag_success_has_default(
        self, auth_session_mock
    ):
        fake_flag = "theme"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_string_flag(fake_flag, default_value="orange")

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_string_flag_not_exist_has_default(
        self, auth_session_mock
    ):
        fake_flag = "cta_color"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_string_flag(fake_flag, default_value="blue")

        self.assertEqual(flag, "blue")

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_string_flag_not_exist_no_default(
        self, auth_session_mock
    ):
        fake_flag = "cta_color"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_string_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_string_flag_wrong_type_has_default(
        self, auth_session_mock
    ):
        fake_flag = "is_dark_mode"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_string_flag(fake_flag, default_value=False)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_integer_flag_success(self, auth_session_mock):
        fake_flag = "competitions_limit"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_integer_flag(fake_flag)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_integer_flag_success_has_default(
        self, auth_session_mock
    ):
        fake_flag = "competitions_limit"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_integer_flag(fake_flag, default_value=3)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_integer_flag_not_exist_has_default(
        self, auth_session_mock
    ):
        fake_flag = "team_count"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_integer_flag(fake_flag, default_value=2)

        self.assertEqual(flag, 2)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_integer_flag_not_exist_no_default(
        self, auth_session_mock
    ):
        fake_flag = "team_count"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_integer_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_integer_flag_wrong_type_has_default(
        self, auth_session_mock
    ):
        fake_flag = "is_dark_mode"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_integer_flag(fake_flag, default_value=False)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_or_refresh_access_token_expired_access_token(
        self, auth_session_mock
    ):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code_expired()
        )

        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        kinde_client._get_or_refresh_access_token()

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_get_or_refresh_access_token_expired_access_refresh_token(
        self, auth_session_mock
    ):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code_invalid()
        )

        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        with self.assertRaises(KindeTokenException):
            kinde_client._get_or_refresh_access_token()

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_is_authenticated(
        self, auth_session_mock
    ):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        is_authenticated = kinde_client.is_authenticated()
        self.assertTrue(is_authenticated)


class TestKindeApiClientAuthorizationCodeWithPKCE(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.grant_type = GrantType.AUTHORIZATION_CODE_WITH_PKCE
        self.code_verifier = "CODE_VERIFIER"
        self.code_challenge_method = "S256"

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_create_client(self, auth_session_mock):
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        auth_session_mock.assert_called_with(
            self.client_id,
            self.client_secret,
            scope=self.scope,
            token_endpoint=kinde_client.token_endpoint,
            redirect_uri=self.callback_url,
            code_challenge_method=self.code_challenge_method,
        )
        auth_session_mock.return_value.create_authorization_url.assert_called_with(
            kinde_client.authorization_endpoint, code_verifier=self.code_verifier
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_create_client_without_code_verifier(
        self, auth_session_mock
    ):
        with self.assertRaises(KindeConfigurationException):
            self._create_kinde_client(auth_session_mock, grant_type=self.grant_type)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_login(self, auth_session_mock):
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        self.assertEqual(kinde_client.get_login_url(), self.login_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_register(self, auth_session_mock):
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        self.assertEqual(kinde_client.get_register_url(), self.registration_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_create_org(self, auth_session_mock):
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        self.assertEqual(kinde_client.create_org(), self.create_org_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_fetch_token(self, auth_session_mock):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        token_endpoint = kinde_client.token_endpoint
        auth_session_mock.return_value.fetch_token.assert_called_with(
            token_endpoint,
            authorization_response="TEST",
            code_verifier=self.code_verifier,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Kinde-SDK": "/".join(("Python", __version__)),
            },
        )
        self.assertEqual(
            kinde_client.configuration.access_token,
            self._get_token_authorization_code()["access_token"],
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_claim(self, auth_session_mock):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        org_code_expected = {
            "name": "org_code",
            "value": self._get_decoded_token()["org_code"],
        }
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        org_code = kinde_client.get_claim("org_code")
        self.assertEqual(org_code, org_code_expected)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_claim_error(self, auth_session_mock):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeTokenException):
            kinde_client.get_claim("org_code", "not_exist")

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_user_details(self, auth_session_mock):
        user_details_key = ["id", "given_name", "family_name", "email", "picture"]
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        user = kinde_client.get_user_details()
        self.assertEqual(list(user.keys()), user_details_key)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_flag_success(self, auth_session_mock):
        fake_flag = "theme"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        flag = kinde_client.get_flag(fake_flag)["value"]
        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_flag_not_exist_has_default(
        self, auth_session_mock
    ):
        fake_flag = "new_feature"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_flag_wrong_flag_type(
        self, auth_session_mock
    ):
        fake_flag = "competitions_limit"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_flag(fake_flag, default_value=3, flag_type="s")["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_flag_not_exist_no_default(
        self, auth_session_mock
    ):
        fake_flag = "new_feature"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_boolean_flag_success(
        self, auth_session_mock
    ):
        fake_flag = "is_dark_mode"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_boolean_flag(fake_flag)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_boolean_flag_success_has_default(
        self, auth_session_mock
    ):
        fake_flag = "is_dark_mode"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_boolean_flag(fake_flag, default_value=False)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_boolean_flag_not_exist_has_default(
        self, auth_session_mock
    ):
        fake_flag = "new_feature"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_boolean_flag(fake_flag, default_value=False)

        self.assertEqual(flag, False)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_boolean_flag_not_exist_no_default(
        self, auth_session_mock
    ):
        fake_flag = "competitions_limit"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_boolean_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_boolean_flag_wrong_type_has_default(
        self, auth_session_mock
    ):
        fake_flag = "theme"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_boolean_flag(fake_flag, default_value=False)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_string_flag_success(
        self, auth_session_mock
    ):
        fake_flag = "theme"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_string_flag(fake_flag)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_string_flag_success_has_default(
        self, auth_session_mock
    ):
        fake_flag = "theme"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_string_flag(fake_flag, default_value="orange")

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_string_flag_not_exist_has_default(
        self, auth_session_mock
    ):
        fake_flag = "cta_color"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_string_flag(fake_flag, default_value="blue")

        self.assertEqual(flag, "blue")

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_string_flag_not_exist_no_default(
        self, auth_session_mock
    ):
        fake_flag = "cta_color"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_string_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_string_flag_wrong_type_has_default(
        self, auth_session_mock
    ):
        fake_flag = "is_dark_mode"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_string_flag(fake_flag, default_value=False)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_integer_flag_success(
        self, auth_session_mock
    ):
        fake_flag = "competitions_limit"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_integer_flag(fake_flag)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_integer_flag_success_has_default(
        self, auth_session_mock
    ):
        fake_flag = "competitions_limit"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_integer_flag(fake_flag, default_value=3)

        self.assertEqual(
            flag, self._get_decoded_token()["feature_flags"][fake_flag]["v"]
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_integer_flag_not_exist_has_default(
        self, auth_session_mock
    ):
        fake_flag = "team_count"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        flag = kinde_client.get_integer_flag(fake_flag, default_value=2)

        self.assertEqual(flag, 2)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_integer_flag_not_exist_no_default(
        self, auth_session_mock
    ):
        fake_flag = "team_count"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_integer_flag(fake_flag)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_integer_flag_wrong_type_has_default(
        self, auth_session_mock
    ):
        fake_flag = "is_dark_mode"
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code()
        )
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        with self.assertRaises(KindeRetrieveException):
            kinde_client.get_integer_flag(fake_flag, default_value=False)["value"]

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_or_refresh_access_token_expired_access_token(
        self, auth_session_mock
    ):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code_expired()
        )

        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        kinde_client._get_or_refresh_access_token()

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_get_or_refresh_access_token_expired_access_refresh_token(
        self, auth_session_mock
    ):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = (
            self._get_token_authorization_code_invalid()
        )

        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)
        with self.assertRaises(KindeTokenException):
            kinde_client._get_or_refresh_access_token()
    
    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_is_authenticated(
        self, auth_session_mock
    ):
        fake_auth_response = "TEST"
        auth_session_mock.return_value.fetch_token.return_value = self._get_token()
        kinde_client = self._create_kinde_client(
            auth_session_mock,
            grant_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        is_authenticated = kinde_client.is_authenticated()
        self.assertTrue(is_authenticated)
