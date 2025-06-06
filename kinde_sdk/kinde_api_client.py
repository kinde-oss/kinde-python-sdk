from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

import jwt
from jwt import PyJWKClient
from authlib.integrations.requests_client import OAuth2Session
from kinde_sdk.api_client import ApiClient
from kinde_sdk.exceptions import (
    KindeConfigurationException,
    KindeLoginException,
    KindeTokenException,
    KindeRetrieveException,
)
from kinde_sdk import __version__ as kinde_sdk_version


class FlagType(Enum):
    s = "string"
    i = "integer"
    b = "boolean"


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
        self.create_authorization_url_params = {}
        if self.grant_type == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
            if self.code_verifier is None:
                raise KindeConfigurationException(
                    '"code_verifier" parameter is required when a grant_type is AUTHORIZATION_CODE_WITH_PKCE.'
                )
            auth_session_params["code_challenge_method"] = "S256"
            self.create_authorization_url_params["code_verifier"] = self.code_verifier

        self.client = OAuth2Session(
            self.client_id,
            self.client_secret,
            redirect_uri=self.callback_url,
            **auth_session_params,
        )

        self.login_url = ""
        self.registration_url = ""

        self.jwks_client = PyJWKClient(
            uri=f"{self.domain}/.well-known/jwks.json",
            cache_keys=True,
        )

    def _get_auth_url(self, state: str = None):
        self.login_url, self.state = self.client.create_authorization_url(
            self.authorization_endpoint, **self.create_authorization_url_params, state=state
        )

        if self.audience:
            self.login_url = f"{self.login_url}&audience={self.audience}"
        if self.org_code:
            self.login_url = f"{self.login_url}&org_code={self.org_code}"

    def get_login_url(self, additional_params: Optional[Dict[str, str]] = None, state: str = None) -> str:
        self._get_auth_url(state=state)

        if additional_params:
            return self._add_additional_params(self.login_url, additional_params=additional_params)
        return self.login_url

    def get_register_url(self, additional_params: Optional[Dict[str, str]] = None, state: str = None) -> str:
        self._get_auth_url(state=state)
        self.registration_url = f"{self.login_url}&start_page=registration"

        if additional_params:
            return self._add_additional_params(self.registration_url, additional_params=additional_params)
        return self.registration_url

    def logout(self, redirect_to: str) -> str:
        self.__access_token_obj = None
        self.configuration.access_token = None
        return f"{self.logout_endpoint}?redirect={redirect_to}"

    def is_authenticated(self) -> bool:
        if self.__access_token_obj:
            if self.__access_token_obj.is_expired():
                self._refresh_token()
            return True
        return False
    
    def is_authenticated_token(self, token_value: dict) -> dict:
        if token_value:
            if token_value.is_expired():
                self._refresh_token_value(token_value)
            return True
        return None

    def create_org(self) -> str:
        return f"{self.registration_url}&is_create_org=true"

    def get_claim(self, key: str, token_name: str = "access_token") -> Any:
        if token_name not in self.TOKEN_NAMES:
            raise KindeTokenException(
                f"Please use only tokens from the list: {self.TOKEN_NAMES}"
            )
        self._decode_token_if_needed(token_name)
        value = self.__decoded_tokens[token_name].get(key)
        return {"name": key, "value": value}
    
    def get_claim_token(self, token_value: dict, key: str, token_name: str = "access_token") -> Any:
        if token_name not in self.TOKEN_NAMES:
            raise KindeTokenException(
                f"Please use only tokens from the list: {self.TOKEN_NAMES}"
            )
        
        decoded_tokens = self._decode_token_if_needed_value(token_name,token_value)
        value = decoded_tokens[token_name].get(key)
        return {"name": key, "value": value}

    def get_permission(self, permission: str) -> Dict[str, Any]:
        return {
            "org_code": self.get_claim("org_code")["value"],
            "is_granted": permission in self.get_claim("permissions")["value"],
        }
    
    def get_permission_token(self, token_value: dict, permission: str) -> Dict[str, Any]:
        return {
            "org_code": self.get_claim_token(token_value, "org_code")["value"],
            "is_granted": permission in self.get_claim_token(token_value, "permissions")["value"],
        }

    def get_permissions(self) -> Dict[str, Any]:
        return {
            "org_code": self.get_claim("org_code")["value"],
            "permissions": self.get_claim("permissions")["value"],
        }
    
    def get_permissions_token(self, token_value: dict) -> Dict[str, Any]:
        return {
            "org_code": self.get_claim_token(token_value, "org_code")["value"],
            "permissions": self.get_claim_token(token_value, "permissions")["value"],
        }

    def get_organization(self) -> Dict[str, str]:
        return {
            "org_code": self.get_claim("org_code")["value"],
        }
    
    def get_organization_token(self, token_value: dict) -> Dict[str, str]:
        return {
            "org_code": self.get_claim_token(token_value, "org_code")["value"],
        }

    def get_user_details(self) -> Dict[str, str]:
        return {
            "id": self.get_claim("sub", "id_token")["value"],
            "given_name": self.get_claim("given_name", "id_token")["value"],
            "family_name": self.get_claim("family_name", "id_token")["value"],
            "email": self.get_claim("email", "id_token")["value"],
            "picture": self.get_claim("picture", "id_token")["value"],
        }
    
    def get_user_details_token(self,token_value: dict) -> Dict[str, str]:
        return {
            "id": self.get_claim_token(token_value, "sub","id_token")["value"],
            "given_name": self.get_claim_token(token_value, "given_name", "id_token")["value"],
            "family_name": self.get_claim_token(token_value, "family_name", "id_token")["value"],
            "email": self.get_claim_token(token_value, "email", "id_token")["value"],
            "picture": self.get_claim_token(token_value, "picture", "id_token")["value"],
        }

    def get_user_organizations(self) -> Dict[str, List[str]]:
        return {
            "org_codes": self.get_claim("org_codes", "id_token")["value"],
        }
    
    def get_user_organizations_token(self, token_value: dict) -> Dict[str, List[str]]:
        return {
            "org_codes": self.get_claim_token(token_value, "org_codes", "id_token")["value"],
        }

    def get_flag(
        self, code: str, default_value: Any = None, flag_type: str = ""
    ) -> Any:
        flags = self.get_claim("feature_flags")["value"] or {}
        flag = {}

        if code not in list(flags.keys()):
            if default_value is None:
                raise KindeRetrieveException(
                    f"Flag {code} was not found, and no default value has been provided"
                )
        else:
            flag = flags[code]
            if flag_type and flag.get("t") and flag_type != flag.get("t"):
                raise KindeRetrieveException(
                    f"Flag {code} is of type {FlagType[flag.get('t')].value} - requested type {FlagType[flag_type].value}"
                )

        result_flag = {
            "code": code,
            "value": flag.get("v") if flag else default_value,
            "is_default": not bool(flag),
        }
        flag_type = flag["t"] if flag else flag_type
        if flag_type:
            result_flag["type"] = FlagType[flag_type].value

        return result_flag
    
    def get_flag_token(
        self, token_value: dict, code: str, default_value: Any = None, flag_type: str = ""
    ) -> Any:
        flags = self.get_claim_token(token_value, "feature_flags")["value"] or {}
        flag = {}

        if code not in list(flags.keys()):
            if default_value is None:
                raise KindeRetrieveException(
                    f"Flag {code} was not found, and no default value has been provided"
                )
        else:
            flag = flags[code]
            if flag_type and flag.get("t") and flag_type != flag.get("t"):
                raise KindeRetrieveException(
                    f"Flag {code} is of type {FlagType[flag.get('t')].value} - requested type {FlagType[flag_type].value}"
                )

        result_flag = {
            "code": code,
            "value": flag.get("v") if flag else default_value,
            "is_default": not bool(flag),
        }
        flag_type = flag["t"] if flag else flag_type
        if flag_type:
            result_flag["type"] = FlagType[flag_type].value

        return result_flag

    def get_boolean_flag(self, code: str, default_value: Any = None) -> bool:
        return self.get_flag(code, default_value, "b")["value"]
    
    def get_boolean_flag_token(self, token_value: dict, code: str, default_value: Any = None) -> bool:
        return self.get_flag_token(token_value, code, default_value, "b")["value"]

    def get_string_flag(self, code: str, default_value: Any = None) -> str:
        return self.get_flag(code, default_value, "s")["value"]
    
    def get_string_flag_token(self, token_value: dict, code: str, default_value: Any = None) -> str:
        return self.get_flag_token(token_value, code, default_value, "s")["value"]

    def get_integer_flag(self, code: str, default_value: Any = None) -> int:
        return self.get_flag(code, default_value, "i")["value"]
    
    def get_integer_flag_token(self, token_value: dict, code: str, default_value: Any = None) -> int:
        return self.get_flag_token(token_value, code, default_value, "i")["value"]

    def call_api(self, *args, **kwargs) -> Any:
        self._get_or_refresh_access_token()
        return super().call_api(*args, **kwargs)

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

            signing_key = self.jwks_client.get_signing_key_from_jwt(token)

            if token:
                decode_token_params = {
                    "jwt":token,
                    "key": signing_key.key,
                    "algorithms":["RS256"],
                    "options":{
                        "verify_signature": True,
                        "verify_exp": True,
                        "verify_aud": False
                    }
                }
                self.__decoded_tokens[token_name] = jwt.decode(**decode_token_params)
            else:
                raise KindeTokenException(f"Token {token_name} doesn't exist.")
    
    def _decode_token_if_needed_value(self, token_name: str, token_value: dict) -> dict:
        token = token_value.get(token_name)

      
        if isinstance(token, bytes):
            try:
                token = token.decode('utf-8')
            except UnicodeDecodeError as err:
                raise KindeTokenException(f"Token {token_name} contains invalid UTF-8 bytes.") from err
        
        if not isinstance(token, str):
            return token_value

        signing_key = self.jwks_client.get_signing_key_from_jwt(token)
        if signing_key:
            decode_token_params = {
                "jwt": token,
                "key": signing_key.key,
                "algorithms": ["RS256"],
                "options": {
                    "verify_signature": True,
                    "verify_exp": True,
                    "verify_aud": False
                }
            }
            return {token_name: jwt.decode(**decode_token_params)}
        else:
            raise KindeTokenException(f"Token {token_name} doesn't exist.")

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

        self.__access_token_obj = self.client.fetch_token(
            self.token_endpoint,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Kinde-SDK": "/".join(("Python", kinde_sdk_version)),
            },
            **params,
        )
        self.configuration.access_token = self.__access_token_obj.get("access_token")
        self._clear_decoded_tokens()

    def fetch_token_value(self, authorization_response: Optional[str] = None) -> dict:
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

        access_token_obj = self.client.fetch_token(
            self.token_endpoint,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Kinde-SDK": "/".join(("Python", kinde_sdk_version)),
            },
            **params,
        )
        return access_token_obj


    def _get_or_refresh_access_token(self) -> None:
        if self.grant_type == GrantType.CLIENT_CREDENTIALS:
            if not self.__access_token_obj or self.__access_token_obj.is_expired():
                self.fetch_token()
        else:
            if not self.__access_token_obj:
                raise KindeLoginException(
                    'Please use "get_login_url()" or "get_register_url()" first.'
                )
            if self.__access_token_obj.is_expired():
                self._refresh_token()

    def _refresh_token(self) -> None:
        refresh_token = self.__access_token_obj.get("refresh_token")

        if refresh_token:
            self.__access_token_obj = self.client.refresh_token(
                self.token_endpoint,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Kinde-SDK": "/".join(("Python", kinde_sdk_version)),
                },
                refresh_token=refresh_token,
            )
            if not self.__access_token_obj:
                raise KindeTokenException(
                    '"Access token" and "Refresh token" are invalid.'
                )

            self.configuration.access_token = self.__access_token_obj.get(
                "access_token"
            )
            self._clear_decoded_tokens()
        else:
            raise KindeTokenException('"Access token" and "Refresh token" are invalid.')
        
    def _refresh_token_value(self, token_value: dict) -> dict:
        refresh_token = token_value.get("refresh_token")

        if refresh_token:
            token_value = self.client.refresh_token(
                self.token_endpoint,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Kinde-SDK": "/".join(("Python", kinde_sdk_version)),
                },
                refresh_token=refresh_token,
            )
            if not token_value:
                raise KindeTokenException(
                    '"Access token" and "Refresh token" are invalid.'
                )

            return token_value
        else:
            raise KindeTokenException('"Access token" and "Refresh token" are invalid.')

    def _add_additional_params(self, url: str, additional_params: Optional[Dict[str, str]] = None) -> str:

        if additional_params.get('auth_url_params'):
            url_parts = urlparse(url)
            query = parse_qs(url_parts.query)

            for key, value in additional_params.get('auth_url_params').items():
                query[key] = value

            url_parts = url_parts._replace(query=urlencode(query, doseq=True))
            return urlunparse(url_parts)
        else:
            return url
