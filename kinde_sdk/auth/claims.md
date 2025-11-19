# Kinde Python SDK Claims

The Kinde Python SDK provides a simple way to access user claims from your application. This guide shows you how to use the claims functionality to access user information and token claims.

## Basic Usage

First, import the claims module:

```python
from kinde_sdk.auth import claims
```

## Getting Individual Claims

To get a specific claim from the user's tokens, use the `get_claim` method:

```python
# Get the audience claim from the access token
claim = await claims.get_claim("aud")

if claim["value"]:
    print(f"Token audience: {claim['value']}")
else:
    print("No audience claim found or user not authenticated")
```

The `get_claim` method returns a dictionary with the following structure:
```python
{
    "name": "aud",                # The name of the claim
    "value": ["api.yourapp.com"]  # The value of the claim
}
```

You can also specify which token type to get the claim from:

```python
# Get the given_name claim from the ID token
claim = await claims.get_claim("given_name", token_type="id_token")

if claim["value"]:
    print(f"User's given name: {claim['value']}")
```

## Getting All Claims

To get all claims from the user's tokens, use the `get_all_claims` method:

```python
# Get all claims from the access token
all_claims = await claims.get_all_claims()

print("User claims:")
for claim_name, claim_value in all_claims.items():
    print(f"- {claim_name}: {claim_value}")

# Get all claims from the ID token
id_token_claims = await claims.get_all_claims(token_type="id_token")
```

## Practical Examples

### Example 1: Accessing User Information

```python
from kinde_sdk.auth import claims

async def get_user_profile():
    # Get user's name from ID token
    given_name = await claims.get_claim("given_name", token_type="id_token")
    family_name = await claims.get_claim("family_name", token_type="id_token")
    
    if given_name["value"] and family_name["value"]:
        return {
            "name": f"{given_name['value']} {family_name['value']}",
            "email": (await claims.get_claim("email", token_type="id_token"))["value"]
        }
    return None
```

### Example 2: Token Validation

```python
from fastapi import APIRouter, HTTPException
from kinde_sdk.auth import claims

router = APIRouter()

@router.get("/api/protected")
async def protected_endpoint():
    # Check if token is valid and has required audience
    aud_claim = await claims.get_claim("aud")
    
    if not aud_claim["value"] or "api.yourapp.com" not in aud_claim["value"]:
        raise HTTPException(
            status_code=401,
            detail="Invalid token audience"
        )
    
    # Token is valid, proceed with request
    return {"message": "Access granted"}
```

### Example 3: Organization Context

```python
from kinde_sdk.auth import claims

async def get_organization_context():
    # Get organization-related claims
    org_code = await claims.get_claim("org_code")
    org_name = await claims.get_claim("org_name")
    
    if org_code["value"]:
        return {
            "organization": {
                "code": org_code["value"],
                "name": org_name["value"]
            }
        }
    return None
```

## Error Handling

The claims module handles various edge cases:

1. If the user is not authenticated:
```python
claim = await claims.get_claim("aud")
# Returns: {"name": "aud", "value": None}
```

2. If the token manager is not available:
```python
claim = await claims.get_claim("aud")
# Returns: {"name": "aud", "value": None}
```

3. If the claim doesn't exist:
```python
claim = await claims.get_claim("non_existent_claim")
# Returns: {"name": "non_existent_claim", "value": None}
```

## Best Practices

1. Always use async/await when calling claim methods
2. Cache claim results if they're accessed frequently
3. Handle cases where claims might be missing or the user is not authenticated
4. Use appropriate token types (access_token vs id_token) for different claims
5. Validate critical claims before performing sensitive operations

## Common Claims

Here are some common claims you might want to access:

```python
# User Information (ID Token)
"given_name"
"family_name"
"email"
"picture"

# Token Information (Access Token)
"aud"           # Audience
"iss"           # Issuer
"exp"           # Expiration time
"iat"           # Issued at time

# Organization Information
"org_code"
"org_name"
"org_id"

# Custom Claims
"custom:role"
"custom:preferences"
"custom:settings"
```

## Token Types

The SDK supports two types of tokens:

1. Access Token (`token_type="access_token"`):
   - Contains authorization information
   - Used for API access
   - Contains permissions and organization context
   - Default token type

2. ID Token (`token_type="id_token"`):
   - Contains user identity information
   - Used for user profile data
   - Contains name, email, and other user details
   - Must be explicitly requested using `token_type="id_token"` 