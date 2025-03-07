import unittest
from urllib.parse import urlparse, parse_qs
from kinde_sdk.auth.oauth import OAuth

class TestOAuth(unittest.TestCase):
    def setUp(self):
        self.oauth = OAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost/callback",
            auth_url="https://example.com/auth",
            token_url="https://example.com/token",
            logout_url="https://example.com/logout",
        )

    def test_get_login_url(self):
        url = self.oauth.get_login_url(state="xyz")
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/auth")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/callback")
        self.assertEqual(query_params["scope"][0], "openid profile email")
        self.assertEqual(query_params["state"][0], "xyz")

    def test_get_login_url_with_pkce(self):
        url = self.oauth.get_login_url_with_pkce(state="xyz")
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/auth")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/callback")
        self.assertEqual(query_params["scope"][0], "openid profile email")
        self.assertEqual(query_params["state"][0], "xyz")
        self.assertIn("code_challenge", query_params)
        self.assertIn("code_challenge_method", query_params)

    def test_get_tokens_for_core(self):
        # Mock the session_manager and token_manager
        self.oauth.session_manager.set_user_data(
            "test_user_id",
            {"client_id": "test_client_id", "client_secret": "test_client_secret", "token_url": "https://example.com/token"},
            {"access_token": "test_access_token", "refresh_token": "test_refresh_token", "expires_in": 3600},
        )

        tokens = self.oauth.get_tokens_for_core("test_user_id")
        self.assertEqual(tokens["access_token"], "test_access_token")
        self.assertEqual(tokens["refresh_token"], "test_refresh_token")

    def test_logout(self):
        logout_url = self.oauth.logout("test_user_id")
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)

        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/logout")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["logout_uri"][0], "http://localhost/callback")

if __name__ == "__main__":
    unittest.main()