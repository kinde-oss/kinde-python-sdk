"""
Agent-client helpers: sign a user in to an MCP server or API protected by an OAuth resource server.

Works against any spec-compliant server (RFC 9728, RFC 8414, RFC 7591, RFC 7636,
RFC 8707 and the CIMD draft), with Kinde's quirks handled: no ``openid`` scope,
no ID token, a secret always returned by registration, and a refresh token that
may or may not rotate.

Agents built on the official ``mcp`` client should use
``kinde_sdk.agents.mcp.KindeOAuthClientProvider`` instead.
"""

import asyncio
import base64
import hashlib
import html
import logging
import secrets
import time
import webbrowser
from dataclasses import asdict, dataclass, field
from typing import Any, Awaitable, Callable, Dict, List, Optional, Sequence, Tuple
from urllib.parse import parse_qs, quote_plus, urlencode, urlsplit

import httpx

from kinde_sdk.agents.client_metadata import validate_client_metadata_url
from kinde_sdk.agents.config import (
    AUTHORIZATION_SERVER_WELL_KNOWN,
    PROTECTED_RESOURCE_WELL_KNOWN,
    is_loopback_host,
)
from kinde_sdk.agents.errors import (
    AgentClientError,
    AgentConfigError,
    AuthorizationError,
    DiscoveryError,
    RegistrationError,
    TokenRequestError,
)
from kinde_sdk.agents.storage import AgentClientStorage, InMemoryAgentStorage
from kinde_sdk.agents.www_authenticate import find_bearer_challenge

logger = logging.getLogger("kinde_sdk.agents")

_METADATA_CACHE_SECONDS = 300
_REFRESH_MARGIN_SECONDS = 60
_REREGISTER_MARGIN_SECONDS = 86400
_DEFAULT_PORTS = {"http": 80, "https": 443}


class AuthorizationRequiredError(AgentClientError):
    """The user has to sign in, and this client can't open a browser on its own.

    Server-hosted agents handle it with :meth:`KindeAgentClient.begin_authorization`
    and :meth:`KindeAgentClient.complete_authorization`.
    """


def _origin(url: str) -> Tuple[str, str, Optional[int]]:
    """Return (scheme, host, port) with the default port filled in, for same-origin checks."""
    parts = urlsplit(url)
    return parts.scheme.lower(), (parts.hostname or "").lower(), parts.port or _DEFAULT_PORTS.get(parts.scheme.lower())


def _require_secure(url: str, what: str) -> None:
    """Raise :class:`DiscoveryError` unless ``url`` is https, or http on a loopback host."""
    parts = urlsplit(url)
    if parts.scheme == "https" and parts.hostname:
        return
    if parts.scheme == "http" and is_loopback_host(parts.hostname):
        return
    raise DiscoveryError(f"Refusing a non-https {what}: {url}")


def resource_covers(prm_resource: str, resource_url: str) -> bool:
    """Whether metadata for ``prm_resource`` applies to ``resource_url``: same origin, same or parent path."""
    if _origin(prm_resource) != _origin(resource_url):
        return False
    base = urlsplit(prm_resource).path.rstrip("/")
    path = urlsplit(resource_url).path.rstrip("/")
    return path == base or path.startswith(base + "/")


def protected_resource_metadata_urls(resource_url: str) -> List[str]:
    """The path-suffixed then root RFC 9728 URLs for a resource."""
    parts = urlsplit(resource_url)
    origin = f"{parts.scheme}://{parts.netloc}"
    path = parts.path.rstrip("/")
    urls = [origin + PROTECTED_RESOURCE_WELL_KNOWN + path] if path else []
    urls.append(origin + PROTECTED_RESOURCE_WELL_KNOWN)
    return urls


def authorization_server_metadata_urls(issuer: str) -> List[str]:
    """RFC 8414 path insertion first (what Kinde serves), then the OIDC discovery forms."""
    parts = urlsplit(issuer)
    origin = f"{parts.scheme}://{parts.netloc}"
    path = parts.path.rstrip("/")
    if not path:
        return [origin + AUTHORIZATION_SERVER_WELL_KNOWN, origin + "/.well-known/openid-configuration"]
    return [
        origin + AUTHORIZATION_SERVER_WELL_KNOWN + path,
        origin + "/.well-known/openid-configuration" + path,
        origin + path + "/.well-known/openid-configuration",
    ]


def _oauth_error(response: httpx.Response) -> Tuple[Optional[str], Optional[str]]:
    """Return the OAuth ``error`` and ``error_description`` from a response, if it has them."""
    try:
        body = response.json()
    except ValueError:
        return None, None
    if not isinstance(body, dict):
        return None, None
    return body.get("error"), body.get("error_description")


