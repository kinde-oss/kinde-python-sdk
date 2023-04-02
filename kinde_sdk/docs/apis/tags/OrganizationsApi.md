<a name="__pageTop"></a>
# kinde_sdk.apis.tags.organizations_api.OrganizationsApi

All URIs are relative to *https://app.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_organization_users**](#add_organization_users) | **post** /api/v1/organization/users | Assign Users to an Organization
[**create_organization**](#create_organization) | **post** /api/v1/organization | Create Organization
[**delete_organization_feature_flag_override**](#delete_organization_feature_flag_override) | **delete** /api/v1/organizations/{org_code}/feature_flags/{feature_flag_key} | Delete organization feature flag override
[**delete_organization_feature_flag_overrides**](#delete_organization_feature_flag_overrides) | **delete** /api/v1/organizations/{org_code}/feature_flags | Delete all organization feature flag overrides
[**get_organization**](#get_organization) | **get** /api/v1/organization | Get Organization
[**get_organization_users**](#get_organization_users) | **get** /api/v1/organization/users | List Organization Users
[**get_organizations**](#get_organizations) | **get** /api/v1/organizations | List Organizations
[**remove_organization_users**](#remove_organization_users) | **patch** /api/v1/organization/users | Remove Users from an Organization
[**update_organization_feature_flag_override**](#update_organization_feature_flag_override) | **patch** /api/v1/organizations/{org_code}/feature_flags/{feature_flag_key} | Update organization feature flag override

# **add_organization_users**
<a name="add_organization_users"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} add_organization_users()

Assign Users to an Organization

Add existing users to an organization.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import organizations_api
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
    api_instance = organizations_api.OrganizationsApi(api_client)

    # example passing only optional values
    query_params = {
        'code': "code_example",
    }
    body = dict(
        users=[
            "users_example"
        ],
    )
    try:
        # Assign Users to an Organization
        api_response = api_instance.add_organization_users(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OrganizationsApi->add_organization_users: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, Unset] | optional, default is unset |
query_params | RequestQueryParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
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
**[users](#users)** | list, tuple,  | tuple,  | List of user ids to be added to the organization. | [optional]
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# users

List of user ids to be added to the organization.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of user ids to be added to the organization. |

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  |

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
code | CodeSchema | | optional


# CodeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#add_organization_users.ApiResponseFor200) | Users successfully added.
204 | [ApiResponseFor204](#add_organization_users.ApiResponseFor204) | No users added.
400 | [ApiResponseFor400](#add_organization_users.ApiResponseFor400) | Bad request.
403 | [ApiResponseFor403](#add_organization_users.ApiResponseFor403) | Invalid credentials.

#### add_organization_users.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  |

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**code** | str,  | str,  | Response code. | [optional]
**message** | str,  | str,  | Response message. | [optional]
**[users_added](#users_added)** | list, tuple,  | tuple,  |  | [optional]
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# users_added

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  |

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  |

#### add_organization_users.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### add_organization_users.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  |


#### add_organization_users.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_organization**
<a name="create_organization"></a>
> create_organization()

Create Organization

Create an organization.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import organizations_api
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
    api_instance = organizations_api.OrganizationsApi(api_client)

    # example passing only optional values
    body = dict(
        name="name_example",
        feature_flags=dict(
            "str": "str",
        ),
    )
    try:
        # Create Organization
        api_response = api_instance.create_organization(
            body=body,
        )
    except kinde_sdk.ApiException as e:
        print("Exception when calling OrganizationsApi->create_organization: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, Unset] | optional, default is unset |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
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
**name** | str,  | str,  | The organization&#x27;s name. | [optional]
**[feature_flags](#feature_flags)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | The organization&#x27;s feature flag settings. | [optional]
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# feature_flags

The organization's feature flag settings.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | The organization&#x27;s feature flag settings. |

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | str,  | str,  | any string name can be used but the value must be the correct type Value of the feature flag. | [optional] must be one of ["str", "int", "bool", ]

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_organization.ApiResponseFor201) | Organization successfully created.
403 | [ApiResponseFor403](#create_organization.ApiResponseFor403) | Invalid credentials.
400 | [ApiResponseFor400](#create_organization.ApiResponseFor400) | Error creating user.
500 | [ApiResponseFor500](#create_organization.ApiResponseFor500) | Could not create organization.

#### create_organization.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### create_organization.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

#### create_organization.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  |


#### create_organization.ApiResponseFor500
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_organization_feature_flag_override**
<a name="delete_organization_feature_flag_override"></a>
> SuccessResponse delete_organization_feature_flag_override(org_codefeature_flag_key)

Delete organization feature flag override

Delete organization feature flag override.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import organizations_api
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
    api_instance = organizations_api.OrganizationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'org_code': "org_code_example",
        'feature_flag_key': "feature_flag_key_example",
    }
    try:
        # Delete organization feature flag override
        api_response = api_instance.delete_organization_feature_flag_override(
            path_params=path_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OrganizationsApi->delete_organization_feature_flag_override: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
org_code | OrgCodeSchema | |
feature_flag_key | FeatureFlagKeySchema | |

# OrgCodeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

# FeatureFlagKeySchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_organization_feature_flag_override.ApiResponseFor200) | Feature flag override successfully deleted.
400 | [ApiResponseFor400](#delete_organization_feature_flag_override.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#delete_organization_feature_flag_override.ApiResponseFor403) | Invalid credentials.

#### delete_organization_feature_flag_override.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  |


#### delete_organization_feature_flag_override.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  |


#### delete_organization_feature_flag_override.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_organization_feature_flag_overrides**
<a name="delete_organization_feature_flag_overrides"></a>
> SuccessResponse delete_organization_feature_flag_overrides(org_code)

Delete all organization feature flag overrides

Delete all organization feature flag overrides.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import organizations_api
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
    api_instance = organizations_api.OrganizationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'org_code': "org_code_example",
    }
    try:
        # Delete all organization feature flag overrides
        api_response = api_instance.delete_organization_feature_flag_overrides(
            path_params=path_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OrganizationsApi->delete_organization_feature_flag_overrides: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
org_code | OrgCodeSchema | |

# OrgCodeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_organization_feature_flag_overrides.ApiResponseFor200) | Feature flag overrides successfully deleted.
400 | [ApiResponseFor400](#delete_organization_feature_flag_overrides.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#delete_organization_feature_flag_overrides.ApiResponseFor403) | Invalid credentials.

#### delete_organization_feature_flag_overrides.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  |


#### delete_organization_feature_flag_overrides.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  |


#### delete_organization_feature_flag_overrides.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_organization**
<a name="get_organization"></a>
> Organization get_organization()

Get Organization

Gets an organization given the organization's code.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import organizations_api
from kinde_sdk.model.organization import Organization
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
    api_instance = organizations_api.OrganizationsApi(api_client)

    # example passing only optional values
    query_params = {
        'code': "code_example",
    }
    try:
        # Get Organization
        api_response = api_instance.get_organization(
            query_params=query_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OrganizationsApi->get_organization: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
code | CodeSchema | | optional


# CodeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_organization.ApiResponseFor200) | Organization successfully retrieved.
400 | [ApiResponseFor400](#get_organization.ApiResponseFor400) | Bad request.
403 | [ApiResponseFor403](#get_organization.ApiResponseFor403) | Invalid credentials.

#### get_organization.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Organization**](../../models/Organization.md) |  |


#### get_organization.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  |


#### get_organization.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_organization_users**
<a name="get_organization_users"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} get_organization_users()

List Organization Users

Get users in an organization.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import organizations_api
from kinde_sdk.model.organization_user import OrganizationUser
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
    api_instance = organizations_api.OrganizationsApi(api_client)

    # example passing only optional values
    query_params = {
        'sort': "name_asc",
        'page_size': 1,
        'next_token': "next_token_example",
        'code': "code_example",
        'permissions': "permissions_example",
    }
    try:
        # List Organization Users
        api_response = api_instance.get_organization_users(
            query_params=query_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OrganizationsApi->get_organization_users: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
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
code | CodeSchema | | optional
permissions | PermissionsSchema | | optional


# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, str,  | NoneClass, str,  |  | must be one of ["name_asc", "name_desc", "email_asc", "email_desc", ]

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

# CodeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

# PermissionsSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_organization_users.ApiResponseFor200) | A succesful response with a list of organization users or an empty list.
400 | [ApiResponseFor400](#get_organization_users.ApiResponseFor400) | Error creating user
403 | [ApiResponseFor403](#get_organization_users.ApiResponseFor403) | Invalid credentials.

#### get_organization_users.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  |

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**code** | str,  | str,  | Response code. | [optional]
**message** | str,  | str,  | Response message. | [optional]
**[organization_users](#organization_users)** | list, tuple,  | tuple,  |  | [optional]
**next_token** | str,  | str,  | Pagination token. | [optional]
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# organization_users

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  |

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**OrganizationUser**]({{complexTypePrefix}}OrganizationUser.md) | [**OrganizationUser**]({{complexTypePrefix}}OrganizationUser.md) | [**OrganizationUser**]({{complexTypePrefix}}OrganizationUser.md) |  |

#### get_organization_users.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  |


#### get_organization_users.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_organizations**
<a name="get_organizations"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} get_organizations()

List Organizations

Get a list of organizations.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import organizations_api
from kinde_sdk.model.organization import Organization
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
    api_instance = organizations_api.OrganizationsApi(api_client)

    # example passing only optional values
    query_params = {
        'sort': "name_asc",
        'page_size': 1,
        'next_token': "next_token_example",
    }
    try:
        # List Organizations
        api_response = api_instance.get_organizations(
            query_params=query_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OrganizationsApi->get_organizations: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
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
None, str,  | NoneClass, str,  |  | must be one of ["name_asc", "name_desc", "email_asc", "email_desc", ]

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
200 | [ApiResponseFor200](#get_organizations.ApiResponseFor200) | A successful response with a list of organizations or an empty list.
403 | [ApiResponseFor403](#get_organizations.ApiResponseFor403) | Invalid credentials.

#### get_organizations.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  |

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**code** | str,  | str,  | Response code. | [optional]
**message** | str,  | str,  | Response message. | [optional]
**[organizations](#organizations)** | list, tuple,  | tuple,  |  | [optional]
**next_token** | str,  | str,  | Pagination token. | [optional]
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# organizations

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  |

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Organization**]({{complexTypePrefix}}Organization.md) | [**Organization**]({{complexTypePrefix}}Organization.md) | [**Organization**]({{complexTypePrefix}}Organization.md) |  |

#### get_organizations.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **remove_organization_users**
<a name="remove_organization_users"></a>
> {str: (bool, date, datetime, dict, float, int, list, str, none_type)} remove_organization_users()

Remove Users from an Organization

Remove existing users from an organization.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import organizations_api
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
    api_instance = organizations_api.OrganizationsApi(api_client)

    # example passing only optional values
    query_params = {
        'code': "code_example",
    }
    body = dict(
        users=[
            "users_example"
        ],
    )
    try:
        # Remove Users from an Organization
        api_response = api_instance.remove_organization_users(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OrganizationsApi->remove_organization_users: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, Unset] | optional, default is unset |
query_params | RequestQueryParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
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
**[users](#users)** | list, tuple,  | tuple,  | List of user ids to be removed from the organization. | [optional]
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# users

List of user ids to be removed from the organization.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of user ids to be removed from the organization. |

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  |

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
code | CodeSchema | | optional


# CodeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#remove_organization_users.ApiResponseFor200) | Users successfully removed.
400 | [ApiResponseFor400](#remove_organization_users.ApiResponseFor400) | Error creating user.
403 | [ApiResponseFor403](#remove_organization_users.ApiResponseFor403) | Invalid credentials.

#### remove_organization_users.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  |

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**message** | str,  | str,  |  | [optional]
**[users_added](#users_added)** | list, tuple,  | tuple,  |  | [optional]
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# users_added

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  |

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  |

#### remove_organization_users.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  |


#### remove_organization_users.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_organization_feature_flag_override**
<a name="update_organization_feature_flag_override"></a>
> SuccessResponse update_organization_feature_flag_override(org_codefeature_flag_keyvalue)

Update organization feature flag override

Update organization feature flag override.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import organizations_api
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
    api_instance = organizations_api.OrganizationsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'org_code': "org_code_example",
        'feature_flag_key': "feature_flag_key_example",
    }
    query_params = {
        'value': "value_example",
    }
    try:
        # Update organization feature flag override
        api_response = api_instance.update_organization_feature_flag_override(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling OrganizationsApi->update_organization_feature_flag_override: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
value | ValueSchema | |


# ValueSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
org_code | OrgCodeSchema | |
feature_flag_key | FeatureFlagKeySchema | |

# OrgCodeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

# FeatureFlagKeySchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  |

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_organization_feature_flag_override.ApiResponseFor200) | Feature flag override successfully updated.
400 | [ApiResponseFor400](#update_organization_feature_flag_override.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#update_organization_feature_flag_override.ApiResponseFor403) | Invalid credentials.

#### update_organization_feature_flag_override.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**SuccessResponse**](../../models/SuccessResponse.md) |  |


#### update_organization_feature_flag_override.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  |


#### update_organization_feature_flag_override.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)
