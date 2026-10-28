"""
Server-side MCP adapter: a ``TokenVerifier`` backed by :class:`KindeAgentAuth`.

    auth = KindeAgentAuth()   # reads KINDE_HOST and KINDE_AGENTS_*
    server = MCPServer(
        "My server",
        token_verifier=KindeTokenVerifier(auth),
        auth=kinde_auth_settings(auth),
    )

    @server.tool()
    async def read_docs() -> str:
        if not has_permission(get_agent_auth_context(), "read:docs"):
            raise ToolError("You don't have permission to read docs.")
"""

from typing import Any, List, Optional, Sequence

from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from kinde_sdk.agents.context import AgentAuthContext
from kinde_sdk.agents.errors import InvalidTokenError
from kinde_sdk.agents.resource_server import KindeAgentAuth

_CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}


class KindeTokenVerifier(TokenVerifier):
    """Verifies bearer tokens for an ``MCPServer`` using Kinde (introspection by default).

    - A bad token returns ``None``, which the MCP SDK answers with 401, so the
      agent refreshes or signs in again.
    - A Kinde outage raises :class:`VerificationUnavailableError` instead, so the
      agent doesn't restart its login over a problem it can't fix.
    - ``resource`` is always set: with ``validate_token_resource`` the MCP SDK
      rejects every token whose ``resource`` is missing or different.
    """

    def __init__(self, auth: Optional[KindeAgentAuth] = None, **options: Any):
        self.auth = auth if auth is not None else KindeAgentAuth(**options)

    async def verify_token(self, token: str) -> Optional[AccessToken]:
        try:
            context = await self.auth.verify_token_async(token)
        except InvalidTokenError:
            return None
        return AccessToken(
            token=token,
            client_id=context.client_id or "",
            scopes=context.scopes,
            expires_at=context.expires_at,
            # The verifier confirmed aud contains the Resource URL; report that entry
            resource=self.auth.config.resource_url,
            subject=context.user_id,
            claims=context.claims,
        )


def kinde_auth_settings(
    auth: KindeAgentAuth,
    *,
    required_scopes: Optional[Sequence[str]] = None,
    **settings: Any,
) -> AuthSettings:
    """``AuthSettings`` for an ``MCPServer`` protected by Kinde.

    ``required_scopes`` defaults to ``["offline"]``. The MCP SDK publishes this
    list as ``scopes_supported`` in the protected resource metadata, and agents
    request what it lists: without ``offline`` they never get a refresh token
    and users sign in again every 24 hours. Note that the SDK also requires
    every listed scope on each token.
    """
    scopes: List[str] = list(required_scopes) if required_scopes is not None else ["offline"]
    options = {
        "issuer_url": AnyHttpUrl(auth.config.issuer),
        "resource_server_url": AnyHttpUrl(auth.config.resource_url),
        "required_scopes": scopes,
        "validate_token_resource": True,
    }
    options.update(settings)
    return AuthSettings(**options)


def get_agent_auth_context() -> Optional[AgentAuthContext]:
    """The Kinde auth context for the current MCP request, for ``has_permission`` in tool handlers."""
    access_token = get_access_token()
    if access_token is None:
        return None
    claims = dict(access_token.claims or {})
    context = AgentAuthContext.from_claims(access_token.token, claims)
    # Scopes and expiry as the verifier reported them
    context.scopes = list(access_token.scopes)
    context.expires_at = access_token.expires_at
    return context


def mount_authorization_server_metadata(server: Any, auth: KindeAgentAuth) -> None:
    """Serve ``/.well-known/oauth-authorization-server`` on the MCP server's own origin.

    Optional. Current MCP clients follow ``authorization_servers`` to Kinde, but
    some older ones look here. The document mirrors Kinde's and always includes
    ``client_id_metadata_document_supported: true``.
    """

    @server.custom_route("/.well-known/oauth-authorization-server", methods=["GET", "OPTIONS"])
    async def authorization_server_metadata(request: Request) -> Response:
        if request.method == "OPTIONS":
            return Response(status_code=204, headers=_CORS_HEADERS)
        document = await auth.fetch_authorization_server_metadata_async()
        return JSONResponse(document, headers={**_CORS_HEADERS, "Cache-Control": "max-age=300"})
