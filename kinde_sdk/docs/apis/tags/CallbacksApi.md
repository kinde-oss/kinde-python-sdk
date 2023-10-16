<a name="__pageTop"></a>
# kinde_sdk.apis.tags.callbacks_api.CallbacksApi

All URIs are relative to *https://app.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_logout_redirect_urls**](#add_logout_redirect_urls) | **post** /api/v1/applications/{app_id}/auth_logout_urls | Add Logout Redirect URLs
[**add_redirect_callback_urls**](#add_redirect_callback_urls) | **post** /api/v1/applications/{app_id}/auth_redirect_urls | Add Redirect Callback URLs
[**delete_callback_urls**](#delete_callback_urls) | **delete** /api/v1/applications/{app_id}/auth_redirect_urls | Delete Callback URLs
[**delete_logout_urls**](#delete_logout_urls) | **delete** /api/v1/applications/{app_id}/auth_logout_urls | Delete Logout URLs
[**get_callback_urls**](#get_callback_urls) | **get** /api/v1/applications/{app_id}/auth_redirect_urls | List Callback URLs
[**get_logout_urls**](#get_logout_urls) | **get** /api/v1/applications/{app_id}/auth_logout_urls | List Logout URLs
[**replace_logout_redirect_urls**](#replace_logout_redirect_urls) | **put** /api/v1/applications/{app_id}/auth_logout_urls | Replace Logout Redirect URLs
[**replace_redirect_callback_urls**](#replace_redirect_callback_urls) | **put** /api/v1/applications/{app_id}/auth_redirect_urls | Replace Redirect Callback URLs

# **add_logout_redirect_urls**
<a name="add_logout_redirect_urls"></a>
> SuccessResponse add_logout_redirect_urls(app_idany_type)

Add Logout Redirect URLs

Add additional logout redirect URLs. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import callbacks_api
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
    api_instance = callbacks_api.CallbacksApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'app_id': "app_id_example",
    }
    body = dict(
        urls=[
            "urls_example"
        ],
    )
    try:
        # Add Logout Redirect URLs
        api_response = api_instance.add_logout_redirect_urls(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling CallbacksApi->add_logout_redirect_urls: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
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
**[urls](#urls)** | list, tuple,  | tuple,  | Array of logout urls. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# urls

Array of logout urls.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Array of logout urls. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
app_id | AppIdSchema | | 

# AppIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#add_logout_redirect_urls.ApiResponseFor200) | Logouts successfully updated
400 | [ApiResponseFor400](#add_logout_redirect_urls.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#add_logout_redirect_urls.ApiResponseFor403) | Invalid credentials.
429 | [ApiResponseFor429](#add_logout_redirect_urls.ApiResponseFor429) | Request was throttled.

#### add_logout_redirect_urls.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


#### add_logout_redirect_urls.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### add_logout_redirect_urls.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### add_logout_redirect_urls.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **add_redirect_callback_urls**
<a name="add_redirect_callback_urls"></a>
> SuccessResponse add_redirect_callback_urls(app_idany_type)

Add Redirect Callback URLs

Add additional redirect callback URLs. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import callbacks_api
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
    api_instance = callbacks_api.CallbacksApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'app_id': "app_id_example",
    }
    body = dict(
        urls=[
            "urls_example"
        ],
    )
    try:
        # Add Redirect Callback URLs
        api_response = api_instance.add_redirect_callback_urls(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling CallbacksApi->add_redirect_callback_urls: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
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
**[urls](#urls)** | list, tuple,  | tuple,  | Array of callback urls. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# urls

Array of callback urls.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Array of callback urls. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
app_id | AppIdSchema | | 

# AppIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#add_redirect_callback_urls.ApiResponseFor200) | Callbacks successfully updated
400 | [ApiResponseFor400](#add_redirect_callback_urls.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#add_redirect_callback_urls.ApiResponseFor403) | Invalid credentials.
429 | [ApiResponseFor429](#add_redirect_callback_urls.ApiResponseFor429) | Request was throttled.

#### add_redirect_callback_urls.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


#### add_redirect_callback_urls.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### add_redirect_callback_urls.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### add_redirect_callback_urls.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_callback_urls**
<a name="delete_callback_urls"></a>
> SuccessResponse delete_callback_urls(app_idurls)

Delete Callback URLs

Delete callback URLs. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import callbacks_api
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
    api_instance = callbacks_api.CallbacksApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'app_id': "app_id_example",
    }
    query_params = {
        'urls': "urls_example",
    }
    try:
        # Delete Callback URLs
        api_response = api_instance.delete_callback_urls(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling CallbacksApi->delete_callback_urls: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
urls | UrlsSchema | | 


# UrlsSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
app_id | AppIdSchema | | 

# AppIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_callback_urls.ApiResponseFor200) | Callback URLs successfully deleted.
400 | [ApiResponseFor400](#delete_callback_urls.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#delete_callback_urls.ApiResponseFor403) | Invalid credentials.
429 | [ApiResponseFor429](#delete_callback_urls.ApiResponseFor429) | Request was throttled.

#### delete_callback_urls.ApiResponseFor200
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


#### delete_callback_urls.ApiResponseFor400
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


#### delete_callback_urls.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### delete_callback_urls.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_logout_urls**
<a name="delete_logout_urls"></a>
> SuccessResponse delete_logout_urls(app_idurls)

Delete Logout URLs

Delete logout URLs. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import callbacks_api
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
    api_instance = callbacks_api.CallbacksApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'app_id': "app_id_example",
    }
    query_params = {
        'urls': "urls_example",
    }
    try:
        # Delete Logout URLs
        api_response = api_instance.delete_logout_urls(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling CallbacksApi->delete_logout_urls: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
urls | UrlsSchema | | 


# UrlsSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
app_id | AppIdSchema | | 

# AppIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_logout_urls.ApiResponseFor200) | Logout URLs successfully deleted.
400 | [ApiResponseFor400](#delete_logout_urls.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#delete_logout_urls.ApiResponseFor403) | Invalid credentials.
429 | [ApiResponseFor429](#delete_logout_urls.ApiResponseFor429) | Request was throttled.

#### delete_logout_urls.ApiResponseFor200
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


#### delete_logout_urls.ApiResponseFor400
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


#### delete_logout_urls.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### delete_logout_urls.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_callback_urls**
<a name="get_callback_urls"></a>
> RedirectCallbackUrls get_callback_urls(app_id)

List Callback URLs

Returns an application's redirect callback URLs. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import callbacks_api
from kinde_sdk.model.redirect_callback_urls import RedirectCallbackUrls
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
    api_instance = callbacks_api.CallbacksApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'app_id': "app_id_example",
    }
    try:
        # List Callback URLs
        api_response = api_instance.get_callback_urls(
            path_params=path_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling CallbacksApi->get_callback_urls: %s\n" % e)
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
app_id | AppIdSchema | | 

# AppIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_callback_urls.ApiResponseFor200) | Callback URLs successfully retrieved.
400 | [ApiResponseFor400](#get_callback_urls.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#get_callback_urls.ApiResponseFor403) | Invalid credentials.
429 | [ApiResponseFor429](#get_callback_urls.ApiResponseFor429) | Request was throttled.

#### get_callback_urls.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**RedirectCallbackUrls**](../../models/RedirectCallbackUrls.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**RedirectCallbackUrls**](../../models/RedirectCallbackUrls.md) |  | 


#### get_callback_urls.ApiResponseFor400
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


#### get_callback_urls.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### get_callback_urls.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_logout_urls**
<a name="get_logout_urls"></a>
> LogoutRedirectUrls get_logout_urls(app_id)

List Logout URLs

Returns an application's logout redirect URLs. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import callbacks_api
from kinde_sdk.model.logout_redirect_urls import LogoutRedirectUrls
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
    api_instance = callbacks_api.CallbacksApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'app_id': "app_id_example",
    }
    try:
        # List Logout URLs
        api_response = api_instance.get_logout_urls(
            path_params=path_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling CallbacksApi->get_logout_urls: %s\n" % e)
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
app_id | AppIdSchema | | 

# AppIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_logout_urls.ApiResponseFor200) | Logout URLs successfully retrieved.
400 | [ApiResponseFor400](#get_logout_urls.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#get_logout_urls.ApiResponseFor403) | Invalid credentials.
429 | [ApiResponseFor429](#get_logout_urls.ApiResponseFor429) | Request was throttled.

#### get_logout_urls.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**LogoutRedirectUrls**](../../models/LogoutRedirectUrls.md) |  | 


# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**LogoutRedirectUrls**](../../models/LogoutRedirectUrls.md) |  | 


#### get_logout_urls.ApiResponseFor400
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


#### get_logout_urls.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### get_logout_urls.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **replace_logout_redirect_urls**
<a name="replace_logout_redirect_urls"></a>
> SuccessResponse replace_logout_redirect_urls(app_idany_type)

Replace Logout Redirect URLs

Replace all logout redirect URLs. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import callbacks_api
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
    api_instance = callbacks_api.CallbacksApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'app_id': "app_id_example",
    }
    body = dict(
        urls=[
            "urls_example"
        ],
    )
    try:
        # Replace Logout Redirect URLs
        api_response = api_instance.replace_logout_redirect_urls(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling CallbacksApi->replace_logout_redirect_urls: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
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
**[urls](#urls)** | list, tuple,  | tuple,  | Array of logout urls. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# urls

Array of logout urls.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Array of logout urls. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
app_id | AppIdSchema | | 

# AppIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#replace_logout_redirect_urls.ApiResponseFor200) | Logout URLs successfully updated
400 | [ApiResponseFor400](#replace_logout_redirect_urls.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#replace_logout_redirect_urls.ApiResponseFor403) | Invalid credentials.
429 | [ApiResponseFor429](#replace_logout_redirect_urls.ApiResponseFor429) | Request was throttled.

#### replace_logout_redirect_urls.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


#### replace_logout_redirect_urls.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### replace_logout_redirect_urls.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### replace_logout_redirect_urls.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **replace_redirect_callback_urls**
<a name="replace_redirect_callback_urls"></a>
> SuccessResponse replace_redirect_callback_urls(app_idany_type)

Replace Redirect Callback URLs

Replace all redirect callback URLs. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import callbacks_api
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
    api_instance = callbacks_api.CallbacksApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'app_id': "app_id_example",
    }
    body = dict(
        urls=[
            "urls_example"
        ],
    )
    try:
        # Replace Redirect Callback URLs
        api_response = api_instance.replace_redirect_callback_urls(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling CallbacksApi->replace_redirect_callback_urls: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
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
**[urls](#urls)** | list, tuple,  | tuple,  | Array of callback urls. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# urls

Array of callback urls.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Array of callback urls. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
app_id | AppIdSchema | | 

# AppIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#replace_redirect_callback_urls.ApiResponseFor200) | Callbacks successfully updated
400 | [ApiResponseFor400](#replace_redirect_callback_urls.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#replace_redirect_callback_urls.ApiResponseFor403) | Invalid credentials.
429 | [ApiResponseFor429](#replace_redirect_callback_urls.ApiResponseFor429) | Request was throttled.

#### replace_redirect_callback_urls.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


#### replace_redirect_callback_urls.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### replace_redirect_callback_urls.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### replace_redirect_callback_urls.ApiResponseFor429
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

