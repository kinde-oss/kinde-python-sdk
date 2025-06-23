# kinde_sdk.OrganizationsApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_organization_logo**](OrganizationsApi.md#add_organization_logo) | **POST** /api/v1/organizations/{org_code}/logos/{type} | Add organization logo
[**add_organization_user_api_scope**](OrganizationsApi.md#add_organization_user_api_scope) | **POST** /api/v1/organizations/{org_code}/users/{user_id}/apis/{api_id}/scopes/{scope_id} | Add scope to organization user api
[**add_organization_users**](OrganizationsApi.md#add_organization_users) | **POST** /api/v1/organizations/{org_code}/users | Add Organization Users
[**create_organization**](OrganizationsApi.md#create_organization) | **POST** /api/v1/organization | Create organization
[**create_organization_user_permission**](OrganizationsApi.md#create_organization_user_permission) | **POST** /api/v1/organizations/{org_code}/users/{user_id}/permissions | Add Organization User Permission
[**create_organization_user_role**](OrganizationsApi.md#create_organization_user_role) | **POST** /api/v1/organizations/{org_code}/users/{user_id}/roles | Add Organization User Role
[**delete_organization**](OrganizationsApi.md#delete_organization) | **DELETE** /api/v1/organization/{org_code} | Delete Organization
[**delete_organization_feature_flag_override**](OrganizationsApi.md#delete_organization_feature_flag_override) | **DELETE** /api/v1/organizations/{org_code}/feature_flags/{feature_flag_key} | Delete Organization Feature Flag Override
[**delete_organization_feature_flag_overrides**](OrganizationsApi.md#delete_organization_feature_flag_overrides) | **DELETE** /api/v1/organizations/{org_code}/feature_flags | Delete Organization Feature Flag Overrides
[**delete_organization_handle**](OrganizationsApi.md#delete_organization_handle) | **DELETE** /api/v1/organization/{org_code}/handle | Delete organization handle
[**delete_organization_logo**](OrganizationsApi.md#delete_organization_logo) | **DELETE** /api/v1/organizations/{org_code}/logos/{type} | Delete organization logo
[**delete_organization_user_api_scope**](OrganizationsApi.md#delete_organization_user_api_scope) | **DELETE** /api/v1/organizations/{org_code}/users/{user_id}/apis/{api_id}/scopes/{scope_id} | Delete scope from organization user API
[**delete_organization_user_permission**](OrganizationsApi.md#delete_organization_user_permission) | **DELETE** /api/v1/organizations/{org_code}/users/{user_id}/permissions/{permission_id} | Delete Organization User Permission
[**delete_organization_user_role**](OrganizationsApi.md#delete_organization_user_role) | **DELETE** /api/v1/organizations/{org_code}/users/{user_id}/roles/{role_id} | Delete Organization User Role
[**enable_org_connection**](OrganizationsApi.md#enable_org_connection) | **POST** /api/v1/organizations/{organization_code}/connections/{connection_id} | Enable connection
[**get_org_user_mfa**](OrganizationsApi.md#get_org_user_mfa) | **GET** /api/v1/organizations/{org_code}/users/{user_id}/mfa | Get an organization user&#39;s MFA configuration
[**get_organization**](OrganizationsApi.md#get_organization) | **GET** /api/v1/organization | Get organization
[**get_organization_connections**](OrganizationsApi.md#get_organization_connections) | **GET** /api/v1/organizations/{organization_code}/connections | Get connections
[**get_organization_feature_flags**](OrganizationsApi.md#get_organization_feature_flags) | **GET** /api/v1/organizations/{org_code}/feature_flags | List Organization Feature Flags
[**get_organization_property_values**](OrganizationsApi.md#get_organization_property_values) | **GET** /api/v1/organizations/{org_code}/properties | Get Organization Property Values
[**get_organization_user_permissions**](OrganizationsApi.md#get_organization_user_permissions) | **GET** /api/v1/organizations/{org_code}/users/{user_id}/permissions | List Organization User Permissions
[**get_organization_user_roles**](OrganizationsApi.md#get_organization_user_roles) | **GET** /api/v1/organizations/{org_code}/users/{user_id}/roles | List Organization User Roles
[**get_organization_users**](OrganizationsApi.md#get_organization_users) | **GET** /api/v1/organizations/{org_code}/users | Get organization users
[**get_organizations**](OrganizationsApi.md#get_organizations) | **GET** /api/v1/organizations | Get organizations
[**read_organization_logo**](OrganizationsApi.md#read_organization_logo) | **GET** /api/v1/organizations/{org_code}/logos | Read organization logo details
[**remove_org_connection**](OrganizationsApi.md#remove_org_connection) | **DELETE** /api/v1/organizations/{organization_code}/connections/{connection_id} | Remove connection
[**remove_organization_user**](OrganizationsApi.md#remove_organization_user) | **DELETE** /api/v1/organizations/{org_code}/users/{user_id} | Remove Organization User
[**replace_organization_mfa**](OrganizationsApi.md#replace_organization_mfa) | **PUT** /api/v1/organizations/{org_code}/mfa | Replace Organization MFA Configuration
[**reset_org_user_mfa**](OrganizationsApi.md#reset_org_user_mfa) | **DELETE** /api/v1/organizations/{org_code}/users/{user_id}/mfa/{factor_id} | Reset specific organization MFA for a user
[**reset_org_user_mfa_all**](OrganizationsApi.md#reset_org_user_mfa_all) | **DELETE** /api/v1/organizations/{org_code}/users/{user_id}/mfa | Reset all organization MFA for a user
[**update_organization**](OrganizationsApi.md#update_organization) | **PATCH** /api/v1/organization/{org_code} | Update Organization
[**update_organization_feature_flag_override**](OrganizationsApi.md#update_organization_feature_flag_override) | **PATCH** /api/v1/organizations/{org_code}/feature_flags/{feature_flag_key} | Update Organization Feature Flag Override
[**update_organization_properties**](OrganizationsApi.md#update_organization_properties) | **PATCH** /api/v1/organizations/{org_code}/properties | Update Organization Property values
[**update_organization_property**](OrganizationsApi.md#update_organization_property) | **PUT** /api/v1/organizations/{org_code}/properties/{property_key} | Update Organization Property value
[**update_organization_sessions**](OrganizationsApi.md#update_organization_sessions) | **PATCH** /api/v1/organizations/{org_code}/sessions | Update organization session configuration
[**update_organization_users**](OrganizationsApi.md#update_organization_users) | **PATCH** /api/v1/organizations/{org_code}/users | Update Organization Users


# **add_organization_logo**
> SuccessResponse add_organization_logo(org_code, type, logo)

Add organization logo

Add organization logo

<div>
  <code>update:organizations</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_1ccfb819462' # str | The organization's code.
    type = 'dark' # str | The type of logo to add.
    logo = None # bytearray | The logo file to upload.

    try:
        # Add organization logo
        api_response = api_instance.add_organization_logo(org_code, type, logo)
        print("The response of OrganizationsApi->add_organization_logo:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->add_organization_logo: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **type** | **str**| The type of logo to add. | 
 **logo** | **bytearray**| The logo file to upload. | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Organization logo successfully updated |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_organization_user_api_scope**
> add_organization_user_api_scope(org_code, user_id, api_id, scope_id)

Add scope to organization user api

Add a scope to an organization user api.

<div>
  <code>create:organization_user_api_scopes</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The identifier for the organization.
    user_id = 'kp_5ce676e5d6a24bc9aac2fba35a46e958' # str | User ID
    api_id = '838f208d006a482dbd8cdb79a9889f68' # str | API ID
    scope_id = 'api_scope_019391daf58d87d8a7213419c016ac95' # str | Scope ID

    try:
        # Add scope to organization user api
        api_instance.add_organization_user_api_scope(org_code, user_id, api_id, scope_id)
    except Exception as e:
        print("Exception when calling OrganizationsApi->add_organization_user_api_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization. | 
 **user_id** | **str**| User ID | 
 **api_id** | **str**| API ID | 
 **scope_id** | **str**| Scope ID | 

### Return type

void (empty response body)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | API scope successfully added to organization user api |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_organization_users**
> AddOrganizationUsersResponse add_organization_users(org_code, add_organization_users_request=add_organization_users_request)

Add Organization Users

Add existing users to an organization.

<div>
  <code>create:organization_users</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.add_organization_users_request import AddOrganizationUsersRequest
from kinde_sdk.models.add_organization_users_response import AddOrganizationUsersResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.
    add_organization_users_request = kinde_sdk.AddOrganizationUsersRequest() # AddOrganizationUsersRequest |  (optional)

    try:
        # Add Organization Users
        api_response = api_instance.add_organization_users(org_code, add_organization_users_request=add_organization_users_request)
        print("The response of OrganizationsApi->add_organization_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->add_organization_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **add_organization_users_request** | [**AddOrganizationUsersRequest**](AddOrganizationUsersRequest.md)|  | [optional] 

### Return type

[**AddOrganizationUsersResponse**](AddOrganizationUsersResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Users successfully added. |  -  |
**204** | No users added. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_organization**
> CreateOrganizationResponse create_organization(create_organization_request)

Create organization

Create a new organization. To learn more read about [multi tenancy using organizations](https://docs.kinde.com/build/organizations/multi-tenancy-using-organizations/)

<div>
  <code>create:organizations</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_organization_request import CreateOrganizationRequest
from kinde_sdk.models.create_organization_response import CreateOrganizationResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    create_organization_request = kinde_sdk.CreateOrganizationRequest() # CreateOrganizationRequest | Organization details.

    try:
        # Create organization
        api_response = api_instance.create_organization(create_organization_request)
        print("The response of OrganizationsApi->create_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->create_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_organization_request** | [**CreateOrganizationRequest**](CreateOrganizationRequest.md)| Organization details. | 

### Return type

[**CreateOrganizationResponse**](CreateOrganizationResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Organization successfully created. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_organization_user_permission**
> SuccessResponse create_organization_user_permission(org_code, user_id, create_organization_user_permission_request)

Add Organization User Permission

Add permission to an organization user.

<div>
  <code>create:organization_user_permissions</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_organization_user_permission_request import CreateOrganizationUserPermissionRequest
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.
    user_id = 'user_id_example' # str | The user's id.
    create_organization_user_permission_request = kinde_sdk.CreateOrganizationUserPermissionRequest() # CreateOrganizationUserPermissionRequest | Permission details.

    try:
        # Add Organization User Permission
        api_response = api_instance.create_organization_user_permission(org_code, user_id, create_organization_user_permission_request)
        print("The response of OrganizationsApi->create_organization_user_permission:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->create_organization_user_permission: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **user_id** | **str**| The user&#39;s id. | 
 **create_organization_user_permission_request** | [**CreateOrganizationUserPermissionRequest**](CreateOrganizationUserPermissionRequest.md)| Permission details. | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User permission successfully updated. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_organization_user_role**
> SuccessResponse create_organization_user_role(org_code, user_id, create_organization_user_role_request)

Add Organization User Role

Add role to an organization user.

<div>
  <code>create:organization_user_roles</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_organization_user_role_request import CreateOrganizationUserRoleRequest
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.
    user_id = 'user_id_example' # str | The user's id.
    create_organization_user_role_request = kinde_sdk.CreateOrganizationUserRoleRequest() # CreateOrganizationUserRoleRequest | Role details.

    try:
        # Add Organization User Role
        api_response = api_instance.create_organization_user_role(org_code, user_id, create_organization_user_role_request)
        print("The response of OrganizationsApi->create_organization_user_role:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->create_organization_user_role: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **user_id** | **str**| The user&#39;s id. | 
 **create_organization_user_role_request** | [**CreateOrganizationUserRoleRequest**](CreateOrganizationUserRoleRequest.md)| Role details. | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Role successfully added. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization**
> SuccessResponse delete_organization(org_code)

Delete Organization

Delete an organization.

<div>
  <code>delete:organizations</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The identifier for the organization.

    try:
        # Delete Organization
        api_response = api_instance.delete_organization(org_code)
        print("The response of OrganizationsApi->delete_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization. | 

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
**200** | Organization successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**404** | The specified resource was not found |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization_feature_flag_override**
> SuccessResponse delete_organization_feature_flag_override(org_code, feature_flag_key)

Delete Organization Feature Flag Override

Delete organization feature flag override.

<div>
  <code>delete:organization_feature_flags</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The identifier for the organization.
    feature_flag_key = 'feature_flag_key_example' # str | The identifier for the feature flag.

    try:
        # Delete Organization Feature Flag Override
        api_response = api_instance.delete_organization_feature_flag_override(org_code, feature_flag_key)
        print("The response of OrganizationsApi->delete_organization_feature_flag_override:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_organization_feature_flag_override: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization. | 
 **feature_flag_key** | **str**| The identifier for the feature flag. | 

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
**200** | Feature flag override successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization_feature_flag_overrides**
> SuccessResponse delete_organization_feature_flag_overrides(org_code)

Delete Organization Feature Flag Overrides

Delete all organization feature flag overrides.

<div>
  <code>delete:organization_feature_flags</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The identifier for the organization.

    try:
        # Delete Organization Feature Flag Overrides
        api_response = api_instance.delete_organization_feature_flag_overrides(org_code)
        print("The response of OrganizationsApi->delete_organization_feature_flag_overrides:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_organization_feature_flag_overrides: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization. | 

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
**200** | Feature flag overrides successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization_handle**
> SuccessResponse delete_organization_handle(org_code)

Delete organization handle

Delete organization handle

<div>
  <code>delete:organization_handles</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.

    try:
        # Delete organization handle
        api_response = api_instance.delete_organization_handle(org_code)
        print("The response of OrganizationsApi->delete_organization_handle:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_organization_handle: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 

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
**200** | Handle successfully deleted. |  -  |
**400** | Bad request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization_logo**
> SuccessResponse delete_organization_logo(org_code, type)

Delete organization logo

Delete organization logo

<div>
  <code>update:organizations</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_1ccfb819462' # str | The organization's code.
    type = 'dark' # str | The type of logo to delete.

    try:
        # Delete organization logo
        api_response = api_instance.delete_organization_logo(org_code, type)
        print("The response of OrganizationsApi->delete_organization_logo:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_organization_logo: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **type** | **str**| The type of logo to delete. | 

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
**200** | Organization logo successfully deleted |  -  |
**204** | No logo found to delete |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization_user_api_scope**
> delete_organization_user_api_scope(org_code, user_id, api_id, scope_id)

Delete scope from organization user API

Delete a scope from an organization user api you previously created.

<div>
  <code>delete:organization_user_api_scopes</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The identifier for the organization.
    user_id = 'kp_5ce676e5d6a24bc9aac2fba35a46e958' # str | User ID
    api_id = '838f208d006a482dbd8cdb79a9889f68' # str | API ID
    scope_id = 'api_scope_019391daf58d87d8a7213419c016ac95' # str | Scope ID

    try:
        # Delete scope from organization user API
        api_instance.delete_organization_user_api_scope(org_code, user_id, api_id, scope_id)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_organization_user_api_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization. | 
 **user_id** | **str**| User ID | 
 **api_id** | **str**| API ID | 
 **scope_id** | **str**| Scope ID | 

### Return type

void (empty response body)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Organization user API scope successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization_user_permission**
> SuccessResponse delete_organization_user_permission(org_code, user_id, permission_id)

Delete Organization User Permission

Delete permission for an organization user.

<div>
  <code>delete:organization_user_permissions</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.
    user_id = 'user_id_example' # str | The user's id.
    permission_id = 'permission_id_example' # str | The permission id.

    try:
        # Delete Organization User Permission
        api_response = api_instance.delete_organization_user_permission(org_code, user_id, permission_id)
        print("The response of OrganizationsApi->delete_organization_user_permission:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_organization_user_permission: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **user_id** | **str**| The user&#39;s id. | 
 **permission_id** | **str**| The permission id. | 

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
**200** | User successfully removed. |  -  |
**400** | Error creating user. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_organization_user_role**
> SuccessResponse delete_organization_user_role(org_code, user_id, role_id)

Delete Organization User Role

Delete role for an organization user.

<div>
  <code>delete:organization_user_roles</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.
    user_id = 'user_id_example' # str | The user's id.
    role_id = 'role_id_example' # str | The role id.

    try:
        # Delete Organization User Role
        api_response = api_instance.delete_organization_user_role(org_code, user_id, role_id)
        print("The response of OrganizationsApi->delete_organization_user_role:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->delete_organization_user_role: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **user_id** | **str**| The user&#39;s id. | 
 **role_id** | **str**| The role id. | 

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
**200** | User successfully removed. |  -  |
**400** | Error creating user. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enable_org_connection**
> enable_org_connection(organization_code, connection_id)

Enable connection

Enable an auth connection for an organization.

<div>
  <code>create:organization_connections</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    organization_code = 'org_7d45b01ef13' # str | The unique code for the organization.
    connection_id = 'conn_0192c16abb53b44277e597d31877ba5b' # str | The identifier for the connection.

    try:
        # Enable connection
        api_instance.enable_org_connection(organization_code, connection_id)
    except Exception as e:
        print("Exception when calling OrganizationsApi->enable_org_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_code** | **str**| The unique code for the organization. | 
 **connection_id** | **str**| The identifier for the connection. | 

### Return type

void (empty response body)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Connection successfully enabled. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_org_user_mfa**
> GetUserMfaResponse get_org_user_mfa(org_code, user_id)

Get an organization user's MFA configuration

Get an organization user’s MFA configuration.

<div>
  <code>read:organization_user_mfa</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_user_mfa_response import GetUserMfaResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_1ccfb819462' # str | The identifier for the organization.
    user_id = 'kp_c3143a4b50ad43c88e541d9077681782' # str | The identifier for the user

    try:
        # Get an organization user's MFA configuration
        api_response = api_instance.get_org_user_mfa(org_code, user_id)
        print("The response of OrganizationsApi->get_org_user_mfa:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_org_user_mfa: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization. | 
 **user_id** | **str**| The identifier for the user | 

### Return type

[**GetUserMfaResponse**](GetUserMfaResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieve user&#39;s MFA configuration. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**404** | The specified resource was not found |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization**
> GetOrganizationResponse get_organization(code=code)

Get organization

Retrieve organization details by code.

<div>
  <code>read:organizations</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_organization_response import GetOrganizationResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    code = 'org_1ccfb819462' # str | The organization's code. (optional)

    try:
        # Get organization
        api_response = api_instance.get_organization(code=code)
        print("The response of OrganizationsApi->get_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **code** | **str**| The organization&#39;s code. | [optional] 

### Return type

[**GetOrganizationResponse**](GetOrganizationResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Organization successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization_connections**
> GetConnectionsResponse get_organization_connections(organization_code)

Get connections

Gets all connections for an organization.

<div>
  <code>read:organization_connections</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_connections_response import GetConnectionsResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    organization_code = 'org_7d45b01ef13' # str | The organization code.

    try:
        # Get connections
        api_response = api_instance.get_organization_connections(organization_code)
        print("The response of OrganizationsApi->get_organization_connections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_organization_connections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_code** | **str**| The organization code. | 

### Return type

[**GetConnectionsResponse**](GetConnectionsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Organization connections successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization_feature_flags**
> GetOrganizationFeatureFlagsResponse get_organization_feature_flags(org_code)

List Organization Feature Flags

Get all organization feature flags.

<div>
  <code>read:organization_feature_flags</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_organization_feature_flags_response import GetOrganizationFeatureFlagsResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The identifier for the organization.

    try:
        # List Organization Feature Flags
        api_response = api_instance.get_organization_feature_flags(org_code)
        print("The response of OrganizationsApi->get_organization_feature_flags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_organization_feature_flags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization. | 

### Return type

[**GetOrganizationFeatureFlagsResponse**](GetOrganizationFeatureFlagsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Feature flag overrides successfully returned. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization_property_values**
> GetPropertyValuesResponse get_organization_property_values(org_code)

Get Organization Property Values

Gets properties for an organization by org code.

<div>
  <code>read:organization_properties</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_property_values_response import GetPropertyValuesResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.

    try:
        # Get Organization Property Values
        api_response = api_instance.get_organization_property_values(org_code)
        print("The response of OrganizationsApi->get_organization_property_values:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_organization_property_values: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 

### Return type

[**GetPropertyValuesResponse**](GetPropertyValuesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Properties successfully retrieved. |  -  |
**400** | Bad request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization_user_permissions**
> GetOrganizationsUserPermissionsResponse get_organization_user_permissions(org_code, user_id, expand=expand)

List Organization User Permissions

Get permissions for an organization user.

<div>
  <code>read:organization_user_permissions</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_organizations_user_permissions_response import GetOrganizationsUserPermissionsResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.
    user_id = 'user_id_example' # str | The user's id.
    expand = 'expand_example' # str | Specify additional data to retrieve. Use \"roles\". (optional)

    try:
        # List Organization User Permissions
        api_response = api_instance.get_organization_user_permissions(org_code, user_id, expand=expand)
        print("The response of OrganizationsApi->get_organization_user_permissions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_organization_user_permissions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **user_id** | **str**| The user&#39;s id. | 
 **expand** | **str**| Specify additional data to retrieve. Use \&quot;roles\&quot;. | [optional] 

### Return type

[**GetOrganizationsUserPermissionsResponse**](GetOrganizationsUserPermissionsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response with a list of user permissions. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization_user_roles**
> GetOrganizationsUserRolesResponse get_organization_user_roles(org_code, user_id)

List Organization User Roles

Get roles for an organization user.

<div>
  <code>read:organization_user_roles</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_organizations_user_roles_response import GetOrganizationsUserRolesResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.
    user_id = 'user_id_example' # str | The user's id.

    try:
        # List Organization User Roles
        api_response = api_instance.get_organization_user_roles(org_code, user_id)
        print("The response of OrganizationsApi->get_organization_user_roles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_organization_user_roles: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **user_id** | **str**| The user&#39;s id. | 

### Return type

[**GetOrganizationsUserRolesResponse**](GetOrganizationsUserRolesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response with a list of user roles. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organization_users**
> GetOrganizationUsersResponse get_organization_users(org_code, sort=sort, page_size=page_size, next_token=next_token, permissions=permissions, roles=roles)

Get organization users

Get user details for all members of an organization.

<div>
  <code>read:organization_users</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_organization_users_response import GetOrganizationUsersResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_1ccfb819462' # str | The organization's code.
    sort = 'email_asc' # str | Field and order to sort the result by. (optional)
    page_size = 10 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    next_token = 'MTo6OmlkX2FzYw==' # str | A string to get the next page of results if there are more results. (optional)
    permissions = 'admin' # str | Filter by user permissions comma separated (where all match) (optional)
    roles = 'manager' # str | Filter by user roles comma separated (where all match) (optional)

    try:
        # Get organization users
        api_response = api_instance.get_organization_users(org_code, sort=sort, page_size=page_size, next_token=next_token, permissions=permissions, roles=roles)
        print("The response of OrganizationsApi->get_organization_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_organization_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **sort** | **str**| Field and order to sort the result by. | [optional] 
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **next_token** | **str**| A string to get the next page of results if there are more results. | [optional] 
 **permissions** | **str**| Filter by user permissions comma separated (where all match) | [optional] 
 **roles** | **str**| Filter by user roles comma separated (where all match) | [optional] 

### Return type

[**GetOrganizationUsersResponse**](GetOrganizationUsersResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response with a list of organization users or an empty list. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_organizations**
> GetOrganizationsResponse get_organizations(sort=sort, page_size=page_size, next_token=next_token)

Get organizations

Get a list of organizations.

<div>
  <code>read:organizations</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_organizations_response import GetOrganizationsResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    sort = 'sort_example' # str | Field and order to sort the result by. (optional)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    next_token = 'next_token_example' # str | A string to get the next page of results if there are more results. (optional)

    try:
        # Get organizations
        api_response = api_instance.get_organizations(sort=sort, page_size=page_size, next_token=next_token)
        print("The response of OrganizationsApi->get_organizations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->get_organizations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sort** | **str**| Field and order to sort the result by. | [optional] 
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **next_token** | **str**| A string to get the next page of results if there are more results. | [optional] 

### Return type

[**GetOrganizationsResponse**](GetOrganizationsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Organizations successfully retreived. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **read_organization_logo**
> ReadLogoResponse read_organization_logo(org_code)

Read organization logo details

Read organization logo details

<div>
  <code>read:organizations</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.read_logo_response import ReadLogoResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_1ccfb819462' # str | The organization's code.

    try:
        # Read organization logo details
        api_response = api_instance.read_organization_logo(org_code)
        print("The response of OrganizationsApi->read_organization_logo:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->read_organization_logo: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 

### Return type

[**ReadLogoResponse**](ReadLogoResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved organization logo details |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_org_connection**
> SuccessResponse remove_org_connection(organization_code, connection_id)

Remove connection

Turn off an auth connection for an organization

<div>
  <code>delete:organization_connections</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    organization_code = 'org_7d45b01ef13' # str | The unique code for the organization.
    connection_id = 'conn_0192c16abb53b44277e597d31877ba5b' # str | The identifier for the connection.

    try:
        # Remove connection
        api_response = api_instance.remove_org_connection(organization_code, connection_id)
        print("The response of OrganizationsApi->remove_org_connection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->remove_org_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **organization_code** | **str**| The unique code for the organization. | 
 **connection_id** | **str**| The identifier for the connection. | 

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
**200** | Connection successfully removed. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_organization_user**
> SuccessResponse remove_organization_user(org_code, user_id)

Remove Organization User

Remove user from an organization.

<div>
  <code>delete:organization_users</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.
    user_id = 'user_id_example' # str | The user's id.

    try:
        # Remove Organization User
        api_response = api_instance.remove_organization_user(org_code, user_id)
        print("The response of OrganizationsApi->remove_organization_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->remove_organization_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **user_id** | **str**| The user&#39;s id. | 

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
**200** | User successfully removed from organization |  -  |
**400** | Error removing user |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_organization_mfa**
> SuccessResponse replace_organization_mfa(org_code, replace_organization_mfa_request)

Replace Organization MFA Configuration

Replace Organization MFA Configuration.

<div>
  <code>update:organization_mfa</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.replace_organization_mfa_request import ReplaceOrganizationMFARequest
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The identifier for the organization
    replace_organization_mfa_request = kinde_sdk.ReplaceOrganizationMFARequest() # ReplaceOrganizationMFARequest | MFA details.

    try:
        # Replace Organization MFA Configuration
        api_response = api_instance.replace_organization_mfa(org_code, replace_organization_mfa_request)
        print("The response of OrganizationsApi->replace_organization_mfa:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->replace_organization_mfa: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization | 
 **replace_organization_mfa_request** | [**ReplaceOrganizationMFARequest**](ReplaceOrganizationMFARequest.md)| MFA details. | 

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
**200** | MFA Configuration updated successfully. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_org_user_mfa**
> SuccessResponse reset_org_user_mfa(org_code, user_id, factor_id)

Reset specific organization MFA for a user

Reset a specific organization MFA factor for a user.

<div>
  <code>delete:organization_user_mfa</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_1ccfb819462' # str | The identifier for the organization.
    user_id = 'kp_c3143a4b50ad43c88e541d9077681782' # str | The identifier for the user
    factor_id = 'mfa_0193278a00ac29b3f6d4e4d462d55c47' # str | The identifier for the MFA factor

    try:
        # Reset specific organization MFA for a user
        api_response = api_instance.reset_org_user_mfa(org_code, user_id, factor_id)
        print("The response of OrganizationsApi->reset_org_user_mfa:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->reset_org_user_mfa: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization. | 
 **user_id** | **str**| The identifier for the user | 
 **factor_id** | **str**| The identifier for the MFA factor | 

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
**200** | User&#39;s MFA successfully reset. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**404** | The specified resource was not found |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_org_user_mfa_all**
> SuccessResponse reset_org_user_mfa_all(org_code, user_id)

Reset all organization MFA for a user

Reset all organization MFA factors for a user.

<div>
  <code>delete:organization_user_mfa</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_1ccfb819462' # str | The identifier for the organization.
    user_id = 'kp_c3143a4b50ad43c88e541d9077681782' # str | The identifier for the user

    try:
        # Reset all organization MFA for a user
        api_response = api_instance.reset_org_user_mfa_all(org_code, user_id)
        print("The response of OrganizationsApi->reset_org_user_mfa_all:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->reset_org_user_mfa_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization. | 
 **user_id** | **str**| The identifier for the user | 

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
**200** | User&#39;s MFA successfully reset. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**404** | The specified resource was not found |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_organization**
> SuccessResponse update_organization(org_code, expand=expand, update_organization_request=update_organization_request)

Update Organization

Update an organization.

<div>
  <code>update:organizations</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_organization_request import UpdateOrganizationRequest
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_1ccfb819462' # str | The identifier for the organization.
    expand = 'expand_example' # str | Specify additional data to retrieve. Use \"billing\". (optional)
    update_organization_request = kinde_sdk.UpdateOrganizationRequest() # UpdateOrganizationRequest | Organization details. (optional)

    try:
        # Update Organization
        api_response = api_instance.update_organization(org_code, expand=expand, update_organization_request=update_organization_request)
        print("The response of OrganizationsApi->update_organization:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->update_organization: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization. | 
 **expand** | **str**| Specify additional data to retrieve. Use \&quot;billing\&quot;. | [optional] 
 **update_organization_request** | [**UpdateOrganizationRequest**](UpdateOrganizationRequest.md)| Organization details. | [optional] 

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
**200** | Organization successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_organization_feature_flag_override**
> SuccessResponse update_organization_feature_flag_override(org_code, feature_flag_key, value)

Update Organization Feature Flag Override

Update organization feature flag override.

<div>
  <code>update:organization_feature_flags</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The identifier for the organization
    feature_flag_key = 'feature_flag_key_example' # str | The identifier for the feature flag
    value = 'value_example' # str | Override value

    try:
        # Update Organization Feature Flag Override
        api_response = api_instance.update_organization_feature_flag_override(org_code, feature_flag_key, value)
        print("The response of OrganizationsApi->update_organization_feature_flag_override:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->update_organization_feature_flag_override: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization | 
 **feature_flag_key** | **str**| The identifier for the feature flag | 
 **value** | **str**| Override value | 

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
**200** | Feature flag override successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_organization_properties**
> SuccessResponse update_organization_properties(org_code, update_organization_properties_request)

Update Organization Property values

Update organization property values.

<div>
  <code>update:organization_properties</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_organization_properties_request import UpdateOrganizationPropertiesRequest
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The identifier for the organization
    update_organization_properties_request = kinde_sdk.UpdateOrganizationPropertiesRequest() # UpdateOrganizationPropertiesRequest | Properties to update.

    try:
        # Update Organization Property values
        api_response = api_instance.update_organization_properties(org_code, update_organization_properties_request)
        print("The response of OrganizationsApi->update_organization_properties:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->update_organization_properties: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization | 
 **update_organization_properties_request** | [**UpdateOrganizationPropertiesRequest**](UpdateOrganizationPropertiesRequest.md)| Properties to update. | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Properties successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_organization_property**
> SuccessResponse update_organization_property(org_code, property_key, value)

Update Organization Property value

Update organization property value.

<div>
  <code>update:organization_properties</code>
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The identifier for the organization
    property_key = 'property_key_example' # str | The identifier for the property
    value = 'value_example' # str | The new property value

    try:
        # Update Organization Property value
        api_response = api_instance.update_organization_property(org_code, property_key, value)
        print("The response of OrganizationsApi->update_organization_property:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->update_organization_property: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The identifier for the organization | 
 **property_key** | **str**| The identifier for the property | 
 **value** | **str**| The new property value | 

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
**200** | Property successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_organization_sessions**
> SuccessResponse update_organization_sessions(org_code, update_organization_sessions_request)

Update organization session configuration

Update the organization's session configuration.

<div>
  <code>update:organizations</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_organization_sessions_request import UpdateOrganizationSessionsRequest
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_1ccfb819462' # str | The organization's code.
    update_organization_sessions_request = kinde_sdk.UpdateOrganizationSessionsRequest() # UpdateOrganizationSessionsRequest | Organization session configuration.

    try:
        # Update organization session configuration
        api_response = api_instance.update_organization_sessions(org_code, update_organization_sessions_request)
        print("The response of OrganizationsApi->update_organization_sessions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->update_organization_sessions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **update_organization_sessions_request** | [**UpdateOrganizationSessionsRequest**](UpdateOrganizationSessionsRequest.md)| Organization session configuration. | 

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
**200** | Organization sessions successfully updated |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_organization_users**
> UpdateOrganizationUsersResponse update_organization_users(org_code, update_organization_users_request=update_organization_users_request)

Update Organization Users

Update users that belong to an organization.

<div>
  <code>update:organization_users</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.update_organization_users_request import UpdateOrganizationUsersRequest
from kinde_sdk.models.update_organization_users_response import UpdateOrganizationUsersResponse
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
    api_instance = kinde_sdk.OrganizationsApi(api_client)
    org_code = 'org_code_example' # str | The organization's code.
    update_organization_users_request = kinde_sdk.UpdateOrganizationUsersRequest() # UpdateOrganizationUsersRequest |  (optional)

    try:
        # Update Organization Users
        api_response = api_instance.update_organization_users(org_code, update_organization_users_request=update_organization_users_request)
        print("The response of OrganizationsApi->update_organization_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationsApi->update_organization_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_code** | **str**| The organization&#39;s code. | 
 **update_organization_users_request** | [**UpdateOrganizationUsersRequest**](UpdateOrganizationUsersRequest.md)|  | [optional] 

### Return type

[**UpdateOrganizationUsersResponse**](UpdateOrganizationUsersResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Users successfully removed. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

