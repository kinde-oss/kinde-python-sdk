"""
An in-process stand-in for Kinde's scoped agents issuer, following the server contract.

It behaves like the real server where SDKs most often go wrong: introspection
only answers the application's own Basic credentials, tokens carry the bare
domain as ``iss`` and the Resource URL in ``aud``, ``openid`` is refused,
registration always returns a secret, and refresh doesn't rotate.
"""

import base64
import hashlib
import json
import secrets
import time
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, unquote_plus, urlsplit

import httpx
import jwt
from cryptography.hazmat.primitives.asymmetric import rsa

DOMAIN = "https://test.kinde.com"
APP_ID = "0123456789abcdef0123456789abcdef"
APP_SECRET = "app-secret"
RESOURCE_URL = "https://api.example.com/mcp"
ISSUER = f"{DOMAIN}/oauth2/agents/{APP_ID}"
KID = "test-key"

_PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
_OTHER_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)


def jwks() -> Dict[str, Any]:
    key = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(_PRIVATE_KEY.public_key()))
    key.update({"kid": KID, "alg": "RS256", "use": "sig"})
    return {"keys": [key]}


def make_token(
    *,
    iss: str = DOMAIN,
    aud: Any = None,
    exp_in: int = 3600,
    kid: str = KID,
    key: Any = None,
    algorithm: str = "RS256",
    **claims: Any,
) -> str:
    """Sign a Kinde-shaped access token with the test key."""
    now = int(time.time())
    payload = {
        "iss": iss,
        "aud": [RESOURCE_URL] if aud is None else aud,
        "sub": "kp_user",
        "azp": "https://claude.ai/oauth/claude-code-client-metadata",
        "scp": ["offline"],
        "iat": now,
        "exp": now + exp_in,
        "jti": secrets.token_hex(8),
    }
    payload.update(claims)
    if algorithm == "RS256":
        return jwt.encode(payload, key or _PRIVATE_KEY, algorithm="RS256", headers={"kid": kid})
    return jwt.encode(
        payload, "a-shared-secret-that-is-long-enough-for-hs256", algorithm=algorithm, headers={"kid": kid}
    )


def other_key():
    return _OTHER_KEY


def authorization_server_metadata() -> Dict[str, Any]:
    return {
        "issuer": ISSUER,
        "authorization_endpoint": f"{ISSUER}/authorize",
        "token_endpoint": f"{ISSUER}/token",
        "registration_endpoint": f"{ISSUER}/register",
        "introspection_endpoint": f"{ISSUER}/introspect",
        "revocation_endpoint": f"{ISSUER}/revoke",
        "jwks_uri": f"{DOMAIN}/.well-known/jwks",
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code", "refresh_token"],
        "token_endpoint_auth_methods_supported": ["client_secret_post", "none"],
        "code_challenge_methods_supported": ["S256"],
        "scopes_supported": ["offline", "profile", "email"],
        "subject_types_supported": ["public"],
        "resource_indicators_supported": True,
        "client_id_metadata_document_supported": True,
    }


