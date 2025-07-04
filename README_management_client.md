# Kinde Management Client

The Kinde Management Client is a Python client for interacting with the Kinde Management API. It provides a clean, easy-to-use interface for managing users, organizations, roles, permissions, feature flags, and more.

## Features

- **Automatic Token Management**: Handles OAuth2 client credentials flow automatically
- **Dynamic Method Generation**: Automatically generates methods for all API endpoints
- **Error Handling**: Comprehensive error handling and logging
- **Framework Detection**: Automatically detects and reports the web framework being used
- **Type Safety**: Full type hints for better development experience

## Installation

The Management Client is part of the Kinde Python SDK. Make sure you have the SDK installed:

```bash
pip install kinde-python-sdk
```

For .env file support, also install python-dotenv:

```bash
pip install python-dotenv
```

## Quick Start

### 1. Set up your credentials

Create a `.env` file in your project root with your Kinde credentials:

```bash
# .env file
KINDE_DOMAIN=your-domain.kinde.com
KINDE_MANAGEMENT_CLIENT_ID=your-management-client-id
KINDE_MANAGEMENT_CLIENT_SECRET=your-management-client-secret
```

### 2. Basic Usage

```python
from kinde_sdk.management.management_client import ManagementClient

# Initialize the client
client = ManagementClient(
    domain="your-domain.kinde.com",
    client_id="your-management-client-id",
    client_secret="your-management-client-secret"
)

# Get all users
users = client.get_users()

# Get a specific user
user = client.get_user("user_id")

# Get organizations
organizations = client.get_organizations()

# Get feature flags
feature_flags = client.get_feature_flags()
```

### 3. Using with .env file

```python
import os
from dotenv import load_dotenv
from kinde_sdk.management.management_client import ManagementClient

# Load environment variables from .env file
load_dotenv()

# Initialize the client using environment variables
client = ManagementClient(
    domain=os.getenv("KINDE_DOMAIN"),
    client_id=os.getenv("KINDE_MANAGEMENT_CLIENT_ID"),
    client_secret=os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET")
)
```

## Available Methods

The Management Client automatically generates methods for all available API endpoints:

### Users
- `get_users()` - Get all users
- `get_user(user_id)` - Get a specific user
- `create_user(**data)` - Create a new user
- `update_user(user_id, **data)` - Update a user
- `delete_user(user_id)` - Delete a user

### Organizations
- `get_organizations()` - Get all organizations
- `get_organization(org_code)` - Get a specific organization
- `create_organization(**data)` - Create a new organization
- `update_organization(org_code, **data)` - Update an organization
- `delete_organization(org_code)` - Delete an organization

### Roles
- `get_roles()` - Get all roles
- `get_role(role_id)` - Get a specific role
- `create_role(**data)` - Create a new role
- `update_role(role_id, **data)` - Update a role
- `delete_role(role_id)` - Delete a role

### Permissions
- `get_permissions()` - Get all permissions
- `get_permission(permission_id)` - Get a specific permission
- `create_permission(**data)` - Create a new permission
- `update_permission(permission_id, **data)` - Update a permission
- `delete_permission(permission_id)` - Delete a permission

### Feature Flags
- `get_feature_flags()` - Get all feature flags
- `get_feature_flag(feature_flag_id)` - Get a specific feature flag
- `create_feature_flag(**data)` - Create a new feature flag
- `update_feature_flag(feature_flag_id, **data)` - Update a feature flag
- `delete_feature_flag(feature_flag_id)` - Delete a feature flag

### Other Resources
- `get_timezones()` - Get available timezones
- `get_industries()` - Get available industries
- `get_subscribers()` - Get all subscribers
- `get_connected_apps()` - Get connected applications
- `get_api_applications()` - Get API applications

## Examples

### Getting Users with Pagination

```python
# Get first 10 users
users = client.get_users(page_size=10)

# Get next page
next_token = users.get('next_token')
if next_token:
    next_page = client.get_users(page_size=10, next_token=next_token)
```

### Creating a User

```python
user_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "identities": [
        {
            "type": "email",
            "details": {
                "email": "john.doe@example.com"
            }
        }
    ]
}

new_user = client.create_user(**user_data)
```

### Creating an Organization

```python
org_data = {
    "name": "My Organization",
    "feature_flags": {
        "theme": "dark"
    }
}

new_org = client.create_organization(**org_data)
```

### Working with Feature Flags

```python
# Get all feature flags
flags = client.get_feature_flags()

# Create a new feature flag
flag_data = {
    "name": "new_feature",
    "type": "boolean",
    "description": "Enable new feature",
    "allow_override": True,
    "default_value": False
}

new_flag = client.create_feature_flag(**flag_data)
```

## Error Handling

The Management Client includes comprehensive error handling:

```python
try:
    users = client.get_users()
except Exception as e:
    print(f"Error getting users: {e}")
    # Handle the error appropriately
```

## Testing

### Quick Test

Run the quick test script to verify everything is working:

```bash
python test_management_client.py
```

The script will automatically create a sample `.env` file if one doesn't exist.

### Full Example

Run the comprehensive example to test all API endpoints:

```bash
# Make sure your .env file is set up with real credentials
python examples/management_client_example.py
```

## Configuration

### Environment Variables (.env file)

Create a `.env` file in your project root:

```bash
# Kinde Management API Configuration
KINDE_DOMAIN=your-domain.kinde.com
KINDE_MANAGEMENT_CLIENT_ID=your-management-client-id
KINDE_MANAGEMENT_CLIENT_SECRET=your-management-client-secret

# Optional: Other Kinde configuration
# KINDE_CLIENT_ID=your-regular-client-id
# KINDE_CLIENT_SECRET=your-regular-client-secret
# KINDE_REDIRECT_URI=http://localhost:3000/callback
```

### Programmatic Configuration

```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

client = ManagementClient(
    domain=os.getenv("KINDE_DOMAIN"),
    client_id=os.getenv("KINDE_MANAGEMENT_CLIENT_ID"),
    client_secret=os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET")
)
```

### Direct Configuration

```python
client = ManagementClient(
    domain="your-domain.kinde.com",
    client_id="your-management-client-id",
    client_secret="your-management-client-secret"
)
```

## SDK Structure

After the restructure, the Kinde Python SDK is organized into three main components:

1. **Auth Module** (`kinde_sdk.auth.*`) - Authentication and OAuth functionality
2. **Core Module** (`kinde_sdk.core.*`) - Core utilities and framework support
3. **Management Module** (`kinde_sdk.management.*`) - Management API client (this module)

The Management Client is completely independent and doesn't rely on the main SDK's generated code.

## Migration from Legacy Code

If you were previously using the legacy `KindeApiClient` for management operations, you can now use the new `ManagementClient`:

### Before (Legacy)
```python
from kinde_sdk.kinde_api_client import KindeApiClient

client = KindeApiClient(
    domain="your-domain.kinde.com",
    client_id="your-management-client-id",
    client_secret="your-management-client-secret",
    grant_type=GrantType.CLIENT_CREDENTIALS
)
```

### After (New)
```python
from kinde_sdk.management.management_client import ManagementClient

client = ManagementClient(
    domain="your-domain.kinde.com",
    client_id="your-management-client-id",
    client_secret="your-management-client-secret"
)
```

## Support

For support and questions about the Management Client:

1. Check the [Kinde Documentation](https://docs.kinde.com/)
2. Review the [API Reference](https://kinde.com/docs/api/)
3. Open an issue on the GitHub repository

## License

This project is licensed under the MIT License - see the LICENSE file for details. 