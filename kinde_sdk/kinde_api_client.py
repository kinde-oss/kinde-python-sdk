from authlib.integrations.requests_client import OAuth2Session
import jwt

from kinde_sdk.api_client import ApiClient


class KindeApiClient(ApiClient):

    GRAND_TYPES = (
        "client_credentials",
        "authorization_code",
        "authorization_code_with_pkce",
    )
    TOKEN_NAMES = ("access_token", "id_token")

    def __init__(
        self,
        *,
        domain,
        client_id,
        grant_type,
        client_secret=None,
        code_verifier = None,
        scope="openid profile email offline",
        audience=None,
        **kwargs,
    ):
        if grant_type not in self.GRAND_TYPES:
            raise ValueError(
                f"Please provide correct grant_type from list: {self.GRAND_TYPES}"
            )
        super().__init__(**kwargs)
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        self.scope = scope
        self.code_verifier = code_verifier
        self.audience = audience
        self.authorization_endpoint = f"{self.domain}/oauth2/auth"
        self.token_endpoint = f"{self.domain}/oauth2/token"
        self.logout_endpoint = f"{self.domain}/logout"
        self.__access_token_obj = None
        self.clear_decoded_tokens()

        auth_session_params = {
            "scope": self.scope,
            "token_endpoint": self.token_endpoint,
        }
        create_authorization_url_params = {}
        if self.grant_type == "authorization_code_with_pkce":
            if self.code_verifier is None:
                raise Exception("No code_verifier")
            auth_session_params["code_challenge_method"] = "S256"
            create_authorization_url_params["code_verifier"] = self.code_verifier

        self.client = OAuth2Session(
            self.client_id, self.client_secret, **auth_session_params
        )

        self.login_url, self.state = self.client.create_authorization_url(
            self.authorization_endpoint, **create_authorization_url_params
        )

        self.registration_url = f"{self.login_url}&start_page=registration"

    def login(self):
        return self.login_url

    def register(self):
        return self.registration_url

    def fetch_token(self, authorization_response=None):
        if self.grant_type == "client_credentials":
            params = {"grant_type": "client_credentials"}
        else:
            if authorization_response is None:
                raise Exception("No authorization_response")
            params = {"authorization_response": authorization_response}
        if self.grant_type == "authorization_code_with_pkce":
            params["code_verifier"] = self.code_verifier
        self.__access_token_obj = self.client.fetch_token(self.token_endpoint, **params)
        self.configuration.access_token = self.__access_token_obj.get("access_token")
        self.clear_decoded_tokens()

    def refresh_token(self):
        if refresh_token := self.__access_token_obj.get("refresh_token"):
            self.__access_token_obj = self.client.refresh_token(
                self.token_endpoint,
                refresh_token=refresh_token,
            )
            self.configuration.access_token = self.__access_token_obj.get(
                "access_token"
            )
            self.clear_decoded_tokens()

    def call_api(self, *args, **kwargs):
        self.get_or_refresh_auth_token()
        return super().call_api(*args, **kwargs)

    def get_or_refresh_auth_token(self):
        if self.grant_type == "client_credentials":
            if not self.__access_token_obj or self.__access_token_obj.is_expired():
                self.fetch_token()
        else:
            if not self.__access_token_obj:
                raise Exception("Please login or register first")
            if self.__access_token_obj.is_expired():
                self.refresh_token()

    def is_authenticated(self):
        if self.__access_token_obj and not self.__access_token_obj.is_expired():
            return True
        return False

    def logout(self, redirect):
        self.__access_token_obj = None
        self.configuration.access_token = None
        return f"{self.logout_endpoint}?redirect={redirect}"

    def clear_decoded_tokens(self):
        self.__decoded_tokens = {}

    def decode_token_if_needed(self, token_name):
        if token_name not in self.__decoded_tokens:
            if token := self.client.token.get(token_name):
                self.__decoded_tokens[token_name] = jwt.decode(
                    token, options={"verify_signature": False}
                )
            else:
                raise Exception("Token doesn't exist")

    def get_claim(self, key, token_name="access_token"):
        if token_name not in self.TOKEN_NAMES:
            raise Exception(f"Please use only tokens from list: {self.TOKEN_NAMES}")
        self.decode_token_if_needed(token_name)
        return self.__decoded_tokens[token_name].get(key)

    def get_user_details(self):
        return {
            "id": self.get_claim("sub", "id_token"),
            "given_name": self.get_claim("given_name", "id_token"),
            "family_name": self.get_claim("family_name", "id_token"),
            "email": self.get_claim("email", "id_token"),
        }

    def get_permissions(self):
        return {
            "org_code": self.get_claim("org_code"),
            "permissions": self.get_claim("permissions"),
        }

    def get_permission(self, permission):
        return {
            "org_code": self.get_claim("org_code"),
            "is_granted": permission in self.get_claim("permissions"),
        }

    def get_organization(self):
        return {
            "org_code": self.get_claim("org_code"),
        }

    def get_user_organizations(self):
        return {
            "org_codes": self.get_claim("org_codes", "id_token"),
        }
