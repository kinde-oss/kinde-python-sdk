# Kinde Python SDK: Async/Sync Consistency Guide

## Overview

The Kinde Python SDK now provides consistent async and sync APIs to support both synchronous and asynchronous applications. This guide explains the new patterns and how to use them effectively.

## Problem Statement

Previously, the SDK had inconsistent async/sync patterns:
- Some methods were async (`login()`, `register()`, `logout()`)
- Some methods were sync (`get_user_info()`, `is_authenticated()`)
- This created confusion and required users to remember which methods to use in which context

## Solution: Three Client Types

### 1. Sync Client (`OAuth`)
The original sync client for synchronous applications.

```python
from kinde_sdk import OAuth

# Sync usage
oauth = OAuth(framework="flask", app=app)

if oauth.is_authenticated():
    user_info = oauth.get_user_info()  # Sync method
    print(f"Welcome, {user_info['email']}!")
```

### 2. Async Client (`AsyncOAuth`)
New async client for asynchronous applications.

```python
from kinde_sdk import AsyncOAuth

# Async usage
oauth = AsyncOAuth(framework="fastapi", app=app)

if oauth.is_authenticated():
    user_info = await oauth.get_user_info_async()  # Async method
    print(f"Welcome, {user_info['email']}!")

# All methods are async
login_url = await oauth.login()
logout_url = await oauth.logout()
```

### 3. Smart Client (`SmartOAuth`)
Context-aware client that automatically adapts to sync/async contexts.

```python
from kinde_sdk import SmartOAuth

# Works in both sync and async contexts
oauth = SmartOAuth(framework="fastapi", app=app)

# In sync context
def sync_function():
    if oauth.is_authenticated():
        user_info = oauth.get_user_info()  # Sync
        return user_info

# In async context
async def async_function():
    if oauth.is_authenticated():
        user_info = await oauth.get_user_info_async()  # Async
        return user_info
```

## Factory Function

Use the factory function for explicit control:

```python
from kinde_sdk import create_oauth_client

# Explicit sync client
oauth = create_oauth_client(async_mode=False, framework="flask", app=app)

# Explicit async client
oauth = create_oauth_client(async_mode=True, framework="fastapi", app=app)

# Smart client (default)
oauth = create_oauth_client(framework="fastapi", app=app)
```

## Migration Guide

### From Existing Sync Code

**Before:**
```python
from kinde_sdk import OAuth

oauth = OAuth(framework="flask", app=app)
user_info = oauth.get_user_info()  # This was inconsistent
```

**After (Option 1 - Keep Sync):**
```python
from kinde_sdk import OAuth

oauth = OAuth(framework="flask", app=app)
user_info = oauth.get_user_info()  # Still works
```

**After (Option 2 - Use Smart Client):**
```python
from kinde_sdk import SmartOAuth

oauth = SmartOAuth(framework="flask", app=app)
user_info = oauth.get_user_info()  # Works in sync context
```

### From Existing Async Code

**Before:**
```python
from kinde_sdk import OAuth

oauth = OAuth(framework="fastapi", app=app)
user_info = oauth.get_user_info()  # Sync method in async context!
```

**After (Option 1 - Use Async Client):**
```python
from kinde_sdk import AsyncOAuth

oauth = AsyncOAuth(framework="fastapi", app=app)
user_info = await oauth.get_user_info_async()  # Properly async
```

**After (Option 2 - Use Smart Client):**
```python
from kinde_sdk import SmartOAuth

oauth = SmartOAuth(framework="fastapi", app=app)
user_info = await oauth.get_user_info_async()  # Explicitly async
```

## Framework-Specific Examples

### Flask (Sync)
```python
from flask import Flask
from kinde_sdk import OAuth

app = Flask(__name__)
oauth = OAuth(framework="flask", app=app)

@app.route('/')
def home():
    if oauth.is_authenticated():
        user_info = oauth.get_user_info()
        return f"Welcome, {user_info['email']}!"
    return "Please login"
```

### FastAPI (Async)
```python
from fastapi import FastAPI
from kinde_sdk import AsyncOAuth

app = FastAPI()
oauth = AsyncOAuth(framework="fastapi", app=app)

@app.get('/')
async def home():
    if oauth.is_authenticated():
        user_info = await oauth.get_user_info_async()
        return {"message": f"Welcome, {user_info['email']}!"}
    return {"message": "Please login"}
```

### FastAPI with Smart Client
```python
from fastapi import FastAPI
from kinde_sdk import SmartOAuth

app = FastAPI()
oauth = SmartOAuth(framework="fastapi", app=app)

@app.get('/')
async def home():
    if oauth.is_authenticated():
        # Smart client warns about sync method in async context
        user_info = oauth.get_user_info()  # Warning shown
        # Better: use async version
        user_info = await oauth.get_user_info_async()
        return {"message": f"Welcome, {user_info['email']}!"}
    return {"message": "Please login"}
```

## Auth Modules

The auth modules (claims, permissions, roles, feature_flags) are already async:

```python
from kinde_sdk.auth import claims, permissions, roles, feature_flags

# All methods are async
user_claims = await claims.get_all_claims()
user_permissions = await permissions.get_permissions()
user_roles = await roles.get_roles()
user_flags = await feature_flags.get_all_flags()
```

## Best Practices

1. **Choose the Right Client**: Use `OAuth` for sync, `AsyncOAuth` for async, `SmartOAuth` for mixed
2. **Be Explicit**: Use `_async` suffix for async methods when using SmartOAuth
3. **Framework Consistency**: Use async clients with FastAPI, sync clients with Flask
4. **Error Handling**: Handle both sync and async exceptions appropriately
5. **Testing**: Test both sync and async paths in your applications

## Backward Compatibility

All existing code continues to work:
- `OAuth` class remains unchanged
- Existing sync methods remain sync
- Existing async methods remain async
- No breaking changes to the public API

## Future Roadmap

1. **Phase 1**: Add async methods alongside existing sync methods ✅
2. **Phase 2**: Add deprecation warnings for sync methods in async contexts ✅
3. **Phase 3**: Eventually deprecate sync methods in favor of explicit async/sync clients
4. **Phase 4**: Consider making all methods async by default in a major version

## Troubleshooting

### Common Issues

1. **"RuntimeError: no running event loop"**
   - Use sync client in sync context
   - Use async client in async context
   - Use SmartOAuth for mixed contexts

2. **"DeprecationWarning: Using sync method in async context"**
   - Use the `_async` version of the method
   - Or switch to `AsyncOAuth` client

3. **"AttributeError: 'OAuth' object has no attribute 'get_user_info_async'"**
   - Use `AsyncOAuth` or `SmartOAuth` for async methods
   - `OAuth` only has sync methods

### Getting Help

- Check the examples in `/examples` directory
- Review the test files in `/testv2` directory
- Open an issue on GitHub for bugs or feature requests
