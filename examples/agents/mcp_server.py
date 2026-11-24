"""
An MCP server protected by a Kinde "AI agents and MCP" application.

    pip install "kinde-python-sdk[mcp]" uvicorn
    export KINDE_HOST=https://yourbiz.kinde.com
    export KINDE_AGENTS_CLIENT_ID=...          # the AI agents and MCP application
    export KINDE_AGENTS_CLIENT_SECRET=...
    export KINDE_AGENTS_RESOURCE_URL=https://<your public host>/mcp
    python examples/agents/mcp_server.py

Connect with MCP Inspector (npx @modelcontextprotocol/inspector) or Claude Code
(claude mcp add --transport http kinde-test https://<your public host>/mcp).
"""

from urllib.parse import urlsplit

import uvicorn
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.server.transport_security import TransportSecuritySettings

from kinde_sdk.agents import KindeAgentAuth, has_permission
from kinde_sdk.agents.mcp import (
    KindeTokenVerifier,
    get_agent_auth_context,
    kinde_auth_settings,
    mount_authorization_server_metadata,
)

auth = KindeAgentAuth()

server = MCPServer(
    "Kinde example server",
    token_verifier=KindeTokenVerifier(auth),
    auth=kinde_auth_settings(auth),
)
# Optional: some older MCP clients look for this on the server's own origin
mount_authorization_server_metadata(server, auth)


@server.tool()
async def whoami() -> str:
    """Who is signed in, and through which agent."""
    context = get_agent_auth_context()
    return f"User {context.user_id} via {context.client_id} with permissions {context.permissions}"


@server.tool()
async def read_docs() -> str:
    """Needs the read:docs permission in Kinde."""
    if not has_permission(get_agent_auth_context(), "read:docs"):
        # A tool error, not an HTTP 403: signing in again can't grant a permission
        raise ToolError("You don't have permission to read docs.")
    return "The docs."


if __name__ == "__main__":
    # Accept the public host from the Resource URL (for example a tunnel) as well as local requests
    public_host = urlsplit(auth.config.resource_url).netloc
    security = TransportSecuritySettings(allowed_hosts=[public_host, "localhost:3001", "127.0.0.1:3001"])
    uvicorn.run(server.streamable_http_app(transport_security=security), host="127.0.0.1", port=3001)
