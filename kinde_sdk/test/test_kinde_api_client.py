from unittest import TestCase
from unittest.mock import patch

from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import (
    GrantType,
    KindeApiClient,
    KindeConfigurationException,
)


class BaseTestCase(TestCase):
    def setUp(self):
        self.host = "HOST_ADDRESS"
        self.client_id = "CLIENT_ID"
        self.client_secret = "CLIENT_SECRET"
        self.login_url = "login_url"
        self.registration_url = f"{self.login_url}&start_page=registration"
        self.create_org_url = f"{self.registration_url}&is_create_org=true"
        self.scope = "openid profile email offline"
        self.state = "state"

    def _create_kindle_client(self, auth_session_mock, grand_type, **kwargs):
        auth_session_mock.return_value.create_authorization_url.return_value = [
            self.login_url,
            self.state,
        ]
        configuration = Configuration(host=self.host)
        kinde_client = KindeApiClient(
            configuration=configuration,
            domain=self.host,
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type=grand_type,
            **kwargs,
        )
        return kinde_client


class TestKindeApiClientClientCredentials(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.grant_type = GrantType.CLIENT_CREDENTIALS

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_create_client(self, auth_session_mock):
        kinde_client = self._create_kindle_client(
            auth_session_mock, grand_type=self.grant_type
        )

        auth_session_mock.assert_called_with(
            self.client_id,
            self.client_secret,
            scope=self.scope,
            token_endpoint=kinde_client.token_endpoint,
        )
        auth_session_mock.return_value.create_authorization_url.assert_called_with(
            kinde_client.authorization_endpoint
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_client_credentials_fetch_token(self, auth_session_mock):
        fake_access_token = {"access_token": "123456789123456789"}
        auth_session_mock.return_value.fetch_token.return_value = fake_access_token
        kinde_client = self._create_kindle_client(
            auth_session_mock, grand_type=self.grant_type
        )

        kinde_client.fetch_token()

        token_endpoint = kinde_client.token_endpoint
        auth_session_mock.return_value.fetch_token.assert_called_with(
            token_endpoint, grant_type=GrantType.CLIENT_CREDENTIALS.value
        )
        self.assertEqual(
            kinde_client.configuration.access_token, fake_access_token["access_token"]
        )


class TestKindeApiClientAutorizationCode(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.grant_type = GrantType.AUTORIZATION_CODE

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_create_client(self, auth_session_mock):
        kinde_client = self._create_kindle_client(
            auth_session_mock, grand_type=self.grant_type
        )

        auth_session_mock.assert_called_with(
            self.client_id,
            self.client_secret,
            scope=self.scope,
            token_endpoint=kinde_client.token_endpoint,
        )
        auth_session_mock.return_value.create_authorization_url.assert_called_with(
            kinde_client.authorization_endpoint
        )

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_login(self, auth_session_mock):
        kinde_client = self._create_kindle_client(
            auth_session_mock, grand_type=self.grant_type
        )

        self.assertEqual(kinde_client.login(), self.login_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_register(self, auth_session_mock):
        kinde_client = self._create_kindle_client(
            auth_session_mock, grand_type=self.grant_type
        )

        self.assertEqual(kinde_client.register(), self.registration_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_create_org(self, auth_session_mock):
        kinde_client = self._create_kindle_client(
            auth_session_mock, grand_type=self.grant_type
        )

        self.assertEqual(kinde_client.create_org(), self.create_org_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_fetch_token(self, auth_session_mock):
        fake_auth_response = "TEST"
        fake_access_token = {"access_token": "123456789123456789"}
        auth_session_mock.return_value.fetch_token.return_value = fake_access_token
        kinde_client = self._create_kindle_client(
            auth_session_mock, grand_type=self.grant_type
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        token_endpoint = kinde_client.token_endpoint
        auth_session_mock.return_value.fetch_token.assert_called_with(
            token_endpoint, authorization_response="TEST"
        )
        self.assertEqual(
            kinde_client.configuration.access_token, fake_access_token["access_token"]
        )


class TestKindeApiClientAutorizationCodeWithPKCE(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.grant_type = GrantType.AUTORIZATION_CODE_WITH_PKCE
        self.code_verifier = "CODE_VERIFIER"
        self.code_challenge_method = "S256"

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_create_client(self, auth_session_mock):
        kinde_client = self._create_kindle_client(
            auth_session_mock,
            grand_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        auth_session_mock.assert_called_with(
            self.client_id,
            self.client_secret,
            scope=self.scope,
            token_endpoint=kinde_client.token_endpoint,
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
            self._create_kindle_client(auth_session_mock, grand_type=self.grant_type)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_login(self, auth_session_mock):
        kinde_client = self._create_kindle_client(
            auth_session_mock,
            grand_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        self.assertEqual(kinde_client.login(), self.login_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_register(self, auth_session_mock):
        kinde_client = self._create_kindle_client(
            auth_session_mock,
            grand_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        self.assertEqual(kinde_client.register(), self.registration_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_create_org(self, auth_session_mock):
        kinde_client = self._create_kindle_client(
            auth_session_mock,
            grand_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        self.assertEqual(kinde_client.create_org(), self.create_org_url)

    @patch("kinde_sdk.kinde_api_client.OAuth2Session")
    def test_authorization_code_with_pkce_fetch_token(self, auth_session_mock):
        fake_auth_response = "TEST"
        fake_access_token = {"access_token": "123456789123456789"}
        auth_session_mock.return_value.fetch_token.return_value = fake_access_token
        kinde_client = self._create_kindle_client(
            auth_session_mock,
            grand_type=self.grant_type,
            code_verifier=self.code_verifier,
        )

        kinde_client.fetch_token(authorization_response=fake_auth_response)

        token_endpoint = kinde_client.token_endpoint
        auth_session_mock.return_value.fetch_token.assert_called_with(
            token_endpoint,
            authorization_response="TEST",
            code_verifier=self.code_verifier,
        )
        self.assertEqual(
            kinde_client.configuration.access_token, fake_access_token["access_token"]
        )
