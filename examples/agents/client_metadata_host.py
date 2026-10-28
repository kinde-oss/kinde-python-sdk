"""
Serves an agent's client ID metadata document (CIMD).

Kinde fetches this from the public internet, so run it on (or tunnel it to) the
public host in CLIENT_METADATA_URL, and add that host to the Kinde application's
Trusted agent hosts.

    export CLIENT_METADATA_URL=https://agent.onzs.co.za/oauth/client-metadata.json
    uvicorn examples.agents.client_metadata_host:app --port 8080
"""

import os

from fastapi import FastAPI

from kinde_fastapi.agents import client_metadata_router
from kinde_sdk.agents import build_client_metadata_document

document = build_client_metadata_document(
    os.environ["CLIENT_METADATA_URL"],
    "Kinde example agent",
    # Loopback works on any port for CIMD; cli_agent.py uses 8765
    ["http://127.0.0.1/callback"],
)

app = FastAPI()
app.include_router(client_metadata_router(document))
