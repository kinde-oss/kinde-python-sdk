import unittest
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
        self.assertIn("client_id=test_client_id", url)
        self.assertIn("scope=openid profile", url)
        self.assertIn("state=xyz", url)
