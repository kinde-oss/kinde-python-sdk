# Route Protection Feature

The Kinde Python SDK now includes comprehensive route protection capabilities that allow you to secure your web application routes based on user roles and permissions. This feature provides declarative, configuration-driven access control that integrates seamlessly with your existing Kinde authentication setup.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Framework Integration](#framework-integration)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

### Features

- **Role-based Access Control**: Protect routes based on user roles (admin, manager, user, etc.)
- **Permission-based Access Control**: Fine-grained control using specific permissions
- **Framework Agnostic**: Works with Flask, FastAPI, and other Python web frameworks
- **Pattern Matching**: Support for wildcard patterns (`/admin/*`) and exact matches
- **Method-specific Protection**: Different rules for GET, POST, PUT, DELETE, etc.
- **Public Routes**: Designate routes that require no authentication
- **Declarative Configuration**: Define rules in YAML/JSON files
- **Automatic Middleware**: Optional automatic route protection before request handlers
- **Graceful Fallback**: Continues to work even if route protection is not configured

### How It Works

1. **Configuration**: Define route protection rules in a YAML/JSON file
2. **Integration**: Initialize OAuth with route protection enabled
3. **Automatic Protection**: Middleware automatically checks routes before handlers execute
4. **Manual Validation**: Optionally validate routes programmatically in your code
5. **Access Control**: Users are granted/denied access based on their roles and permissions

## Quick Start

### 1. Install Dependencies

The route protection feature is built into the Kinde Python SDK - no additional packages required.

```bash
pip install kinde-python-sdk
```

### 2. Create Configuration File

Create a `routes.yaml` file with your protection rules:

```yaml
# routes.yaml
settings:
  default_allow: false  # Secure by default
  
routes:
  admin_routes:
    path: "/admin/*"
    methods: ["GET", "POST", "PUT", "DELETE"]
    roles: ["admin"]
    
  user_profile:
    path: "/profile/*" 
    methods: ["GET", "POST"]
    roles: ["user", "manager", "admin"]
    
  public_content:
    path: "/public/*"
    methods: ["GET"]
    public: true
```

### 3. Enable in Your Application

#### Flask Example

```python
from flask import Flask
from kinde_sdk.auth import OAuth

app = Flask(__name__)

# Enable route protection with your configuration file
oauth = OAuth(
    framework="flask",
    app=app,
    route_protection_file="routes.yaml"  # Enable protection
)

# Routes are automatically protected based on your configuration
@app.route('/admin/dashboard')
def admin_dashboard():
    return "Admin Dashboard - Only visible to admins!"

@app.route('/profile/settings')  
def profile_settings():
    return "Profile Settings - Visible to authenticated users!"

if __name__ == '__main__':
    app.run()
```

#### FastAPI Example

```python
from fastapi import FastAPI
from kinde_sdk.auth import OAuth

app = FastAPI()

# Enable route protection
oauth = OAuth(
    framework="fastapi", 
    app=app,
    route_protection_file="routes.yaml"
)

@app.get("/admin/dashboard")
async def admin_dashboard():
    return {"message": "Admin Dashboard - Only visible to admins!"}

@app.get("/profile/settings")
async def profile_settings():
    return {"message": "Profile Settings - Visible to authenticated users!"}
```

### 4. Test Your Protection

1. **Start your application**
2. **Try accessing protected routes** without authentication → Should get 403 Forbidden
3. **Login with different user roles** → Should see appropriate access granted/denied
4. **Check logs** for detailed information about access decisions

## Configuration

### Configuration File Format

Route protection uses YAML or JSON configuration files with the following structure:

```yaml
# Global settings
settings:
  default_allow: false    # true = allow by default, false = deny by default
  
# Route protection rules  
routes:
  rule_name:              # Arbitrary name for the rule
    path: "/route/path"   # Route pattern to match
    methods: ["GET"]      # HTTP methods (optional, defaults to ["GET"])
    roles: ["admin"]      # Required roles (optional)
    permissions: ["read:users"]  # Required permissions (optional)  
    public: false         # Set to true for public routes (optional)
```

### Path Patterns

The route protection engine supports several path matching patterns:

| Pattern | Description | Examples |
|---------|-------------|----------|
| `/admin` | Exact match | Matches only `/admin` |
| `/admin/*` | Wildcard match | Matches `/admin/users`, `/admin/settings/view`, etc. (does not match `/admin` or `/adminXYZ`) |
| `/api/v1/*` | Prefix wildcard | Matches `/api/v1/users`, `/api/v1/organizations`, etc. |

### Access Control Logic

- **Public Routes**: `public: true` allows access without authentication
- **Role-based**: User must have ANY of the specified roles (OR logic)
- **Permission-based**: User must have ANY of the specified permissions (OR logic)  
- **Combined**: If both roles AND permissions are specified, user must have BOTH (AND logic)
- **No Rules**: Falls back to `default_allow` setting

### Example Configuration

```yaml
settings:
  default_allow: false

routes:
  # Admin-only section
  admin_panel:
    path: "/admin/*"
    methods: ["GET", "POST", "PUT", "DELETE"]
    roles: ["admin"]
    
  # Manager or admin can manage users
  user_management:
    path: "/manage/users/*"
    methods: ["POST", "PUT", "DELETE"]
    roles: ["manager", "admin"]
    
  # Any authenticated user can view their profile
  user_profile:
    path: "/profile/*"
    methods: ["GET", "POST"]
    roles: ["user", "manager", "admin"]
    
  # Permission-based API access
  users_api:
    path: "/api/users"
    methods: ["GET"]
    permissions: ["read:users"]
    
  # Combined role and permission requirement
  advanced_reports:
    path: "/reports/advanced/*"
    methods: ["GET"]
    roles: ["manager", "admin"]      # Must be manager or admin
    permissions: ["read:reports"]    # AND have reports permission
    
  # Public routes
  documentation:
    path: "/docs/*"
    methods: ["GET"]
    public: true
    
  health_check:
    path: "/health"
    methods: ["GET"]
    public: true
```

## Framework Integration

### Flask Integration

#### Automatic Protection (Recommended)

```python
from flask import Flask
from kinde_sdk.auth import OAuth

app = Flask(__name__)

# OAuth with route protection
oauth = OAuth(
    framework="flask",
    app=app,
    route_protection_file="routes.yaml"
)

# Routes are automatically protected - no additional code needed!
@app.route('/admin/dashboard')
def admin_dashboard():
    return "Protected content!"
```

#### Manual Protection

```python
from flask import Flask, request
from kinde_sdk.auth import OAuth
import asyncio

app = Flask(__name__)
oauth = OAuth(framework="flask", app=app, route_protection_file="routes.yaml")

@app.before_request
def check_access():
    if oauth.is_route_protection_enabled():
        # Check if current route is protected
        result = asyncio.run(oauth.validate_route_access(request.path, request.method))
        if not result["allowed"]:
            return {"error": "Access Denied"}, 403
    return None
```

#### Custom Middleware

```python
from kinde_sdk.auth.route_middleware import FlaskRouteProtectionMiddleware

# Create custom middleware
middleware = FlaskRouteProtectionMiddleware(
    oauth,
    skip_patterns=["/health", "/metrics"]  # Skip certain routes
)

# Apply to Flask app
app.before_request(middleware.before_request)
```

### FastAPI Integration

#### Automatic Protection (Recommended)

```python
from fastapi import FastAPI
from kinde_sdk.auth import OAuth

app = FastAPI()

# OAuth with route protection
oauth = OAuth(
    framework="fastapi",
    app=app,
    route_protection_file="routes.yaml"
)

# Routes are automatically protected
@app.get("/admin/dashboard")
async def admin_dashboard():
    return {"message": "Protected content!"}
```

#### Custom Middleware

```python
from kinde_sdk.auth.route_middleware import FastAPIRouteProtectionMiddleware

app.add_middleware(
    FastAPIRouteProtectionMiddleware,
    oauth_client=oauth,
    skip_patterns=["/docs", "/openapi.json", "/health"]
)
```

#### Manual Protection

```python
from fastapi import FastAPI, Request, HTTPException
from kinde_sdk.auth import OAuth

app = FastAPI()
oauth = OAuth(framework="fastapi", app=app, route_protection_file="routes.yaml")

@app.middleware("http") 
async def route_protection_middleware(request: Request, call_next):
    if oauth.is_route_protection_enabled():
        result = await oauth.validate_route_access(str(request.url.path), request.method)
        if not result["allowed"]:
            raise HTTPException(status_code=403, detail="Access Denied")
    
    response = await call_next(request)
    return response
```

## API Reference

### OAuth Class

#### Constructor

```python
OAuth(
    framework: str,
    app: Any,
    route_protection_file: Optional[str] = None,
    # ... other parameters
)
```

**Parameters:**
- `route_protection_file`: Path to YAML/JSON configuration file

#### Methods

##### `is_route_protection_enabled() -> bool`

Check if route protection is configured and enabled.

```python
if oauth.is_route_protection_enabled():
    print("Route protection is active")
```

##### `async validate_route_access(path: str, method: str = "GET") -> Dict[str, Any]`

Validate access to a specific route.

```python
result = await oauth.validate_route_access("/admin/users", "GET")
if result["allowed"]:
    print(f"Access granted: {result['reason']}")
else:
    print(f"Access denied: {result['reason']}")
    print(f"Required roles: {result['required_roles']}")
```

**Returns:**
```python
{
    "allowed": bool,                    # Whether access is granted
    "reason": str,                     # Human-readable reason
    "required_roles": List[str],       # Required roles (if any)
    "required_permissions": List[str], # Required permissions (if any)
    "matched_rule": str               # Name of matched rule (if any)
}
```

##### `check_route_access(path: str, method: str = "GET") -> bool`

Synchronous convenience method for route access checking.

```python
oauth_client = OAuth(framework="flask", app=app)
if oauth_client.check_route_access("/admin/users", "GET"):
    print("Access granted")
else:
    print("Access denied")
```

##### `get_route_protection_info() -> Optional[Dict[str, Any]]`

Get summary of all configured route protection rules.

```python
oauth_client = OAuth(framework="flask", app=app)
info = oauth_client.get_route_protection_info()
if info:
    print(f"Total protected routes: {info['total_routes']}")
    for route in info['routes']:
        print(f"- {route['path']} ({route['methods']}) -> {route['roles']}")
```

##### `get_route_info(path: str, method: str = "GET") -> Optional[Dict[str, Any]]`

Get protection info for a specific route.

```python
route_info = oauth.get_route_info("/admin/users", "GET")
if route_info:
    print(f"Rule: {route_info['rule_name']}")
    print(f"Required roles: {route_info['required_roles']}")
    print(f"Is public: {route_info['is_public']}")
```

### RouteProtectionEngine Class

#### Constructor

```python
from kinde_sdk.auth import RouteProtectionEngine

engine = RouteProtectionEngine("routes.yaml")
```

#### Methods

##### `async validate_route_access(path: str, method: str, options: Optional[ApiOptions] = None) -> Dict[str, Any]`

Core validation method (same return format as OAuth.validate_route_access).

##### `list_protected_routes() -> Dict[str, Any]`

Get summary of all configured routes.

##### `get_route_info(path: str, method: str) -> Optional[Dict[str, Any]]`

Get information about a specific route's protection rules.

### Middleware Classes

#### FlaskRouteProtectionMiddleware

```python
from kinde_sdk.auth.route_middleware import FlaskRouteProtectionMiddleware

middleware = FlaskRouteProtectionMiddleware(
    oauth_client=oauth,
    skip_patterns=["/health", "/static/*"],  # Optional: routes to skip
    error_handler=custom_error_handler       # Optional: custom error handler
)

app.before_request(middleware.before_request)
```

#### FastAPIRouteProtectionMiddleware

```python
from kinde_sdk.auth.route_middleware import FastAPIRouteProtectionMiddleware

app.add_middleware(
    FastAPIRouteProtectionMiddleware,
    oauth_client=oauth,
    skip_patterns=["/docs", "/openapi.json"]
)
```

## Examples

### Basic Admin Protection

```yaml
# routes.yaml
settings:
  default_allow: true  # Allow by default for development

routes:
  admin_only:
    path: "/admin/*"
    methods: ["GET", "POST", "PUT", "DELETE"]
    roles: ["admin"]
```

```python
# app.py
from flask import Flask
from kinde_sdk.auth import OAuth

app = Flask(__name__)
oauth = OAuth(framework="flask", app=app, route_protection_file="routes.yaml")

@app.route('/admin/dashboard')
def admin_dashboard():
    return "Welcome to the admin dashboard!"

@app.route('/public')  
def public_page():
    return "This page is accessible to everyone!"
```

### Multi-tier Access Control

```yaml
# routes.yaml
settings:
  default_allow: false

routes:
  # Three-tier access: admin > manager > user
  admin_functions:
    path: "/admin/*"
    roles: ["admin"]
    
  management_functions:
    path: "/manage/*" 
    roles: ["manager", "admin"]
    
  user_functions:
    path: "/dashboard/*"
    roles: ["user", "manager", "admin"]
    
  # Permission-based API
  read_users:
    path: "/api/users"
    methods: ["GET"]
    permissions: ["read:users"]
    
  write_users:
    path: "/api/users"
    methods: ["POST", "PUT", "DELETE"]
    permissions: ["write:users"]
```

### Method-specific Protection

```yaml
# routes.yaml
routes:
  # Anyone can read user profiles
  user_profiles_read:
    path: "/users/*"
    methods: ["GET"]
    roles: ["user", "manager", "admin"]
    
  # Only managers/admins can modify profiles
  user_profiles_write:
    path: "/users/*"
    methods: ["POST", "PUT", "DELETE"]
    roles: ["manager", "admin"]
```

### Public and Protected Mixed

```yaml
# routes.yaml
settings:
  default_allow: false

routes:
  # Public documentation
  docs:
    path: "/docs/*"
    public: true
    
  # Public API info  
  api_info:
    path: "/api/info"
    methods: ["GET"]
    public: true
    
  # Protected API endpoints
  api_data:
    path: "/api/data/*"
    permissions: ["read:api"]
    
  # Health checks (public)
  health:
    path: "/health"
    public: true
```

### Combined Roles and Permissions

```yaml
# routes.yaml
routes:
  # Must be manager AND have reports permission
  advanced_reporting:
    path: "/reports/advanced/*"
    roles: ["manager", "admin"]
    permissions: ["read:advanced_reports"]
    
  # Must be admin AND have system permission  
  system_management:
    path: "/system/*"
    roles: ["admin"]
    permissions: ["manage:system"]
```

## Best Practices

### Security Best Practices

1. **Use `default_allow: false`** in production for security by default
2. **Be specific with path patterns** - avoid overly broad wildcards
3. **Use least-privilege principle** - grant minimum necessary access
4. **Regularly audit your route configurations** for unused or overly permissive rules
5. **Test route protection thoroughly** with different user roles

### Configuration Best Practices

1. **Organize rules logically** - group related routes together
2. **Use descriptive rule names** that explain their purpose
3. **Document your access control decisions** in comments
4. **Version control your configuration files** alongside your application code
5. **Use environment-specific configurations** for dev/staging/production

### Performance Best Practices

1. **Place more specific patterns first** in your configuration file
2. **Use `skip_patterns` in middleware** for frequently accessed public routes
3. **Consider caching** for high-traffic applications (future feature)
4. **Monitor route protection performance** in production

### Development Best Practices

1. **Start with `default_allow: true`** during development for easier testing
2. **Use comprehensive logging** to debug access control decisions
3. **Create test users with different roles** to verify your protection rules
4. **Set up automated tests** for your route protection scenarios

### Configuration Organization

```yaml
# Good: Organized by application section
settings:
  default_allow: false

routes:
  # === ADMIN SECTION ===
  admin_dashboard:
    path: "/admin/*"
    roles: ["admin"]
    
  # === USER MANAGEMENT ===
  user_profiles:
    path: "/users/*"
    methods: ["GET"]
    roles: ["user", "manager", "admin"]
    
  user_admin:
    path: "/users/*"
    methods: ["POST", "PUT", "DELETE"]
    roles: ["admin"]
    
  # === API ENDPOINTS ===
  api_read:
    path: "/api/*"
    methods: ["GET"]
    permissions: ["read:api"]
    
  api_write:
    path: "/api/*"
    methods: ["POST", "PUT", "DELETE"]
    permissions: ["write:api"]
    
  # === PUBLIC ROUTES ===
  public_content:
    path: "/public/*"
    public: true
```

## Troubleshooting

### Common Issues

#### 1. Route Protection Not Working

**Symptoms:**
- Routes that should be protected are accessible to everyone
- No access control being applied

**Solutions:**
```python
# Check if route protection is enabled
if oauth.is_route_protection_enabled():
    print("Route protection is active")
else:
    print("Route protection is not configured")
    
# Check your configuration file path
oauth = OAuth(
    framework="flask",
    app=app,
    route_protection_file="/full/path/to/routes.yaml"  # Use absolute path
)

# Check configuration file syntax
import yaml
with open("routes.yaml", "r") as file:
    config = yaml.safe_load(file)
    print("Configuration loaded successfully:", config)
```

#### 2. Getting 403 Forbidden Unexpectedly

**Symptoms:**
- Users with correct roles still getting denied access
- Routes that should be accessible are blocked

**Solutions:**
```python
# Debug route access decisions
result = await oauth.validate_route_access("/your/route", "GET")
print(f"Access allowed: {result['allowed']}")
print(f"Reason: {result['reason']}")
print(f"Required roles: {result['required_roles']}")
print(f"Required permissions: {result['required_permissions']}")
print(f"Matched rule: {result['matched_rule']}")

# Check user's actual roles
from kinde_sdk.auth import Roles
roles_client = Roles()
user_roles = await roles_client.get_roles()
print(f"User roles: {user_roles}")
```

#### 3. Configuration File Not Found

**Symptoms:**
- Error messages about missing configuration file
- Route protection not initializing

**Solutions:**
```python
import os

# Check if file exists
config_path = "routes.yaml"
if os.path.exists(config_path):
    print(f"Configuration file found: {os.path.abspath(config_path)}")
else:
    print(f"Configuration file NOT found: {os.path.abspath(config_path)}")

# Use absolute path
oauth = OAuth(
    framework="flask",
    app=app,
    route_protection_file=os.path.join(os.path.dirname(__file__), "routes.yaml")
)
```

#### 4. Roles/Permissions Not Found in Token

**Symptoms:**
- Users have roles in Kinde admin but route protection doesn't see them
- Empty roles/permissions being returned

**Solutions:**
1. **Check Kinde Admin Panel:**
   - Applications → Your App → Token customization
   - Ensure "Include roles in tokens" is enabled
   - Ensure "Include permissions in tokens" is enabled

2. **Force API calls instead of token claims:**
```python
# Enable force_api to fetch fresh data from API
oauth = OAuth(
    framework="flask",
    app=app,
    route_protection_file="routes.yaml",
    force_api=True  # This will fetch roles/permissions from API instead of token
)
```

3. **Debug token contents:**
```python
# Check what's actually in the user's token
user = oauth.get_user_info()
print(f"User token claims: {user}")

# Check token manager
token_manager = oauth._get_token_manager()
if token_manager:
    claims = token_manager.get_claims()
    print(f"Full token claims: {claims}")
```

#### 5. Pattern Matching Issues

**Symptoms:**
- Route patterns not matching expected paths
- Wildcard patterns not working correctly

**Solutions:**
```yaml
# Correct pattern usage:
routes:
  # Good: Matches /admin/users, /admin/settings, etc.
  admin_routes:
    path: "/admin/*"
    roles: ["admin"]
    
  # Good: Exact match
  specific_route:
    path: "/admin/users"
    roles: ["admin"]
    
  # Bad: This won't match subdirectories
  # admin_routes:
  #   path: "/admin*"  # Missing slash
```

```python
# Test pattern matching
route_info = oauth.get_route_info("/admin/users", "GET")
if route_info:
    print(f"Route matched rule: {route_info['rule_name']}")
    print(f"Pattern: {route_info['path_pattern']}")
else:
    print("No route protection rule matched this path")
```

### Debugging Tools

#### Enable Debug Logging

```python
import logging

# Enable debug logging for route protection
logging.getLogger("kinde_sdk.route_protection").setLevel(logging.DEBUG)
logging.getLogger("kinde_sdk.route_middleware").setLevel(logging.DEBUG)

# Add console handler to see logs
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
logging.getLogger("kinde_sdk").addHandler(handler)
```

#### Configuration Validation

```python
# Validate your configuration file
from kinde_sdk.auth import RouteProtectionEngine

try:
    engine = RouteProtectionEngine("routes.yaml")
    info = engine.list_protected_routes()
    print(f"Successfully loaded {info['total_routes']} route rules:")
    for route in info['routes']:
        print(f"  - {route['name']}: {route['path']} -> {route['roles'] or route['permissions']}")
except Exception as e:
    print(f"Configuration error: {e}")
```

#### Manual Route Testing

```python
# Test specific routes manually
test_routes = [
    ("/admin/dashboard", "GET"),
    ("/user/profile", "GET"),
    ("/api/users", "POST"),
    ("/public/info", "GET")
]

for path, method in test_routes:
    result = await oauth.validate_route_access(path, method)
    status = "✅ ALLOWED" if result["allowed"] else "❌ DENIED"
    print(f"{status} {method} {path} - {result['reason']}")
```

### Getting Help

If you continue to experience issues:

1. **Check the logs** for detailed error messages and debugging information
2. **Verify your Kinde configuration** in the admin panel (roles, permissions, token settings)
3. **Test with simple configurations** first, then add complexity
4. **Create minimal reproduction cases** to isolate the problem
5. **Review the examples** in this documentation for reference implementations

For additional support, please refer to the Kinde documentation or contact support with:
- Your configuration file
- Debug logs showing the issue
- Steps to reproduce the problem
- Expected vs actual behavior
