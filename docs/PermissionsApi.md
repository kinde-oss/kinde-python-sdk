# kinde_sdk.PermissionsApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_permission**](PermissionsApi.md#create_permission) | **POST** /api/v1/permissions | Create Permission
[**delete_permission**](PermissionsApi.md#delete_permission) | **DELETE** /api/v1/permissions/{permission_id} | Delete Permission
[**get_permissions**](PermissionsApi.md#get_permissions) | **GET** /api/v1/permissions | List Permissions
[**get_user_permissions**](PermissionsApi.md#get_user_permissions) | **GET** /account_api/v1/permissions | Get permissions
[**update_permissions**](PermissionsApi.md#update_permissions) | **PATCH** /api/v1/permissions/{permission_id} | Update Permission


# **create_permission**
> SuccessResponse create_permission(create_permission_request=create_permission_request)

Create Permission

Create a new permission.

<div>
  <code>create:permissions</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_permission_request import CreatePermissionRequest
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://your_kinde_subdomain.kinde.com
# See configuration.py for a list of all supported configuration parameters.
configuration = kinde_sdk.Configuration(
    host = "https://your_kinde_subdomain.kinde.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kinde_sdk.PermissionsApi(api_client)
    create_permission_request = kinde_sdk.CreatePermissionRequest() # CreatePermissionRequest | Permission details. (optional)

    try:
        # Create Permission
        api_response = api_instance.create_permission(create_permission_request=create_permission_request)
        print("The response of PermissionsApi->create_permission:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->create_permission: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_permission_request** | [**CreatePermissionRequest**](CreatePermissionRequest.md)| Permission details. | [optional] 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Permission successfully created |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_permission**
> SuccessResponse delete_permission(permission_id)

Delete Permission

Delete permission

<div>
  <code>delete:permissions</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://your_kinde_subdomain.kinde.com
# See configuration.py for a list of all supported configuration parameters.
configuration = kinde_sdk.Configuration(
    host = "https://your_kinde_subdomain.kinde.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kinde_sdk.PermissionsApi(api_client)
    permission_id = 'permission_id_example' # str | The identifier for the permission.

    try:
        # Delete Permission
        api_response = api_instance.delete_permission(permission_id)
        print("The response of PermissionsApi->delete_permission:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->delete_permission: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **permission_id** | **str**| The identifier for the permission. | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | permission successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_permissions**
> GetPermissionsResponse get_permissions(sort=sort, page_size=page_size, next_token=next_token)

List Permissions

The returned list can be sorted by permission name or permission ID in ascending or descending order. The number of records to return at a time can also be controlled using the `page_size` query string parameter.

<div>
  <code>read:permissions</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_permissions_response import GetPermissionsResponse
from kinde_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://your_kinde_subdomain.kinde.com
# See configuration.py for a list of all supported configuration parameters.
configuration = kinde_sdk.Configuration(
    host = "https://your_kinde_subdomain.kinde.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kinde_sdk.PermissionsApi(api_client)
    sort = 'sort_example' # str | Field and order to sort the result by. (optional)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    next_token = 'next_token_example' # str | A string to get the next page of results if there are more results. (optional)

    try:
        # List Permissions
        api_response = api_instance.get_permissions(sort=sort, page_size=page_size, next_token=next_token)
        print("The response of PermissionsApi->get_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sort** | **str**| Field and order to sort the result by. | [optional] 
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **next_token** | **str**| A string to get the next page of results if there are more results. | [optional] 

### Return type

[**GetPermissionsResponse**](GetPermissionsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Permissions successfully retrieved. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_permissions**
> GetUserPermissionsResponse get_user_permissions(page_size=page_size, starting_after=starting_after)

Get permissions

Returns all the permissions the user has


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_user_permissions_response import GetUserPermissionsResponse
from kinde_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://your_kinde_subdomain.kinde.com
# See configuration.py for a list of all supported configuration parameters.
configuration = kinde_sdk.Configuration(
    host = "https://your_kinde_subdomain.kinde.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kinde_sdk.PermissionsApi(api_client)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    starting_after = 'perm_1234567890abcdef' # str | The ID of the permission to start after. (optional)

    try:
        # Get permissions
        api_response = api_instance.get_user_permissions(page_size=page_size, starting_after=starting_after)
        print("The response of PermissionsApi->get_user_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->get_user_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **starting_after** | **str**| The ID of the permission to start after. | [optional] 

### Return type

[**GetUserPermissionsResponse**](GetUserPermissionsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Permissions successfully retrieved. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_permissions**
> SuccessResponse update_permissions(permission_id, create_permission_request=create_permission_request)

Update Permission

Update permission

<div>
  <code>update:permissions</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_permission_request import CreatePermissionRequest
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://your_kinde_subdomain.kinde.com
# See configuration.py for a list of all supported configuration parameters.
configuration = kinde_sdk.Configuration(
    host = "https://your_kinde_subdomain.kinde.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kinde_sdk.PermissionsApi(api_client)
    permission_id = 'permission_id_example' # str | The identifier for the permission.
    create_permission_request = kinde_sdk.CreatePermissionRequest() # CreatePermissionRequest | Permission details. (optional)

    try:
        # Update Permission
        api_response = api_instance.update_permissions(permission_id, create_permission_request=create_permission_request)
        print("The response of PermissionsApi->update_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PermissionsApi->update_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **permission_id** | **str**| The identifier for the permission. | 
 **create_permission_request** | [**CreatePermissionRequest**](CreatePermissionRequest.md)| Permission details. | [optional] 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Permission successfully updated |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

