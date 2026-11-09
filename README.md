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
