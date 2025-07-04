# Kinde Python SDK Permissions

The Kinde Python SDK provides a simple way to check user permissions in your application. This guide shows you how to use the permissions functionality to control access to features and resources.

## Basic Usage

First, import the permissions module:

```python
from kinde_sdk.auth import permissions
```

## Checking Individual Permissions

To check if a user has a specific permission, use the `get_permission` method:

```python
# Check if user has permission to create todos
permission = await permissions.get_permission("create:todos")

if permission["isGranted"]:
    # User has permission to create todos
    print(f"User has permission to create todos in organization: {permission['orgCode']}")
else:
    # User does not have permission
    print("User does not have permission to create todos")
```

The `get_permission` method returns a dictionary with the following structure:
```python
{
    "permissionKey": "create:todos",  # The permission that was checked
    "orgCode": "org_1234",           # The organization code (if applicable)
    "isGranted": True                # Whether the user has the permission
}
```

## Getting All Permissions

To get all permissions for the current user, use the `get_permissions` method:

```python
# Get all permissions for the current user
all_permissions = await permissions.get_permissions()

print(f"User belongs to organization: {all_permissions['orgCode']}")
print("User has the following permissions:")
for permission in all_permissions["permissions"]:
    print(f"- {permission}")
```

The `get_permissions` method returns a dictionary with the following structure:
```python
{
    "orgCode": "org_1234",                    # The organization code (if applicable)
    "permissions": [                          # List of all permissions
        "create:todos",
        "update:todos",
        "read:todos",
        "delete:todos"
    ]
}
```

## Practical Examples

### Example 1: Conditional Feature Access

```python
from kinde_sdk.auth import permissions

async def create_todo_button():
    permission = await permissions.get_permission("create:todos")
    
    if permission["isGranted"]:
        return """
        <button onclick="createTodo()">Create Todo</button>
        """
    return None
```

### Example 2: Permission-Based API Endpoint

```python
from fastapi import APIRouter, HTTPException
from kinde_sdk.auth import permissions

router = APIRouter()

@router.post("/todos")
async def create_todo(todo_data: dict):
    # Check if user has permission to create todos
    permission = await permissions.get_permission("create:todos")
    
    if not permission["isGranted"]:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to create todos"
        )
    
    # User has permission, proceed with creating todo
    # ... create todo logic ...
    return {"message": "Todo created successfully"}
```

### Example 3: Organization-Specific Permissions

```python
from kinde_sdk.auth import permissions

async def get_organization_todos(org_code: str):
    # Get all permissions
    all_permissions = await permissions.get_permissions()
    
    # Check if user belongs to the specified organization
    if all_permissions["orgCode"] != org_code:
        raise ValueError("User does not belong to this organization")
    
    # Check if user has permission to read todos
    if "read:todos" not in all_permissions["permissions"]:
        raise ValueError("User does not have permission to read todos")
    
    # User has permission, proceed with fetching todos
    # ... fetch todos logic ...
    return todos
```

## Error Handling

The permissions module handles various edge cases:

1. If the user is not authenticated:
```python
permission = await permissions.get_permission("create:todos")
# Returns: {"permissionKey": "create:todos", "orgCode": None, "isGranted": False}
```

2. If the token manager is not available:
```python
permission = await permissions.get_permission("create:todos")
# Returns: {"permissionKey": "create:todos", "orgCode": None, "isGranted": False}
```

3. If no permissions are found in the claims:
```python
all_permissions = await permissions.get_permissions()
# Returns: {"orgCode": None, "permissions": []}
```

## Best Practices

1. Always use async/await when calling permission methods
2. Check permissions before performing sensitive operations
3. Cache permission results if they're checked frequently
4. Use descriptive permission keys (e.g., "create:todos" instead of just "create")
5. Handle cases where permissions might be missing or the user is not authenticated

## Common Permission Patterns

Here are some common permission patterns you might want to use:

```python
# Resource-based permissions
"create:todos"
"read:todos"
"update:todos"
"delete:todos"

# Feature-based permissions
"can:export_data"
"can:manage_users"
"can:view_analytics"

# Organization-based permissions
"org:manage_members"
"org:view_billing"
"org:update_settings"
``` 