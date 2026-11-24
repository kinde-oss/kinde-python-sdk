"""
Client-side MCP adapter: an ``OAuthClientProvider`` with Kinde's defaults.

The MCP SDK already does discovery, PKCE, CIMD-or-registration and refresh.
This adapter sets the client metadata Kinde expects, keeps ``openid`` out of
the scope and ``offline`` in it, and stores tokens in the core's storage.

    provider = KindeOAuthClientProvider(
        "https://api.example.com/mcp",
        client_metadata_url="https://agent.example.com/oauth/client-metadata.json",
        client_name="Example Agent",
        redirect_uri="http://127.0.0.1:8765/callback",
        redirect_handler=open_in_browser,
        callback_handler=wait_for_callback,
    )
    async with streamable_http_client(url, auth=provider) as streams: ...
"""

from typing import Any, Optional, Sequence

from mcp.client.auth import OAuthClientProvider
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken

from kinde_sdk.agents.client_metadata import validate_client_metadata_url
from kinde_sdk.agents.storage import AgentClientStorage, InMemoryAgentStorage


class KindeTokenStorage:
    """The MCP SDK's ``TokenStorage`` on top of the core's :class:`AgentClientStorage`.

    Lets an MCP client keep its tokens and registration in, for example,
    :class:`FileAgentStorage`.
    """

    def __init__(self, storage: Optional[AgentClientStorage] = None, key: str = "default"):
        """Store under ``mcp|<key>`` in ``storage`` (in memory by default)."""
        self.storage = storage or InMemoryAgentStorage()
        self.key = f"mcp|{key}"

    async def get_tokens(self) -> Optional[OAuthToken]:
        """Return the stored tokens, or ``None``."""
        data = await self.storage.get_tokens(self.key)
        return OAuthToken.model_validate(data) if data else None

    async def set_tokens(self, tokens: OAuthToken) -> None:
        await self.storage.set_tokens(self.key, tokens.model_dump(mode="json", exclude_none=True))

    async def get_client_info(self) -> Optional[OAuthClientInformationFull]:
        """Return the stored client registration, or ``None``."""
        data = await self.storage.get_registration(self.key)
        return OAuthClientInformationFull.model_validate(data) if data else None

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        await self.storage.set_registration(self.key, client_info.model_dump(mode="json", exclude_none=True))


class KindeOAuthClientProvider(OAuthClientProvider):
    """``OAuthClientProvider`` for agents signing in through Kinde (or any MCP authorization server).

    Prefers the client ID metadata document when ``client_metadata_url`` is set
    and the server supports it, and registers dynamically otherwise.
    """

    def __init__(
        self,
        server_url: str,
        *,
        client_name: str = "Kinde agent",
        redirect_uri: str = "http://127.0.0.1:8765/callback",
        client_metadata_url: Optional[str] = None,
        scopes: Sequence[str] = ("offline",),
        storage: Optional[Any] = None,
        client_metadata: Optional[OAuthClientMetadata] = None,
        **options: Any,
    ):
        """Build the client metadata from the Kinde defaults unless ``client_metadata`` is given."""
        if client_metadata_url is not None:
            validate_client_metadata_url(client_metadata_url)
        self._default_scopes = [scope for scope in scopes if scope != "openid"] or ["offline"]
        metadata = client_metadata or OAuthClientMetadata(
            client_name=client_name,
            redirect_uris=[redirect_uri],
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
            # Kinde returns client_secret_post and a secret on registration anyway; the SDK uses what comes back
            token_endpoint_auth_method="none",
            scope=" ".join(self._default_scopes),
        )
        super().__init__(
            server_url=server_url,
            client_metadata=metadata,
            storage=storage if storage is not None else KindeTokenStorage(key=server_url),
            client_metadata_url=client_metadata_url,
            **options,
        )

    def _kinde_scope(self, selected: Optional[str]) -> str:
        """The scope to request: never ``openid`` where unsupported, and ``offline`` where supported."""
        metadata = self.context.oauth_metadata
        supported = list(metadata.scopes_supported) if metadata and metadata.scopes_supported is not None else None
        scopes = (selected or "").split() or list(self._default_scopes)
        if supported is not None:
            # Kinde's agent issuer refuses openid with invalid_scope
            if "openid" not in supported:
                scopes = [scope for scope in scopes if scope != "openid"]
            if "offline" in supported and "offline" not in scopes:
                scopes.insert(0, "offline")
        return " ".join(dict.fromkeys(scopes))

    async def _perform_authorization(self):
        # The MCP SDK picks the scope from the challenge or metadata just before this step.
        # This relies on a private hook, so the mcp extra is pinned below 3.0.
        self.context.client_metadata.scope = self._kinde_scope(self.context.client_metadata.scope)
        return await super()._perform_authorization()
