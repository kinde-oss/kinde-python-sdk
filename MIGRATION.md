# Migrating from Kinde Python SDK v1 to v2

This document outlines the key changes and migration steps when upgrading from Kinde Python SDK v1 to v2.

## ⚠️ Important: Breaking Changes

**The `KindeClient` class from v1 has been completely replaced.** If you're getting import errors for `KindeClient`, this is expected - you need to use the new `OAuth` class instead.

## Major Changes

### 1. Framework-Specific Implementations
The v2.0 SDK introduces dedicated framework implementations for:
- Flask
- FastAPI

Each framework has its own package with optimized implementations:
- `kinde_flask`
- `kinde_fastapi`

### 2. Authentication Flow
The authentication implementation has been completely revamped:
- **NEW**: `OAuth` class replaces `KindeClient` for authentication flows
- **NEW**: `ManagementClient` class for management API operations
- Improved token management with `TokenManager`
- Better session handling with `UserSession`
- Support for feature flags and permissions

### 3. Storage and Framework Abstraction
- New storage abstraction layer with `StorageFactory`
- Framework abstraction with `FrameworkFactory` and `FrameworkInterface`
- Support for custom storage implementations

## Which Client Should You Use?

### For User Authentication (Most Common)
```python
from kinde_sdk import OAuth

# Use this for:
# - User login/logout flows
# - Checking if users are authenticated
# - Getting user information
# - Accessing user claims, permissions, feature flags
```

### For Management Operations (Admin/Backend)
```python
from kinde_sdk.management import ManagementClient

# Use this for:
# - Managing users, organizations, roles
# - Creating/updating permissions
# - Managing feature flags
# - Administrative operations
```

## Migration Steps

### 1. Update Dependencies
Update your `requirements.txt` or `pyproject.toml` to use the new SDK:
```toml
kinde-python-sdk = "^2.X.X"
```

Or install directly using pip:
```bash
# Install the latest v2 version
pip install kinde-python-sdk>=2.X.X

# Install a specific v2 version
pip install kinde-python-sdk==2.0.0b12
```

### 2. Framework-Specific Changes

#### Flask
```python
# ❌ OLD (v1) - This will NOT work in v2
from kinde_sdk import KindeClient  # This class no longer exists!

# ✅ NEW (v2) - Use this instead
from kinde_sdk import OAuth

# Initialize Flask app
app = Flask(__name__)

# Initialize Kinde OAuth with Flask framework
kinde_oauth = OAuth(
    framework="flask",
    app=app
)

# Check authentication
if kinde_oauth.is_authenticated():
    user = kinde_oauth.get_user_info()
```

**📖 See complete Flask example:** `kinde_flask/examples/example_app.py`

#### FastAPI
```python
# ✅ NEW (v2)
from kinde_sdk import OAuth
from kinde_sdk.auth import claims, feature_flags, permissions

# Initialize FastAPI app
app = FastAPI(title="Kinde FastAPI Example")

# Initialize Kinde OAuth with FastAPI framework
kinde_oauth = OAuth(
    framework="fastapi",
    app=app
)

# Check authentication and get user info
if kinde_oauth.is_authenticated():
    user = kinde_oauth.get_user_info()
    all_claims = await claims.get_all_claims()
    all_flags = await feature_flags.get_all_flags()
    all_permissions = await permissions.get_permissions()
```

**📖 See complete FastAPI example:** `kinde_fastapi/examples/example_app.py`

### 3. Authentication Changes
```python
# ❌ OLD (v1) - This will NOT work in v2
client = KindeClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    domain="your_domain"
)

# ✅ NEW (v2) - Use this instead
from kinde_sdk import OAuth

oauth = OAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    domain="your_domain",
    redirect_uri="your_redirect_uri"
)
```

### 4. Token Management
```python
# ❌ OLD (v1)
token = client.get_token()

# ✅ NEW (v2)
# Token management is handled internally by the SDK for most use cases.
# For advanced use cases, you can access the token manager via the new tokens class:
from kinde_sdk.auth import tokens

token_manager = tokens.get_token_manager()
if token_manager:
    # Access raw tokens and claims
    access_token = token_manager.tokens.get("access_token")
    id_token = token_manager.tokens.get("id_token")
    refresh_token = token_manager.tokens.get("refresh_token")
    claims = token_manager.get_claims()

# You can also get a summary of the token state:
token_info = tokens.get_token_info()
print(token_info)
```

