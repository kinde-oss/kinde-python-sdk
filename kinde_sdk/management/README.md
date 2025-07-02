## Developer Documentation

### Architecture

The Management API module uses a dynamic method generation approach to create a clean, maintainable interface to the Kinde Management APIs.

```
kinde_sdk/management/
├── __init__.py                  # Exports ManagementClient and ManagementTokenManager
├── client.py                    # Dynamic API client 
└── management_token_manager.py  # Handles auth token management
```

### Token Management

The `ManagementTokenManager` uses a singleton pattern to efficiently manage token state:

```python
# Get a token, refreshing if necessary
token = token_manager.get_access_token()

# Request a new token (happens automatically when needed)
token = token_manager.request_new_token()
```

**Token Storage Format:**
```python
self.tokens = {
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6...",
    "expires_at": 1683921234,  # Unix timestamp
    "token_type": "Bearer"
}
```

### Dynamic Method Generation

The client dynamically creates methods for all API endpoints at initialization time:

```python
# Configuration of endpoints
API_ENDPOINTS = {
    'users': {
        'list': ('GET', '/users'),
        'get': ('GET', '/users/{user_id}'),
        # ...
    },
    # ...
}

# Method generation (simplified)
for resource, endpoints in self.API_ENDPOINTS.items():
    for action, (method, path) in endpoints.items():
        method_name = get_method_name(action, resource)
        setattr(self, method_name, create_method(method, path))
```

### API Method Naming Convention

| API Action | HTTP Method | Path Pattern | Generated Method |
|------------|-------------|--------------|------------------|
| List       | GET         | `/resource`  | `get_resources()`|
| Get        | GET         | `/resource/{id}` | `get_resource(id)` |
| Create     | POST        | `/resource`  | `create_resource(**data)` |
| Update     | PATCH       | `/resource/{id}` | `update_resource(id, **data)` |
| Delete     | DELETE      | `/resource/{id}` | `delete_resource(id)` |

### Request Processing

1. Path parameters: Filled from positional arguments
2. Query params: Used for GET/DELETE methods from keyword arguments
3. Body data: Used for POST/PATCH/PUT methods from keyword arguments

```python
# Request handling (simplified)
def api_method(*args, **kwargs):
    # Format path with path parameters
    formatted_path = format_path(path, args)
    
    # Prepare query params or body based on HTTP method
    if http_method in ('GET', 'DELETE'):
        query_params = kwargs
        body = None
    else:
        query_params = None
        body = kwargs
        
    # Make the API call
    return self.api_client.call_api(
        formatted_path, http_method,
        query_params=query_params,
        body=body
    )
```

### Extending the API

To add support for new API endpoints, simply add them to the `API_ENDPOINTS` dictionary:

```python
# Add a new resource
API_ENDPOINTS['new_resource'] = {
    'list': ('GET', '/new_resource'),
    'get': ('GET', '/new_resource/{id}'),
    'create': ('POST', '/new_resource'),
    'update': ('PATCH', '/new_resource/{id}'),
    'delete': ('DELETE', '/new_resource/{id}'),
}
```

No additional code is required - methods are generated automatically.

### Thread Safety

- Token manager uses locks to ensure thread safety
- Multiple threads can share the same client instance
- Token refresh operations are atomic

### Integration Pattern

The Management API integrates with the existing API client using lazy initialization:

```python
def get_management(self):
    """Get management client, initializing if needed."""
    if self._management is None:
        self._management = ManagementClient(
            domain=self.domain,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
    return self._management
```

### Error Handling

Errors from the API are passed through to the caller:

```python
try:
    user = management.get_user(user_id)
except Exception as e:
    # Handle API-specific errors here
    logger.error(f"API error: {e}")
```

### Testing Considerations

For unit testing the client:

1. Mock the `ApiClient.call_api` method
2. Clear token cache between tests with `ManagementTokenManager.reset_instances()`
3. Inject test tokens by directly setting `token_manager.tokens`

### Contribution Guidelines

When contributing to the Management API module:

1. Maintain the dynamic method approach
2. Add new endpoints to the `API_ENDPOINTS` dictionary
3. Add tests for new endpoints
4. Update documentation for any public API changes