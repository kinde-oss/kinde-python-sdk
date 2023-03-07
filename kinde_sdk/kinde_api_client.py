from enum import Enum
from typing import Any, Dict, List, Optional

from authlib.integrations.requests_client import OAuth2Session
import jwt

from kinde_sdk.api_client import ApiClient
from kinde_sdk.exceptions import (
    KindeConfigurationException,
    KindeLoginException,
    KindeTokenException,
)


class GrantType(Enum):
    CLIENT_CREDENTIALS = "client_credentials"
    AUTHORIZATION_CODE = "authorization_code"
    AUTHORIZATION_CODE_WITH_PKCE = "authorization_code_with_pkce"


class KindeApiClient(ApiClient):

    TOKEN_NAMES = ("access_token", "id_token")

    def __init__(
        self,
        *,
        domain,
        callback_url,
        client_id,
        grant_type,
        client_secret=None,
        code_verifier=None,
        scope="openid profile email offline",
        audience=None,
        org_code=None,
        **kwargs,
    ):
        if not isinstance(grant_type, GrantType):
            raise ValueError(
                f"Please provide a grant_type one of the following: {list(GrantType)}"
            )
        super().__init__(**kwargs)
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.grant_type = grant_type
        if self.grant_type == GrantType.CLIENT_CREDENTIALS:
            self.scope = ""
        else:
            self.scope = scope
        self.code_verifier = code_verifier
        self.audience = audience
        self.org_code = org_code
        self.callback_url = callback_url
        self.authorization_endpoint = f"{self.domain}/oauth2/auth"
        self.token_endpoint = f"{self.domain}/oauth2/token"
        self.logout_endpoint = f"{self.domain}/logout"

        self.__access_token_obj = None

        self._clear_decoded_tokens()

        auth_session_params = {
            "scope": self.scope,
            "token_endpoint": self.token_endpoint,
        }
        create_authorization_url_params = {}
        if self.grant_type == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
            if self.code_verifier is None:
                raise KindeConfigurationException(
                    '"code_verifier" parameter is required when a grant_type is AUTHORIZATION_CODE_WITH_PKCE.'
                )
            auth_session_params["code_challenge_method"] = "S256"
            create_authorization_url_params["code_verifier"] = self.code_verifier

        self.client = OAuth2Session(
            self.client_id,
            self.client_secret,
            redirect_uri=self.callback_url,
            **auth_session_params,
        )

        self.login_url, self.state = self.client.create_authorization_url(
            self.authorization_endpoint, **create_authorization_url_params
        )

        if self.audience:
            self.login_url = f"{self.login_url}&audience={self.audience}"
        if self.org_code:
            self.login_url = f"{self.login_url}&org_code={self.org_code}"

        self.registration_url = f"{self.login_url}&start_page=registration"
        self.create_org_url = f"{self.registration_url}&is_create_org=true"

    def get_login_url(self) -> str:
        return self.login_url

    def get_register_url(self) -> str:
        return self.registration_url

    def create_org(self) -> str:
        return self.create_org_url

    def fetch_token(self, authorization_response: Optional[str] = None) -> None:
        if self.grant_type == GrantType.CLIENT_CREDENTIALS:
            params = {"grant_type": "client_credentials"}
            if self.audience:
                params["audience"] = self.audience
        else:
            if authorization_response is None:
                raise KindeConfigurationException(
                    '"authorization_response" parameter is required when grant_type is different than CLIENT_CREDENTIALS.'
                )
            params = {"authorization_response": authorization_response}
        if self.grant_type == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
            params["code_verifier"] = self.code_verifier
        self.__access_token_obj = self.client.fetch_token(self.token_endpoint, **params)
        self.configuration.access_token = self.__access_token_obj.get("access_token")
        self._clear_decoded_tokens()

    def refresh_token(self) -> None:
        refresh_token = self.__access_token_obj.get("refresh_token")
        if refresh_token:
            self.__access_token_obj = self.client.refresh_token(
                self.token_endpoint,
                refresh_token=refresh_token,
            )
            self.configuration.access_token = self.__access_token_obj.get(
                "access_token"
            )
            self._clear_decoded_tokens()

    def call_api(self, *args, **kwargs) -> Any:
        self.get_or_refresh_access_token()
        return super().call_api(*args, **kwargs)

    def get_or_refresh_access_token(self) -> None:
        if self.grant_type == GrantType.CLIENT_CREDENTIALS:
            if not self.__access_token_obj or self.__access_token_obj.is_expired():
                self.fetch_token()
        else:
            if not self.__access_token_obj:
                raise KindeLoginException(
                    'Please use "get_login_url()" or "get_register_url()" first.'
                )
            if self.__access_token_obj.is_expired():
                self.refresh_token()

    def is_authenticated(self) -> bool:
        return self.__access_token_obj and not self.__access_token_obj.is_expired()

    def logout(self, redirect_to: str) -> str:
        self.__access_token_obj = None
        self.configuration.access_token = None
        return f"{self.logout_endpoint}?redirect={redirect_to}"

    def _clear_decoded_tokens(self) -> None:
        self.__decoded_tokens = {}

    def _decode_token_if_needed(self, token_name: str) -> None:
        if token_name not in self.__decoded_tokens:
            if not self.__access_token_obj:
                raise KindeTokenException(
                    "Access token doesn't exist.\n"
                    "When grant_type is CLIENT_CREDENTIALS use fetch_token().\n"
                    'For other grant_type use "get_login_url()" or "get_register_url()".'
                )
            token = self.__access_token_obj.get(token_name)
            if token:
                self.__decoded_tokens[token_name] = jwt.decode(
                    token, options={"verify_signature": False}
                )
            else:
                raise KindeTokenException(f"Token {token_name} doesn't exist.")

    def get_claim(self, key: str, token_name: str = "access_token") -> Any:
        if token_name not in self.TOKEN_NAMES:
            raise KindeTokenException(
                f"Please use only tokens from the list: {self.TOKEN_NAMES}"
            )
        self._decode_token_if_needed(token_name)
        return self.__decoded_tokens[token_name].get(key)

    def get_user_details(self) -> Dict[str, str]:
        return {
            "id": self.get_claim("sub", "id_token"),
            "given_name": self.get_claim("given_name", "id_token"),
            "family_name": self.get_claim("family_name", "id_token"),
            "email": self.get_claim("email", "id_token"),
        }

    def get_permissions(self) -> Dict[str, Any]:
        return {
            "org_code": self.get_claim("org_code"),
            "permissions": self.get_claim("permissions"),
        }

    def get_permission(self, permission: str) -> Dict[str, Any]:
        return {
            "org_code": self.get_claim("org_code"),
            "is_granted": permission in self.get_claim("permissions"),
        }

    def get_organization(self) -> Dict[str, str]:
        return {
            "org_code": self.get_claim("org_code"),
        }

    def get_user_organizations(self) -> Dict[str, List[str]]:
        return {
            "org_codes": self.get_claim("org_codes", "id_token"),
        }