class FakeKinde:
    """Routes for the scoped issuer plus a protected resource, recording every request."""

    def __init__(self):
        self.requests: List[httpx.Request] = []
        self.active_tokens: Dict[str, Dict[str, Any]] = {}
        self.registrations: Dict[str, Dict[str, Any]] = {}
        self.codes: Dict[str, Dict[str, Any]] = {}
        self.refresh_tokens: Dict[str, Dict[str, Any]] = {}
        self.revoked: List[str] = []
        self.as_metadata = authorization_server_metadata()
        self.introspection_status: Optional[int] = None
        self.introspection_raises = False
        self.inactive_as_200 = False  # the RFC 7662 answer the contract describes
        self.jwks_status = 200
        self.jwks_body: Optional[Any] = None  # overrides the real key set when set
        self.register_status: Optional[int] = None
        self.register_error: Optional[Dict[str, str]] = None
        self.prm: Optional[Dict[str, Any]] = {
            "resource": RESOURCE_URL,
            "authorization_servers": [ISSUER],
            "bearer_methods_supported": ["header"],
            "scopes_supported": ["offline"],
        }
        self.serve_prm_at_well_known = True
        self.resource_required_scope: Optional[str] = None
        self.rotate_refresh_tokens = False
        self.secret_expires_in = 30 * 86400

    # -- helpers --------------------------------------------------------------

    def paths(self) -> List[str]:
        """The method and URL of every request seen, without query strings."""
        return [f"{r.method} {r.url.copy_with(query=None)}" for r in self.requests]

    def count(self, path_suffix: str) -> int:
        """How many requests went to a path ending in ``path_suffix``."""
        return sum(1 for r in self.requests if r.url.path.endswith(path_suffix))

    def issue(self, *, scope: str = "offline", client_id: str = "https://agent.example.com/cimd.json", **claims) -> str:
        token = make_token(azp=client_id, scp=scope.split(), **claims)
        self.active_tokens[token] = {
            "active": True,
            "client_id": client_id,
            "sub": claims.get("sub", "kp_user"),
            "scope": scope,
            "aud": [RESOURCE_URL],
            "exp": int(time.time()) + 3600,
            "iat": int(time.time()),
        }
        return token

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handle)

    def async_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(transport=self.transport())

    def client(self) -> httpx.Client:
        return httpx.Client(transport=self.transport())

    # -- routing --------------------------------------------------------------

    def handle(self, request: httpx.Request) -> httpx.Response:
        """Route a request to the fake endpoint, failing on any shared ``/oauth2/*`` endpoint."""
        self.requests.append(request)
        url = str(request.url.copy_with(query=None))
        path = request.url.path
        if url == f"{DOMAIN}/.well-known/oauth-authorization-server/oauth2/agents/{APP_ID}":
            return httpx.Response(200, json=self.as_metadata)
        if url == f"{DOMAIN}/.well-known/jwks":
            return httpx.Response(self.jwks_status, json=jwks() if self.jwks_body is None else self.jwks_body)
        if url == f"{ISSUER}/introspect":
            return self._introspect(request)
        if url == f"{ISSUER}/register":
            return self._register(request)
        if url == f"{ISSUER}/token":
            return self._token(request)
        if url == f"{ISSUER}/revoke":
            form = _form(request)
            self.revoked.append(form.get("token", ""))
            self.active_tokens.pop(form.get("token", ""), None)
            return httpx.Response(200)
        if path.startswith("/oauth2/") and not path.startswith(f"/oauth2/agents/{APP_ID}"):
            raise AssertionError(f"Request to a shared Kinde endpoint: {url}")
        if request.url.host == "api.example.com":
            return self._resource(request)
        return httpx.Response(404)

    def _introspect(self, request: httpx.Request) -> httpx.Response:
        """Answer introspection as live Kinde does: 401 ``token_inactive`` for unknown tokens."""
        if self.introspection_raises:
            raise httpx.ConnectError("boom", request=request)
        if self.introspection_status is not None:
            return httpx.Response(self.introspection_status)
        # These answers were observed on a live Kinde business (2026-10-27). They differ from the
        # skill's contract, which says 200 {"active": false} in both cases.
        expected = "Basic " + base64.b64encode(f"{APP_ID}:{APP_SECRET}".encode()).decode()
        if request.headers.get("authorization") != expected:
            return httpx.Response(
                401,
                json={
                    "error": "request_unauthorized",
                    "error_description": "The request could not be authorized. Client credentials are invalid.",
                },
            )
        data = self.active_tokens.get(_form(request).get("token", ""))
        if data:
            return httpx.Response(200, json=data)
        if self.inactive_as_200:
            return httpx.Response(200, json={"active": False})
        return httpx.Response(
            401,
            json={
                "error": "token_inactive",
                "error_description": "Token is inactive because it is malformed, expired or otherwise invalid.",
            },
        )

    def _register(self, request: httpx.Request) -> httpx.Response:
        """Answer DCR the way Kinde does: always a secret and ``client_secret_post``."""
        if self.register_status is not None:
            return httpx.Response(self.register_status, json=self.register_error or {})
        body = json.loads(request.content)
        client_id = APP_ID + secrets.token_hex(16)
        registration = {
            "client_id": client_id,
            # Kinde always issues a secret and reports client_secret_post, whatever was asked for
            "client_secret": secrets.token_hex(16),
            "client_id_issued_at": int(time.time()),
            "client_secret_expires_at": int(time.time()) + self.secret_expires_in,
            "redirect_uris": body["redirect_uris"],
            "token_endpoint_auth_method": "client_secret_post",
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
        }
        self.registrations[client_id] = registration
        return httpx.Response(201, json=registration)

    def authorize(self, authorization_url: str) -> str:
        """Act as the browser plus the user: approve and return the callback URL."""
        query = {k: v[0] for k, v in parse_qs(urlsplit(authorization_url).query).items()}
        assert authorization_url.startswith(f"{ISSUER}/authorize?")
        if "openid" in query.get("scope", "").split():
            return f"{query['redirect_uri']}?error=invalid_scope&state={query['state']}"
        assert query["code_challenge_method"] == "S256"
        assert len(query["state"]) >= 8
        code = secrets.token_hex(8)
        self.codes[code] = query
        return f"{query['redirect_uri']}?code={code}&state={query['state']}&iss={ISSUER}"

    def _client_ok(self, form: Dict[str, str]) -> bool:
        """Check client authentication: no secret for CIMD, the registered secret for DCR."""
        client_id = form.get("client_id", "")
        if client_id.startswith("https://"):
            return "client_secret" not in form
        registration = self.registrations.get(client_id)
        return registration is not None and form.get("client_secret") == registration["client_secret"]

    def _token(self, request: httpx.Request) -> httpx.Response:
        """Answer the authorization code and refresh token grants."""
        form = _form(request)
        if not self._client_ok(form):
            return httpx.Response(401, json={"error": "invalid_client"})
        if form["grant_type"] == "authorization_code":
            query = self.codes.pop(form.get("code", ""), None)
            if query is None or query["redirect_uri"] != form.get("redirect_uri"):
                return httpx.Response(400, json={"error": "invalid_grant"})
            challenge = (
                base64.urlsafe_b64encode(hashlib.sha256(form["code_verifier"].encode()).digest()).rstrip(b"=").decode()
            )
            if challenge != query["code_challenge"]:
                return httpx.Response(400, json={"error": "invalid_grant"})
            scope = query.get("scope", "")
            refresh = secrets.token_hex(8) if "offline" in scope.split() else None
            if refresh:
                self.refresh_tokens[refresh] = {"client_id": form["client_id"], "scope": scope}
            access = self.issue(scope=scope, client_id=form["client_id"])
            body = {"access_token": access, "token_type": "bearer", "expires_in": 86400, "scope": scope}
            if refresh:
                body["refresh_token"] = refresh
            return httpx.Response(200, json=body)
        if form["grant_type"] == "refresh_token":
            grant = self.refresh_tokens.get(form.get("refresh_token", ""))
            if grant is None or grant["client_id"] != form["client_id"]:
                return httpx.Response(400, json={"error": "invalid_grant"})
            access = self.issue(scope=grant["scope"], client_id=form["client_id"])
            body = {"access_token": access, "token_type": "bearer", "expires_in": 86400, "scope": grant["scope"]}
            if self.rotate_refresh_tokens:
                new_refresh = secrets.token_hex(8)
                self.refresh_tokens[new_refresh] = self.refresh_tokens.pop(form["refresh_token"])
                body["refresh_token"] = new_refresh
            return httpx.Response(200, json=body)
        return httpx.Response(400, json={"error": "unsupported_grant_type"})

    def _resource(self, request: httpx.Request) -> httpx.Response:
        """Act as the protected resource: metadata, 401 challenges and scope checks."""
        if request.url.path.startswith("/.well-known/oauth-protected-resource"):
            if self.serve_prm_at_well_known and self.prm is not None:
                return httpx.Response(200, json=self.prm)
            return httpx.Response(404)
        if request.url.path == "/hidden-prm" and self.prm is not None:
            return httpx.Response(200, json=self.prm)
        challenge_url = (
            "https://api.example.com/.well-known/oauth-protected-resource/mcp"
            if self.serve_prm_at_well_known
            else "https://api.example.com/hidden-prm"
        )
        authorization = request.headers.get("authorization", "")
        token = authorization[7:] if authorization.lower().startswith("bearer ") else None
        data = self.active_tokens.get(token or "")
        if not data:
            error = ', error="invalid_token"' if token else ""
            return httpx.Response(
                401, headers={"WWW-Authenticate": f'Bearer resource_metadata="{challenge_url}"{error}'}
            )
        if self.resource_required_scope and self.resource_required_scope not in data["scope"].split():
            return httpx.Response(
                403,
                headers={
                    "WWW-Authenticate": f'Bearer error="insufficient_scope", scope="{self.resource_required_scope}", '
                    f'resource_metadata="{challenge_url}"'
                },
            )
        return httpx.Response(200, json={"ok": True, "sub": data["sub"]})


def _form(request: httpx.Request) -> Dict[str, str]:
    """Decode a form-encoded request body."""
    return {
        k: unquote_plus(v)
        for k, v in (pair.split("=", 1) for pair in request.content.decode().split("&") if "=" in pair)
    }
