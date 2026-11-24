"""
Adapters that plug the Kinde agents core into the official ``mcp`` package.

Install with ``pip install "kinde-python-sdk[mcp]"`` (Python 3.10 or newer).

- :class:`KindeTokenVerifier`: the ``token_verifier`` for an ``MCPServer``.
- :func:`kinde_auth_settings`: the matching ``AuthSettings``.
- :class:`KindeOAuthClientProvider`: the auth hook for an MCP client.
"""

try:
    import mcp  # noqa: F401
except ImportError as exc:  # pragma: no cover - exercised only without the extra
    raise ImportError(
        'kinde_sdk.agents.mcp needs the mcp package. Install it with: pip install "kinde-python-sdk[mcp]"'
    ) from exc

from kinde_sdk.agents.mcp.client import KindeOAuthClientProvider, KindeTokenStorage
from kinde_sdk.agents.mcp.server import (
    KindeTokenVerifier,
    get_agent_auth_context,
    kinde_auth_settings,
    mount_authorization_server_metadata,
)

__all__ = [
    "KindeOAuthClientProvider",
    "KindeTokenStorage",
    "KindeTokenVerifier",
    "get_agent_auth_context",
    "kinde_auth_settings",
    "mount_authorization_server_metadata",
]
