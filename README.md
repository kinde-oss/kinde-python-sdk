# Kinde Python SDK

The Kinde SDK for Python.

You can also use the [Python starter kit here](https://github.com/kinde-starter-kits/python-starter-kit).

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com) [![Kinde Docs](https://img.shields.io/badge/Kinde-Docs-eee?style=flat-square)](https://kinde.com/docs/developer-tools) [![Kinde Community](https://img.shields.io/badge/Kinde-Community-eee?style=flat-square)](https://thekindecommunity.slack.com)

## Documentation

For details on integrating this SDK into your project, head over to the [Kinde docs](https://kinde.com/docs/) and see the [Python SDK](https://kinde.com/docs/developer-tools/python-sdk/) doc 👍🏼.

## Storage Usage Examples

### Basic Usage
```python
from kinde_sdk.auth import OAuth
from kinde_sdk.core.storage import StorageManager

# Basic initialization via OAuth
# This is the recommended way to initialize the storage system
# OAuth automatically initializes the StorageManager with the provided config
oauth = OAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="your_redirect_uri"
)

# Direct access to the storage manager
# This is safe to use after OAuth initialization
storage_manager = StorageManager()

# Store authentication data
storage_manager.set("user_tokens", {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_at": 1678901234
})

# Retrieve tokens
tokens = storage_manager.get("user_tokens")
if tokens:
    access_token = tokens.get("access_token")
    # Use the access token for API requests
    
# Delete tokens when logging out
storage_manager.delete("user_tokens")
```

### Using a Custom Storage Backend
```python
oauth = OAuth(
    client_id="your_client_id",
    storage_config={
        "type": "local_storage",
        "options": {
            # backend-specific options
        }
    }
)
```

### Handling Multi-Device Usage
The StorageManager automatically assigns a unique device ID to each client instance, ensuring that
the same user logged in on different devices won't experience session clashes. Keys are namespaced
with the device ID by default.

```python
# Get the current device ID
device_id = storage_manager.get_device_id()
print(f"Current device ID: {device_id}")

# Clear all data for the current device (useful for logout)
storage_manager.clear_device_data()

# For data that should be shared across all devices for the same user
# Use the "user:" prefix
storage_manager.set("user:shared_preferences", {"theme": "dark"})

# For data that should be global across all users and devices
# Use the "global:" prefix
storage_manager.set("global:app_settings", {"version": "1.0.0"})
```

## Best Practices for Storage Management

1. **Always initialize OAuth first**: The OAuth constructor initializes the StorageManager, so create your OAuth instance before accessing the storage.

2. **Manual initialization (if needed)**: If you need to use StorageManager before creating an OAuth instance, explicitly initialize it first:
```python
# Manual initialization
storage_manager = StorageManager()
storage_manager.initialize({"type": "memory"})  # or your preferred storage config

# You can also provide a specific device ID
storage_manager.initialize(
    config={"type": "memory"},
    device_id="custom-device-identifier"
)

# Now safe to use
storage_manager.set("some_key", {"some": "value"})
```

3. **Safe access pattern**: If you're unsure about initialization status, you can use this pattern:
```python
storage_manager = StorageManager()
if not storage_manager._initialized:
    storage_manager.initialize()
    
# Now safe to use
data = storage_manager.get("some_key")
```

4. **Single configuration**: Configure the storage only once at application startup. Changing storage configuration mid-operation may lead to data inconsistency.

5. **Access from anywhere**: After initialization, you can safely access the StorageManager from any part of your application without passing it around.

6. **Device-specific data**: Understand that by default, data is stored with device-specific namespacing. To share data across devices, use the appropriate prefixes.

7. **Complete logout**: To ensure all device-specific data is cleared during logout, call `storage_manager.clear_device_data()`.



# After initializing both OAuth and KindeApiClient use the following fn to get proper urls
api_client.fetch_openid_configuration(oauth)

## Publishing

The core team handles publishing.

## Contributing

Please refer to Kinde’s [contributing guidelines](https://github.com/kinde-oss/.github/blob/489e2ca9c3307c2b2e098a885e22f2239116394a/CONTRIBUTING.md).

## License

By contributing to Kinde, you agree that your contributions will be licensed under its MIT License.