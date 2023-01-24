from authlib.integrations.requests_client import OAuth2Session

from kinde_sdk.api_client import ApiClient


class KindeApiClient(ApiClient):

    GRAND_TYPES = ("client_credentials", "authorization_code")

    def __init__(
        self,
        *,
        domain,
        client_id,
        grant_type,
        client_secret=None,
        scope="openid profile email offline",
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
        self.authorization_endpoint = f"{self.domain}/oauth2/auth"
        self.token_endpoint = f"{self.domain}/oauth2/token"
        self.__access_token_obj = None

        self.access_token_obj = None

    def login(self):
        self.client = OAuth2Session(
            self.client_id,
            self.client_secret,
            scope=self.scope,
            token_endpoint=self.token_endpoint,
        )

    def get_authorization_url(self):
        self.authorization_url, self.state = self.client.create_authorization_url(
            self.authorization_endpoint
        )

    def fetch_token(self, authorization_response):
        self.access_token_obj = self.client.fetch_token(
            self.token_endpoint, authorization_response=authorization_response
        )

    def call_api(self, *args, **kwargs):
        self.get_or_refresh_auth_token()
        return super().call_api(*args, **kwargs)

    def get_or_refresh_auth_token(self):
        if not self.__access_token_obj or (
            self.__access_token_obj and self.__access_token_obj.is_expired()
        ):
            self.__access_token_obj = self.client.fetch_token(
                self.token_endpoint,
                authorization_response=self.authorization_endpoint,
                grant_type=self.grant_type,
            )
            self.configuration.access_token = self.__access_token_obj.get(
                "access_token"
            )
