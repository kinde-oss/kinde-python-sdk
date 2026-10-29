"""
The verified identity handed to route and tool handlers, and permission checks on it.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

from kinde_sdk.agents.errors import InsufficientScopeError, PermissionDeniedError


def _scopes_from(claims: Mapping[str, Any]) -> List[str]:
    """Read scopes from ``scp`` (a list) or ``scope`` (a space-separated string)."""
    scp = claims.get("scp")
    if isinstance(scp, list):
        return [str(scope) for scope in scp]
    scope = claims.get("scope") or scp
    if isinstance(scope, str):
        return scope.split()
    return []


def _role_keys(claims: Mapping[str, Any]) -> List[str]:
    """Return the ``key`` of each role in the ``roles`` claim."""
    roles = claims.get("roles")
    if not isinstance(roles, list):
        return []
    keys = []
    for role in roles:
        if isinstance(role, Mapping):
            key = role.get("key")
            if key:
                keys.append(str(key))
        elif isinstance(role, str):
            keys.append(role)
    return keys


@dataclass
class AgentAuthContext:
    """Who is calling: the Kinde user, the agent acting for them, and what they may do.

    ``client_id`` identifies the agent: a CIMD metadata document URL, or a DCR
    registrant ID. Identity comes from the verified access token, never from the
    user profile endpoint, which can't resolve agent tokens.
    """

    token: str = field(repr=False)
    user_id: Optional[str]
    client_id: Optional[str]
    expires_at: Optional[int]
    scopes: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    roles: List[str] = field(default_factory=list)
    email: Optional[str] = None
    org_code: Optional[str] = None
    audience: List[str] = field(default_factory=list)
    claims: Dict[str, Any] = field(default_factory=dict, repr=False)

    @classmethod
    def from_claims(
        cls,
        token: str,
        claims: Mapping[str, Any],
        introspection: Optional[Mapping[str, Any]] = None,
    ) -> "AgentAuthContext":
        """Build a context from token claims, preferring introspection values where Kinde returned them."""
        merged: Dict[str, Any] = dict(claims)
        if introspection:
            for key in ("sub", "client_id", "scope", "exp", "aud"):
                if introspection.get(key) is not None:
                    merged[key] = introspection[key]
        if introspection and introspection.get("scope") is not None:
            scopes = str(introspection["scope"]).split()
        else:
            scopes = _scopes_from(claims)
        audience = merged.get("aud")
        if isinstance(audience, str):
            audience = [audience]
        permissions = merged.get("permissions")
        exp = merged.get("exp")
        return cls(
            token=token,
            user_id=merged.get("sub"),
            # azp names the agent on Kinde tokens; client_id is the RFC 7662/9068 name for it
            client_id=claims.get("azp") or merged.get("client_id"),
            expires_at=int(exp) if isinstance(exp, (int, float)) else None,
            scopes=scopes,
            permissions=[str(p) for p in permissions] if isinstance(permissions, list) else [],
            roles=_role_keys(merged),
            email=merged.get("email"),
            org_code=merged.get("org_code"),
            audience=[str(a) for a in audience] if isinstance(audience, list) else [],
            claims=merged,
        )


def has_permission(context: Optional[AgentAuthContext], permission: str) -> bool:
    """Return whether the caller holds a Kinde permission.

    Use it inside each MCP tool, and answer a failure with a tool error
    (``isError``), not an HTTP 403: signing in again can't grant a permission.
    """
    return context is not None and permission in context.permissions


def has_role(context: Optional[AgentAuthContext], role: str) -> bool:
    """Whether the context has the Kinde role key. ``False`` when there's no context."""
    return context is not None and role in context.roles


def has_scope(context: Optional[AgentAuthContext], scope: str) -> bool:
    """Whether the context has the OAuth scope. ``False`` when there's no context."""
    return context is not None and scope in context.scopes


def require_permission(context: Optional[AgentAuthContext], *permissions: str) -> None:
    """Raise :class:`PermissionDeniedError` (a plain 403) unless every permission is held."""
    missing = [p for p in permissions if not has_permission(context, p)]
    if missing:
        raise PermissionDeniedError(missing)


def require_scope(context: Optional[AgentAuthContext], *scopes: str) -> None:
    """Raise :class:`InsufficientScopeError` (403 ``insufficient_scope``) unless every OAuth scope is held."""
    missing = [s for s in scopes if not has_scope(context, s)]
    if missing:
        raise InsufficientScopeError(missing)
