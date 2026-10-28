"""
FastAPI integration for Kinde "AI agents and MCP" applications.

Thin wiring over ``kinde_sdk.agents``: it mounts the metadata routes and turns
the core's errors into responses. No protocol logic lives here.

    from kinde_fastapi.agents import FastAPIAgentAuth
    from kinde_sdk.agents import AgentAuthContext

    agents = FastAPIAgentAuth()          # reads KINDE_HOST and KINDE_AGENTS_*
    agents.install(app)

    @app.get("/api/docs")
    async def docs(auth: AgentAuthContext = Depends(agents.require_permission("read:docs"))):
        ...
"""

from typing import Any, Callable, Dict, Optional
from urllib.parse import urlsplit

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, Response

from kinde_sdk.agents.client_metadata import client_metadata_response
from kinde_sdk.agents.config import AUTHORIZATION_SERVER_WELL_KNOWN, PROTECTED_RESOURCE_WELL_KNOWN
from kinde_sdk.agents.context import AgentAuthContext, require_permission, require_scope
from kinde_sdk.agents.errors import AgentAuthError
from kinde_sdk.agents.resource_server import KindeAgentAuth

# Browser-based MCP clients fetch metadata cross-origin
_CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
}


class AgentAuthHTTPException(HTTPException):
    """Carries the core's error response. :meth:`FastAPIAgentAuth.install` renders its body as is."""

    def __init__(self, status_code: int, body: Dict[str, str], headers: Dict[str, str]):
        super().__init__(status_code=status_code, detail=body, headers=headers)
        self.body = body


async def agent_auth_exception_handler(request: Request, exc: AgentAuthHTTPException) -> Response:
    return JSONResponse(exc.body, status_code=exc.status_code, headers=exc.headers)


class FastAPIAgentAuth:
    """FastAPI dependencies and metadata routes for a :class:`KindeAgentAuth`.

    Args:
        auth: The core helper. Built from the environment when omitted.
        mirror_authorization_server_metadata: Also serve
            ``/.well-known/oauth-authorization-server`` for older MCP clients
            that look on the resource server's origin.
    """

    def __init__(
        self,
        auth: Optional[KindeAgentAuth] = None,
        *,
        mirror_authorization_server_metadata: bool = True,
    ):
        self.auth = auth if auth is not None else KindeAgentAuth()
        self.router = APIRouter()
        self._add_metadata_routes(mirror_authorization_server_metadata)

    def install(self, app: FastAPI) -> None:
        """Mount the metadata routes and render auth errors as ``{"error", "error_description"}``."""
        app.include_router(self.router)
        app.add_exception_handler(AgentAuthHTTPException, agent_auth_exception_handler)

    def _add_metadata_routes(self, mirror: bool) -> None:
        async def protected_resource_metadata(request: Request) -> Response:
            if request.method == "OPTIONS":
                return Response(status_code=204, headers=_CORS_HEADERS)
            return JSONResponse(
                self.auth.protected_resource_metadata(),
                headers={**_CORS_HEADERS, "Cache-Control": "max-age=3600"},
            )

        paths = [self.auth.config.protected_resource_metadata_path]
        if PROTECTED_RESOURCE_WELL_KNOWN not in paths:
            paths.append(PROTECTED_RESOURCE_WELL_KNOWN)
        for path in paths:
            self.router.add_api_route(
                path, protected_resource_metadata, methods=["GET", "OPTIONS"], include_in_schema=False
            )

        if mirror:

            async def authorization_server_metadata(request: Request) -> Response:
                if request.method == "OPTIONS":
                    return Response(status_code=204, headers=_CORS_HEADERS)
                document = await self.auth.fetch_authorization_server_metadata_async()
                return JSONResponse(document, headers={**_CORS_HEADERS, "Cache-Control": "max-age=300"})

            self.router.add_api_route(
                AUTHORIZATION_SERVER_WELL_KNOWN,
                authorization_server_metadata,
                methods=["GET", "OPTIONS"],
                include_in_schema=False,
            )

    def _http_error(self, error: AgentAuthError) -> AgentAuthHTTPException:
        response = self.auth.error_response(error)
        return AgentAuthHTTPException(response.status_code, response.body, response.headers)

    def require(self, *scopes: str) -> Callable[..., Any]:
        """A dependency that verifies the bearer token and returns the :class:`AgentAuthContext`.

        ``scopes`` are OAuth scopes (``offline``, ``profile``, ``email``); a
        missing one answers 403 ``insufficient_scope``. Check Kinde permissions
        with :meth:`require_permission` or ``has_permission`` instead.
        """

        async def dependency(request: Request) -> AgentAuthContext:
            try:
                context = await self.auth.authenticate_async(request.headers.get("authorization"))
                if scopes:
                    require_scope(context, *scopes)
            except AgentAuthError as exc:
                raise self._http_error(exc) from exc
            request.state.kinde_agent_auth = context
            return context

        return dependency

    def require_permission(self, *permissions: str) -> Callable[..., Any]:
        """A dependency for REST routes: like :meth:`require`, plus a plain 403 when a Kinde permission is missing.

        Inside an MCP tool, use ``has_permission`` and return a tool error instead.
        """
        authenticate = self.require()

        async def dependency(request: Request) -> AgentAuthContext:
            context = await authenticate(request)
            try:
                require_permission(context, *permissions)
            except AgentAuthError as exc:
                raise self._http_error(exc) from exc
            return context

        return dependency


def client_metadata_router(document: Dict[str, Any], path: Optional[str] = None) -> APIRouter:
    """Serve a client ID metadata document (built with ``build_client_metadata_document``).

    ``path`` defaults to the path of the document's ``client_id``, which must be
    the exact URL the document is served at.
    """
    body, headers = client_metadata_response(document)
    router = APIRouter()

    async def client_metadata() -> Response:
        return Response(content=body, headers=headers, media_type="application/json")

    router.add_api_route(
        path or urlsplit(document["client_id"]).path, client_metadata, methods=["GET"], include_in_schema=False
    )
    return router
