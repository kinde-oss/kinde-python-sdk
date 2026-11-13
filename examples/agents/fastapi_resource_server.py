"""
A REST API protected by a Kinde "AI agents and MCP" application, with FastAPI.

    pip install "kinde-python-sdk[fastapi]"
    export KINDE_HOST=https://yourbiz.kinde.com
    export KINDE_AGENTS_CLIENT_ID=... KINDE_AGENTS_CLIENT_SECRET=...
    export KINDE_AGENTS_RESOURCE_URL=http://localhost:3001/api
    uvicorn examples.agents.fastapi_resource_server:app --port 3001

    curl -i http://localhost:3001/api/docs     # 401 with a WWW-Authenticate challenge
    curl http://localhost:3001/.well-known/oauth-protected-resource/api
"""

from fastapi import Depends, FastAPI

from kinde_fastapi.agents import FastAPIAgentAuth
from kinde_sdk.agents import AgentAuthContext

app = FastAPI()
agents = FastAPIAgentAuth()
agents.install(app)


@app.get("/api/me")
async def me(auth: AgentAuthContext = Depends(agents.require())):
    return {"user": auth.user_id, "agent": auth.client_id, "permissions": auth.permissions}


@app.get("/api/docs")
async def docs(auth: AgentAuthContext = Depends(agents.require_permission("read:docs"))):
    return {"docs": "...", "user": auth.user_id}
