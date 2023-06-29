<a name="__pageTop"></a>
# kinde_sdk.apis.tags.environments_api.EnvironmentsApi

All URIs are relative to *https://app.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_environement_feature_flag_override**](#delete_environement_feature_flag_override) | **delete** /api/v1/environment/feature_flags/{feature_flag_key} | Delete Environment Feature Flag Override
[**delete_environement_feature_flag_overrides**](#delete_environement_feature_flag_overrides) | **delete** /api/v1/environment/feature_flags | Delete Environment Feature Flag Overrides
[**get_environement_feature_flags**](#get_environement_feature_flags) | **get** /api/v1/environment/feature_flags | List Environment Feature Flags
[**update_environement_feature_flag_override**](#update_environement_feature_flag_override) | **patch** /api/v1/environment/feature_flags/{feature_flag_key} | Update Environment Feature Flag Override

# **delete_environement_feature_flag_override**
<a name="delete_environement_feature_flag_override"></a>
> SuccessResponse delete_environement_feature_flag_override(feature_flag_key)

Delete Environment Feature Flag Override

Delete environment feature flag override.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import environments_api
from kinde_sdk.model.success_response import SuccessResponse
from kinde_sdk.model.error_response import ErrorResponse
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
    api_instance = environments_api.EnvironmentsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'feature_flag_key': "feature_flag_key_example",
    }
    try:
        # Delete Environment Feature Flag Override
        api_response = api_instance.delete_environement_feature_flag_override(
            path_params=path_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling EnvironmentsApi->delete_environement_feature_flag_override: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
feature_flag_key | FeatureFlagKeySchema | | 

# FeatureFlagKeySchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_environement_feature_flag_override.ApiResponseFor200) | Feature flag deleted successfully.
400 | [ApiResponseFor400](#delete_environement_feature_flag_override.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#delete_environement_feature_flag_override.ApiResponseFor403) | Invalid credentials.

#### delete_environement_feature_flag_override.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


#### delete_environement_feature_flag_override.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### delete_environement_feature_flag_override.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_environement_feature_flag_overrides**
<a name="delete_environement_feature_flag_overrides"></a>
> SuccessResponse delete_environement_feature_flag_overrides()

Delete Environment Feature Flag Overrides

Delete all environment feature flag overrides.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import environments_api
from kinde_sdk.model.success_response import SuccessResponse
from kinde_sdk.model.error_response import ErrorResponse
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
    api_instance = environments_api.EnvironmentsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Delete Environment Feature Flag Overrides
        api_response = api_instance.delete_environement_feature_flag_overrides()
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling EnvironmentsApi->delete_environement_feature_flag_overrides: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_environement_feature_flag_overrides.ApiResponseFor200) | Feature flag overrides deleted successfully.
400 | [ApiResponseFor400](#delete_environement_feature_flag_overrides.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#delete_environement_feature_flag_overrides.ApiResponseFor403) | Invalid credentials.

#### delete_environement_feature_flag_overrides.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


#### delete_environement_feature_flag_overrides.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### delete_environement_feature_flag_overrides.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_environement_feature_flags**
<a name="get_environement_feature_flags"></a>
> GetEnvironmentFeatureFlagsResponse get_environement_feature_flags()

List Environment Feature Flags

Get environment feature flags.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import environments_api
from kinde_sdk.model.error_response import ErrorResponse
from kinde_sdk.model.get_environment_feature_flags_response import GetEnvironmentFeatureFlagsResponse
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
    api_instance = environments_api.EnvironmentsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # List Environment Feature Flags
        api_response = api_instance.get_environement_feature_flags()
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling EnvironmentsApi->get_environement_feature_flags: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_environement_feature_flags.ApiResponseFor200) | Feature flags retrieved successfully.
400 | [ApiResponseFor400](#get_environement_feature_flags.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#get_environement_feature_flags.ApiResponseFor403) | Invalid credentials.

#### get_environement_feature_flags.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**GetEnvironmentFeatureFlagsResponse**](../../models/GetEnvironmentFeatureFlagsResponse.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**GetEnvironmentFeatureFlagsResponse**](../../models/GetEnvironmentFeatureFlagsResponse.md) |  | 


#### get_environement_feature_flags.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### get_environement_feature_flags.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_environement_feature_flag_override**
<a name="update_environement_feature_flag_override"></a>
> SuccessResponse update_environement_feature_flag_override(feature_flag_keyany_type)

Update Environment Feature Flag Override

Update environment feature flag override.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import environments_api
from kinde_sdk.model.success_response import SuccessResponse
from kinde_sdk.model.error_response import ErrorResponse
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
    api_instance = environments_api.EnvironmentsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'feature_flag_key': "feature_flag_key_example",
    }
    body = dict(
        value="value_example",
    )
    try:
        # Update Environment Feature Flag Override
        api_response = api_instance.update_environement_feature_flag_override(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling EnvironmentsApi->update_environement_feature_flag_override: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**value** | str,  | str,  | The flag override value. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
feature_flag_key | FeatureFlagKeySchema | | 

# FeatureFlagKeySchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_environement_feature_flag_override.ApiResponseFor200) | Feature flag override successful
400 | [ApiResponseFor400](#update_environement_feature_flag_override.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#update_environement_feature_flag_override.ApiResponseFor403) | Invalid credentials.

#### update_environement_feature_flag_override.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


#### update_environement_feature_flag_override.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### update_environement_feature_flag_override.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