def _pkce_pair() -> Tuple[str, str]:
    # 86 characters from the unreserved set: 512 bits of entropy
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    return verifier, challenge


@dataclass
class PendingAuthorization:
    """One authorization attempt. Keep it server-side (for example in the session) until the callback.

    Use :meth:`to_dict` and :meth:`from_dict` to store it. It holds the PKCE
    verifier, so never send it to the browser.
    """

    authorization_url: str
    state: str
    redirect_uri: str
    scope: str
    issuer: str
    client_id: str
    code_verifier: str = field(repr=False)
    registration_key: Optional[str] = None
    created_at: float = field(default_factory=time.time)
    used: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PendingAuthorization":
        return cls(**data)


class _LoopbackListener:
    """Accepts one browser redirect on a loopback address (RFC 8252 §7.3), then stops."""

    def __init__(self, redirect_uri: str):
        """Check the redirect URI is http on a loopback host and remember where to listen."""
        parts = urlsplit(redirect_uri)
        if parts.scheme != "http" or not is_loopback_host(parts.hostname):
            raise AgentConfigError(f"A loopback redirect URI is required, got {redirect_uri!r}")
        self._host = parts.hostname
        self._netloc_host = f"[{parts.hostname}]" if ":" in parts.hostname else parts.hostname
        self._port = parts.port or 0
        self._bound_port = self._port
        self._path = parts.path or "/"
        self._server: Optional[asyncio.AbstractServer] = None
        self._result: Optional[asyncio.Future] = None
        self.redirect_uri = redirect_uri
        # Set once the authorization request exists; callbacks with any other state are ignored
        self.expected_state: Optional[str] = None

    async def start(self) -> None:
        """Start listening, on an ephemeral port when the redirect URI has none."""
        self._result = asyncio.get_running_loop().create_future()
        bind = "127.0.0.1" if self._host == "localhost" else self._host
        self._server = await asyncio.start_server(self._handle, bind, self._port)
        self._bound_port = self._server.sockets[0].getsockname()[1]
        self.redirect_uri = f"http://{self._netloc_host}:{self._bound_port}{self._path}"

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Answer one HTTP request; complete the sign-in only for the callback path with the expected state."""
        try:
            request_line = (await asyncio.wait_for(reader.readline(), 10)).decode("latin-1")
            while (await asyncio.wait_for(reader.readline(), 10)) not in (b"\r\n", b"\n", b""):
                pass
            method, _, rest = request_line.partition(" ")
            target = rest.rsplit(" ", 1)[0]
            query = parse_qs(urlsplit(target).query)
            state = (query.get("state") or [""])[0]
            if (
                method != "GET"
                or urlsplit(target).path != self._path
                or self._result.done()
                or self.expected_state is None
                or not secrets.compare_digest(state.encode(), self.expected_state.encode())
            ):
                # Another local process can't end the sign-in by calling the callback first
                writer.write(b"HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
                return
            failed = "error" in query
            message = "Sign-in failed. You can close this tab." if failed else "Signed in. You can close this tab."
            body = f"<!doctype html><title>Kinde</title><p>{html.escape(message)}</p>".encode()
            writer.write(
                b"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nConnection: close\r\n"
                + f"Content-Length: {len(body)}\r\n\r\n".encode()
                + body
            )
            self._result.set_result(f"http://{self._netloc_host}:{self._bound_port}{target}")
        except (asyncio.TimeoutError, ConnectionError, UnicodeDecodeError):
            pass
        finally:
            try:
                await writer.drain()
            except ConnectionError:
                pass
            writer.close()

    async def wait(self, timeout: float) -> str:
        """Wait for the callback URL, raising :class:`AuthorizationError` on timeout."""
        try:
            return await asyncio.wait_for(asyncio.shield(self._result), timeout)
        except asyncio.TimeoutError as exc:
            raise AuthorizationError("Timed out waiting for the browser to finish signing in") from exc

    async def close(self) -> None:
        """Stop listening."""
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
            self._server = None


class KindeAgentClient:
    """Signs a user in to a protected MCP server or API, then calls it with a bearer token.

    Client identity is chosen in this order: the CIMD document URL when the
    authorization server supports it, a pre-registered ``client_id``, then
    dynamic client registration.

    CLI agent with a loopback redirect::

        client = KindeAgentClient(
            "https://api.example.com/mcp",
            client_metadata_url="https://agent.example.com/oauth/client-metadata.json",
            client_name="Example Agent",
        )
        await client.connect()             # opens the browser if a sign-in is needed
        response = await client.request("POST", json={...})

    Server-hosted agent: pass ``redirect_uri`` and use :meth:`begin_authorization`
    and :meth:`complete_authorization` in your login and callback routes.
    """

    def __init__(
        self,
        resource_url: str,
        *,
        client_metadata_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token_endpoint_auth_method: Optional[str] = None,
        client_name: str = "Kinde agent",
        redirect_uri: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        storage: Optional[AgentClientStorage] = None,
        account: str = "default",
        open_browser: Optional[Callable[[str], Any]] = None,
        authorization_handler: Optional[Callable[[str], Awaitable[str]]] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        timeout_seconds: float = 10.0,
        callback_timeout_seconds: float = 300.0,
    ):
        """Validate the configuration and set up storage and the HTTP client."""
        _require_secure_resource(resource_url)
        if client_metadata_url is not None:
            validate_client_metadata_url(client_metadata_url)
        if client_secret and not client_id:
            raise AgentConfigError("client_secret needs a client_id")
        self.resource_url = resource_url
        self.client_metadata_url = client_metadata_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint_auth_method = token_endpoint_auth_method or (
            "client_secret_post" if client_secret else "none"
        )
        self.client_name = client_name
        # No port means "pick a free one" for a loopback listener
        self.redirect_uri = redirect_uri or "http://127.0.0.1/callback"
        self.scopes = list(scopes) if scopes else ["offline"]
        self.storage = storage or InMemoryAgentStorage()
        self.account = account
        self.open_browser = open_browser or webbrowser.open
        self.authorization_handler = authorization_handler
        self.callback_timeout_seconds = callback_timeout_seconds
        self._http = http_client or httpx.AsyncClient(timeout=timeout_seconds)
        self._owns_http = http_client is None
        self._prm: Optional[Dict[str, Any]] = None
        self._as_metadata: Optional[Dict[str, Any]] = None
        self._metadata_at = 0.0
        self._locks: Dict[str, asyncio.Lock] = {}

    # -- Lifecycle ------------------------------------------------------------

    async def aclose(self) -> None:
        """Close the HTTP client if this client created it."""
        if self._owns_http:
            await self._http.aclose()

    async def __aenter__(self) -> "KindeAgentClient":
        return self

    async def __aexit__(self, *exc_info) -> None:
        await self.aclose()

    def _lock_for(self, name: str) -> asyncio.Lock:
        """Return the named lock, creating it lazily so it binds to the running event loop."""
        lock = self._locks.get(name)
        if lock is None:
            lock = self._locks[name] = asyncio.Lock()
        return lock

    @property
    def _token_key(self) -> str:
        return f"{self.resource_url}|{self.account}"

    @property
    def issuer(self) -> Optional[str]:
        """The discovered authorization server's issuer, or ``None`` before discovery."""
        return self._as_metadata.get("issuer") if self._as_metadata else None

    # -- Discovery ------------------------------------------------------------

    async def discover(
        self, challenge_response: Optional[httpx.Response] = None, *, force: bool = False
    ) -> Dict[str, Any]:
        """Find the authorization server for the resource and return its metadata (cached 5 minutes)."""
        fresh = self._as_metadata is not None and time.monotonic() - self._metadata_at < _METADATA_CACHE_SECONDS
        if fresh and not force and challenge_response is None:
            return self._as_metadata

        prm = await self._fetch_protected_resource_metadata(challenge_response)
        resource = prm.get("resource")
        if not isinstance(resource, str) or not resource_covers(resource, self.resource_url):
            raise DiscoveryError(f"The protected resource metadata is for a different resource: {resource!r}")
        servers = prm.get("authorization_servers")
        if not isinstance(servers, list) or not servers or not isinstance(servers[0], str):
            raise DiscoveryError("The protected resource metadata lists no authorization server")
        issuer = servers[0]
        _require_secure(issuer, "authorization server")

        metadata = await self._fetch_authorization_server_metadata(issuer)
        stored = await self.storage.get_tokens(self._token_key)
        if stored and stored.get("issuer") != issuer:
            # Tokens are bound to the issuer that granted them
            logger.info("The authorization server changed; discarding stored tokens")
            await self.storage.delete_tokens(self._token_key)
        self._prm, self._as_metadata, self._metadata_at = prm, metadata, time.monotonic()
        return metadata

    async def _get_json(self, url: str) -> Optional[Dict[str, Any]]:
        """GET a URL; return its JSON object body, or ``None`` when it isn't one."""
        try:
            response = await self._http.get(url, headers={"Accept": "application/json"})
        except httpx.HTTPError as exc:
            raise DiscoveryError(f"Could not fetch {url}: {type(exc).__name__}") from exc
        if response.status_code != 200:
            return None
        try:
            body = response.json()
        except ValueError:
            return None
        return body if isinstance(body, dict) else None

    async def _fetch_protected_resource_metadata(self, challenge_response: Optional[httpx.Response]) -> Dict[str, Any]:
        """Find the RFC 9728 document: challenge URL, then well-known URLs, then a probe."""
        candidates: List[str] = []
        if challenge_response is not None:
            challenge = find_bearer_challenge(challenge_response.headers.get_list("www-authenticate"))
            metadata_url = challenge.get("resource_metadata") if challenge else None
            if metadata_url and self._may_fetch(metadata_url):
                candidates.append(metadata_url)
        for url in protected_resource_metadata_urls(self.resource_url):
            if url not in candidates:
                candidates.append(url)
        for url in candidates:
            _require_secure(url, "protected resource metadata URL")
            document = await self._get_json(url)
            if document is not None:
                return document
        if challenge_response is None:
            # No well-known document: ask the resource itself for a challenge
            try:
                probe = await self._http.get(self.resource_url)
            except httpx.HTTPError as exc:
                raise DiscoveryError(f"Could not reach {self.resource_url}: {type(exc).__name__}") from exc
            challenge = find_bearer_challenge(probe.headers.get_list("www-authenticate"))
            metadata_url = challenge.get("resource_metadata") if challenge else None
            if probe.status_code == 401 and metadata_url not in (None, *candidates) and self._may_fetch(metadata_url):
                return await self._fetch_protected_resource_metadata(probe)
        raise DiscoveryError(f"No protected resource metadata found for {self.resource_url}")

    def _may_fetch(self, metadata_url: str) -> bool:
        """Whether a ``resource_metadata`` URL from a challenge is safe to fetch."""
        # A remote resource must not point the agent at a service on this machine
        if is_loopback_host(urlsplit(metadata_url).hostname) and not is_loopback_host(
            urlsplit(self.resource_url).hostname
        ):
            logger.warning("Ignoring a loopback resource_metadata URL from a remote resource: %s", metadata_url)
            return False
        return True

    async def _fetch_authorization_server_metadata(self, issuer: str) -> Dict[str, Any]:
        """Fetch and validate the issuer's metadata (issuer match, PKCE S256, https)."""
        for url in authorization_server_metadata_urls(issuer):
            metadata = await self._get_json(url)
            if metadata is None:
                continue
            # RFC 8414 §3.3: the document must name the issuer it was fetched for
            if metadata.get("issuer") != issuer:
                raise DiscoveryError(
                    f"Authorization server metadata issuer mismatch: {metadata.get('issuer')!r} != {issuer!r}"
                )
            if "S256" not in (metadata.get("code_challenge_methods_supported") or []):
                raise DiscoveryError("The authorization server does not advertise PKCE S256")
            for name in ("authorization_endpoint", "token_endpoint"):
                if not isinstance(metadata.get(name), str):
                    raise DiscoveryError(f"The authorization server metadata has no {name}")
            for name in ("authorization_endpoint", "token_endpoint", "registration_endpoint", "revocation_endpoint"):
                if metadata.get(name):
                    _require_secure(metadata[name], name.replace("_", " "))
            return metadata
        raise DiscoveryError(f"No authorization server metadata found for {issuer}")

    # -- Client identity ------------------------------------------------------

    def _effective_scope(self, scopes: Optional[Sequence[str]] = None) -> str:
        """The scope to request: configured or given scopes, without ``openid`` if unsupported."""
        requested = list(scopes) if scopes else list(self.scopes)
        supported = (self._as_metadata or {}).get("scopes_supported")
        if isinstance(supported, list) and "openid" not in supported and "openid" in requested:
            # Kinde's agent issuer refuses openid with invalid_scope
            logger.debug("Dropping the openid scope, which the authorization server does not support")
            requested = [scope for scope in requested if scope != "openid"]
        seen: List[str] = []
        for scope in requested:
            if scope not in seen:
                seen.append(scope)
        return " ".join(seen)

    async def _client_identity(self, redirect_uri: str) -> Dict[str, Any]:
        """Pick the client identity: CIMD URL, pre-registered client, or a (re)used DCR registration."""
        metadata = self._as_metadata or {}
        if self.client_metadata_url and metadata.get("client_id_metadata_document_supported") is True:
            return {"client_id": self.client_metadata_url, "auth_method": "none"}
        if self.client_id:
            return {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "auth_method": self.token_endpoint_auth_method,
            }
        if not metadata.get("registration_endpoint"):
            raise AgentConfigError(
                "The authorization server supports neither client ID metadata documents nor registration; "
                "configure client_id"
            )
        key = f"{metadata['issuer']}|{redirect_uri}"
        registration = await self.storage.get_registration(key)
        if registration:
            expires_at = registration.get("client_secret_expires_at") or 0
            if not expires_at or expires_at - time.time() > _REREGISTER_MARGIN_SECONDS:
                return _identity_from_registration(registration, key)
        return _identity_from_registration(await self._register(redirect_uri, key), key)

    async def _register(self, redirect_uri: str, key: str) -> Dict[str, Any]:
        """Register this agent with DCR and store the registration."""
        endpoint = self._as_metadata["registration_endpoint"]
        request = {
            "redirect_uris": [redirect_uri],
            "client_name": self.client_name,
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
            # Spec-correct for a public client; Kinde answers client_secret_post and a secret regardless
            "token_endpoint_auth_method": "none",
        }
        try:
            response = await self._http.post(endpoint, json=request)
        except httpx.HTTPError as exc:
            raise RegistrationError(f"Could not reach the registration endpoint: {type(exc).__name__}") from exc
        error, description = _oauth_error(response)
        if response.status_code == 429:
            raise RegistrationError("Too many registrations; try again later", error=error or "too_many_registrations")
        if response.status_code == 404:
            # The application behind this issuer is gone
            await self.storage.delete_tokens(self._token_key)
            await self.storage.delete_registration(key)
            raise RegistrationError("The authorization server no longer exists", error=error)
        if response.status_code not in (200, 201):
            if error == "invalid_redirect_uri":
                # The description names the host to add to the application's Trusted agent hosts
                raise RegistrationError(
                    description or "The redirect URI was refused", error=error, error_description=description
                )
            raise RegistrationError(
                f"Registration failed with HTTP {response.status_code}: {description or error or 'no details'}",
                error=error,
                error_description=description,
            )
        try:
            body = response.json()
        except ValueError as exc:
            raise RegistrationError("The registration response was not JSON") from exc
        if not isinstance(body, dict) or not body.get("client_id"):
            raise RegistrationError("The registration response has no client_id")
        secret = body.get("client_secret")
        registration = {
            "client_id": body["client_id"],
            "client_secret": secret,
            # Use what came back, not what was asked for
            "token_endpoint_auth_method": body.get("token_endpoint_auth_method")
            or ("client_secret_post" if secret else "none"),
            "client_secret_expires_at": body.get("client_secret_expires_at") or 0,
            "redirect_uri": redirect_uri,
            "issuer": self._as_metadata["issuer"],
        }
        await self.storage.set_registration(key, registration)
        return registration

    async def _identity_for(
        self, client_id: Optional[str], registration_key: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """The identity (with its secret) that a token or authorization attempt was issued to."""
        if registration_key:
            registration = await self.storage.get_registration(registration_key)
            if not registration or registration.get("client_id") != client_id:
                return None
            return _identity_from_registration(registration, registration_key)
        if self.client_id and client_id == self.client_id:
            return {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "auth_method": self.token_endpoint_auth_method,
            }
        return {"client_id": client_id, "auth_method": "none"}

    async def _identity_for_tokens(self, tokens: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return await self._identity_for(tokens.get("client_id"), tokens.get("registration_key"))

    @staticmethod
    def _apply_client_auth(identity: Dict[str, Any], data: Dict[str, str], headers: Dict[str, str]) -> None:
        """Add client authentication to a token request, using the method the server returned."""
        method = identity.get("auth_method") or "none"
        secret = identity.get("client_secret")
        if method == "client_secret_basic" and secret:
            raw = f"{quote_plus(identity['client_id'])}:{quote_plus(secret)}"
            headers["Authorization"] = "Basic " + base64.b64encode(raw.encode()).decode()
            return
        data["client_id"] = identity["client_id"]
        if method == "client_secret_post" and secret:
            data["client_secret"] = secret

    # -- Authorization --------------------------------------------------------

    async def begin_authorization(
        self, *, redirect_uri: Optional[str] = None, scopes: Optional[Sequence[str]] = None
    ) -> PendingAuthorization:
        """Start a sign-in: returns the URL to send the user to and the state to keep until the callback."""
        metadata = await self.discover()
        redirect_uri = redirect_uri or self.redirect_uri
        identity = await self._client_identity(redirect_uri)
        verifier, challenge = _pkce_pair()
        state = secrets.token_urlsafe(32)
        scope = self._effective_scope(scopes)
        params = {
            "response_type": "code",
            "client_id": identity["client_id"],
            "redirect_uri": redirect_uri,
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            # RFC 8707, which MCP requires; Kinde ignores it and sets the audience from the path
            "resource": self.resource_url,
        }
        if scope:
            params["scope"] = scope
        endpoint = metadata["authorization_endpoint"]
        url = endpoint + ("&" if "?" in endpoint else "?") + urlencode(params)
        return PendingAuthorization(
            authorization_url=url,
            state=state,
            redirect_uri=redirect_uri,
            scope=scope,
            issuer=metadata["issuer"],
            client_id=identity["client_id"],
            code_verifier=verifier,
            registration_key=identity.get("registration_key"),
        )

    async def complete_authorization(self, pending: PendingAuthorization, callback_url: str) -> None:
        """Finish a sign-in from the full callback URL the browser was sent to."""
        if pending.used:
            raise AuthorizationError("This authorization attempt was already used")
        pending.used = True
        query = parse_qs(urlsplit(callback_url).query)
        state = (query.get("state") or [""])[0]
        if not secrets.compare_digest(state.encode(), pending.state.encode()):
            raise AuthorizationError("The state on the callback does not match")
        error = (query.get("error") or [None])[0]
        if error:
            description = (query.get("error_description") or [None])[0]
            message = f"Authorization failed: {error}" + (f" ({description})" if description else "")
            if error == "invalid_client" and self.client_metadata_url:
                message += ". Check the client metadata host is in the application's Trusted agent hosts."
            raise AuthorizationError(message, error=error, error_description=description)
        issuer = (query.get("iss") or [None])[0]
        if issuer is not None and issuer != pending.issuer:
            # RFC 9207: a different issuer means a mix-up attack or misconfiguration
            raise AuthorizationError("The callback came from a different authorization server")
        code = (query.get("code") or [None])[0]
        if not code:
            raise AuthorizationError("The callback has no authorization code")

        metadata = await self.discover()
        if metadata.get("issuer") != pending.issuer:
            # Never send the code and verifier to an authorization server other than the one that issued the code
            raise AuthorizationError("The authorization server changed since sign-in started; start again")
        # The code is bound to the client that started this attempt, so never re-resolve or re-register here
        identity = await self._identity_for(pending.client_id, pending.registration_key)
        if identity is None:
            raise AuthorizationError("The client registration for this attempt is gone; start again")
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": pending.redirect_uri,
            "code_verifier": pending.code_verifier,
            "resource": self.resource_url,
        }
        headers = {"Accept": "application/json"}
        self._apply_client_auth(identity, data, headers)
        response = await self._post_token(metadata["token_endpoint"], data, headers)
        if response.status_code != 200:
            error, description = _oauth_error(response)
            if error == "invalid_client" and identity.get("registration_key"):
                await self.storage.delete_registration(identity["registration_key"])
            raise TokenRequestError(
                f"The code exchange failed: {error or response.status_code}", error=error, error_description=description
            )
        await self._store_token_response(response, identity, pending.redirect_uri, previous=None)

    async def authorize(
        self, *, scopes: Optional[Sequence[str]] = None, challenge_response: Optional[httpx.Response] = None
    ) -> None:
        """Run a full sign-in now, through ``authorization_handler`` or a loopback listener and the system browser."""
        await self.discover(challenge_response)
        if self.authorization_handler is not None:
            pending = await self.begin_authorization(scopes=scopes)
            callback_url = await self.authorization_handler(pending.authorization_url)
            await self.complete_authorization(pending, callback_url)
            return
        parts = urlsplit(self.redirect_uri)
        if not (parts.scheme == "http" and is_loopback_host(parts.hostname)):
            raise AuthorizationRequiredError(
                "The user must sign in. Send them to begin_authorization().authorization_url, "
                "then call complete_authorization() from your callback route."
            )
        listener = _LoopbackListener(self.redirect_uri)
        await listener.start()
        try:
            pending = await self.begin_authorization(redirect_uri=listener.redirect_uri, scopes=scopes)
            listener.expected_state = pending.state
            result = self.open_browser(pending.authorization_url)
            if asyncio.iscoroutine(result):
                await result
            callback_url = await listener.wait(self.callback_timeout_seconds)
        finally:
            await listener.close()
        await self.complete_authorization(pending, callback_url)

    # -- Tokens ---------------------------------------------------------------

    async def _post_token(self, endpoint: str, data: Dict[str, str], headers: Dict[str, str]) -> httpx.Response:
        """POST to the token endpoint, turning network errors into :class:`TokenRequestError`."""
        try:
            return await self._http.post(endpoint, data=data, headers=headers)
        except httpx.HTTPError as exc:
            raise TokenRequestError(f"Could not reach the token endpoint: {type(exc).__name__}") from exc

    async def _store_token_response(
        self,
        response: httpx.Response,
        identity: Dict[str, Any],
        redirect_uri: Optional[str],
        previous: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Store a token response, keeping the previous refresh token when none is returned."""
        try:
            body = response.json()
        except ValueError as exc:
            raise TokenRequestError("The token response was not JSON") from exc
        if not isinstance(body, dict) or not body.get("access_token"):
            raise TokenRequestError("The token response has no access_token")
        # No id_token is expected: Kinde's agent issuer never returns one
        expires_in = body.get("expires_in")
        tokens = {
            "access_token": body["access_token"],
            "token_type": body.get("token_type", "bearer"),
            # Replace a rotated refresh token; keep the old one when the server doesn't send one
            "refresh_token": body.get("refresh_token") or (previous or {}).get("refresh_token"),
            "expires_at": time.time() + float(expires_in) if isinstance(expires_in, (int, float)) else None,
            "scope": body.get("scope") or (previous or {}).get("scope"),
            "issuer": self._as_metadata["issuer"],
            "resource_url": self.resource_url,
            "client_id": identity["client_id"],
            "registration_key": identity.get("registration_key"),
            "redirect_uri": redirect_uri,
        }
        await self.storage.set_tokens(self._token_key, tokens)
        return tokens

    @staticmethod
    def _expiring(tokens: Dict[str, Any]) -> bool:
        """Whether the access token expires within the refresh margin."""
        expires_at = tokens.get("expires_at")
        return expires_at is not None and expires_at - time.time() < _REFRESH_MARGIN_SECONDS

    async def refresh(self, *, stale_access_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Refresh the stored tokens. Returns ``None`` when a new sign-in is needed.

        Concurrent callers share one refresh request: whoever waits behind it
        picks up the tokens it stored.
        """
        async with self._lock_for("_refresh_lock"):
            tokens = await self.storage.get_tokens(self._token_key)
            if not tokens:
                return None
            if stale_access_token and tokens.get("access_token") != stale_access_token and not self._expiring(tokens):
                return tokens  # someone else refreshed while we waited
            if not tokens.get("refresh_token"):
                return None
            metadata = await self.discover()
            # discover() drops the tokens when the issuer changed: never send them to the new one
            tokens = await self.storage.get_tokens(self._token_key)
            if not tokens or not tokens.get("refresh_token") or tokens.get("issuer") != metadata.get("issuer"):
                return None
            identity = await self._identity_for_tokens(tokens)
            if identity is None:
                await self.storage.delete_tokens(self._token_key)
                return None
            data = {
                "grant_type": "refresh_token",
                "refresh_token": tokens["refresh_token"],
                "resource": self.resource_url,
            }
            headers = {"Accept": "application/json"}
            self._apply_client_auth(identity, data, headers)
            response = await self._post_token(metadata["token_endpoint"], data, headers)
            if response.status_code == 200:
                return await self._store_token_response(response, identity, tokens.get("redirect_uri"), previous=tokens)
            error, description = _oauth_error(response)
            if error == "invalid_grant":
                # Revoked, expired after 15 days, or the application was deleted
                await self.storage.delete_tokens(self._token_key)
                return None
            if error == "invalid_client":
                # The registration expired: register again and sign in again
                if identity.get("registration_key"):
                    await self.storage.delete_registration(identity["registration_key"])
                await self.storage.delete_tokens(self._token_key)
                return None
            raise TokenRequestError(
                f"The refresh failed: {error or response.status_code}", error=error, error_description=description
            )

    async def _usable_tokens(self) -> Dict[str, Any]:
        """Return stored tokens, refreshing or signing in first when needed."""
        tokens = await self.storage.get_tokens(self._token_key)
        if tokens and self._expiring(tokens):
            tokens = await self.refresh(stale_access_token=tokens["access_token"])
        if not tokens:
            tokens = await self._sign_in(None)
        return tokens

    async def _sign_in(
        self,
        stale_access_token: Optional[str],
        *,
        scopes: Optional[Sequence[str]] = None,
        challenge_response: Optional[httpx.Response] = None,
    ) -> Dict[str, Any]:
        """Run one sign-in for every caller that needs it, so concurrent requests open one browser, not many."""
        async with self._lock_for("_sign_in_lock"):
            tokens = await self.storage.get_tokens(self._token_key)
            if (
                tokens
                and tokens.get("access_token") != stale_access_token
                and not self._expiring(tokens)
                and set(scopes or ()) <= set((tokens.get("scope") or "").split())
            ):
                return tokens  # another caller signed in while we waited
            await self.authorize(scopes=scopes, challenge_response=challenge_response)
            tokens = await self.storage.get_tokens(self._token_key)
            if not tokens:
                raise AuthorizationRequiredError("No tokens after signing in")
            return tokens

    async def connect(self) -> None:
        """Make sure the client holds usable tokens, signing the user in if needed."""
        await self._usable_tokens()

    async def get_token_info(self) -> Optional[Dict[str, Any]]:
        """What the client holds, without the raw tokens."""
        tokens = await self.storage.get_tokens(self._token_key)
        if not tokens:
            return None
        return {
            "scopes": (tokens.get("scope") or "").split(),
            "expires_at": tokens.get("expires_at"),
            "client_id": tokens.get("client_id"),
            "issuer": tokens.get("issuer"),
            "has_refresh_token": bool(tokens.get("refresh_token")),
        }

    async def get_access_token(self) -> str:
        """A valid access token for the resource, refreshing or signing in first if needed."""
        return (await self._usable_tokens())["access_token"]

    # -- Calling the resource -------------------------------------------------

    def _resolve(self, url: str) -> str:
        """Resolve ``url`` against the resource URL, refusing other origins."""
        if not url:
            return self.resource_url
        if url.startswith("/"):
            parts = urlsplit(self.resource_url)
            return f"{parts.scheme}://{parts.netloc}{url}"
        if _origin(url) != _origin(self.resource_url):
            # The token is for this resource only
            raise AgentConfigError(f"Refusing to send the access token to another origin: {url}")
        return url

    async def request(self, method: str, url: str = "", **kwargs: Any) -> httpx.Response:
        """Call the resource with the bearer token, refreshing, re-authorizing and stepping up as needed.

        ``url`` is empty (the resource URL itself), a path on the resource's
        origin, or an absolute URL on that origin.
        """
        target = self._resolve(url)
        headers = dict(kwargs.pop("headers", None) or {})
        tokens = await self._usable_tokens()

        async def send(access_token: str) -> httpx.Response:
            return await self._http.request(
                method, target, headers={**headers, "Authorization": f"Bearer {access_token}"}, **kwargs
            )

        response = await send(tokens["access_token"])
        if response.status_code == 401:
            refreshed = await self.refresh(stale_access_token=tokens["access_token"])
            if refreshed:
                response = await send(refreshed["access_token"])
            if response.status_code == 401:
                tokens = await self._sign_in(tokens["access_token"], challenge_response=response)
                response = await send(tokens["access_token"])
        if response.status_code == 403:
            challenge = find_bearer_challenge(response.headers.get_list("www-authenticate"))
            if challenge and challenge.get("error") == "insufficient_scope":
                # Step up once: we are signed in, but need more scope
                current = (await self.storage.get_tokens(self._token_key) or {}).get("scope") or " ".join(self.scopes)
                wanted = list(dict.fromkeys(current.split() + (challenge.get("scope") or "").split()))
                tokens = await self._sign_in(tokens["access_token"], scopes=wanted, challenge_response=response)
                response = await send(tokens["access_token"])
        return response

    async def disconnect(self, *, forget: bool = False) -> None:
        """Revoke the tokens (best effort) and clear them.

        ``forget`` also drops the DCR registration for this redirect URI, even when
        no tokens are stored.
        """
        tokens = await self.storage.get_tokens(self._token_key)
        if forget and not tokens:
            try:
                metadata = await self.discover()
            except AgentClientError:
                return
            await self.storage.delete_registration(f"{metadata['issuer']}|{self.redirect_uri}")
            return
        if tokens:
            identity = await self._identity_for_tokens(tokens)
            try:
                metadata = await self.discover()
            except AgentClientError:
                metadata = {}
            endpoint = metadata.get("revocation_endpoint")
            if endpoint and identity:
                # On Kinde revoking either token of the pair revokes both
                token, hint = (
                    (tokens["refresh_token"], "refresh_token")
                    if tokens.get("refresh_token")
                    else (tokens["access_token"], "access_token")
                )
                data = {"token": token, "token_type_hint": hint}
                headers: Dict[str, str] = {}
                self._apply_client_auth(identity, data, headers)
                try:
                    response = await self._http.post(endpoint, data=data, headers=headers)
                    if response.status_code != 200:
                        logger.info("Token revocation returned HTTP %s", response.status_code)
                except httpx.HTTPError as exc:
                    logger.info("Token revocation failed: %s", type(exc).__name__)
            await self.storage.delete_tokens(self._token_key)
            if forget and tokens.get("registration_key"):
                await self.storage.delete_registration(tokens["registration_key"])


def _identity_from_registration(registration: Dict[str, Any], key: str) -> Dict[str, Any]:
    """Turn a stored DCR registration into a client identity."""
    return {
        "client_id": registration["client_id"],
        "client_secret": registration.get("client_secret"),
        "auth_method": registration.get("token_endpoint_auth_method") or "none",
        "registration_key": key,
    }


def _require_secure_resource(resource_url: str) -> None:
    """Raise :class:`AgentConfigError` unless the resource URL is https or http loopback."""
    try:
        _require_secure(resource_url, "resource URL")
    except DiscoveryError as exc:
        raise AgentConfigError(str(exc)) from exc