## Framework Examples

For complete, working examples of how to integrate the Kinde Python SDK v2 with your framework, see:

### Flask Example
- **Location:** `kinde_flask/examples/example_app.py`
- **Features:** Basic authentication flow, user info display, login/logout functionality
- **Key highlights:** Simple Flask integration with session management

### FastAPI Example  
- **Location:** `kinde_fastapi/examples/example_app.py`
- **Features:** Full authentication flow, claims, feature flags, permissions, and token access
- **Key highlights:** Async/await support, comprehensive SDK feature demonstration

Both examples include:
- Environment variable configuration
- Session middleware setup
- Authentication status checking
- User information retrieval
- Login/logout endpoints

## New Features

### 1. Feature Flags
```python
# ✅ NEW (v2)
from kinde_sdk.auth import feature_flags

flags = await feature_flags.get_flags()
```

### 2. Permissions
```python
# ✅ NEW (v2)
from kinde_sdk.auth import permissions

has_permission = await permissions.check("permission_name")
```

### 3. Claims
```python
# ✅ NEW (v2)
from kinde_sdk.auth import claims

user_claims = await claims.get_claims()
```

## Breaking Changes

1. **`KindeClient` class has been completely removed** - use `OAuth` instead
2. The authentication flow has been completely redesigned
3. Framework-specific implementations are now separate packages
4. Token management is now handled through the `TokenManager` class
5. Session management is now handled through the `UserSession` class
6. Storage and framework abstractions are now required

### Historical v1 Methods

#### Feature Flags
```python
# ❌ OLD (v1) - These methods no longer exist
client.get_flag(code="flag_name", default_value=None, flag_type="")
client.get_boolean_flag(code="flag_name", default_value=None)
client.get_string_flag(code="flag_name", default_value=None)
client.get_integer_flag(code="flag_name", default_value=None)

# ✅ NEW (v2) - Use these instead
from kinde_sdk.auth import feature_flags

flag = await feature_flags.get_flag("flag_name", default_value=None)
all_flags = await feature_flags.get_all_flags()
```

#### Permissions
```python
# ❌ OLD (v1) - These methods no longer exist
client.get_permission(permission="permission_name")
client.get_permissions()

# ✅ NEW (v2) - Use these instead
from kinde_sdk.auth import permissions

permission = await permissions.get_permission("permission_name")
all_permissions = await permissions.get_permissions()
```

#### Claims
```python
# ❌ OLD (v1) - These methods no longer exist
client.get_claim(key="claim_name", token_name="access_token")
client.get_claim_token(token_value={}, key="claim_name", token_name="access_token")

# ✅ NEW (v2) - Use these instead
from kinde_sdk.auth import claims

claim = await claims.get_claim("claim_name")
all_claims = await claims.get_all_claims()
```

## Troubleshooting Common Issues

### Issue: "ImportError: cannot import name 'KindeClient'"
**Solution:** The `KindeClient` class has been removed in v2. Use `OAuth` instead:
```python
# ❌ This will fail
from kinde_sdk import KindeClient

# ✅ Use this instead
from kinde_sdk import OAuth
```

### Issue: "AttributeError: 'OAuth' object has no attribute 'get_flag'"
**Solution:** Feature flag methods have moved to a separate module:
```python
# ❌ This will fail
oauth.get_flag("flag_name")

# ✅ Use this instead
from kinde_sdk.auth import feature_flags
await feature_flags.get_flag("flag_name")
```

### Issue: "ModuleNotFoundError: No module named 'kinde_sdk.auth'"
**Solution:** Make sure you're using the correct SDK version:
```bash
pip install kinde-python-sdk>=2.0.0
```

### Issue: "TypeError: 'OAuth' object is not callable"
**Solution:** Make sure you're instantiating the class correctly:
```python
# ❌ Wrong
oauth = OAuth()

# ✅ Correct
oauth = OAuth(
    framework="flask",  # or "fastapi"
    app=app
)
```

## Additional Notes

- The v2.0 SDK provides better type hints and documentation
- Improved error handling and logging
- Better support for custom implementations
- More robust token refresh mechanism
- Enhanced security features

## Support

For additional support or questions about migration, please:
1. Check the [documentation](https://kinde.com/docs)
2. Visit our [GitHub repository](https://github.com/kinde-oss/kinde-python-sdk)
3. Contact our support team at support@kinde.com 