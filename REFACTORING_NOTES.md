# Refactoring Notes: Token Manager Access

## Overview

This refactoring addresses the duplication of `_get_token_manager` logic across multiple authentication modules and provides a cleaner API for consumers who need direct access to the token manager.

## Changes Made

### 1. Created BaseAuth Class

- **File**: `kinde_sdk/auth/base_auth.py`
- **Purpose**: Eliminates code duplication by providing shared `_get_framework()` and `_get_token_manager()` methods
- **Usage**: All auth classes now inherit from `BaseAuth`

### 2. Refactored Existing Classes

The following classes now inherit from `BaseAuth` and have their duplicated methods removed:

- `FeatureFlags` (in `feature_flags.py`)
- `Claims` (in `claims.py`) 
- `Permissions` (in `permissions.py`)

### 3. Created Tokens Wrapper

- **File**: `kinde_sdk/auth/tokens.py`
- **Purpose**: Provides a clean API for consumers who need direct access to the token manager
- **Exported as**: `tokens` singleton instance

## New Tokens API

### Basic Usage

```python
from kinde_sdk.auth import tokens

# Check authentication status
if tokens.is_authenticated():
    print("User is authenticated")

# Get user ID
user_id = tokens.get_user_id()

# Get token manager for direct access
token_manager = tokens.get_token_manager()
if token_manager:
    claims = token_manager.get_claims()
    access_token = token_manager.tokens.get("access_token")
```

### Available Methods

#### `tokens.get_token_manager() -> Optional[Any]`
Returns the token manager instance if available, `None` otherwise.

#### `tokens.get_user_id() -> Optional[str]`
Returns the current user ID if available, `None` otherwise.

#### `tokens.is_authenticated() -> bool`
Returns `True` if the user is authenticated, `False` otherwise.

#### `tokens.get_token_info() -> Dict[str, Any]`
Returns a dictionary with token information:
```python
{
    "isAuthenticated": bool,
    "userId": Optional[str],
    "hasAccessToken": bool,
    "hasIdToken": bool,
    "hasRefreshToken": bool
}
```

## Benefits

1. **Eliminated Code Duplication**: The `_get_token_manager` logic is now centralized in `BaseAuth`
2. **Cleaner API**: Consumers can access token manager functionality through the `tokens` wrapper
3. **Better Separation of Concerns**: Internal token manager access logic is abstracted away
4. **Consistent Interface**: All auth modules now follow the same pattern
5. **Easier Testing**: Shared logic can be tested once in `BaseAuth`

## Migration Guide

### For Existing Code

Existing code using `feature_flags`, `claims`, or `permissions` will continue to work without changes. The refactoring is backward compatible.

### For New Code

If you need direct access to the token manager, use the new `tokens` wrapper:

```python
# Old approach (exposed internal workings)
from kinde_sdk.auth import feature_flags
# Would need to understand internal structure

# New approach (clean API)
from kinde_sdk.auth import tokens
token_manager = tokens.get_token_manager()
```

## Testing

New tests have been added:
- `test_base_auth.py`: Tests the `BaseAuth` class functionality
- `test_tokens.py`: Tests the new `tokens` wrapper

Run tests to ensure everything works correctly:
```bash
pytest testv2/testv2_auth/test_base_auth.py
pytest testv2/testv2_auth/test_tokens.py
``` 