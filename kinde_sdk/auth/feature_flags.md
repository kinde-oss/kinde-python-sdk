# Kinde Python SDK Feature Flags

The Kinde Python SDK provides a simple way to access feature flags from your application. Feature flags are stored in the user's access token and can be used to control feature access and configuration.

## Basic Usage

First, import the feature flags module:

```python
from kinde_sdk.auth import feature_flags
```

## Getting Individual Feature Flags

To get a specific feature flag value, use the `get_flag` method:

```python
# Get a string feature flag
theme_flag = await feature_flags.get_flag("theme")
if theme_flag.value:
    print(f"Current theme: {theme_flag.value}")

# Get a boolean feature flag with default value
dark_mode = await feature_flags.get_flag("is_dark_mode", default_value=False)
if dark_mode.value:
    print("Dark mode is enabled")

# Get a numeric feature flag
competitions_limit = await feature_flags.get_flag("competitions_limit")
if competitions_limit.value:
    print(f"User can create up to {competitions_limit.value} competitions")
```

The `get_flag` method returns a `FeatureFlag` object with the following structure:
```python
{
    "code": "theme",           # The feature flag code
    "type": "string",          # The type of the value (string, boolean, integer)
    "value": "pink",           # The actual value
    "is_default": False        # Whether the default value was used
}
```

## Getting All Feature Flags

To get all feature flags for the current user, use the `get_all_flags` method:

```python
# Get all feature flags
all_flags = await feature_flags.get_all_flags()

print("User feature flags:")
for code, flag in all_flags.items():
    print(f"- {code}: {flag.value} ({flag.type})")
```

## Practical Examples

### Example 1: Conditional Feature Rendering

```python
from kinde_sdk.auth import feature_flags

async def render_create_competition_button():
    # Check if user has access to create competitions
    can_create = await feature_flags.get_flag("create_competition", default_value=False)
    
    if can_create.value:
        return """
        <button class="create-competition-btn">Create Competition</button>
        """
    return None
```

### Example 2: Theme Configuration

```python
from kinde_sdk.auth import feature_flags

async def get_user_theme():
    # Get theme and dark mode settings
    theme = await feature_flags.get_flag("theme", default_value="light")
    dark_mode = await feature_flags.get_flag("is_dark_mode", default_value=False)
    
    return {
        "theme": theme.value,
        "is_dark_mode": dark_mode.value
    }
```

### Example 3: Feature Limits

```python
from fastapi import APIRouter, HTTPException
from kinde_sdk.auth import feature_flags

router = APIRouter()

@router.post("/competitions")
async def create_competition(competition_data: dict):
    # Check competition limit
    limit_flag = await feature_flags.get_flag("competitions_limit", default_value=3)
    current_count = await get_user_competition_count()  # Your implementation
    
    if current_count >= limit_flag.value:
        raise HTTPException(
            status_code=403,
            detail=f"Competition limit reached (max: {limit_flag.value})"
        )
    
    # Create competition
    # ... your implementation ...
    return {"message": "Competition created successfully"}
```

## Error Handling

The feature flags module handles various edge cases:

1. If the user is not authenticated:
```python
flag = await feature_flags.get_flag("theme", default_value="light")
# Returns: FeatureFlag(code="theme", type="unknown", value="light", is_default=True)
```

2. If the token manager is not available:
```python
flag = await feature_flags.get_flag("theme", default_value="light")
# Returns: FeatureFlag(code="theme", type="unknown", value="light", is_default=True)
```

3. If the feature flag doesn't exist:
```python
flag = await feature_flags.get_flag("non_existent_flag", default_value=False)
# Returns: FeatureFlag(code="non_existent_flag", type="unknown", value=False, is_default=True)
```

## Best Practices

1. Always use async/await when calling feature flag methods
2. Provide default values for critical feature flags
3. Cache feature flag results if they're accessed frequently
4. Handle cases where feature flags might be missing
5. Use type hints to ensure correct value types

## Feature Flag Types

The SDK supports the following feature flag types:

1. String (`"s"`):
   ```python
   {
       "t": "s",
       "v": "pink"
   }
   ```

2. Boolean (`"b"`):
   ```python
   {
       "t": "b",
       "v": true
   }
   ```

3. Integer (`"i"`):
   ```python
   {
       "t": "i",
       "v": 5
   }
   ```

## Common Use Cases

1. Feature Toggles:
   ```python
   can_use_feature = await feature_flags.get_flag("enable_new_feature", default_value=False)
   if can_use_feature.value:
       # Enable new feature
   ```

2. User Preferences:
   ```python
   theme = await feature_flags.get_flag("theme", default_value="light")
   dark_mode = await feature_flags.get_flag("is_dark_mode", default_value=False)
   ```

3. Usage Limits:
   ```python
   max_uploads = await feature_flags.get_flag("max_uploads", default_value=10)
   if current_uploads < max_uploads.value:
       # Allow upload
   ```

4. A/B Testing:
   ```python
   test_group = await feature_flags.get_flag("ab_test_group", default_value="control")
   if test_group.value == "variant":
       # Show variant
   ``` 