"""
Flask integration for Kinde "AI agents and MCP" applications.

Thin wiring over ``kinde_sdk.agents``: it registers the metadata routes and
turns the core's errors into responses. No protocol logic lives here.

    from kinde_flask.agents import FlaskAgentAuth, current_agent_auth

    agents = FlaskAgentAuth(app=app)     # reads KINDE_HOST and KINDE_AGENTS_*

    @app.get("/api/docs")
    @agents.require_permission("read:docs")
    def docs():
        return {"user": current_agent_auth().user_id}
"""

from functools import wraps
from typing import Any, Callable, Dict, Optional
from urllib.parse import unquote, urlsplit

from flask import Blueprint, Flask, Response, current_app, g, jsonify, request

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


def current_agent_auth() -> Optional[AgentAuthContext]:
    """The :class:`AgentAuthContext` for the current request, set by ``require``."""
    return g.get("kinde_agent_auth")


class FlaskAgentAuth:
    """Flask decorators and metadata routes for a :class:`KindeAgentAuth`.

    Args:
        auth: The core helper. Built from the environment when omitted.
        app: Register the routes now, or later with :meth:`init_app`.
        mirror_authorization_server_metadata: Also serve
            ``/.well-known/oauth-authorization-server`` for older MCP clients
            that look on the resource server's origin.
    """

    def __init__(
        self,
        auth: Optional[KindeAgentAuth] = None,
        app: Optional[Flask] = None,
        *,
        mirror_authorization_server_metadata: bool = True,
    ):
        """Build the core helper from the environment unless one is passed, and register on ``app`` if given."""
        self.auth = auth if auth is not None else KindeAgentAuth()
        self.blueprint = self._metadata_blueprint(mirror_authorization_server_metadata)
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.register_blueprint(self.blueprint)

    def _metadata_blueprint(self, mirror: bool) -> Blueprint:
        """Build the blueprint serving the metadata routes, with the authorization server mirror if asked."""
        blueprint = Blueprint("kinde_agent_auth", __name__)

        def protected_resource_metadata():
            """Serve the RFC 9728 document, answering CORS preflight requests."""
            if request.method == "OPTIONS":
                return Response(status=204, headers=_CORS_HEADERS)
            response = jsonify(self.auth.protected_resource_metadata())
            response.headers.update({**_CORS_HEADERS, "Cache-Control": "max-age=3600"})
            return response

        paths = [self.auth.config.protected_resource_metadata_path]
        if PROTECTED_RESOURCE_WELL_KNOWN not in paths:
            paths.append(PROTECTED_RESOURCE_WELL_KNOWN)
        for index, path in enumerate(paths):
            blueprint.add_url_rule(
                path,
                endpoint=f"protected_resource_metadata_{index}",
                view_func=protected_resource_metadata,
                methods=["GET", "OPTIONS"],
                provide_automatic_options=False,
            )

        if mirror:

            def authorization_server_metadata():
                """Serve Kinde's scoped authorization server metadata from this origin."""
                if request.method == "OPTIONS":
                    return Response(status=204, headers=_CORS_HEADERS)
                response = jsonify(self.auth.fetch_authorization_server_metadata())
                response.headers.update({**_CORS_HEADERS, "Cache-Control": "max-age=300"})
                return response

            blueprint.add_url_rule(
                AUTHORIZATION_SERVER_WELL_KNOWN,
                endpoint="authorization_server_metadata",
                view_func=authorization_server_metadata,
                methods=["GET", "OPTIONS"],
                provide_automatic_options=False,
            )
        return blueprint

    def error_response(self, error: AgentAuthError) -> Response:
        result = self.auth.error_response(error)
        response = jsonify(result.body)
        response.status_code = result.status_code
        response.headers.update(result.headers)
        return response

    def _authenticate(self, scopes) -> AgentAuthContext:
        """Verify the request's bearer token and scopes, and store the context on ``g``."""
        context = self.auth.authenticate(request.headers.get("Authorization"))
        if scopes:
            require_scope(context, *scopes)
        g.kinde_agent_auth = context
        return context

    def require(self, *scopes: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorate a view so it only runs with a valid bearer token.

        ``scopes`` are OAuth scopes (``offline``, ``profile``, ``email``); a
        missing one answers 403 ``insufficient_scope``. The context is available
        from :func:`current_agent_auth`.
        """

        def decorator(view: Callable[..., Any]) -> Callable[..., Any]:
            """Wrap ``view`` so it runs only with a valid bearer token."""

            @wraps(view)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                """Answer with the auth error, or run the view."""
                try:
                    self._authenticate(scopes)
                except AgentAuthError as exc:
                    return self.error_response(exc)
                return current_app.ensure_sync(view)(*args, **kwargs)

            return wrapper

        return decorator

    def require_permission(self, *permissions: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Like :meth:`require`, plus a plain 403 when a Kinde permission is missing. For REST routes.

        Inside an MCP tool, use ``has_permission`` and return a tool error instead.
        """

        def decorator(view: Callable[..., Any]) -> Callable[..., Any]:
            """Wrap ``view`` so it runs only with a valid token carrying the permissions."""

            @wraps(view)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                """Answer with the auth error, or run the view."""
                try:
                    require_permission(self._authenticate(()), *permissions)
                except AgentAuthError as exc:
                    return self.error_response(exc)
                return current_app.ensure_sync(view)(*args, **kwargs)

            return wrapper

        return decorator


def client_metadata_blueprint(document: Dict[str, Any], path: Optional[str] = None) -> Blueprint:
    """Serve a client ID metadata document (built with ``build_client_metadata_document``).

    ``path`` defaults to the path of the document's ``client_id``, which must be
    the exact URL the document is served at.
    """
    body, headers = client_metadata_response(document)
    blueprint = Blueprint("kinde_client_metadata", __name__)

    def client_metadata():
        return Response(body, headers=headers)

    # Routes match the decoded request path, so decode any %-escapes in the client_id
    route = path or unquote(urlsplit(document["client_id"]).path)
    blueprint.add_url_rule(route, view_func=client_metadata, methods=["GET"])
    return blueprint
