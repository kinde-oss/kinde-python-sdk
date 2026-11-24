"""
Kinde "AI agents and MCP" support: CIMD and Dynamic Client Registration.

Two halves, both opt-in and separate from the SDK's normal login flow:

- Resource server (:class:`KindeAgentAuth`): protect your MCP server or API.
  Serves protected resource metadata, answers 401 with the right challenge,
  verifies tokens (introspection by default) and checks permissions.
- Agent client (:class:`KindeAgentClient`): sign a user in to a protected
  server, preferring a client ID metadata document over registration.

The adapters for the official ``mcp`` package are in ``kinde_sdk.agents.mcp``
(install ``kinde-python-sdk[mcp]``). This package never imports ``mcp``.
"""

from kinde_sdk.agents.client import AuthorizationRequiredError, KindeAgentClient, PendingAuthorization
from kinde_sdk.agents.client_metadata import (
    build_client_metadata_document,
    client_metadata_response,
    validate_client_metadata_url,
)
from kinde_sdk.agents.config import AgentAuthConfig
from kinde_sdk.agents.context import (
    AgentAuthContext,
    has_permission,
    has_role,
    has_scope,
    require_permission,
    require_scope,
)
from kinde_sdk.agents.errors import (
    AgentAuthError,
    AgentClientError,
    AgentConfigError,
    AuthenticationRequired,
    AuthorizationError,
    DiscoveryError,
    InsufficientScopeError,
    InvalidTokenError,
    PermissionDeniedError,
    RegistrationError,
    TokenRequestError,
    VerificationUnavailableError,
)
from kinde_sdk.agents.resource_server import AgentAuthResponse, KindeAgentAuth
from kinde_sdk.agents.storage import AgentClientStorage, FileAgentStorage, InMemoryAgentStorage
from kinde_sdk.agents.www_authenticate import build_challenge, find_bearer_challenge, parse_www_authenticate


def create_kinde_agent_auth(config=None, **options) -> KindeAgentAuth:
    """Alias for :class:`KindeAgentAuth`, matching ``createKindeAgentAuth`` in the other SDKs."""
    return KindeAgentAuth(config, **options)


__all__ = [
    "AgentAuthConfig",
    "AgentAuthContext",
    "AgentAuthError",
    "AgentAuthResponse",
    "AgentClientError",
    "AgentClientStorage",
    "AgentConfigError",
    "AuthenticationRequired",
    "AuthorizationError",
    "AuthorizationRequiredError",
    "DiscoveryError",
    "FileAgentStorage",
    "InMemoryAgentStorage",
    "InsufficientScopeError",
    "InvalidTokenError",
    "KindeAgentAuth",
    "KindeAgentClient",
    "PendingAuthorization",
    "PermissionDeniedError",
    "RegistrationError",
    "TokenRequestError",
    "VerificationUnavailableError",
    "build_challenge",
    "build_client_metadata_document",
    "client_metadata_response",
    "create_kinde_agent_auth",
    "find_bearer_challenge",
    "has_permission",
    "has_role",
    "has_scope",
    "parse_www_authenticate",
    "require_permission",
    "require_scope",
    "validate_client_metadata_url",
]
