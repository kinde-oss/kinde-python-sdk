"""
Resource-server helpers: protect an MCP server or API with a Kinde "AI agents and MCP" application.

Everything protocol-related lives here so the FastAPI, Flask and MCP integrations
only adapt request and response types. Every method that talks to Kinde has a
sync form and an ``_async`` form.
"""

import base64
import hashlib
import logging
import re
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Mapping, Optional, Tuple, Union
from urllib.parse import quote_plus

import httpx
import jwt

from kinde_sdk.agents.config import (
    VERIFICATION_JWT,
    VERIFICATION_JWT_AND_INTROSPECTION,
    AgentAuthConfig,
)
from kinde_sdk.agents.context import AgentAuthContext
from kinde_sdk.agents.errors import (
    AgentAuthError,
    AuthenticationRequired,
    InsufficientScopeError,
    InvalidTokenError,
    PermissionDeniedError,
    VerificationUnavailableError,
)
from kinde_sdk.agents.www_authenticate import build_challenge

logger = logging.getLogger("kinde_sdk.agents")

# RFC 6750 §2.1 b64token
_BEARER_TOKEN = re.compile(r"^[A-Za-z0-9\-._~+/]+=*$")

_AS_METADATA_CACHE_SECONDS = 300
_JWKS_CACHE_SECONDS = 3600
_JWKS_MIN_REFETCH_SECONDS = 60
_JWKS_RETRY_SECONDS = 5
_INTROSPECTION_CACHE_MAX_ENTRIES = 10_000
# Error codes Kinde's introspection endpoint uses for a bad token (as opposed to bad application credentials)
_INACTIVE_TOKEN_ERRORS = frozenset({"token_inactive", "invalid_token"})


@dataclass
class AgentAuthResponse:
    """An HTTP error response for a framework integration to send as is."""

    status_code: int
    headers: Dict[str, str] = field(default_factory=dict)
    body: Dict[str, str] = field(default_factory=dict)


class _JwksCache:
    """Signing keys by ``kid``, refetched at most once a minute when an unknown ``kid`` shows up.

    The rate limit matters: a public MCP endpoint receiving tokens with made-up
    ``kid`` values must not turn into a flood of JWKS requests to Kinde.
    """

    def __init__(self, url: str):
        self.url = url
        self._keys: Dict[str, Any] = {}
        self._fetched_at: Optional[float] = None
        self._last_attempt: Optional[float] = None
        self._last_unknown_kid_fetch: Optional[float] = None
        self._lock = threading.Lock()

    def _should_fetch(self, kid: str, now: float) -> bool:
        if self._fetched_at is None or now - self._fetched_at >= _JWKS_CACHE_SECONDS:
            # Missing or stale: retry, but not on every request while Kinde is down
            return self._last_attempt is None or now - self._last_attempt >= _JWKS_RETRY_SECONDS
        if kid in self._keys:
            return False
        # Unknown kid (a key rotation, or a forged token): at most one refetch a minute
        if self._last_unknown_kid_fetch is not None and now - self._last_unknown_kid_fetch < _JWKS_MIN_REFETCH_SECONDS:
            return False
        self._last_unknown_kid_fetch = now
        return True

    def _store(self, response: httpx.Response, now: float) -> None:
        if response.status_code != 200:
            raise VerificationUnavailableError(f"Kinde JWKS request failed with HTTP {response.status_code}")
        try:
            document = response.json()
        except ValueError as exc:
            raise VerificationUnavailableError("Kinde JWKS response was not JSON") from exc
        keys = {}
        for jwk in document.get("keys", []) if isinstance(document, dict) else []:
            kid = jwk.get("kid") if isinstance(jwk, dict) else None
            if not kid:
                continue
            try:
                keys[kid] = jwt.PyJWK(jwk).key
            except (jwt.PyJWKError, jwt.InvalidKeyError, ValueError, TypeError):
                logger.debug("Skipping unusable JWKS key %s", kid)
        self._keys = keys
        self._fetched_at = now

    def _fetch_failed(self, exc: Exception) -> None:
        # Keep verifying with the keys we have; only fail when there are none
        if self._fetched_at is None:
            if isinstance(exc, VerificationUnavailableError):
                raise exc
            raise VerificationUnavailableError("Could not reach Kinde for signing keys") from exc
        logger.warning("Kinde JWKS refresh failed; using cached keys")

    def _lookup(self, kid: str) -> Any:
        key = self._keys.get(kid)
        if key is None:
            if self._fetched_at is None:
                raise VerificationUnavailableError("Kinde signing keys are unavailable")
            raise InvalidTokenError("The access token was signed by an unknown key")
        return key

    def get_key(self, kid: str, client: httpx.Client) -> Any:
        with self._lock:
            now = time.monotonic()
            if self._should_fetch(kid, now):
                self._last_attempt = now
                try:
                    self._store(client.get(self.url), now)
                except (httpx.HTTPError, VerificationUnavailableError) as exc:
                    self._fetch_failed(exc)
            return self._lookup(kid)

    async def get_key_async(self, kid: str, client: httpx.AsyncClient) -> Any:
        now = time.monotonic()
        if self._should_fetch(kid, now):
            self._last_attempt = now
            try:
                self._store(await client.get(self.url), now)
            except (httpx.HTTPError, VerificationUnavailableError) as exc:
                self._fetch_failed(exc)
        return self._lookup(kid)


