# Migration Guide

This document outlines breaking changes between major versions of the Kinde Python SDK.

## OpenAPI Generator Upgrade (6.5.0 → 7.19.0)

The Management API client has been regenerated using OpenAPI Generator 7.19.0 (previously 6.5.0). This brings significant improvements but also breaking changes for users who directly import models.

### Breaking Changes

#### 1. Import Paths

Model import paths have changed from `kinde_sdk.model.*` to `kinde_sdk.management.models.*`:

```python
# Before (OpenAPI Generator 6.x)
from kinde_sdk.model.user import User
from kinde_sdk.model.organization import Organization
from kinde_sdk.model.success_response import SuccessResponse

# After (OpenAPI Generator 7.x)
from kinde_sdk.management.models.user import User
from kinde_sdk.management.models.organization import Organization
from kinde_sdk.management.models.success_response import SuccessResponse
```

#### 2. Model Base Class

Models now use Pydantic `BaseModel` instead of the custom schema-based approach:

```python
# Before (6.x) - Custom schema-based models
user = User({"email": "test@example.com"})
email = user["email"]  # Dictionary-style access
email = user.get_item_oapg("email")  # Schema access method

# After (7.x) - Pydantic models
user = User(email="test@example.com")
email = user.email  # Attribute access
```

#### 3. Model Serialization

Serialization methods have changed to use Pydantic conventions:

```python
# Before (6.x)
user_dict = user.to_dict()
user_json = user.to_str()

# After (7.x)
user_dict = user.model_dump()  # or user.to_dict() (compatibility method provided)
user_json = user.model_dump_json()  # or user.to_json() (compatibility method provided)
```

#### 4. Optional Fields

Optional fields are now explicitly typed and default to `None`:

```python
# Before (6.x)
from kinde_sdk.management import schemas
if user.get_item_oapg("middle_name") is schemas.unset:
    # Field was not set

# After (7.x)
if user.middle_name is None:
    # Field was not set or explicitly None
```

#### 5. Model Validation

Pydantic provides stricter validation at instantiation time:

```python
# Before (6.x) - Validation could be deferred
user = User({})  # Empty dict accepted

# After (7.x) - Required fields must be provided
user = User()  # Works if all fields are Optional
user = User(email="required@example.com")  # Required fields must be passed
```

### Migration Steps

1. **Update imports**: Search and replace `from kinde_sdk.model.` with `from kinde_sdk.management.models.`

2. **Update model instantiation**: Change dictionary-style instantiation to keyword arguments:
   ```python
   # Before
   User({"email": "test@example.com", "given_name": "John"})
   
   # After
   User(email="test@example.com", given_name="John")
   ```

3. **Update field access**: Change dictionary/schema access to attribute access:
   ```python
   # Before
   user["email"] or user.get_item_oapg("email")
   
   # After
   user.email
   ```

4. **Update unset checks**: Replace `schemas.unset` checks with `None` checks:
   ```python
   # Before
   if field is schemas.unset:
   
   # After
   if field is None:
   ```

### API Client Usage (Unchanged)

The high-level `ManagementClient` API remains unchanged:

```python
from kinde_sdk.management import ManagementClient

client = ManagementClient(
    domain="https://your-domain.kinde.com",
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# These patterns still work the same
users = client.users_api.get_users()
user = client.users_api.get_user_data(id="user_id")
```

### Benefits of the Upgrade

- **Better type hints**: Full typing support with Pydantic
- **Improved validation**: Automatic validation of model fields
- **Modern Python**: Uses Python 3.8+ features and patterns
- **Better IDE support**: Autocomplete and type checking work correctly
- **Smaller footprint**: Cleaner generated code
