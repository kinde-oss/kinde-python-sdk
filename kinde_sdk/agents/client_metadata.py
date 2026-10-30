"""
Client ID Metadata Documents (CIMD): the agent publishes this JSON, and its URL is the ``client_id``.

draft-ietf-oauth-client-id-metadata-document. Kinde fetches the document from
the public internet, so the host serving it must be listed in the application's
Trusted agent hosts (vendor agents such as Claude and ChatGPT are pre-trusted).
"""

import json
import warnings
from typing import Any, Dict, Iterable, Optional, Tuple
from urllib.parse import urlsplit

from kinde_sdk.agents.config import is_loopback_host
from kinde_sdk.agents.errors import AgentConfigError

MAX_DOCUMENT_BYTES = 64 * 1024


def validate_client_metadata_url(url: str) -> None:
    """Raise :class:`AgentConfigError` unless ``url`` can be a CIMD ``client_id``."""
    parts = urlsplit(url or "")
    if parts.scheme != "https" or not parts.hostname:
        raise AgentConfigError(f"The client metadata URL must be an https URL: {url!r}")
    if parts.path in ("", "/"):
        raise AgentConfigError(f"The client metadata URL needs a path, not a bare origin: {url!r}")
    if parts.username or parts.password:
        raise AgentConfigError(f"The client metadata URL must not contain userinfo: {url!r}")
    if parts.query or parts.fragment:
        raise AgentConfigError(f"The client metadata URL must not have a query or fragment: {url!r}")
    if is_loopback_host(parts.hostname):
        raise AgentConfigError("Kinde can't fetch a client metadata document from localhost; use a public host")


def _redirect_uri_problem(redirect_uri: str, document_host: str) -> Optional[Tuple[bool, str]]:
    """Return (fatal, reason) when Kinde would drop this redirect URI for a customer-trusted host."""
    parts = urlsplit(redirect_uri)
    if parts.fragment:
        return True, f"redirect URI {redirect_uri!r} must not have a fragment"
    if parts.username or parts.password:
        return True, f"redirect URI {redirect_uri!r} must not contain userinfo"
    try:
        parts.port
    except ValueError:
        return True, f"redirect URI {redirect_uri!r} has an invalid port"
    if parts.scheme == "http" and is_loopback_host(parts.hostname):
        return None  # any port is honoured (RFC 8252 §7.3)
    if parts.scheme == "https" and parts.hostname:
        if parts.hostname.lower() == document_host:
            return None
        return False, (
            f"redirect URI {redirect_uri!r} is not on the document's host ({document_host}); "
            "Kinde drops it for customer-hosted agents"
        )
    return False, (
        f"redirect URI {redirect_uri!r} uses an unsupported scheme; Kinde honours only https on the "
        "document's host and http loopback, and rejects custom schemes"
    )


def build_client_metadata_document(
    client_id: str,
    client_name: str,
    redirect_uris: Iterable[str],
    *,
    client_uri: Optional[str] = None,
    logo_uri: Optional[str] = None,
    strict: bool = True,
    **extra: Any,
) -> Dict[str, Any]:
    """Build and validate a client ID metadata document.

    Args:
        client_id: The https URL the document will be served at, byte for byte.
        client_name: Shown to the user on the consent screen. Required.
        redirect_uris: Callbacks. Kinde honours https on the same host as
            ``client_id`` and ``http://127.0.0.1`` / ``localhost`` / ``[::1]`` on any port.
        strict: When true (default), redirect URIs Kinde would drop raise an
            error. When false they only warn, for documents also used with other
            authorization servers.
        extra: Other RFC 7591 metadata, for example ``tos_uri`` or ``contacts``.
    """
    validate_client_metadata_url(client_id)
    if not client_name or not str(client_name).strip():
        raise AgentConfigError("client_name is required")
    uris = list(redirect_uris)
    if not uris:
        raise AgentConfigError("At least one redirect URI is required")
    document_host = urlsplit(client_id).hostname.lower()
    for uri in uris:
        problem = _redirect_uri_problem(uri, document_host)
        if problem is None:
            continue
        fatal, reason = problem
        if fatal or strict:
            raise AgentConfigError(reason)
        warnings.warn(reason, stacklevel=2)

    document: Dict[str, Any] = {
        "client_id": client_id,
        "client_name": client_name,
        "redirect_uris": uris,
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
    }
    if client_uri:
        document["client_uri"] = client_uri
    if logo_uri:
        document["logo_uri"] = logo_uri
    document.update(extra)
    if len(json.dumps(document).encode()) > MAX_DOCUMENT_BYTES:
        raise AgentConfigError("The client metadata document must be under 64 KiB")
    return document


def client_metadata_response(document: Dict[str, Any]) -> Tuple[bytes, Dict[str, str]]:
    """The body and headers to serve a document with: JSON, cacheable for an hour, never a redirect."""
    body = json.dumps(document, separators=(",", ":")).encode()
    if len(body) > MAX_DOCUMENT_BYTES:
        raise AgentConfigError("The client metadata document must be under 64 KiB")
    return body, {
        "Content-Type": "application/json",
        # Kinde clamps this to between 5 minutes and 24 hours
        "Cache-Control": "public, max-age=3600",
    }