class KindeAgentAuth:
    """Resource-server helpers for one Kinde "AI agents and MCP" application.

    Build it from an :class:`AgentAuthConfig`, from keyword arguments, or from
    the environment (``KindeAgentAuth()`` reads ``KINDE_AGENTS_*`` and ``KINDE_HOST``)::

        auth = KindeAgentAuth(
            domain="https://yourbiz.kinde.com",
            client_id="<agents application client id>",
            client_secret="<agents application client secret>",
            resource_url="https://api.example.com/mcp",
        )
        context = await auth.authenticate_async(request.headers.get("authorization"))

    ``http_client`` and ``async_http_client`` may be passed to share connection
    pools or for tests. Clients created here are closed by :meth:`close` and
    :meth:`aclose`.
    """

    def __init__(
        self,
        config: Optional[AgentAuthConfig] = None,
        *,
        http_client: Optional[httpx.Client] = None,
        async_http_client: Optional[httpx.AsyncClient] = None,
        clock: Callable[[], float] = time.time,
        **options: Any,
    ):
        if config is None:
            config = AgentAuthConfig.from_env(**options)
        elif options:
            raise TypeError("Pass either config or keyword options, not both")
        self.config = config
        self._clock = clock
        self._http_client = http_client
        self._owns_http_client = http_client is None
        self._async_http_client = async_http_client
        self._owns_async_http_client = async_http_client is None
        self._jwks = _JwksCache(config.jwks_url)
        self._introspection_cache: Dict[str, Tuple[float, Dict[str, Any]]] = {}
        self._as_metadata_cache: Optional[Tuple[float, Dict[str, Any]]] = None

    # -- HTTP clients ---------------------------------------------------------

    def _client(self) -> httpx.Client:
        if self._http_client is None:
            self._http_client = httpx.Client(timeout=self.config.timeout_seconds)
        return self._http_client

    def _async_client(self) -> httpx.AsyncClient:
        if self._async_http_client is None:
            self._async_http_client = httpx.AsyncClient(timeout=self.config.timeout_seconds)
        return self._async_http_client

    def close(self) -> None:
        if self._owns_http_client and self._http_client is not None:
            self._http_client.close()
            self._http_client = None

    async def aclose(self) -> None:
        if self._owns_async_http_client and self._async_http_client is not None:
            await self._async_http_client.aclose()
            self._async_http_client = None
        self.close()

    # -- Metadata -------------------------------------------------------------

    def protected_resource_metadata(self) -> Dict[str, Any]:
        """The RFC 9728 document for both well-known metadata paths.

        ``authorization_servers`` holds the scoped issuer, which is what steers
        agents to this application's endpoints and makes CIMD resolve.
        """
        document: Dict[str, Any] = {
            "resource": self.config.resource_url,
            "authorization_servers": [self.config.issuer],
            "bearer_methods_supported": ["header"],
            "scopes_supported": list(self.config.scopes_supported),
        }
        if self.config.resource_name:
            document["resource_name"] = self.config.resource_name
        return document

    def authorization_server_metadata(self) -> Dict[str, Any]:
        """A static copy of Kinde's scoped authorization server metadata, built from the derived URLs."""
        issuer = self.config.issuer
        return {
            "issuer": issuer,
            "authorization_endpoint": f"{issuer}/authorize",
            "token_endpoint": f"{issuer}/token",
            "registration_endpoint": f"{issuer}/register",
            "introspection_endpoint": self.config.introspection_url,
            "revocation_endpoint": self.config.revocation_url,
            "jwks_uri": self.config.jwks_url,
            "response_types_supported": ["code"],
            "grant_types_supported": ["authorization_code", "refresh_token"],
            "token_endpoint_auth_methods_supported": ["client_secret_post", "none"],
            "code_challenge_methods_supported": ["S256"],
            "scopes_supported": ["offline", "profile", "email"],
            "subject_types_supported": ["public"],
            "resource_indicators_supported": True,
            "client_id_metadata_document_supported": True,
        }

    def _cached_as_metadata(self) -> Optional[Dict[str, Any]]:
        if self._as_metadata_cache and time.monotonic() - self._as_metadata_cache[0] < _AS_METADATA_CACHE_SECONDS:
            return dict(self._as_metadata_cache[1])
        return None

    def _store_as_metadata(self, response: Optional[httpx.Response]) -> Dict[str, Any]:
        document = None
        if response is not None and response.status_code == 200:
            try:
                document = response.json()
            except ValueError:
                document = None
        if not isinstance(document, dict):
            if response is not None:
                logger.warning(
                    "Kinde authorization server metadata returned HTTP %s; serving the static copy",
                    response.status_code,
                )
            # Not cached, so the next request tries Kinde again
            return self.authorization_server_metadata()
        # Without this flag agents fall back to registration, which MCP has deprecated
        document["client_id_metadata_document_supported"] = True
        self._as_metadata_cache = (time.monotonic(), document)
        return dict(document)

    def fetch_authorization_server_metadata(self) -> Dict[str, Any]:
        """Kinde's scoped metadata (cached 5 minutes), falling back to the static copy if Kinde is unreachable.

        For the optional ``/.well-known/oauth-authorization-server`` mirror that
        some older MCP clients fetch from the resource server's own origin.
        """
        cached = self._cached_as_metadata()
        if cached is not None:
            return cached
        try:
            response = self._client().get(self.config.authorization_server_metadata_url)
        except httpx.HTTPError:
            logger.warning("Could not reach Kinde for authorization server metadata; serving the static copy")
            response = None
        return self._store_as_metadata(response)

    async def fetch_authorization_server_metadata_async(self) -> Dict[str, Any]:
        cached = self._cached_as_metadata()
        if cached is not None:
            return cached
        try:
            response = await self._async_client().get(self.config.authorization_server_metadata_url)
        except httpx.HTTPError:
            logger.warning("Could not reach Kinde for authorization server metadata; serving the static copy")
            response = None
        return self._store_as_metadata(response)

    # -- Challenges -----------------------------------------------------------

    def challenge(self, error: Optional[AgentAuthError] = None) -> Optional[str]:
        """The ``WWW-Authenticate`` value for an error, or ``None`` when the response carries no challenge."""
        prm_url = self.config.protected_resource_metadata_url
        if error is None or isinstance(error, AuthenticationRequired):
            return build_challenge("Bearer", [("resource_metadata", prm_url)])
        if isinstance(error, InvalidTokenError):
            return build_challenge(
                "Bearer",
                [
                    ("error", "invalid_token"),
                    ("error_description", error.description),
                    ("resource_metadata", prm_url),
                ],
            )
        if isinstance(error, InsufficientScopeError):
            return build_challenge(
                "Bearer",
                [
                    ("error", "insufficient_scope"),
                    ("scope", " ".join(error.scopes)),
                    ("resource_metadata", prm_url),
                ],
            )
        # Missing permissions and Kinde outages are never challenges: a challenge makes the agent sign in again
        return None

    def error_response(self, error: AgentAuthError) -> AgentAuthResponse:
        """Map an error from :meth:`authenticate` (or a permission check) to the response to send."""
        status = getattr(error, "status_code", 500)
        headers: Dict[str, str] = {}
        challenge = self.challenge(error)
        if challenge is not None:
            headers["WWW-Authenticate"] = challenge
            headers["Access-Control-Expose-Headers"] = "WWW-Authenticate"
        if isinstance(error, AuthenticationRequired):
            body = {"error": "unauthorized", "error_description": error.description}
        elif isinstance(
            error, (InvalidTokenError, InsufficientScopeError, PermissionDeniedError, VerificationUnavailableError)
        ):
            body = {"error": error.error, "error_description": error.description}
        else:
            status = 500
            body = {"error": "server_error", "error_description": "Authentication failed"}
        return AgentAuthResponse(status_code=status, headers=headers, body=body)

    # -- Bearer extraction ----------------------------------------------------

    @staticmethod
    def extract_bearer_token(authorization: Optional[str]) -> str:
        """Return the token from an ``Authorization`` header value.

        Raises :class:`AuthenticationRequired` when there is no header and
        :class:`InvalidTokenError` when it isn't ``Bearer <token>``. Tokens in a
        query string or cookie are never accepted.
        """
        if authorization is None or not authorization.strip():
            raise AuthenticationRequired()
        scheme, separator, token = authorization.partition(" ")
        if scheme.lower() != "bearer" or not separator:
            raise InvalidTokenError("The Authorization header must use the Bearer scheme")
        if not _BEARER_TOKEN.match(token):
            raise InvalidTokenError("The Authorization header is malformed")
        return token

    def authenticate(self, authorization: Optional[str]) -> AgentAuthContext:
        """Extract and verify the bearer token from an ``Authorization`` header value."""
        return self.verify_token(self.extract_bearer_token(authorization))

    async def authenticate_async(self, authorization: Optional[str]) -> AgentAuthContext:
        return await self.verify_token_async(self.extract_bearer_token(authorization))

    # -- Verification ---------------------------------------------------------

    def verify_token(self, token: str) -> AgentAuthContext:
        """Verify an access token with the configured strategy.

        Raises :class:`InvalidTokenError` for a bad token and
        :class:`VerificationUnavailableError` when Kinde can't be reached.
        """
        strategy = self.config.verification
        claims = None
        if strategy in (VERIFICATION_JWT, VERIFICATION_JWT_AND_INTROSPECTION):
            claims = self._verify_jwt(token, self._jwks.get_key(self._kid(token), self._client()))
            if strategy == VERIFICATION_JWT:
                return AgentAuthContext.from_claims(token, claims)
        data = self._cached_introspection(token)
        if data is None:
            data = self._handle_introspection(self._post_introspection(token), token)
        return self._context_from_introspection(token, data, claims)

    async def verify_token_async(self, token: str) -> AgentAuthContext:
        strategy = self.config.verification
        claims = None
        if strategy in (VERIFICATION_JWT, VERIFICATION_JWT_AND_INTROSPECTION):
            key = await self._jwks.get_key_async(self._kid(token), self._async_client())
            claims = self._verify_jwt(token, key)
            if strategy == VERIFICATION_JWT:
                return AgentAuthContext.from_claims(token, claims)
        data = self._cached_introspection(token)
        if data is None:
            data = self._handle_introspection(await self._post_introspection_async(token), token)
        return self._context_from_introspection(token, data, claims)

    def _application_auth_header(self) -> str:
        # RFC 6749 §2.3.1: form-urlencode each part before joining
        credentials = f"{quote_plus(self.config.client_id)}:{quote_plus(self.config.client_secret or '')}"
        return "Basic " + base64.b64encode(credentials.encode()).decode()

    def _post_introspection(self, token: str) -> Union[httpx.Response, Exception]:
        try:
            return self._client().post(
                self.config.introspection_url,
                data={"token": token},
                headers={"Authorization": self._application_auth_header(), "Accept": "application/json"},
            )
        except httpx.HTTPError as exc:
            return exc

    async def _post_introspection_async(self, token: str) -> Union[httpx.Response, Exception]:
        try:
            return await self._async_client().post(
                self.config.introspection_url,
                data={"token": token},
                headers={"Authorization": self._application_auth_header(), "Accept": "application/json"},
            )
        except httpx.HTTPError as exc:
            return exc

    def _handle_introspection(self, response: Union[httpx.Response, Exception], token: str) -> Dict[str, Any]:
        if isinstance(response, Exception):
            logger.warning("Kinde introspection request failed: %s", type(response).__name__)
            raise VerificationUnavailableError("Could not reach Kinde to verify the token")
        if response.status_code in (400, 401, 403):
            error = _oauth_error_code(response)
            # Kinde answers an inactive token with 401 token_inactive, not 200 {"active": false}
            if error in _INACTIVE_TOKEN_ERRORS:
                raise InvalidTokenError("The access token is not active")
            # Anything else (request_unauthorized, invalid_client) means the application's credentials are wrong
            logger.error(
                "Kinde refused the introspection request (HTTP %s, %s). Check KINDE_AGENTS_CLIENT_ID "
                "and KINDE_AGENTS_CLIENT_SECRET belong to the AI agents and MCP application.",
                response.status_code,
                error or "no error code",
            )
            raise VerificationUnavailableError("Token verification is misconfigured")
        if response.status_code == 404:
            logger.error(
                "Kinde introspection endpoint returned 404: %s does not name a live AI agents and MCP application",
                self.config.introspection_url,
            )
            raise VerificationUnavailableError("Token verification is misconfigured")
        if response.status_code != 200:
            logger.warning("Kinde introspection returned HTTP %s", response.status_code)
            raise VerificationUnavailableError()
        try:
            data = response.json()
        except ValueError as exc:
            raise VerificationUnavailableError("Kinde introspection response was not JSON") from exc
        if not isinstance(data, dict) or data.get("active") is not True:
            raise InvalidTokenError("The access token is not active")
        audience = data.get("aud")
        audiences = [audience] if isinstance(audience, str) else audience if isinstance(audience, list) else []
        # Kinde already enforces this; checking again guards against a misrouted introspection call
        if self.config.resource_url not in audiences:
            raise InvalidTokenError("The access token was not issued for this resource")
        exp = data.get("exp")
        if isinstance(exp, (int, float)) and exp <= self._clock() - self.config.clock_tolerance_seconds:
            raise InvalidTokenError("The access token has expired")
        self._remember_introspection(token, data)
        return data

    def _context_from_introspection(
        self, token: str, data: Mapping[str, Any], verified_claims: Optional[Mapping[str, Any]]
    ) -> AgentAuthContext:
        claims = verified_claims
        if claims is None:
            # Safe without a signature check: Kinde has just said the token is active.
            # Introspection doesn't carry permissions, roles or org_code; the token does.
            try:
                claims = jwt.decode(token, options={"verify_signature": False})
            except jwt.PyJWTError:
                claims = {}
        return AgentAuthContext.from_claims(token, claims, introspection=data)

    # -- Introspection cache --------------------------------------------------

    @staticmethod
    def _cache_key(token: str) -> str:
        # Keyed by a hash so raw tokens never sit in the cache
        return hashlib.sha256(token.encode()).hexdigest()

    def _cached_introspection(self, token: str) -> Optional[Dict[str, Any]]:
        if not self.config.introspection_cache_seconds:
            return None
        entry = self._introspection_cache.get(self._cache_key(token))
        if entry is None:
            return None
        if entry[0] <= self._clock():
            self._introspection_cache.pop(self._cache_key(token), None)
            return None
        return entry[1]

    def _remember_introspection(self, token: str, data: Dict[str, Any]) -> None:
        if not self.config.introspection_cache_seconds:
            return
        now = self._clock()
        expires = now + self.config.introspection_cache_seconds
        exp = data.get("exp")
        if isinstance(exp, (int, float)):
            expires = min(expires, float(exp))
        if len(self._introspection_cache) >= _INTROSPECTION_CACHE_MAX_ENTRIES:
            self._introspection_cache = {k: v for k, v in self._introspection_cache.items() if v[0] > now}
            if len(self._introspection_cache) >= _INTROSPECTION_CACHE_MAX_ENTRIES:
                self._introspection_cache.clear()
        self._introspection_cache[self._cache_key(token)] = (expires, data)

    # -- Local JWT verification -----------------------------------------------

    @staticmethod
    def _kid(token: str) -> str:
        try:
            header = jwt.get_unverified_header(token)
        except jwt.PyJWTError as exc:
            raise InvalidTokenError("The access token is not a valid JWT") from exc
        # Reject "none", HS* and everything else before touching any key
        if header.get("alg") != "RS256":
            raise InvalidTokenError("The access token uses an unsupported algorithm")
        kid = header.get("kid")
        if not kid or not isinstance(kid, str):
            raise InvalidTokenError("The access token has no key ID")
        return kid

    def _verify_jwt(self, token: str, key: Any) -> Dict[str, Any]:
        try:
            claims = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                # PyJWT matches when the aud array contains this value, comparing exactly
                audience=self.config.resource_url,
                leeway=self.config.clock_tolerance_seconds,
                options={"require": ["exp", "iss", "aud"], "verify_iss": False},
            )
        except jwt.ExpiredSignatureError as exc:
            raise InvalidTokenError("The access token has expired") from exc
        except jwt.InvalidAudienceError as exc:
            raise InvalidTokenError("The access token was not issued for this resource") from exc
        except jwt.ImmatureSignatureError as exc:
            raise InvalidTokenError("The access token is not valid yet") from exc
        except jwt.PyJWTError as exc:
            raise InvalidTokenError("The access token is invalid") from exc
        # iss is the Kinde domain, not the scoped issuer: comparing with the scoped issuer rejects every token
        issuer = claims.get("iss")
        if not isinstance(issuer, str) or _strip_one_slash(issuer) != self.config.domain:
            raise InvalidTokenError("The access token has the wrong issuer")
        return claims

    # -- Admin revoke ---------------------------------------------------------

    def revoke_token(self, token: str, token_type_hint: Optional[str] = None) -> None:
        """Revoke an agent's token with the application's credentials.

        Revoking either token of a pair revokes both. Only works for tokens
        issued for this application's Resource URL.
        """
        data = {"token": token}
        if token_type_hint:
            data["token_type_hint"] = token_type_hint
        try:
            response = self._client().post(
                self.config.revocation_url, data=data, headers={"Authorization": self._application_auth_header()}
            )
        except httpx.HTTPError as exc:
            raise VerificationUnavailableError("Could not reach Kinde to revoke the token") from exc
        self._check_revocation(response, token)

    async def revoke_token_async(self, token: str, token_type_hint: Optional[str] = None) -> None:
        data = {"token": token}
        if token_type_hint:
            data["token_type_hint"] = token_type_hint
        try:
            response = await self._async_client().post(
                self.config.revocation_url, data=data, headers={"Authorization": self._application_auth_header()}
            )
        except httpx.HTTPError as exc:
            raise VerificationUnavailableError("Could not reach Kinde to revoke the token") from exc
        self._check_revocation(response, token)

    def _check_revocation(self, response: httpx.Response, token: str) -> None:
        if response.status_code != 200:
            raise AgentAuthError(f"Kinde token revocation failed with HTTP {response.status_code}")
        self._introspection_cache.pop(self._cache_key(token), None)


def _oauth_error_code(response: httpx.Response) -> Optional[str]:
    try:
        body = response.json()
    except ValueError:
        return None
    error = body.get("error") if isinstance(body, dict) else None
    return error if isinstance(error, str) else None


def _strip_one_slash(value: str) -> str:
    return value[:-1] if value.endswith("/") else value
