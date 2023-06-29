<a name="__pageTop"></a>
# kinde_sdk.apis.tags.permissions_api.PermissionsApi

All URIs are relative to *https://app.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_permission**](#create_permission) | **post** /api/v1/permissions | Create Permission
[**get_permissions**](#get_permissions) | **get** /api/v1/permissions | List Permissions
[**update_permissions**](#update_permissions) | **patch** /api/v1/permissions/{permission_id} | Update Permission

# **create_permission**
<a name="create_permission"></a>
> SuccessResponse create_permission()

Create Permission

Create a new permission.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import permissions_api
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
    api_instance = permissions_api.PermissionsApi(api_client)

    # example passing only optional values
    body = dict(
        name="name_example",
        description="description_example",
        key="key_example",
    )
    try:
        # Create Permission
        api_response = api_instance.create_permission(
            body=body,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling PermissionsApi->create_permission: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, Unset] | optional, default is unset |
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
**name** | str,  | str,  | The permission&#x27;s name. | [optional] 
**description** | str,  | str,  | The permission&#x27;s description. | [optional] 
**key** | str,  | str,  | The permission identifier to use in code. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_permission.ApiResponseFor201) | Permission successfully created
400 | [ApiResponseFor400](#create_permission.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#create_permission.ApiResponseFor403) | Invalid credentials.

#### create_permission.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


#### create_permission.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### create_permission.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_permissions**
<a name="get_permissions"></a>
> SuccessResponse get_permissions()

List Permissions

The returned list can be sorted by permission name or permission ID in ascending or descending order. The number of records to return at a time can also be controlled using the `page_size` query string parameter. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import permissions_api
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
    api_instance = permissions_api.PermissionsApi(api_client)

    # example passing only optional values
    query_params = {
        'sort': "name_asc",
        'page_size': 1,
        'next_token': "next_token_example",
    }
    try:
        # List Permissions
        api_response = api_instance.get_permissions(
            query_params=query_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling PermissionsApi->get_permissions: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
sort | SortSchema | | optional
page_size | PageSizeSchema | | optional
next_token | NextTokenSchema | | optional


# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, str,  | NoneClass, str,  |  | must be one of ["name_asc", "name_desc", "id_asc", "id_desc", ] 

# PageSizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, decimal.Decimal, int,  | NoneClass, decimal.Decimal,  |  | 

# NextTokenSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, str,  | NoneClass, str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_permissions.ApiResponseFor200) | Permissions successfully retrieved.
403 | [ApiResponseFor403](#get_permissions.ApiResponseFor403) | Invalid credentials.

#### get_permissions.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

#### get_permissions.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_permissions**
<a name="update_permissions"></a>
> SuccessResponse update_permissions(permission_id)

Update Permission

Update permission

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import permissions_api
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
    api_instance = permissions_api.PermissionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'permission_id': 1,
    }
    try:
        # Update Permission
        api_response = api_instance.update_permissions(
            path_params=path_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling PermissionsApi->update_permissions: %s\n" % e)

    # example passing only optional values
    path_params = {
        'permission_id': 1,
    }
    body = dict(
        name="name_example",
        description="description_example",
        key="key_example",
    )
    try:
        # Update Permission
        api_response = api_instance.update_permissions(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling PermissionsApi->update_permissions: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, Unset] | optional, default is unset |
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
**name** | str,  | str,  | The permission&#x27;s name. | [optional] 
**description** | str,  | str,  | The permission&#x27;s description. | [optional] 
**key** | str,  | str,  | The permission identifier to use in code. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
permission_id | PermissionIdSchema | | 

# PermissionIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#update_permissions.ApiResponseFor201) | Permission successfully updated
400 | [ApiResponseFor400](#update_permissions.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#update_permissions.ApiResponseFor403) | Invalid credentials.

#### update_permissions.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  | 


#### update_permissions.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### update_permissions.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

