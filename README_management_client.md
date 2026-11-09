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
from kinde_sdk.management import ManagementClient

# Initialize the client
client = ManagementClient(
    domain="your-domain.kinde.com",
    client_id="your-management-client-id",
    client_secret="your-management-client-secret"
)

# Get all users
users = client.users_api.get_users()

# Get a specific user
user = client.users_api.get_user_data(id="user_id")

# Get organizations
organizations = client.organizations_api.get_organizations()

# Get environment feature flags
feature_flags = client.environments_api.get_environement_feature_flags()
```

### 3. Using with .env file

```python
import os
from dotenv import load_dotenv
from kinde_sdk.management import ManagementClient

# Load environment variables from .env file
load_dotenv()

# Initialize the client using environment variables
client = ManagementClient(
    domain=os.getenv("KINDE_DOMAIN"),
    client_id=os.getenv("KINDE_MANAGEMENT_CLIENT_ID"),
    client_secret=os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET")
)
```

## Available APIs

Each Management API resource group is exposed as a `<resource>_api` attribute on the client. All methods, parameters, and typed request/response models are generated directly from the Kinde API spec:

- `client.users_api` - User management
- `client.organizations_api` - Organization management
- `client.roles_api` - Role management
- `client.permissions_api` - Permission management
- `client.feature_flags_api` - Feature flag management
- `client.environments_api` - Environment settings and feature flags
- `client.apis_api` - API (resource server) management
- `client.applications_api` - Application management
- `client.subscribers_api` - Subscriber management
- `client.properties_api` - Property management
- `client.webhooks_api` - Webhook management
- `client.connections_api` - Connection management
- `client.business_api` - Business information

For example, `client.users_api.get_users()`, `client.organizations_api.create_organization(...)`, `client.roles_api.get_roles()`.

> **Note**: Flat convenience methods on the client itself (e.g. `client.get_users()`) still work but are **deprecated** and emit a `DeprecationWarning`. Use the resource APIs above for full functionality and proper type hints.

## Examples

### Getting Users with Pagination

```python
# Get first 10 users
users = client.users_api.get_users(page_size=10)

# Get next page
if users.next_token:
    next_page = client.users_api.get_users(page_size=10, next_token=users.next_token)
```

### Creating a User

```python
from kinde_sdk.management.models.create_user_request import CreateUserRequest
from kinde_sdk.management.models.create_user_request_profile import CreateUserRequestProfile
from kinde_sdk.management.models.create_user_request_identities_inner import CreateUserRequestIdentitiesInner

new_user = client.users_api.create_user(
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
```

### Creating an Organization

```python
from kinde_sdk.management.models.create_organization_request import CreateOrganizationRequest

new_org = client.organizations_api.create_organization(
    create_organization_request=CreateOrganizationRequest(name="My Organization")
)
```

### Working with Feature Flags

```python
from kinde_sdk.management.models.create_feature_flag_request import CreateFeatureFlagRequest

# Get all environment feature flags
flags = client.environments_api.get_environement_feature_flags()

# Create a new feature flag
new_flag = client.feature_flags_api.create_feature_flag(
    create_feature_flag_request=CreateFeatureFlagRequest(
        name="new_feature",
        key="new_feature",
        type="bool",
        description="Enable new feature",
        allow_override_level="env",
        default_value="false",
    )
)
```

## Error Handling

The Management Client includes comprehensive error handling. API errors raise `ApiException` (or a status-specific subclass such as `NotFoundException` or `UnauthorizedException`):

```python
from kinde_sdk.management.exceptions import ApiException, NotFoundException

try:
    users = client.users_api.get_users()
except NotFoundException:
    print("Resource not found")
except ApiException as e:
    print(f"API error ({e.status}): {e.reason}")
```

## Testing

### Unit Tests

Run the management test suite:

```bash
pytest testv2/testv2_management/
```

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
from kinde_sdk.management.kinde_api_client import KindeApiClient

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