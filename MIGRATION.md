# Migrating from Kinde Python SDK v1 to v2

This document outlines the key changes and migration steps when upgrading from Kinde Python SDK v1 to v2.

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
- New `OAuth` class for handling authentication flows
- Improved token management with `TokenManager`
- Better session handling with `UserSession`
- Support for feature flags and permissions

### 3. Storage and Framework Abstraction
- New storage abstraction layer with `StorageFactory`
- Framework abstraction with `FrameworkFactory` and `FrameworkInterface`
- Support for custom storage implementations

## Migration Steps

### 1. Update Dependencies
Update your `requirements.txt` or `pyproject.toml` to use the new SDK:
```toml
kinde-python-sdk = "^2.0.0"
```

Or install directly using pip:
```bash
# Install the latest v2 version
pip install kinde-python-sdk>=2.0.0

# Install a specific v2 version
pip install kinde-python-sdk==2.0.0b11
```

### 2. Framework-Specific Changes

#### Flask
```python
# Old (v1)
from kinde_sdk import KindeClient

# New (v2)
from kinde_flask import KindeFlask
```

#### FastAPI
```python
# New (v2)
from kinde_fastapi import KindeFastAPI
```

### 3. Authentication Changes
```python
# Old (v1)
client = KindeClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    domain="your_domain"
)

# New (v2)
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
# Old (v1)
token = client.get_token()

# New (v2)
from kinde_sdk import TokenManager

token_manager = TokenManager(oauth)
token = token_manager.get_token()
```

### 5. User Session
```python
# New (v2)
from kinde_sdk import UserSession

session = UserSession(oauth)
user_info = session.get_user_info()
```

## New Features

### 1. Feature Flags
```python
# New (v2)
from kinde_sdk import feature_flags

flags = feature_flags.get_flags()
```

### 2. Permissions
```python
# New (v2)
from kinde_sdk import permissions

has_permission = permissions.check("permission_name")
```

### 3. Claims
```python
# New (v2)
from kinde_sdk import claims

user_claims = claims.get_claims()
```

## Breaking Changes

1. The authentication flow has been completely redesigned
2. Framework-specific implementations are now separate packages
3. Token management is now handled through the `TokenManager` class
4. Session management is now handled through the `UserSession` class
5. Storage and framework abstractions are now required

### Historical v1 Methods

#### Feature Flags
```python
# Old (v1)
client.get_flag(code="flag_name", default_value=None, flag_type="")
client.get_boolean_flag(code="flag_name", default_value=None)
client.get_string_flag(code="flag_name", default_value=None)
client.get_integer_flag(code="flag_name", default_value=None)

# New (v2)
from kinde_sdk import feature_flags

flag = await feature_flags.get_flag("flag_name", default_value=None)
all_flags = await feature_flags.get_all_flags()
```

#### Permissions
```python
# Old (v1)
client.get_permission(permission="permission_name")
client.get_permissions()

# New (v2)
from kinde_sdk import permissions

permission = await permissions.get_permission("permission_name")
all_permissions = await permissions.get_permissions()
```

#### Claims
```python
# Old (v1)
client.get_claim(key="claim_name", token_name="access_token")
client.get_claim_token(token_value={}, key="claim_name", token_name="access_token")

# New (v2)
from kinde_sdk import claims

claim = await claims.get_claim("claim_name")
all_claims = await claims.get_all_claims()
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