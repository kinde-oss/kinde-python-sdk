"""
Exceptions raised by the agents core.

The resource-server errors carry the HTTP status and RFC 6750 error code that a
framework integration should answer with, so the integrations never decide
those themselves.
"""

from typing import Optional


class AgentAuthError(Exception):
    """Base class for every error raised by ``kinde_sdk.agents``."""


class AgentConfigError(AgentAuthError, ValueError):
    """The agents configuration is missing a value or has an invalid one."""


class AuthenticationRequired(AgentAuthError):
    """The request carried no ``Authorization`` header (answer 401, no ``error``)."""

    status_code = 401
    error: Optional[str] = None

    def __init__(self, description: str = "Authentication required"):
        super().__init__(description)
        self.description = description


class InvalidTokenError(AgentAuthError):
    """The bearer token is malformed, inactive, expired or for another resource (answer 401)."""

    status_code = 401
    error = "invalid_token"

    def __init__(self, description: str = "The access token is invalid"):
        super().__init__(description)
        self.description = description


class InsufficientScopeError(AgentAuthError):
    """The token lacks an OAuth scope (answer 403 ``insufficient_scope``).

    Only for OAuth scopes (``offline``, ``profile``, ``email``). A missing Kinde
    permission is :class:`PermissionDeniedError`, never this.
    """

    status_code = 403
    error = "insufficient_scope"

    def __init__(self, scopes, description: Optional[str] = None):
        """Record the missing scopes, for the ``scope`` parameter of the challenge."""
        self.scopes = list(scopes)
        self.description = description or "Required scope: " + " ".join(self.scopes)
        super().__init__(self.description)


class PermissionDeniedError(AgentAuthError):
    """The token lacks a Kinde permission (answer a plain 403, no challenge)."""

    status_code = 403
    error = "forbidden"

    def __init__(self, permissions, description: Optional[str] = None):
        """Record the missing permissions."""
        self.permissions = list(permissions)
        self.description = description or "Missing permission: " + ", ".join(self.permissions)
        super().__init__(self.description)


class VerificationUnavailableError(AgentAuthError):
    """Kinde could not be reached, or refused the application's credentials (answer 503).

    Never answered with 401: that would make the agent restart its login.
    """

    status_code = 503
    error = "temporarily_unavailable"

    def __init__(self, description: str = "Token verification is temporarily unavailable"):
        super().__init__(description)
        self.description = description


class AgentClientError(AgentAuthError):
    """An agent-client step failed (discovery, registration, authorization or token exchange)."""

    def __init__(self, message: str, *, error: Optional[str] = None, error_description: Optional[str] = None):
        super().__init__(message)
        self.error = error
        self.error_description = error_description


class DiscoveryError(AgentClientError):
    """Protected resource or authorization server metadata was missing or invalid."""


class RegistrationError(AgentClientError):
    """Dynamic client registration failed."""


class AuthorizationError(AgentClientError):
    """The authorization step failed (for example a ``state`` mismatch or an ``error`` on the callback)."""


class TokenRequestError(AgentClientError):
    """The token endpoint refused a code exchange or a refresh."""
