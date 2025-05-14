# Kinde Python SDK

The Kinde SDK for Python.

You can also use the [Python starter kit here](https://github.com/kinde-starter-kits/python-starter-kit).

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com) [![Kinde Docs](https://img.shields.io/badge/Kinde-Docs-eee?style=flat-square)](https://kinde.com/docs/developer-tools) [![Kinde Community](https://img.shields.io/badge/Kinde-Community-eee?style=flat-square)](https://thekindecommunity.slack.com)

## Documentation

For details on integrating this SDK into your project, head over to the [Kinde docs](https://kinde.com/docs/) and see the [Python SDK](https://kinde.com/docs/developer-tools/python-sdk/) doc 👍🏼.

## Storage Usage Examples

### Basic Usage
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

## Best Practices for Storage Management

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



# After initializing both OAuth and KindeApiClient use the following fn to get proper urls
api_client.fetch_openid_configuration(oauth)

## Framework Integrations

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
from fastapi import Depends
from kinde_sdk.kinde_api_client import KindeApiClient

@router.get("/protected")
async def protected_route(
    kinde_client: KindeApiClient = Depends(get_kinde_client)
):
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

## Installation

No additional installation is required if you already have the Kinde Python SDK installed. The Management API module is included as part of the SDK.

## Usage

The Management API client requires:
- Your Kinde domain
- Client ID
- Client secret

### Initializing the client

You can access the Management API through the existing `KindeApiClient`:

```python
from kinde_sdk.kinde_api_client import KindeApiClient
from kinde_sdk.enums import GrantType

# Initialize the client with client credentials
client = KindeApiClient(
    domain="your-domain.kinde.com",
    callback_url="https://your-app.com/callback",
    client_id="your-client-id",
    client_secret="your-client-secret", # Required for management API
    grant_type=GrantType.CLIENT_CREDENTIALS,
)

# Get the management client
management = client.get_management()
```

### Managing Users

```python
# List users
users = management.get_users(page_size=10)

# Get a specific user
user = management.get_user(user_id="user_id")

# Create a new user
new_user = management.create_user(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com"
)

# Update a user
updated_user = management.update_user(
    user_id="user_id",
    first_name="John",
    last_name="Smith"
)

# Delete a user
result = management.delete_user(user_id="user_id")
```

### Managing Organizations

```python
# List organizations
organizations = management.get_organizations(page_size=10)

# Get a specific organization
org = management.get_organization(org_code="org_code")

# Create a new organization
new_org = management.create_organization(
    name="Example Organization"
)

# Update an organization
updated_org = management.update_organization(
    org_code="org_code",
    name="Updated Organization Name"
)

# Delete an organization
result = management.delete_organization(org_code="org_code")
```

### Managing Roles

```python
# List roles
roles = management.get_roles(page_size=10)

# Get a specific role
role = management.get_role(role_id="role_id")

# Create a new role
new_role = management.create_role(
    name="Admin",
    description="Administrator role",
    key="admin_role"
)

# Update a role
updated_role = management.update_role(
    role_id="role_id",
    name="Super Admin",
    description="Super administrator role"
)

# Delete a role
result = management.delete_role(role_id="role_id")
```

### Managing Feature Flags

```python
# List feature flags
flags = management.get_feature_flags(page_size=10)

# Create a new feature flag
new_flag = management.create_feature_flag(
    name="Dark Mode",
    key="dark_mode",
    description="Enable dark mode theme",
    type="boolean",
    default_value=False
)

# Update a feature flag
updated_flag = management.update_feature_flag(
    feature_flag_id="flag_id",
    name="Dark Theme",
    description="Enable dark theme for the application"
)

# Delete a feature flag
result = management.delete_feature_flag(feature_flag_id="flag_id")
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
    user = management.get_user(user_id="non_existent_id")
except Exception as e:
    print(f"Error: {e}")
```

Complete example given below

```python
from kinde_sdk.kinde_api_client import KindeApiClient
from kinde_sdk.enums import GrantType

def main():
    """Main function demonstrating Management API usage."""
    # Initialize the Kinde client with management capabilities
    client = KindeApiClient(
        domain="your-domain.kinde.com",  # Replace with your Kinde domain
        callback_url="https://your-app.com/callback",  # Your auth callback URL
        client_id="your-client-id",  # Your client ID
        client_secret="your-client-secret",  # Required for management API
        grant_type=GrantType.CLIENT_CREDENTIALS,  # Use client credentials for management API
    )

    # Get the management client
    management = client.get_management()
    
    # Example 1: List users
    print("Example 1: List users")
    print("-" * 50)
    users_result = management.get_users(page_size=10)
    if users_result and "users" in users_result:
        users = users_result["users"]
        print(f"Total users: {len(users)}")
        for user in users:
            print(f"User: {user.get('first_name', '')} {user.get('last_name', '')} ({user.get('email', '')})")
    else:
        print("No users found or error occurred")
    print()

    # Example 2: Create a new user
    print("Example 2: Create a new user")
    print("-" * 50)
    try:
        new_user = management.create_user(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
        )
        print(f"User created: {new_user}")
        
        # Store the user ID for later examples
        user_id = new_user.get("id")
        print(f"User ID: {user_id}")
    except Exception as e:
        print(f"Error creating user: {e}")
    print()

    # Example 3: Update a user
    print("Example 3: Update a user")
    print("-" * 50)
    try:
        # Use the user ID from Example 2
        if 'user_id' in locals():
            updated_user = management.update_user(user_id,
                first_name="Updated",
                last_name="User"
            )
            print(f"User updated: {updated_user}")
        else:
            print("No user ID available for update")
    except Exception as e:
        print(f"Error updating user: {e}")
    print()

    # Example 4: List organizations
    print("Example 4: List organizations")
    print("-" * 50)
    orgs_result = management.get_organizations(page_size=10)
    if orgs_result and "organizations" in orgs_result:
        orgs = orgs_result["organizations"]
        print(f"Total organizations: {len(orgs)}")
        for org in orgs:
            print(f"Organization: {org.get('name', '')} (Code: {org.get('code', '')})")
    else:
        print("No organizations found or error occurred")
    print()

    # Example 5: Create a new organization
    print("Example 5: Create a new organization")
    print("-" * 50)
    try:
        new_org = management.create_organization(
            name="Test Organization"
        )
        print(f"Organization created: {new_org}")
        
        # Store the org code for later examples
        org_code = new_org.get("code")
        print(f"Organization Code: {org_code}")
    except Exception as e:
        print(f"Error creating organization: {e}")
    print()

    # Example 6: Update an organization
    print("Example 6: Update an organization")
    print("-" * 50)
    try:
        # Use the org code from Example 5
        if 'org_code' in locals():
            updated_org = management.update_organization(org_code,
                name="Updated Organization"
            )
            print(f"Organization updated: {updated_org}")
        else:
            print("No organization code available for update")
    except Exception as e:
        print(f"Error updating organization: {e}")
    print()

    # Example 7: List roles
    print("Example 7: List roles")
    print("-" * 50)
    roles_result = management.get_roles(page_size=10)
    if roles_result and "roles" in roles_result:
        roles = roles_result["roles"]
        print(f"Total roles: {len(roles)}")
        for role in roles:
            print(f"Role: {role.get('name', '')} (Key: {role.get('key', '')})")
    else:
        print("No roles found or error occurred")
    print()

    # Example 8: Create a new role
    print("Example 8: Create a new role")
    print("-" * 50)
    try:
        new_role = management.create_role(
            name="Test Role",
            description="A test role created via the Management API",
            key="test_role"
        )
        print(f"Role created: {new_role}")
        
        # Store the role ID for later examples
        role_id = new_role.get("id")
        print(f"Role ID: {role_id}")
    except Exception as e:
        print(f"Error creating role: {e}")
    print()

    # Example 9: Get feature flags
    print("Example 9: Get feature flags")
    print("-" * 50)
    flags_result = management.get_feature_flags(page_size=10)
    if flags_result and "feature_flags" in flags_result:
        flags = flags_result["feature_flags"]
        print(f"Total feature flags: {len(flags)}")
        for flag in flags:
            print(f"Flag: {flag.get('name', '')} (Key: {flag.get('key', '')})")
    else:
        print("No feature flags found or error occurred")
    print()

    # Example 10: Create a new feature flag
    print("Example 10: Create a new feature flag")
    print("-" * 50)
    try:
        new_flag = management.create_feature_flag(
            name="Test Flag",
            key="test_flag",
            description="A test feature flag created via the Management API",
            type="boolean",
            default_value=False
        )
        print(f"Feature flag created: {new_flag}")
        
        # Store the flag ID for later examples
        flag_id = new_flag.get("id")
        print(f"Flag ID: {flag_id}")
    except Exception as e:
        print(f"Error creating feature flag: {e}")
    print()

    # Example 11: Clean up (delete created resources)
    print("Example 11: Clean up")
    print("-" * 50)
    
    # Delete the feature flag (if created)
    if 'flag_id' in locals():
        try:
            result = management.delete_feature_flag(flag_id)
            print(f"Feature flag deleted: {result}")
        except Exception as e:
            print(f"Error deleting feature flag: {e}")
    
    # Delete the role (if created)
    if 'role_id' in locals():
        try:
            result = management.delete_role(role_id)
            print(f"Role deleted: {result}")
        except Exception as e:
            print(f"Error deleting role: {e}")
    
    # Delete the organization (if created)
    if 'org_code' in locals():
        try:
            result = management.delete_organization(org_code)
            print(f"Organization deleted: {result}")
        except Exception as e:
            print(f"Error deleting organization: {e}")
    
    # Delete the user (if created)
    if 'user_id' in locals():
        try:
            result = management.delete_user(user_id)
            print(f"User deleted: {result}")
        except Exception as e:
            print(f"Error deleting user: {e}")

if __name__ == "__main__":
    main()

## Publishing

The core team handles publishing.

## Contributing

Please refer to Kinde's [contributing guidelines](https://github.com/kinde-oss/.github/blob/489e2ca9c3307c2b2e098a885e22f2239116394a/CONTRIBUTING.md).

## License

By contributing to Kinde, you agree that your contributions will be licensed under its MIT License.