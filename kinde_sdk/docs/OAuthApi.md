# kinde_sdk.OAuthApi

All URIs are relative to *https://app.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user**](OAuthApi.md#get_user) | **GET** /oauth2/user_profile | Returns the details of the currently logged in user
[**get_user_profile_v2**](OAuthApi.md#get_user_profile_v2) | **GET** /oauth2/v2/user_profile | Returns the details of the currently logged in user


# **get_user**
> UserProfile get_user()

Returns the details of the currently logged in user

Contains the id, names and email of the currently logged in user 

### Example

* OAuth Authentication (OAuth2):
* OAuth Authentication (OAuth2):
* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import time
import kinde_sdk
from kinde_sdk.api import o_auth_api
from kinde_sdk.model.user_profile import UserProfile
from pprint import pprint
# Defining the host is optional and defaults to https://app.kinde.com
# See configuration.py for a list of all supported configuration parameters.
configuration = kinde_sdk.Configuration(
    host = "https://app.kinde.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure OAuth2 access token for authorization: OAuth2
configuration = kinde_sdk.Configuration(
    host = "https://app.kinde.com"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: OAuth2
configuration = kinde_sdk.Configuration(
    host = "https://app.kinde.com"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = o_auth_api.OAuthApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Returns the details of the currently logged in user
        api_response = api_instance.get_user()
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OAuthApi->get_user: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**UserProfile**](UserProfile.md)

### Authorization

[OAuth2](../README.md#OAuth2), [OAuth2](../README.md#OAuth2), [kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A succesful response with the user details |  -  |
**403** | invalid_credentials |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_profile_v2**
> UserProfileV2 get_user_profile_v2()

Returns the details of the currently logged in user

Contains the id, names and email of the currently logged in user 

### Example

* OAuth Authentication (OAuth2):
* OAuth Authentication (OAuth2):
* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import time
import kinde_sdk
from kinde_sdk.api import o_auth_api
from kinde_sdk.model.user_profile_v2 import UserProfileV2
from pprint import pprint
# Defining the host is optional and defaults to https://app.kinde.com
# See configuration.py for a list of all supported configuration parameters.
configuration = kinde_sdk.Configuration(
    host = "https://app.kinde.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure OAuth2 access token for authorization: OAuth2
configuration = kinde_sdk.Configuration(
    host = "https://app.kinde.com"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: OAuth2
configuration = kinde_sdk.Configuration(
    host = "https://app.kinde.com"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = o_auth_api.OAuthApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Returns the details of the currently logged in user
        api_response = api_instance.get_user_profile_v2()
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OAuthApi->get_user_profile_v2: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**UserProfileV2**](UserProfileV2.md)

### Authorization

[OAuth2](../README.md#OAuth2), [OAuth2](../README.md#OAuth2), [kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A succesful response with the user details |  -  |
**403** | invalid_credentials |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

