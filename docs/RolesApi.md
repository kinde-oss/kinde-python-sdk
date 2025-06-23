# kinde_sdk.RolesApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_role_scope**](RolesApi.md#add_role_scope) | **POST** /api/v1/roles/{role_id}/scopes | Add role scope
[**create_role**](RolesApi.md#create_role) | **POST** /api/v1/roles | Create role
[**delete_role**](RolesApi.md#delete_role) | **DELETE** /api/v1/roles/{role_id} | Delete role
[**delete_role_scope**](RolesApi.md#delete_role_scope) | **DELETE** /api/v1/roles/{role_id}/scopes/{scope_id} | Delete role scope
[**get_role**](RolesApi.md#get_role) | **GET** /api/v1/roles/{role_id} | Get role
[**get_role_permissions**](RolesApi.md#get_role_permissions) | **GET** /api/v1/roles/{role_id}/permissions | Get role permissions
[**get_role_scopes**](RolesApi.md#get_role_scopes) | **GET** /api/v1/roles/{role_id}/scopes | Get role scopes
[**get_roles**](RolesApi.md#get_roles) | **GET** /api/v1/roles | List roles
[**get_user_roles**](RolesApi.md#get_user_roles) | **GET** /account_api/v1/roles | Get roles
[**remove_role_permission**](RolesApi.md#remove_role_permission) | **DELETE** /api/v1/roles/{role_id}/permissions/{permission_id} | Remove role permission
[**update_role_permissions**](RolesApi.md#update_role_permissions) | **PATCH** /api/v1/roles/{role_id}/permissions | Update role permissions
[**update_roles**](RolesApi.md#update_roles) | **PATCH** /api/v1/roles/{role_id} | Update role


# **add_role_scope**
> AddRoleScopeResponse add_role_scope(role_id, add_role_scope_request)

Add role scope

Add scope to role.

<div>
  <code>create:role_scopes</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.add_role_scope_request import AddRoleScopeRequest
from kinde_sdk.models.add_role_scope_response import AddRoleScopeResponse
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
    api_instance = kinde_sdk.RolesApi(api_client)
    role_id = 'role_id_example' # str | The role id.
    add_role_scope_request = kinde_sdk.AddRoleScopeRequest() # AddRoleScopeRequest | Add scope to role.

    try:
        # Add role scope
        api_response = api_instance.add_role_scope(role_id, add_role_scope_request)
        print("The response of RolesApi->add_role_scope:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->add_role_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The role id. | 
 **add_role_scope_request** | [**AddRoleScopeRequest**](AddRoleScopeRequest.md)| Add scope to role. | 

### Return type

[**AddRoleScopeResponse**](AddRoleScopeResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Role scope successfully added. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_role**
> CreateRolesResponse create_role(create_role_request=create_role_request)

Create role

Create role.

<div>
  <code>create:roles</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_role_request import CreateRoleRequest
from kinde_sdk.models.create_roles_response import CreateRolesResponse
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
    api_instance = kinde_sdk.RolesApi(api_client)
    create_role_request = kinde_sdk.CreateRoleRequest() # CreateRoleRequest | Role details. (optional)

    try:
        # Create role
        api_response = api_instance.create_role(create_role_request=create_role_request)
        print("The response of RolesApi->create_role:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->create_role: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_role_request** | [**CreateRoleRequest**](CreateRoleRequest.md)| Role details. | [optional] 

### Return type

[**CreateRolesResponse**](CreateRolesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Role successfully created |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_role**
> SuccessResponse delete_role(role_id)

Delete role

Delete role

<div>
  <code>delete:roles</code>
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
    api_instance = kinde_sdk.RolesApi(api_client)
    role_id = 'role_id_example' # str | The identifier for the role.

    try:
        # Delete role
        api_response = api_instance.delete_role(role_id)
        print("The response of RolesApi->delete_role:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->delete_role: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The identifier for the role. | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Role successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_role_scope**
> DeleteRoleScopeResponse delete_role_scope(role_id, scope_id)

Delete role scope

Delete scope from role.

<div>
  <code>delete:role_scopes</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.delete_role_scope_response import DeleteRoleScopeResponse
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
    api_instance = kinde_sdk.RolesApi(api_client)
    role_id = 'role_id_example' # str | The role id.
    scope_id = 'scope_id_example' # str | The scope id.

    try:
        # Delete role scope
        api_response = api_instance.delete_role_scope(role_id, scope_id)
        print("The response of RolesApi->delete_role_scope:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->delete_role_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The role id. | 
 **scope_id** | **str**| The scope id. | 

### Return type

[**DeleteRoleScopeResponse**](DeleteRoleScopeResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Role scope successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_role**
> GetRoleResponse get_role(role_id)

Get role

Get a role

<div>
  <code>read:roles</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_role_response import GetRoleResponse
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
    api_instance = kinde_sdk.RolesApi(api_client)
    role_id = 'role_id_example' # str | The identifier for the role.

    try:
        # Get role
        api_response = api_instance.get_role(role_id)
        print("The response of RolesApi->get_role:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->get_role: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The identifier for the role. | 

### Return type

[**GetRoleResponse**](GetRoleResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Role successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_role_permissions**
> RolePermissionsResponse get_role_permissions(role_id, sort=sort, page_size=page_size, next_token=next_token)

Get role permissions

Get permissions for a role.

<div>
  <code>read:role_permissions</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.role_permissions_response import RolePermissionsResponse
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
    api_instance = kinde_sdk.RolesApi(api_client)
    role_id = 'role_id_example' # str | The role's public id.
    sort = 'sort_example' # str | Field and order to sort the result by. (optional)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    next_token = 'next_token_example' # str | A string to get the next page of results if there are more results. (optional)

    try:
        # Get role permissions
        api_response = api_instance.get_role_permissions(role_id, sort=sort, page_size=page_size, next_token=next_token)
        print("The response of RolesApi->get_role_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->get_role_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The role&#39;s public id. | 
 **sort** | **str**| Field and order to sort the result by. | [optional] 
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **next_token** | **str**| A string to get the next page of results if there are more results. | [optional] 

### Return type

[**RolePermissionsResponse**](RolePermissionsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of permissions for a role |  -  |
**400** | Error removing user |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_role_scopes**
> RoleScopesResponse get_role_scopes(role_id)

Get role scopes

Get scopes for a role.

<div>
  <code>read:role_scopes</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.role_scopes_response import RoleScopesResponse
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
    api_instance = kinde_sdk.RolesApi(api_client)
    role_id = 'role_id_example' # str | The role id.

    try:
        # Get role scopes
        api_response = api_instance.get_role_scopes(role_id)
        print("The response of RolesApi->get_role_scopes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->get_role_scopes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The role id. | 

### Return type

[**RoleScopesResponse**](RoleScopesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of scopes for a role |  -  |
**400** | Error removing user |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_roles**
> GetRolesResponse get_roles(sort=sort, page_size=page_size, next_token=next_token)

List roles

The returned list can be sorted by role name or role ID in ascending or descending order. The number of records to return at a time can also be controlled using the `page_size` query string parameter.

<div>
  <code>read:roles</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_roles_response import GetRolesResponse
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
    api_instance = kinde_sdk.RolesApi(api_client)
    sort = 'sort_example' # str | Field and order to sort the result by. (optional)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    next_token = 'next_token_example' # str | A string to get the next page of results if there are more results. (optional)

    try:
        # List roles
        api_response = api_instance.get_roles(sort=sort, page_size=page_size, next_token=next_token)
        print("The response of RolesApi->get_roles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->get_roles: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sort** | **str**| Field and order to sort the result by. | [optional] 
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **next_token** | **str**| A string to get the next page of results if there are more results. | [optional] 

### Return type

[**GetRolesResponse**](GetRolesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Roles successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_roles**
> GetUserRolesResponse get_user_roles(page_size=page_size, starting_after=starting_after)

Get roles

Returns all roles for the user


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_user_roles_response import GetUserRolesResponse
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
    api_instance = kinde_sdk.RolesApi(api_client)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    starting_after = 'role_1234567890abcdef' # str | The ID of the role to start after. (optional)

    try:
        # Get roles
        api_response = api_instance.get_user_roles(page_size=page_size, starting_after=starting_after)
        print("The response of RolesApi->get_user_roles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->get_user_roles: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **starting_after** | **str**| The ID of the role to start after. | [optional] 

### Return type

[**GetUserRolesResponse**](GetUserRolesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Roles successfully retrieved. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_role_permission**
> SuccessResponse remove_role_permission(role_id, permission_id)

Remove role permission

Remove a permission from a role.

<div>
  <code>delete:role_permissions</code>
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
    api_instance = kinde_sdk.RolesApi(api_client)
    role_id = 'role_id_example' # str | The role's public id.
    permission_id = 'permission_id_example' # str | The permission's public id.

    try:
        # Remove role permission
        api_response = api_instance.remove_role_permission(role_id, permission_id)
        print("The response of RolesApi->remove_role_permission:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->remove_role_permission: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The role&#39;s public id. | 
 **permission_id** | **str**| The permission&#39;s public id. | 

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
**200** | Permission successfully removed from role |  -  |
**400** | Error removing user |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_role_permissions**
> UpdateRolePermissionsResponse update_role_permissions(role_id, update_role_permissions_request)

Update role permissions

Update role permissions.

<div>
  <code>update:role_permissions</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.update_role_permissions_request import UpdateRolePermissionsRequest
from kinde_sdk.models.update_role_permissions_response import UpdateRolePermissionsResponse
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
    api_instance = kinde_sdk.RolesApi(api_client)
    role_id = 'role_id_example' # str | The identifier for the role.
    update_role_permissions_request = kinde_sdk.UpdateRolePermissionsRequest() # UpdateRolePermissionsRequest | 

    try:
        # Update role permissions
        api_response = api_instance.update_role_permissions(role_id, update_role_permissions_request)
        print("The response of RolesApi->update_role_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->update_role_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The identifier for the role. | 
 **update_role_permissions_request** | [**UpdateRolePermissionsRequest**](UpdateRolePermissionsRequest.md)|  | 

### Return type

[**UpdateRolePermissionsResponse**](UpdateRolePermissionsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Permissions successfully updated. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_roles**
> SuccessResponse update_roles(role_id, update_roles_request=update_roles_request)

Update role

Update a role

<div>
  <code>update:roles</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_roles_request import UpdateRolesRequest
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
    api_instance = kinde_sdk.RolesApi(api_client)
    role_id = 'role_id_example' # str | The identifier for the role.
    update_roles_request = kinde_sdk.UpdateRolesRequest() # UpdateRolesRequest | Role details. (optional)

    try:
        # Update role
        api_response = api_instance.update_roles(role_id, update_roles_request=update_roles_request)
        print("The response of RolesApi->update_roles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RolesApi->update_roles: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **str**| The identifier for the role. | 
 **update_roles_request** | [**UpdateRolesRequest**](UpdateRolesRequest.md)| Role details. | [optional] 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Role successfully updated |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

