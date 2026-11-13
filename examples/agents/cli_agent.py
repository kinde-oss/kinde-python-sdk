"""
A CLI agent that signs a user in to a protected MCP server and calls it.

    export RESOURCE_URL=https://<your public host>/mcp
    # CIMD (preferred): the URL where client_metadata_host.py serves the document,
    # whose host is in the Kinde application's Trusted agent hosts. Leave unset to use DCR.
    export CLIENT_METADATA_URL=https://agent.onzs.co.za/oauth/client-metadata.json
    python examples/agents/cli_agent.py

The browser opens for sign-in. Tokens are kept in ~/.kinde-example-agent/tokens.json.
"""

import asyncio
import os

from kinde_sdk.agents import FileAgentStorage, KindeAgentClient


async def main() -> None:
    async with KindeAgentClient(
        os.environ["RESOURCE_URL"],
        client_metadata_url=os.getenv("CLIENT_METADATA_URL"),
        client_name="Kinde example agent",
        # A fixed port, so a DCR registration (tied to its exact redirect URI) is reused between runs
        redirect_uri="http://127.0.0.1:8765/callback",
        storage=FileAgentStorage("~/.kinde-example-agent/tokens.json"),
    ) as client:
        await client.connect()
        print("Signed in:", await client.get_token_info())

        response = await client.request(
            "POST",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "kinde-example-agent", "version": "1"},
                },
            },
            headers={"Accept": "application/json, text/event-stream"},
        )
        print(response.status_code, response.text)


if __name__ == "__main__":
    asyncio.run(main())
