# SmartOAuth FastAPI Example

This example demonstrates how to use the new SmartOAuth client in a FastAPI application.

## What is SmartOAuth?

SmartOAuth is a new client that automatically detects whether you're running in a synchronous or asynchronous context and uses the appropriate methods. This provides a consistent API across different frameworks while maintaining optimal performance.

## Key Features

- **Automatic Context Detection**: SmartOAuth detects if you're in an async context (like FastAPI) and uses async methods automatically
- **Warning System**: Shows warnings when using sync methods in async contexts to guide developers toward best practices
- **Backward Compatibility**: Works with existing code while providing new async capabilities
- **Consistent API**: Same interface across different frameworks

## Setup

1. **Environment Variables**: Create a `.env` file with your Kinde credentials:
   ```env
   KINDE_DOMAIN=your-domain.kinde.com
   KINDE_CLIENT_ID=your-client-id
   KINDE_CLIENT_SECRET=your-client-secret
   KINDE_REDIRECT_URI=http://localhost:5000/callback
   KINDE_MANAGEMENT_CLIENT_ID=your-management-client-id
   KINDE_MANAGEMENT_CLIENT_SECRET=your-management-client-secret
   ```

2. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn python-dotenv
   ```

3. **Run the Example**:
   ```bash
   python -m uvicorn kinde_fastapi.examples.example_app:app --reload --port 5000
   ```

## Available Routes

- **`/`**: Home page showing authentication status and user info
- **`/login`**: Initiate login with SmartOAuth
- **`/logout`**: Logout using SmartOAuth
- **`/demo_smart_oauth`**: JSON endpoint demonstrating SmartOAuth features
- **`/demo_auth_modules`**: JSON endpoint showing sync and async auth modules
- **`/call_management_users`**: Management API integration example

## Code Examples

### Basic SmartOAuth Usage

```python
from kinde_sdk import SmartOAuth

# Initialize SmartOAuth
kinde_oauth = SmartOAuth(
    framework="fastapi",
    app=app
)

# In FastAPI (async context), SmartOAuth automatically uses async methods
if kinde_oauth.is_authenticated():
    user = await kinde_oauth.get_user_info_async()  # Recommended
    # OR
    user = kinde_oauth.get_user_info()  # Will show warning but still work
```

### Factory Function Usage

```python
from kinde_sdk import create_oauth_client

# Create SmartOAuth (auto-detect)
kinde_oauth = create_oauth_client(
    async_mode=None,  # None = auto-detect
    framework="fastapi",
    app=app
)

# Create explicit async client
async_oauth = create_oauth_client(
    async_mode=True,
    framework="fastapi",
    app=app
)

# Create explicit sync client
sync_oauth = create_oauth_client(
    async_mode=False,
    framework="fastapi",
    app=app
)
```

### Auth Modules Integration

```python
from kinde_sdk.auth import claims, async_claims, feature_flags, permissions

# Sync auth modules
claims_data = await claims.get_all_claims()

# Async auth modules
async_claims_data = await async_claims.get_all_claims()
feature_flags_data = await feature_flags.get_all_flags()
permissions_data = await permissions.get_permissions()
```

## What You'll See

When you run this example:

1. **Home Page**: Shows user info, claims, feature flags, and permissions
2. **Context Detection**: SmartOAuth automatically detects the async FastAPI context
3. **Warnings**: If you use sync methods in async contexts, you'll see deprecation warnings
4. **Performance**: Async methods are used automatically for better performance

## Benefits

- **Simplified Development**: No need to worry about sync vs async - SmartOAuth handles it
- **Better Performance**: Automatic use of async methods in async contexts
- **Future-Proof**: Easy migration path as you adopt more async patterns
- **Consistent Experience**: Same API across Flask, FastAPI, and other frameworks

## Migration from OAuth

If you're migrating from the old `OAuth` client:

```python
# Old way
from kinde_sdk import OAuth
kinde_oauth = OAuth(framework="fastapi", app=app)

# New way
from kinde_sdk import SmartOAuth
kinde_oauth = SmartOAuth(framework="fastapi", app=app)

# Your existing code will work, but you can now also use async methods
user = await kinde_oauth.get_user_info_async()  # New async method
```

The SmartOAuth client is a drop-in replacement for the existing OAuth client with additional async capabilities!
