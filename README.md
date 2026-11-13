# Kinde Python SDK

The Kinde SDK for Python.

You can also use the [Python starter kit here](https://github.com/kinde-starter-kits/python-starter-kit).

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com) [![Kinde Docs](https://img.shields.io/badge/Kinde-Docs-eee?style=flat-square)](https://kinde.com/docs/developer-tools) [![Kinde Community](https://img.shields.io/badge/Kinde-Community-eee?style=flat-square)](https://thekindecommunity.slack.com)

## 🚨 Important: Migrating from v1?

If you're upgrading from Kinde Python SDK v1, **the API has changed significantly**. The `KindeClient` class has been completely replaced with `OAuth`.

**📖 [Migration Guide](MIGRATION.md)** - Complete step-by-step migration instructions  
**📋 [Quick Reference](QUICK_REFERENCE.md)** - At-a-glance v1 to v2 conversion table

### Key Changes:
- `KindeClient` → `OAuth` (main authentication class)
- `client.get_flag()` → `await feature_flags.get_flag()` (feature flags)
- `client.get_permission()` → `await permissions.get_permission()` (permissions)
- Most operations are now asynchronous

## Documentation

For details on integrating this SDK into your project, head over to the [Kinde docs](https://kinde.com/docs/) and see the [Python SDK](https://kinde.com/docs/developer-tools/python-sdk/) doc 👍🏼.

## Basic Usage: Framework Integrations

The Kinde Python SDK provides seamless integration with popular Python web frameworks. Below are detailed guides for using Kinde with FastAPI and Flask.

### FastAPI Integration

The `kinde_fastapi` module provides easy integration with FastAPI applications.

#### Installation

```bash
pip install fastapi uvicorn python-multipart
```

#### Basic Setup

```python
from fastapi import FastAPI
from kinde_sdk.auth.oauth import OAuth

# Initialize FastAPI app
app = FastAPI()

# Initialize Kinde OAuth with FastAPI framework
kinde_oauth = OAuth(
    framework="fastapi",
    app=app
)

# Example home route
@app.get("/")
async def home(request: Request):
    if kinde_oauth.is_authenticated():
        user = kinde_oauth.get_user_info()
        return f"Welcome, {user.get('email', 'User')}!"
    return "Please log in"
```

#### Configuration

Create a `.env` file with your Kinde credentials:

```env
KINDE_CLIENT_ID=your_client_id
KINDE_CLIENT_SECRET=your_client_secret
KINDE_REDIRECT_URI=http://localhost:8000/callback
KINDE_DOMAIN=your_kinde_domain
```

#### Available Routes

The FastAPI integration automatically provides these routes:

- `/login` - Redirects to Kinde login
- `/callback` - Handles OAuth callback
- `/logout` - Logs out the user
- `/register` - Redirects to Kinde registration
- `/user` - Returns user information

#### Protected Routes

```python
from fastapi import HTTPException

@app.get("/protected")
async def protected_route():
    if not kinde_oauth.is_authenticated():
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"message": "This is a protected route"}
```

### Flask Integration

The `kinde_flask` module provides easy integration with Flask applications.

#### Installation

```bash
pip install flask python-dotenv flask-session
```

#### Basic Setup

```python
from flask import Flask
from kinde_sdk.auth.oauth import OAuth

# Initialize Flask app
app = Flask(__name__)

# Configure Flask session
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

# Initialize Kinde OAuth with Flask framework
kinde_oauth = OAuth(
    framework="flask",
    app=app
)

# Example home route
@app.route('/')
def home():
    if kinde_oauth.is_authenticated():
        user = kinde_oauth.get_user_info()
        return f"Welcome, {user.get('email', 'User')}!"
    return "Please log in"
```

#### Configuration

Create a `.env` file with your Kinde credentials:

```env
KINDE_CLIENT_ID=your_client_id
KINDE_CLIENT_SECRET=your_client_secret
KINDE_REDIRECT_URI=http://localhost:5000/callback
KINDE_DOMAIN=your_kinde_domain
```

#### Available Routes

The Flask integration automatically provides these routes:

- `/login` - Redirects to Kinde login
- `/callback` - Handles OAuth callback
- `/logout` - Logs out the user
- `/register` - Redirects to Kinde registration
- `/user` - Returns user information

#### Protected Routes

```python
from functools import wraps
from flask import session, redirect

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not kinde_oauth.is_authenticated():
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/protected')
@login_required
def protected_route():
    return {"message": "This is a protected route"}
```

#### Security Considerations

For both FastAPI and Flask integrations:

1. Always use HTTPS in production
2. Use a secure session secret key
3. Implement proper state parameter validation
4. Handle OAuth errors appropriately
5. Implement proper session management
6. Consider implementing CSRF protection

# AI agents and MCP (CIMD and DCR)

`kinde_sdk.agents` lets you protect your own MCP server (or any API) with Kinde, and build agents that sign users in to such servers. It is separate from the login flow above and changes nothing about it.

Agents identify themselves in one of two ways:

- **Client ID Metadata Document (CIMD), preferred.** The agent publishes a small JSON document on its own domain, and the document's URL is its client ID. There's no registration step. Claude and ChatGPT already work this way.
- **Dynamic Client Registration (DCR), the fallback.** The agent registers with Kinde and gets back a client ID and secret. It's for agents that can't host a document.

## Set up Kinde

1. Create an application of type **AI agents and MCP** and set its **Resource URL** to your server's URL, for example `https://api.example.com/mcp`. The application has no callback URLs, on purpose: agents bring their own.
2. If you run your own agent, add the domain that serves its metadata document to **Trusted agent hosts** (bare domains, up to 10). Vendor agents such as Claude and ChatGPT are already trusted.
3. Set the environment variables. These belong to the AI agents and MCP application, not your login application:

```bash
KINDE_HOST=https://yourbiz.kinde.com
KINDE_AGENTS_CLIENT_ID=<agents application client id>
KINDE_AGENTS_CLIENT_SECRET=<agents application client secret>
KINDE_AGENTS_RESOURCE_URL=https://api.example.com/mcp
```

`KINDE_AGENTS_RESOURCE_URL` must match the Resource URL in Kinde exactly, character for character.

## Protect an MCP server

Install the extra (needs Python 3.10 or newer):

```bash
pip install "kinde-python-sdk[mcp]"
```

```python
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from kinde_sdk.agents import KindeAgentAuth, has_permission
from kinde_sdk.agents.mcp import KindeTokenVerifier, get_agent_auth_context, kinde_auth_settings

auth = KindeAgentAuth()  # reads the environment variables above

server = MCPServer(
    "Docs server",
    token_verifier=KindeTokenVerifier(auth),
    auth=kinde_auth_settings(auth),
)

@server.tool()
async def read_docs() -> str:
    if not has_permission(get_agent_auth_context(), "read:docs"):
        raise ToolError("You don't have permission to read docs.")
    return "..."
```

`kinde_auth_settings` sets the values the MCP SDK needs: the scoped issuer, `required_scopes=["offline"]` (agents request what's listed here, and without `offline` they get no refresh token and users sign in again every 24 hours), and `validate_token_resource=True`.

Check permissions inside each tool with `has_permission`, and fail with a tool error. Don't answer with an HTTP 403: agents treat that as "sign in again", and signing in again can't grant a permission. Use permissions and roles managed in Kinde rather than email allowlists.

## Protect a FastAPI or Flask API

```python
from fastapi import Depends, FastAPI
from kinde_fastapi.agents import FastAPIAgentAuth
from kinde_sdk.agents import AgentAuthContext

app = FastAPI()
agents = FastAPIAgentAuth()   # serves /.well-known/oauth-protected-resource[/path]
agents.install(app)

@app.get("/api/docs")
async def docs(auth: AgentAuthContext = Depends(agents.require_permission("read:docs"))):
    return {"user": auth.user_id, "agent": auth.client_id}
```

```python
from flask import Flask
from kinde_flask.agents import FlaskAgentAuth, current_agent_auth

app = Flask(__name__)
agents = FlaskAgentAuth(app=app)

@app.get("/api/docs")
@agents.require_permission("read:docs")
def docs():
    return {"user": current_agent_auth().user_id}
```

Requests without a valid token get `401` with a `WWW-Authenticate` challenge pointing at the protected resource metadata, which is how agents discover Kinde. If Kinde can't be reached, the response is `503`, so agents don't restart their sign-in.

### How tokens are verified

Tokens are checked with Kinde's introspection endpoint by default, using the application's client ID and secret, so a revoked token stops working immediately. To verify signatures locally instead (no network call per request, but a revoked token stays valid until it expires, 24 hours by default), pass `verification="jwt"`. `"jwt+introspection"` does both. `introspection_cache_seconds` (up to 60) caches successful introspections to cut traffic. With caching on, `revoke_token` clears only the calling process's cache: other workers keep accepting a revoked token until their cached entry expires, at most `introspection_cache_seconds` later.

To cut off an agent, revoke its token with `auth.revoke_token(token)`. This revokes both the access token and refresh token of the pair.

## Build an agent

`KindeAgentClient` signs a user in to a protected server and calls it. It uses the CIMD document when the server supports it and you set `client_metadata_url`, and registers dynamically otherwise.

```python
from kinde_sdk.agents import FileAgentStorage, KindeAgentClient

async with KindeAgentClient(
    "https://api.example.com/mcp",
    client_metadata_url="https://agent.example.com/oauth/client-metadata.json",
    client_name="Example Agent",
    storage=FileAgentStorage("~/.example-agent/tokens.json"),
) as client:
    await client.connect()                 # opens the browser if a sign-in is needed
    response = await client.request("POST", json={...})
```

A CLI agent uses a loopback redirect (`http://127.0.0.1/callback`, port picked automatically). A server-hosted agent passes its own `redirect_uri` and uses `begin_authorization()` and `complete_authorization()` in its login and callback routes. For DCR, prefer a fixed port (`http://127.0.0.1:8765/callback`), because a registration is tied to its exact redirect URI. Each account keeps one registration, and signing in on a new redirect URI replaces it. Two processes signing in the same account at the same moment on different ports can replace each other's registration; the loser gets an error and should sign in again.

Agents built on the official MCP client use the adapter instead:

```python
from kinde_sdk.agents.mcp import KindeOAuthClientProvider

provider = KindeOAuthClientProvider(
    "https://api.example.com/mcp",
    client_metadata_url="https://agent.example.com/oauth/client-metadata.json",
    client_name="Example Agent",
    redirect_handler=..., callback_handler=...,
)
```

### Publish the client metadata document

```python
from kinde_sdk.agents import build_client_metadata_document
from kinde_fastapi.agents import client_metadata_router   # or kinde_flask.agents.client_metadata_blueprint

document = build_client_metadata_document(
    "https://agent.example.com/oauth/client-metadata.json",   # must be the exact URL it's served at
    "Example Agent",
    ["http://127.0.0.1/callback", "https://agent.example.com/oauth/callback"],
)
app.include_router(client_metadata_router(document))
```

Kinde fetches the document from the public internet, so it can't be served from `localhost`; use a tunnel with a real domain when testing. Kinde honours redirect URIs that are https on the document's own host, or http loopback on any port. It drops custom schemes (`myapp://`) and other hosts, and the builder raises an error for those.

See [examples/agents](examples/agents) for complete examples.

# Kinde Management API Module

This module provides a client for the Kinde Management API, allowing you to manage users, organizations, roles, permissions, and feature flags programmatically.

> **Note for v1 users**: The Management API usage has changed in v2. See the [Migration Guide](MIGRATION.md) for details on the new `ManagementClient` class.

## Installation

No additional installation is required if you already have the Kinde Python SDK installed. The Management API module is included as part of the SDK.

## Usage

The Management API client requires:
- Your Kinde domain
- Client ID
- Client secret

### Initializing the client

Create a `ManagementClient` with your M2M application's client credentials. It
authenticates automatically using the `client_credentials` grant — no callback
URL or grant type is required.

```python
from kinde_sdk.management import ManagementClient

# Initialize the client with client credentials (M2M application)
management = ManagementClient(
    domain="your-domain.kinde.com",
    client_id="your-client-id",
    client_secret="your-client-secret",
)
```

Each API group is exposed as a `<resource>_api` attribute, e.g.
`management.users_api`, `management.organizations_api`, `management.roles_api`.
The examples below use these resource APIs. Note that the client is
**synchronous** — calls are not awaited.

### Managing Users

```python
from kinde_sdk.management.models.create_user_request import CreateUserRequest
from kinde_sdk.management.models.create_user_request_profile import CreateUserRequestProfile
from kinde_sdk.management.models.create_user_request_identities_inner import CreateUserRequestIdentitiesInner
from kinde_sdk.management.models.update_user_request import UpdateUserRequest

# List users
users = management.users_api.get_users(page_size=10)

# Get a specific user
user = management.users_api.get_user_data(id="user_id")

# Create a new user
new_user = management.users_api.create_user(
    create_user_request=CreateUserRequest(
        profile=CreateUserRequestProfile(given_name="John", family_name="Doe"),
        identities=[
            CreateUserRequestIdentitiesInner(
                type="email",
                details={"email": "john.doe@example.com"},
            )
        ],
    )
)

# Update a user
updated_user = management.users_api.update_user(
    id="user_id",
    update_user_request=UpdateUserRequest(given_name="John", family_name="Smith"),
)

# Delete a user
result = management.users_api.delete_user(id="user_id")
```

### Managing Organizations

```python
from kinde_sdk.management.models.create_organization_request import CreateOrganizationRequest
from kinde_sdk.management.models.update_organization_request import UpdateOrganizationRequest

# List organizations
organizations = management.organizations_api.get_organizations(page_size=10)

# Get a specific organization
org = management.organizations_api.get_organization(code="org_code")

# Create a new organization
new_org = management.organizations_api.create_organization(
    create_organization_request=CreateOrganizationRequest(name="Example Organization")
)

# Update an organization
updated_org = management.organizations_api.update_organization(
    org_code="org_code",
    update_organization_request=UpdateOrganizationRequest(name="Updated Organization Name"),
)

# Delete an organization
result = management.organizations_api.delete_organization(org_code="org_code")
```

### Managing Organization Invites

```python
from kinde_sdk.management.models.create_organization_invite_request import CreateOrganizationInviteRequest

# List invites for an organization
invites = management.organizations_api.get_organization_invites(org_code="org_code")

# Create an invite
new_invite = management.organizations_api.create_organization_invite(
    org_code="org_code",
    create_organization_invite_request=CreateOrganizationInviteRequest(
        email="invitee@example.com",
        first_name="Jane",
        last_name="Doe",
        roles=["member"],  # role keys to assign on acceptance
    ),
)

# Get a single invite
invite = management.organizations_api.get_organization_invite(
    org_code="org_code", invite_code="invite_code"
)

# Delete an invite
result = management.organizations_api.delete_organization_invite(
    org_code="org_code", invite_code="invite_code"
)
```

### Managing Roles

```python
from kinde_sdk.management.models.create_role_request import CreateRoleRequest
from kinde_sdk.management.models.update_roles_request import UpdateRolesRequest

# List roles
roles = management.roles_api.get_roles(page_size=10)

# Get a specific role
role = management.roles_api.get_role(role_id="role_id")

# Create a new role
new_role = management.roles_api.create_role(
    create_role_request=CreateRoleRequest(
        name="Admin",
        description="Administrator role",
        key="admin_role",
    )
)

# Update a role
updated_role = management.roles_api.update_roles(
    role_id="role_id",
    update_roles_request=UpdateRolesRequest(
        name="Super Admin",
        key="admin_role",
        description="Super administrator role",
    ),
)

# Delete a role
result = management.roles_api.delete_role(role_id="role_id")
```

### Managing Feature Flags

Feature flags are created against your business and read back per organization
or environment.

```python
from kinde_sdk.management.models.create_feature_flag_request import CreateFeatureFlagRequest

# List feature flags for an organization
flags = management.organizations_api.get_organization_feature_flags(org_code="org_code")

# Create a new feature flag
new_flag = management.feature_flags_api.create_feature_flag(
    create_feature_flag_request=CreateFeatureFlagRequest(
        name="Dark Mode",
        key="dark_mode",
        description="Enable dark mode theme",
        type="bool",
        allow_override_level="env",
        default_value="false",
    )
)

# Update a feature flag (identified by its key)
updated_flag = management.feature_flags_api.update_feature_flag(
    feature_flag_key="dark_mode",
    name="Dark Theme",
    description="Enable dark theme for the application",
    type="bool",
    allow_override_level="env",
    default_value="false",
)

# Delete a feature flag
result = management.feature_flags_api.delete_feature_flag(feature_flag_key="dark_mode")
```

## Token Management

The Management API client automatically handles token management using client credentials:

- Tokens are automatically obtained when needed
- Tokens are cached to avoid unnecessary requests
- Tokens are refreshed when they expire
- Multiple instances of the client with the same domain and client ID share the same token

## Error Handling

All API methods can raise exceptions for HTTP errors. It's recommended to wrap calls in try/except blocks:

```python
try:
    user = management.users_api.get_user_data(id="non_existent_id")
except Exception as e:
    print(f"Error: {e}")
```

Complete example given below

```python
from kinde_sdk.management import ManagementClient
from kinde_sdk.management.models.create_user_request import CreateUserRequest
from kinde_sdk.management.models.create_user_request_profile import CreateUserRequestProfile
from kinde_sdk.management.models.create_user_request_identities_inner import CreateUserRequestIdentitiesInner
from kinde_sdk.management.models.create_organization_request import CreateOrganizationRequest


def main():
    """Demonstrates Management API usage with the synchronous ManagementClient."""
    # Initialize with your M2M application's client credentials.
    management = ManagementClient(
        domain="your-domain.kinde.com",      # Replace with your Kinde domain
        client_id="your-client-id",          # Your M2M client ID
        client_secret="your-client-secret",  # Your M2M client secret
    )

    user_id = None
    org_code = None

    # Example 1: List users
    print("Example 1: List users")
    print("-" * 50)
    users_result = management.users_api.get_users(page_size=10)
    for user in users_result.users or []:
        print(f"User: {user.first_name} {user.last_name} ({user.email})")
    print()

    # Example 2: Create a new user
    print("Example 2: Create a new user")
    print("-" * 50)
    try:
        new_user = management.users_api.create_user(
            create_user_request=CreateUserRequest(
                profile=CreateUserRequestProfile(given_name="Test", family_name="User"),
                identities=[
                    CreateUserRequestIdentitiesInner(
                        type="email",
                        details={"email": "testuser@example.com"},
                    )
                ],
            )
        )
        user_id = new_user.id
        print(f"User created: {user_id}")
    except Exception as e:
        print(f"Error creating user: {e}")
    print()

    # Example 3: List organizations
    print("Example 3: List organizations")
    print("-" * 50)
    orgs_result = management.organizations_api.get_organizations(page_size=10)
    for org in orgs_result.organizations or []:
        print(f"Organization: {org.name} (Code: {org.code})")
    print()

    # Example 4: Create a new organization
    print("Example 4: Create a new organization")
    print("-" * 50)
    try:
        new_org = management.organizations_api.create_organization(
            create_organization_request=CreateOrganizationRequest(name="Test Organization")
        )
        org_code = new_org.organization.code
        print(f"Organization created: {org_code}")
    except Exception as e:
        print(f"Error creating organization: {e}")
    print()

    # Example 5: List organization invites
    if org_code:
        print("Example 5: List organization invites")
        print("-" * 50)
        try:
            invites = management.organizations_api.get_organization_invites(org_code=org_code)
            print(f"Invites: {invites}")
        except Exception as e:
            print(f"Error listing invites: {e}")
        print()

    # Example 6: Clean up created resources
    print("Example 6: Clean up")
    print("-" * 50)
    if org_code:
        try:
            management.organizations_api.delete_organization(org_code=org_code)
            print("Organization deleted")
        except Exception as e:
            print(f"Error deleting organization: {e}")
    if user_id:
        try:
            management.users_api.delete_user(id=user_id)
            print("User deleted")
        except Exception as e:
            print(f"Error deleting user: {e}")


if __name__ == "__main__":
    main()
```

## Step-up authentication

Ask Kinde for a stronger or more recent authentication before a sensitive action, for example "MFA in the last 5 minutes before changing payout details". Kinde collects only what is missing (the second factor, or a passkey), and the user keeps their session. This is [RFC 9470](https://www.rfc-editor.org/rfc/rfc9470) on the normal Kinde login flow. There is nothing to register in Kinde, and nothing changes for existing logins.

| What | How |
|---|---|
| Ask for a context at login | `LoginOptions.ACR_VALUES` (`"mfa"` or `"phr"`) and `LoginOptions.MAX_AGE` (seconds) on `login()` and `register()` |
| Start a step-up | `await oauth.step_up(acr="mfa", max_age=300)` returns the URL to redirect to |
| Read how the user signed in | `oauth.get_authentication_context()` returns `{"acr": ..., "amr": [...], "auth_time": ...}` |
| Check a requirement | `oauth.has_authentication_context(acr="mfa", max_age=300)` |
| Check the environment | `oauth.is_step_up_supported()` |
| Callback errors | `UnmetAuthenticationRequirementsError`, `LoginRequiredError` |

`mfa` means a second factor. `phr` means phishing-resistant (a passkey with user verification) and also meets an `mfa` requirement. Kinde leaves `acr` out for a single-factor sign-in, so `acr` is `None` then.

### Require MFA in the last 5 minutes

#### FastAPI

```python
from fastapi.responses import PlainTextResponse, RedirectResponse
from kinde_sdk.core.exceptions import UnmetAuthenticationRequirementsError

@app.get("/payouts")
async def payouts():
    if not kinde_oauth.is_authenticated():
        return RedirectResponse("/login")
    if not kinde_oauth.has_authentication_context(acr="mfa", max_age=300):
        # The built-in /callback route brings the user back to this page
        return RedirectResponse(await kinde_oauth.step_up(acr="mfa", max_age=300))
    return {"message": "Payout details"}

@app.exception_handler(UnmetAuthenticationRequirementsError)
async def step_up_not_possible(request, error):
    # The user can't meet the requirement. This is final: don't send them back to Kinde.
    return PlainTextResponse("Add an authenticator app to your account to continue.", status_code=403)
```

#### Flask

```python
import asyncio
from flask import redirect
from kinde_sdk.core.exceptions import UnmetAuthenticationRequirementsError

@app.route("/payouts")
def payouts():
    if not kinde_oauth.is_authenticated():
        return redirect("/login")
    if not kinde_oauth.has_authentication_context(acr="mfa", max_age=300):
        # The built-in /callback route brings the user back to this page
        return redirect(asyncio.run(kinde_oauth.step_up(acr="mfa", max_age=300)))
    return {"message": "Payout details"}

@app.errorhandler(UnmetAuthenticationRequirementsError)
def step_up_not_possible(error):
    # The user can't meet the requirement. This is final: don't send them back to Kinde.
    return "Add an authenticator app to your account to continue.", 403
```

`step_up()` is a coroutine, like `login()`. In an `async def` Flask view (which needs `flask[async]`), `await` it instead of using `asyncio.run()`.

### When the user can't step up

If the user has no enrolled MFA factor or no passkey, Kinde returns `error=unmet_authentication_requirements` to your callback instead of tokens. The SDK validates `state` and raises `UnmetAuthenticationRequirementsError`. The built-in `/callback` routes let it reach your app, so handle it with `@app.exception_handler(...)` (FastAPI) or `@app.errorhandler(...)` (Flask), as above. Without a handler of your own, the user sees a plain-text 403 page.

- It is a final answer. Retrying gives the same error, and sending the user to login would sign them in without the step-up. Tell them why instead, for example "add a passkey to continue".
- The error has `error_description`, `state`, and the `acr_values` and `max_age` that were asked for, so you can say what is missing.
- A user who was signed in stays signed in, with the tokens they already had.
- `LoginRequiredError` is the same kind of error for `login_required`, which Kinde returns when a `prompt=none` request needs a screen. Both extend `KindeCallbackError`.

If you handle the callback yourself, pass the error through and catch it:

```python
try:
    await oauth.handle_redirect(code, user_id, state, error=error, error_description=error_description)
except UnmetAuthenticationRequirementsError as e:
    show_error(e.error_description)
```

### Good to know

- **After a step-up, the callback replaces the access, ID and refresh tokens.** Refreshing never upgrades a session: a refreshed token keeps the `acr`, `amr` and `auth_time` it had. When `has_authentication_context()` is false, the only way forward is `step_up()`.
- **`step_up()` is interactive.** It raises `ValueError` for `prompt=none` (also inside `auth_params`), for an invalid `acr` or `max_age`, and when neither is given. `max_age` must be a non-negative `int`. `0` is valid and forces a fresh verification.
- **Don't check `max_age=0`.** `has_authentication_context(max_age=0)` is only true in the same second as the sign-in, so the user would be sent back to Kinde every time. Use a short window such as 60 seconds.
- **Call `step_up()` when you redirect, not to render a link.** Each call stores a new `state`, replacing any login in progress.
- **Where the user lands.** With FastAPI and Flask, the user comes back to the page that called `step_up()` when that request was a GET. For any other method nothing is remembered, so the user lands on `/`: pass `post_login_redirect_url="/somewhere"` to choose the page, which you should do for a form POST (the POST is not replayed). Without a framework integration, your own callback decides.
- **Environments without step-up.** If the discovery document has no `acr_values_supported`, Kinde ignores `acr_values` and `max_age`. `step_up()` then raises `KindeConfigurationException` and sends nothing, instead of pretending it worked. `get_authentication_context()` reports `auth_time` as `None` there, because the claim may be the token's issue time, so `has_authentication_context(max_age=...)` is always false. Check `is_step_up_supported()` first and deny the action, or force a fresh sign-in with `login({"prompt": "login"})`, which only proves the user signed in again.
- **If discovery can't be fetched.** While the discovery document is unavailable, `is_step_up_supported()` returns `False` and `step_up()` raises `KindeRetrieveException`. That one is temporary: `step_up()` retries the fetch, at most once every 5 seconds.
- **More than one worker process.** Tokens are saved in the session with a revision, and every worker follows the newest one: a step-up handled by one worker is picked up by the others, and refreshed tokens are saved. This needs a session store that every worker shares (for Flask, the same `SECRET_KEY` and session backend).
- **Overlapping requests.** Session backends save a request's whole session when it ends, so a request that began before a step-up can write the old tokens back. A worker that has the newer tokens ignores that and repairs the session on its next request. A worker that has never seen the session (another process, or after a restart) trusts what it reads, so in that window it can still see the old tokens and ask for the step-up again.
- **`auth_time` comes from the ID token.** `amr` is informational. `has_authentication_context()` decides on `acr` and `auth_time` only.
- **What `mfa` asserts.** `acr: "mfa"` means two factors were accepted under your MFA policy. It does not assert that they are independent: a social sign-in followed by a one-time code to the same mailbox proves one channel twice. `phr` is the stronger value, because a phishing site can't use a passkey. For payments and regulated workloads, assess factor independence, enrolment and recovery against your own configuration rather than relying on `acr` alone.
- **APIs.** `kinde_sdk.has_authentication_context(claims, acr="mfa", max_age=300)` is the same check as a pure function, for the claims of an access token you have verified yourself. A `require_authentication_context` dependency/decorator that answers with the RFC 9470 `401` challenge is planned as a follow-up.

### Differences from the cross-SDK recommendations

- **No `returnTo` in `state` for standalone use.** Returning the user is done through the FastAPI and Flask post-login redirect. Without a framework integration the SDK doesn't own the callback, so your callback chooses the destination.
- **Only a GET returns the user automatically.** `step_up()` from a POST (or any other method) doesn't send the user back to the page that made it. Pass `post_login_redirect_url=` for those.
- **No `prompt=login` fallback.** On an environment without step-up, `step_up(max_age=...)` raises like `step_up(acr=...)` does, and the app decides what to do. A fallback sign-in could never satisfy `has_authentication_context(max_age=...)` there, so a guarded page would redirect in a loop.
- **`auth_params` is a raw passthrough.** `LoginOptions.ACR_VALUES` accepts only `mfa` and `phr`, and `LoginOptions.MAX_AGE` only an `int`. Inside `auth_params`, `acr_values` is sent as given and `max_age` may also be a string of digits, as before. In both places an unset value is never sent and an invalid `max_age` raises `ValueError`.
- **No clock tolerance by default.** `oauth.has_authentication_context()` compares `auth_time` with the server clock exactly. The pure function takes `leeway=` if you need one.

## Advanced Usage: Direct Storage Management

This section covers direct interaction with the `StorageManager` for custom storage solutions.
This is considered an advanced approach. For most use cases, the framework integrations provide sufficient storage handling.

> **Note for v1 users**: Storage management has been completely redesigned in v2. See the [Migration Guide](MIGRATION.md) for details on the new storage abstraction layer.

### Direct StorageManager Usage
```python
from kinde_sdk.auth import OAuth
from kinde_sdk.core.storage import StorageManager

# Basic initialization via OAuth
# This is the recommended way to initialize the storage system
# OAuth automatically initializes the StorageManager with the provided config
oauth = OAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="your_redirect_uri"
)

# Direct access to the storage manager
# This is safe to use after OAuth initialization
storage_manager = StorageManager()

# Store authentication data
storage_manager.set("user_tokens", {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_at": 1678901234
})

# Retrieve tokens
tokens = storage_manager.get("user_tokens")
if tokens:
    access_token = tokens.get("access_token")
    # Use the access token for API requests
    
# Delete tokens when logging out
storage_manager.delete("user_tokens")
```

### Using a Custom Storage Backend
```python
oauth = OAuth(
    client_id="your_client_id",
    storage_config={
        "type": "local_storage",
        "options": {
            # backend-specific options
        }
    }
)
```

### Handling Multi-Device Usage
The StorageManager automatically assigns a unique device ID to each client instance, ensuring that
the same user logged in on different devices won't experience session clashes. Keys are namespaced
with the device ID by default.

```python
# Get the current device ID
device_id = storage_manager.get_device_id()
print(f"Current device ID: {device_id}")

# Clear all data for the current device (useful for logout)
storage_manager.clear_device_data()

# For data that should be shared across all devices for the same user
# Use the "user:" prefix
storage_manager.set("user:shared_preferences", {"theme": "dark"})

# For data that should be global across all users and devices
# Use the "global:" prefix
storage_manager.set("global:app_settings", {"version": "1.0.0"})
```

### Best Practices for Storage Management

1. **Always initialize OAuth first**: The OAuth constructor initializes the StorageManager, so create your OAuth instance before accessing the storage.

2. **Manual initialization (if needed)**: If you need to use StorageManager before creating an OAuth instance, explicitly initialize it first:
```python
# Manual initialization
storage_manager = StorageManager()
storage_manager.initialize({"type": "memory"})  # or your preferred storage config

# You can also provide a specific device ID
storage_manager.initialize(
    config={"type": "memory"},
    device_id="custom-device-identifier"
)

# Now safe to use
storage_manager.set("some_key", {"some": "value"})
```

3. **Safe access pattern**: If you're unsure about initialization status, you can use this pattern:
```python
storage_manager = StorageManager()
if not storage_manager._initialized:
    storage_manager.initialize()
    
# Now safe to use
data = storage_manager.get("some_key")
```

4. **Single configuration**: Configure the storage only once at application startup. Changing storage configuration mid-operation may lead to data inconsistency.

5. **Access from anywhere**: After initialization, you can safely access the StorageManager from any part of your application without passing it around.

6. **Device-specific data**: Understand that by default, data is stored with device-specific namespacing. To share data across devices, use the appropriate prefixes.

7. **Complete logout**: To ensure all device-specific data is cleared during logout, call `storage_manager.clear_device_data()`.

# Version Tracking And Framework detection

The implementation generates headers in the exact format specified:

No Framework: Python/2.0.0

With Framework: Python-Flask/2.0.0/3.11.0/python


## Framework Detection

Auto-detects these frameworks:

Django, Flask, FastAPI (more frameworks can be added)

## Version Detection

SDK Version: Automatically detected from package metadata
Python Version: Detected from  ```sys.version_info```          
Fallback: Uses "2.0.0-dev" during development


## Publishing

The core team handles publishing.

## Migration Support

If you're upgrading from v1 of the Kinde Python SDK, we've prepared comprehensive migration resources:

- **[Migration Guide](MIGRATION.md)** - Detailed step-by-step instructions for upgrading from v1 to v2
- **[Quick Reference](QUICK_REFERENCE.md)** - At-a-glance conversion table for common v1 to v2 changes
- **[Troubleshooting](MIGRATION.md#troubleshooting-common-issues)** - Solutions for common migration issues

## Contributing

Please refer to Kinde's [contributing guidelines](https://github.com/kinde-oss/.github/blob/489e2ca9c3307c2b2e098a885e22f2239116394a/CONTRIBUTING.md).

### Development Setup

To set up the development environment, install the package in editable mode with development dependencies:

```bash
pip install -e ".[dev]"
```

**Note:** The `dev` optional dependency group includes all development tools (pytest, mypy, pylint, etc.). Pylint is conditionally installed based on your Python version:
- **Python 3.10+**: pylint >=4.0.0
- **Python 3.9**: pylint >=2.0, <4.0

This ensures compatibility with Python 3.9 while allowing newer Python versions to use the latest pylint features.

## License

By contributing to Kinde, you agree that your contributions will be licensed under its MIT License.
