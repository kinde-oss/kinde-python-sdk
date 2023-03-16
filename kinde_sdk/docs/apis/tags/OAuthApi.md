<a name="__pageTop"></a>
# kinde_sdk.apis.tags.o_auth_api.OAuthApi

All URIs are relative to *https://app.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user**](#get_user) | **get** /oauth2/user_profile | Returns the details of the currently logged in user
[**get_user_profile_v2**](#get_user_profile_v2) | **get** /oauth2/v2/user_profile | Returns the details of the currently logged in user

# **get_user**
<a name="get_user"></a>
> UserProfile get_user()

Returns the details of the currently logged in user

Contains the id, names and email of the currently logged in user.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import o_auth_api
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

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_user.ApiResponseFor200) | Details of logged in user V1.
403 | [ApiResponseFor403](#get_user.ApiResponseFor403) | Invalid credentials.

#### get_user.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**UserProfile**](../../models/UserProfile.md) |  |


#### get_user.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_user_profile_v2**
<a name="get_user_profile_v2"></a>
> UserProfileV2 get_user_profile_v2()

Returns the details of the currently logged in user

Contains the id, names, profile picture URL and email of the currently logged in user.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import o_auth_api
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

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_user_profile_v2.ApiResponseFor200) | Details of logged in user V2.
403 | [ApiResponseFor403](#get_user_profile_v2.ApiResponseFor403) | Invalid credentials.

#### get_user_profile_v2.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**UserProfileV2**](../../models/UserProfileV2.md) |  |


#### get_user_profile_v2.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)
