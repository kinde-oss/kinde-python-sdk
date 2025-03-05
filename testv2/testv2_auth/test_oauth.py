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
        )

    def test_get_authorization_url(self):
        url = self.oauth.get_authorization_url(scopes=["openid", "profile"], state="xyz")
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        self.assertEqual(parsed_url.scheme, "https")
        self.assertEqual(parsed_url.netloc, "example.com")
        self.assertEqual(parsed_url.path, "/auth")
        self.assertEqual(query_params["client_id"][0], "test_client_id")
        self.assertEqual(query_params["redirect_uri"][0], "http://localhost/callback")
        self.assertEqual(query_params["scope"][0], "openid profile")
        self.assertEqual(query_params["state"][0], "xyz")

if __name__ == "__main__":
    unittest.main()