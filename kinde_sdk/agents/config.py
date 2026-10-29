"""
Configuration for the resource-server helpers.

The application here is the Kinde application of type "AI agents and MCP", not
the SDK's normal login application. Its issuer and endpoints are derived from
the domain and its client ID, so users never type them.
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional, Sequence
from urllib.parse import urlsplit

from kinde_sdk.agents.errors import AgentConfigError

VERIFICATION_INTROSPECTION = "introspection"
VERIFICATION_JWT = "jwt"
VERIFICATION_JWT_AND_INTROSPECTION = "jwt+introspection"
VERIFICATION_STRATEGIES = (
    VERIFICATION_INTROSPECTION,
    VERIFICATION_JWT,
    VERIFICATION_JWT_AND_INTROSPECTION,
)

PROTECTED_RESOURCE_WELL_KNOWN = "/.well-known/oauth-protected-resource"
AUTHORIZATION_SERVER_WELL_KNOWN = "/.well-known/oauth-authorization-server"

_LOOPBACK_HOSTS = ("localhost", "127.0.0.1", "::1")


def is_loopback_host(host: Optional[str]) -> bool:
    """Whether ``host`` is localhost, 127.0.0.1 or ::1."""
    return (host or "").lower() in _LOOPBACK_HOSTS


def normalize_domain(domain: str) -> str:
    """Return the Kinde domain as ``https://host``, without a trailing slash.

    Accepts a bare host (``yourbiz.kinde.com``) or a URL. A custom domain is fine.
    """
    if not domain or not domain.strip():
        raise AgentConfigError("A Kinde domain is required (set KINDE_HOST or pass domain=...)")
    value = domain.strip()
    if "://" not in value:
        value = "https://" + value
    parts = urlsplit(value)
    if not parts.hostname:
        raise AgentConfigError(f"Invalid Kinde domain: {domain!r}")
    if parts.username or parts.password:
        # https://yourbiz.kinde.com@other.example would send tokens to other.example
        raise AgentConfigError(f"The Kinde domain must not contain userinfo: {domain!r}")
    if parts.scheme != "https" and not (parts.scheme == "http" and is_loopback_host(parts.hostname)):
        raise AgentConfigError(f"The Kinde domain must use https: {domain!r}")
    if parts.path not in ("", "/") or parts.query or parts.fragment:
        raise AgentConfigError(f"The Kinde domain must not have a path, query or fragment: {domain!r}")
    return f"{parts.scheme}://{parts.netloc}"


def _validate_resource_url(resource_url: str) -> str:
    """Check the Resource URL is https (http only on localhost) with no fragment or userinfo; return it as is."""
    # Kept byte for byte: Kinde stores and compares the Resource URL exactly as configured
    if not resource_url:
        raise AgentConfigError("resource_url is required (set KINDE_AGENTS_RESOURCE_URL)")
    parts = urlsplit(resource_url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise AgentConfigError(f"resource_url must be an absolute http(s) URL: {resource_url!r}")
    if parts.scheme == "http" and not is_loopback_host(parts.hostname):
        raise AgentConfigError(f"resource_url must use https unless it is on localhost: {resource_url!r}")
    if parts.fragment or parts.username or parts.password:
        raise AgentConfigError(f"resource_url must not have a fragment or userinfo: {resource_url!r}")
    return resource_url


def _with_offline(scopes: Optional[Sequence[str]]) -> List[str]:
    """Return the scopes with ``offline`` first, so agents get refresh tokens."""
    # Without offline, MCP clients never ask for a refresh token and users sign in every 24 hours
    result = list(scopes) if scopes else []
    if "offline" not in result:
        result.insert(0, "offline")
    return result


@dataclass
class AgentAuthConfig:
    """Settings for a resource server protected by a Kinde "AI agents and MCP" application.

    Args:
        domain: The Kinde domain, for example ``https://yourbiz.kinde.com`` or a custom domain.
        client_id: The AI agents and MCP application's client ID (not the login application's).
        client_secret: That application's client secret. Used for introspection and admin revoke.
        resource_url: The Resource URL configured on the application, byte for byte.
        verification: ``"introspection"`` (default), ``"jwt"`` or ``"jwt+introspection"``.
        scopes_supported: Advertised in the protected resource metadata. ``offline`` is always added.
        resource_name: Optional human-readable name advertised in the metadata.
        clock_tolerance_seconds: Leeway for ``exp`` and ``nbf``.
        introspection_cache_seconds: Cache active introspection results this long (0 disables, max 60).
        timeout_seconds: Timeout for every request to Kinde.
    """

    domain: str
    client_id: str
    resource_url: str
    client_secret: Optional[str] = field(default=None, repr=False)
    verification: str = VERIFICATION_INTROSPECTION
    scopes_supported: List[str] = field(default_factory=lambda: ["offline"])
    resource_name: Optional[str] = None
    clock_tolerance_seconds: int = 30
    introspection_cache_seconds: int = 0
    timeout_seconds: float = 5.0

    def __post_init__(self):
        """Normalise and validate the configuration."""
        self.domain = normalize_domain(self.domain)
        if not self.client_id:
            raise AgentConfigError("client_id is required (set KINDE_AGENTS_CLIENT_ID)")
        self.resource_url = _validate_resource_url(self.resource_url)
        if self.verification not in VERIFICATION_STRATEGIES:
            raise AgentConfigError(
                f"verification must be one of {', '.join(VERIFICATION_STRATEGIES)}, got {self.verification!r}"
            )
        if self.verification != VERIFICATION_JWT and not self.client_secret:
            raise AgentConfigError(
                "client_secret is required for introspection (set KINDE_AGENTS_CLIENT_SECRET), "
                "or use verification='jwt'"
            )
        self.scopes_supported = _with_offline(self.scopes_supported)
        if not 0 <= self.introspection_cache_seconds <= 60:
            raise AgentConfigError("introspection_cache_seconds must be between 0 and 60")

    @classmethod
    def from_env(cls, **overrides) -> "AgentAuthConfig":
        """Build the configuration from environment variables, with keyword overrides.

        Reads ``KINDE_AGENTS_DOMAIN`` (falling back to ``KINDE_HOST``),
        ``KINDE_AGENTS_CLIENT_ID``, ``KINDE_AGENTS_CLIENT_SECRET`` and
        ``KINDE_AGENTS_RESOURCE_URL``. ``KINDE_CLIENT_ID`` is the login
        application and is deliberately not used.
        """
        values = {
            "domain": os.getenv("KINDE_AGENTS_DOMAIN") or os.getenv("KINDE_HOST"),
            "client_id": os.getenv("KINDE_AGENTS_CLIENT_ID"),
            "client_secret": os.getenv("KINDE_AGENTS_CLIENT_SECRET"),
            "resource_url": os.getenv("KINDE_AGENTS_RESOURCE_URL"),
        }
        values.update({key: value for key, value in overrides.items() if value is not None})
        if not values.get("domain"):
            raise AgentConfigError("A Kinde domain is required (set KINDE_AGENTS_DOMAIN or KINDE_HOST)")
        return cls(**values)

    @property
    def issuer(self) -> str:
        return f"{self.domain}/oauth2/agents/{self.client_id}"

    @property
    def authorization_server_metadata_url(self) -> str:
        # RFC 8414 path insertion: the well-known segment goes between host and issuer path
        return f"{self.domain}{AUTHORIZATION_SERVER_WELL_KNOWN}/oauth2/agents/{self.client_id}"

    @property
    def jwks_url(self) -> str:
        return f"{self.domain}/.well-known/jwks"

    @property
    def introspection_url(self) -> str:
        return f"{self.issuer}/introspect"

    @property
    def revocation_url(self) -> str:
        return f"{self.issuer}/revoke"

    @property
    def protected_resource_metadata_path(self) -> str:
        """Path-suffixed metadata path, for example ``/.well-known/oauth-protected-resource/mcp``."""
        path = urlsplit(self.resource_url).path
        if path == "/":
            path = ""
        return PROTECTED_RESOURCE_WELL_KNOWN + path

    @property
    def protected_resource_metadata_url(self) -> str:
        parts = urlsplit(self.resource_url)
        return f"{parts.scheme}://{parts.netloc}{self.protected_resource_metadata_path}"
