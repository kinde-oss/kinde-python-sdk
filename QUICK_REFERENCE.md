# Kinde Python SDK v2 Quick Reference

## Quick Migration Guide

### ❌ v1 (Old) → ✅ v2 (New)

| v1 (Old) | v2 (New) | Purpose |
|----------|----------|---------|
| `from kinde_sdk import KindeClient` | `from kinde_sdk import OAuth` | User authentication |
| `client = KindeClient(...)` | `oauth = OAuth(framework="flask", app=app)` | Initialize client |
| `client.get_flag(...)` | `await feature_flags.get_flag(...)` | Feature flags |
| `client.get_permission(...)` | `await permissions.get_permission(...)` | Permissions |
| `client.get_claim(...)` | `await claims.get_claim(...)` | User claims |
| `client.get_token()` | `tokens.get_token_manager()` | Token access |

## Common Import Patterns

### For User Authentication (Most Common)
```python
from kinde_sdk import OAuth

# Initialize
oauth = OAuth(
    framework="flask",  # or "fastapi"
    app=app
)

# Check authentication
if oauth.is_authenticated():
    user = oauth.get_user_info()
```

### For Feature Flags, Permissions, Claims
```python
from kinde_sdk.auth import feature_flags, permissions, claims

# Feature flags
flags = await feature_flags.get_all_flags()
flag = await feature_flags.get_flag("flag_name")

# Permissions
perms = await permissions.get_permissions()
has_perm = await permissions.check("permission_name")

# Claims
user_claims = await claims.get_all_claims()
claim = await claims.get_claim("claim_name")
```

### For Management Operations (Admin/Backend)
```python
from kinde_sdk.management import ManagementClient

# Initialize
client = ManagementClient(
    domain="your-domain.kinde.com",
    client_id="your_client_id",
    client_secret="your_client_secret"
)

# Use
users = client.get_users()
organizations = client.get_organizations()
```

## Framework-Specific Examples

### Flask
```python
from flask import Flask
from kinde_sdk import OAuth

app = Flask(__name__)
oauth = OAuth(framework="flask", app=app)

@app.route("/")
def home():
    if oauth.is_authenticated():
        return f"Hello, {oauth.get_user_info()['email']}!"
    return "Please login"
```

### FastAPI
```python
from fastapi import FastAPI
from kinde_sdk import OAuth
from kinde_sdk.auth import feature_flags

app = FastAPI()
oauth = OAuth(framework="fastapi", app=app)

@app.get("/")
async def home():
    if oauth.is_authenticated():
        flags = await feature_flags.get_all_flags()
        return {"user": oauth.get_user_info(), "flags": flags}
    return {"message": "Please login"}
```

## Common Error Solutions

| Error | Solution |
|-------|----------|
| `ImportError: cannot import name 'KindeClient'` | Use `from kinde_sdk import OAuth` |
| `AttributeError: 'OAuth' object has no attribute 'get_flag'` | Use `from kinde_sdk.auth import feature_flags` |
| `ModuleNotFoundError: No module named 'kinde_sdk.auth'` | Install v2: `pip install kinde-python-sdk>=2.0.0` |
| `TypeError: 'OAuth' object is not callable` | Pass framework and app: `OAuth(framework="flask", app=app)` |

## Key Differences Summary

1. **`KindeClient` → `OAuth`**: Main authentication class renamed
2. **Method calls → Module calls**: `client.get_flag()` → `await feature_flags.get_flag()`
3. **Synchronous → Asynchronous**: Most operations now use `await`
4. **Framework-specific**: Must specify framework when initializing
5. **Separated concerns**: Authentication vs Management operations split into different classes 