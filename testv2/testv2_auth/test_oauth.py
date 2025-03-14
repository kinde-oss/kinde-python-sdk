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
            userinfo_url="https://example.com/userinfo"
        )
    
    def test_register(self):
        url = self.oauth.get_login_url(state="xyz", scope=["openid", "profile", "email"], login_type="register")
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/auth")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/callback")
        self.assertEqual(query_params["scope"][0], "openid profile email")
        self.assertEqual(query_params["state"][0], "xyz")
        self.assertEqual(query_params["login_type"][0], "register")

    def test_login(self):
        url = self.oauth.get_login_url(state="xyz", scope=["openid", "profile", "email"], login_type="login")
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/auth")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/callback")
        self.assertEqual(query_params["scope"][0], "openid profile email")
        self.assertEqual(query_params["state"][0], "xyz")
        self.assertEqual(query_params["login_type"][0], "login")

    def test_logout(self):
        logout_url = self.oauth.logout(params={"state": "xyz"})
        parsed_url = urlparse(logout_url)
        query_params = parse_qs(parsed_url.query)

        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/logout")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["logout_uri"][0], "http://localhost/callback")
        self.assertEqual(query_params["state"][0], "xyz")

if __name__ == "__main__":
    unittest.main()