<a name="__pageTop"></a>
# kinde_sdk.apis.tags.o_auth_api.OAuthApi

All URIs are relative to *https://app.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user**](#get_user) | **get** /oauth2/user_profile | Get User Profile
[**get_user_profile_v2**](#get_user_profile_v2) | **get** /oauth2/v2/user_profile | Returns the details of the currently logged in user
[**token_introspection**](#token_introspection) | **post** /oauth2/introspect | Get token details
[**token_revocation**](#token_revocation) | **post** /oauth2/revoke | Revoke token

# **get_user**
<a name="get_user"></a>
> UserProfile get_user()

Get User Profile

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
        # Get User Profile
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
429 | [ApiResponseFor429](#get_user_profile_v2.ApiResponseFor429) | Request was throttled.

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

#### get_user_profile_v2.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **token_introspection**
<a name="token_introspection"></a>
> TokenIntrospect token_introspection()

Get token details

Retrieve information about the provided token.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import o_auth_api
from kinde_sdk.model.token_error_response import TokenErrorResponse
from kinde_sdk.model.token_introspect import TokenIntrospect
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

    # example passing only optional values
    body = dict(
        token="token_example",
        token_type="token_type_example",
    )
    try:
        # Get token details
        api_response = api_instance.token_introspection(
            body=body,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OAuthApi->token_introspection: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationXWwwFormUrlencoded, Unset] | optional, default is unset |
content_type | str | optional, default is 'application/x-www-form-urlencoded' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationXWwwFormUrlencoded

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**token** | str,  | str,  | The token to be introspected. | [optional] 
**token_type** | str,  | str,  | The provided token&#x27;s type. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#token_introspection.ApiResponseFor200) | Details of the token.
401 | [ApiResponseFor401](#token_introspection.ApiResponseFor401) | Bad request.
403 | [ApiResponseFor403](#token_introspection.ApiResponseFor403) | Invalid credentials.
429 | [ApiResponseFor429](#token_introspection.ApiResponseFor429) | Request was throttled.

#### token_introspection.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TokenIntrospect**](../../models/TokenIntrospect.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**TokenIntrospect**](../../models/TokenIntrospect.md) |  | 


#### token_introspection.ApiResponseFor401
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor401ResponseBodyApplicationJson, SchemaFor401ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor401ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TokenErrorResponse**](../../models/TokenErrorResponse.md) |  | 


# SchemaFor401ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**TokenErrorResponse**](../../models/TokenErrorResponse.md) |  | 


#### token_introspection.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### token_introspection.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **token_revocation**
<a name="token_revocation"></a>
> token_revocation()

Revoke token

Revoke a previously issued token.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import o_auth_api
from kinde_sdk.model.token_error_response import TokenErrorResponse
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

    # example passing only optional values
    body = dict(
        token="token_example",
        client_id="client_id_example",
        client_secret="client_secret_example",
    )
    try:
        # Revoke token
        api_response = api_instance.token_revocation(
            body=body,
        )
    except kinde_sdk.ApiException as e:
        print("Exception when calling OAuthApi->token_revocation: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationXWwwFormUrlencoded, Unset] | optional, default is unset |
content_type | str | optional, default is 'application/x-www-form-urlencoded' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationXWwwFormUrlencoded

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**token** | str,  | str,  | The token to be revoked. | [optional] 
**client_id** | str,  | str,  | The identifier for your client. | [optional] 
**client_secret** | str,  | str,  | The secret associated with your client. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#token_revocation.ApiResponseFor200) | Token successfully revoked.
401 | [ApiResponseFor401](#token_revocation.ApiResponseFor401) | Bad request.
403 | [ApiResponseFor403](#token_revocation.ApiResponseFor403) | Invalid credentials.
429 | [ApiResponseFor429](#token_revocation.ApiResponseFor429) | Request was throttled.

#### token_revocation.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### token_revocation.ApiResponseFor401
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor401ResponseBodyApplicationJson, SchemaFor401ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor401ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**TokenErrorResponse**](../../models/TokenErrorResponse.md) |  | 


# SchemaFor401ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**TokenErrorResponse**](../../models/TokenErrorResponse.md) |  | 


#### token_revocation.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### token_revocation.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

