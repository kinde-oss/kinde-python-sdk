# kinde_sdk.UsersApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_user**](UsersApi.md#create_user) | **POST** /api/v1/user | Create user
[**create_user_identity**](UsersApi.md#create_user_identity) | **POST** /api/v1/users/{user_id}/identities | Create identity
[**delete_user**](UsersApi.md#delete_user) | **DELETE** /api/v1/user | Delete user
[**delete_user_sessions**](UsersApi.md#delete_user_sessions) | **DELETE** /api/v1/users/{user_id}/sessions | Delete user sessions
[**get_user_data**](UsersApi.md#get_user_data) | **GET** /api/v1/user | Get user
[**get_user_identities**](UsersApi.md#get_user_identities) | **GET** /api/v1/users/{user_id}/identities | Get identities
[**get_user_property_values**](UsersApi.md#get_user_property_values) | **GET** /api/v1/users/{user_id}/properties | Get property values
[**get_user_sessions**](UsersApi.md#get_user_sessions) | **GET** /api/v1/users/{user_id}/sessions | Get user sessions
[**get_users**](UsersApi.md#get_users) | **GET** /api/v1/users | Get users
[**get_users_mfa**](UsersApi.md#get_users_mfa) | **GET** /api/v1/users/{user_id}/mfa | Get user&#39;s MFA configuration
[**refresh_user_claims**](UsersApi.md#refresh_user_claims) | **POST** /api/v1/users/{user_id}/refresh_claims | Refresh User Claims and Invalidate Cache
[**reset_users_mfa**](UsersApi.md#reset_users_mfa) | **DELETE** /api/v1/users/{user_id}/mfa/{factor_id} | Reset specific environment MFA for a user
[**reset_users_mfa_all**](UsersApi.md#reset_users_mfa_all) | **DELETE** /api/v1/users/{user_id}/mfa | Reset all environment MFA for a user
[**set_user_password**](UsersApi.md#set_user_password) | **PUT** /api/v1/users/{user_id}/password | Set User password
[**update_user**](UsersApi.md#update_user) | **PATCH** /api/v1/user | Update user
[**update_user_feature_flag_override**](UsersApi.md#update_user_feature_flag_override) | **PATCH** /api/v1/users/{user_id}/feature_flags/{feature_flag_key} | Update User Feature Flag Override
[**update_user_properties**](UsersApi.md#update_user_properties) | **PATCH** /api/v1/users/{user_id}/properties | Update Property values
[**update_user_property**](UsersApi.md#update_user_property) | **PUT** /api/v1/users/{user_id}/properties/{property_key} | Update Property value


# **create_user**
> CreateUserResponse create_user(create_user_request=create_user_request)

Create user

Creates a user record and optionally zero or more identities for the user. An example identity could be the email
address of the user.

<div>
  <code>create:users</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_user_request import CreateUserRequest
from kinde_sdk.models.create_user_response import CreateUserResponse
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
    api_instance = kinde_sdk.UsersApi(api_client)
    create_user_request = kinde_sdk.CreateUserRequest() # CreateUserRequest | The details of the user to create. (optional)

    try:
        # Create user
        api_response = api_instance.create_user(create_user_request=create_user_request)
        print("The response of UsersApi->create_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->create_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_user_request** | [**CreateUserRequest**](CreateUserRequest.md)| The details of the user to create. | [optional] 

### Return type

[**CreateUserResponse**](CreateUserResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User successfully created. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_identity**
> CreateIdentityResponse create_user_identity(user_id, create_user_identity_request=create_user_identity_request)

Create identity

Creates an identity for a user.

<div>
  <code>create:user_identities</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_identity_response import CreateIdentityResponse
from kinde_sdk.models.create_user_identity_request import CreateUserIdentityRequest
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'user_id_example' # str | The user's ID.
    create_user_identity_request = kinde_sdk.CreateUserIdentityRequest() # CreateUserIdentityRequest | The identity details. (optional)

    try:
        # Create identity
        api_response = api_instance.create_user_identity(user_id, create_user_identity_request=create_user_identity_request)
        print("The response of UsersApi->create_user_identity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->create_user_identity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The user&#39;s ID. | 
 **create_user_identity_request** | [**CreateUserIdentityRequest**](CreateUserIdentityRequest.md)| The identity details. | [optional] 

### Return type

[**CreateIdentityResponse**](CreateIdentityResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Identity successfully created. |  -  |
**400** | Error creating identity. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user**
> SuccessResponse delete_user(id, is_delete_profile=is_delete_profile)

Delete user

Delete a user record.

<div>
  <code>delete:users</code>
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
    api_instance = kinde_sdk.UsersApi(api_client)
    id = 'kp_c3143a4b50ad43c88e541d9077681782' # str | The user's id.
    is_delete_profile = true # bool | Delete all data and remove the user's profile from all of Kinde, including the subscriber list (optional)

    try:
        # Delete user
        api_response = api_instance.delete_user(id, is_delete_profile=is_delete_profile)
        print("The response of UsersApi->delete_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->delete_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user&#39;s id. | 
 **is_delete_profile** | **bool**| Delete all data and remove the user&#39;s profile from all of Kinde, including the subscriber list | [optional] 

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
**200** | User successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_sessions**
> SuccessResponse delete_user_sessions(user_id)

Delete user sessions

Invalidate user sessions.

<div>
  <code>delete:user_sessions</code>
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'kp_c3143a4b50ad43c88e541d9077681782' # str | The identifier for the user

    try:
        # Delete user sessions
        api_response = api_instance.delete_user_sessions(user_id)
        print("The response of UsersApi->delete_user_sessions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->delete_user_sessions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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
**200** | User sessions successfully invalidated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**404** | The specified resource was not found |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_data**
> User get_user_data(id, expand=expand)

Get user

Retrieve a user record.

<div>
  <code>read:users</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.user import User
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
    api_instance = kinde_sdk.UsersApi(api_client)
    id = 'id_example' # str | The user's id.
    expand = 'expand_example' # str | Specify additional data to retrieve. Use \"organizations\" and/or \"identities\". (optional)

    try:
        # Get user
        api_response = api_instance.get_user_data(id, expand=expand)
        print("The response of UsersApi->get_user_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->get_user_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user&#39;s id. | 
 **expand** | **str**| Specify additional data to retrieve. Use \&quot;organizations\&quot; and/or \&quot;identities\&quot;. | [optional] 

### Return type

[**User**](User.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_identities**
> GetIdentitiesResponse get_user_identities(user_id, starting_after=starting_after, ending_before=ending_before)

Get identities

Gets a list of identities for an user by ID.

<div>
  <code>read:user_identities</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_identities_response import GetIdentitiesResponse
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'user_id_example' # str | The user's ID.
    starting_after = 'starting_after_example' # str | The ID of the identity to start after. (optional)
    ending_before = 'ending_before_example' # str | The ID of the identity to end before. (optional)

    try:
        # Get identities
        api_response = api_instance.get_user_identities(user_id, starting_after=starting_after, ending_before=ending_before)
        print("The response of UsersApi->get_user_identities:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->get_user_identities: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The user&#39;s ID. | 
 **starting_after** | **str**| The ID of the identity to start after. | [optional] 
 **ending_before** | **str**| The ID of the identity to end before. | [optional] 

### Return type

[**GetIdentitiesResponse**](GetIdentitiesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Identities successfully retrieved. |  -  |
**400** | Bad request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_property_values**
> GetPropertyValuesResponse get_user_property_values(user_id)

Get property values

Gets properties for an user by ID.

<div>
  <code>read:user_properties</code>
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'user_id_example' # str | The user's ID.

    try:
        # Get property values
        api_response = api_instance.get_user_property_values(user_id)
        print("The response of UsersApi->get_user_property_values:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->get_user_property_values: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The user&#39;s ID. | 

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

# **get_user_sessions**
> GetUserSessionsResponse get_user_sessions(user_id)

Get user sessions

Retrieve the list of active sessions for a specific user.

<div>
  <code>read:user_sessions</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_user_sessions_response import GetUserSessionsResponse
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'kp_c3143a4b50ad43c88e541d9077681782' # str | The identifier for the user

    try:
        # Get user sessions
        api_response = api_instance.get_user_sessions(user_id)
        print("The response of UsersApi->get_user_sessions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->get_user_sessions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The identifier for the user | 

### Return type

[**GetUserSessionsResponse**](GetUserSessionsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved user sessions. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**404** | The specified resource was not found |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users**
> UsersResponse get_users(page_size=page_size, user_id=user_id, next_token=next_token, email=email, username=username, expand=expand, has_organization=has_organization)

Get users

The returned list can be sorted by full name or email address in ascending or descending order. The number of records to return at a time can also be controlled using the `page_size` query string parameter.

<div>
  <code>read:users</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.users_response import UsersResponse
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
    api_instance = kinde_sdk.UsersApi(api_client)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    user_id = 'user_id_example' # str | Filter the results by User ID. The query string should be comma separated and url encoded. (optional)
    next_token = 'next_token_example' # str | A string to get the next page of results if there are more results. (optional)
    email = 'email_example' # str | Filter the results by email address. The query string should be comma separated and url encoded. (optional)
    username = 'username_example' # str | Filter the results by username. The query string should be comma separated and url encoded. (optional)
    expand = 'expand_example' # str | Specify additional data to retrieve. Use \"organizations\" and/or \"identities\". (optional)
    has_organization = True # bool | Filter the results by if the user has at least one organization assigned. (optional)

    try:
        # Get users
        api_response = api_instance.get_users(page_size=page_size, user_id=user_id, next_token=next_token, email=email, username=username, expand=expand, has_organization=has_organization)
        print("The response of UsersApi->get_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->get_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **user_id** | **str**| Filter the results by User ID. The query string should be comma separated and url encoded. | [optional] 
 **next_token** | **str**| A string to get the next page of results if there are more results. | [optional] 
 **email** | **str**| Filter the results by email address. The query string should be comma separated and url encoded. | [optional] 
 **username** | **str**| Filter the results by username. The query string should be comma separated and url encoded. | [optional] 
 **expand** | **str**| Specify additional data to retrieve. Use \&quot;organizations\&quot; and/or \&quot;identities\&quot;. | [optional] 
 **has_organization** | **bool**| Filter the results by if the user has at least one organization assigned. | [optional] 

### Return type

[**UsersResponse**](UsersResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Users successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users_mfa**
> GetUserMfaResponse get_users_mfa(user_id)

Get user's MFA configuration

Get a user’s MFA configuration.

<div>
  <code>read:user_mfa</code>
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'kp_c3143a4b50ad43c88e541d9077681782' # str | The identifier for the user

    try:
        # Get user's MFA configuration
        api_response = api_instance.get_users_mfa(user_id)
        print("The response of UsersApi->get_users_mfa:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->get_users_mfa: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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

# **refresh_user_claims**
> SuccessResponse refresh_user_claims(user_id)

Refresh User Claims and Invalidate Cache

Refreshes the user's claims and invalidates the current cache.

<div>
  <code>update:user_refresh_claims</code>
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'user_id_example' # str | The id of the user whose claims needs to be updated.

    try:
        # Refresh User Claims and Invalidate Cache
        api_response = api_instance.refresh_user_claims(user_id)
        print("The response of UsersApi->refresh_user_claims:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->refresh_user_claims: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The id of the user whose claims needs to be updated. | 

### Return type

[**SuccessResponse**](SuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Claims successfully refreshed. |  -  |
**400** | Bad request. |  -  |
**403** | Bad request. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_users_mfa**
> SuccessResponse reset_users_mfa(user_id, factor_id)

Reset specific environment MFA for a user

Reset a specific environment MFA factor for a user.

<div>
  <code>delete:user_mfa</code>
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'kp_c3143a4b50ad43c88e541d9077681782' # str | The identifier for the user
    factor_id = 'mfa_0193278a00ac29b3f6d4e4d462d55c47' # str | The identifier for the MFA factor

    try:
        # Reset specific environment MFA for a user
        api_response = api_instance.reset_users_mfa(user_id, factor_id)
        print("The response of UsersApi->reset_users_mfa:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->reset_users_mfa: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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

# **reset_users_mfa_all**
> SuccessResponse reset_users_mfa_all(user_id)

Reset all environment MFA for a user

Reset all environment MFA factors for a user.

<div>
  <code>delete:user_mfa</code>
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'kp_c3143a4b50ad43c88e541d9077681782' # str | The identifier for the user

    try:
        # Reset all environment MFA for a user
        api_response = api_instance.reset_users_mfa_all(user_id)
        print("The response of UsersApi->reset_users_mfa_all:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->reset_users_mfa_all: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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

# **set_user_password**
> SuccessResponse set_user_password(user_id, set_user_password_request)

Set User password

Set user password.

<div>
  <code>update:user_passwords</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.set_user_password_request import SetUserPasswordRequest
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'user_id_example' # str | The identifier for the user
    set_user_password_request = kinde_sdk.SetUserPasswordRequest() # SetUserPasswordRequest | Password details.

    try:
        # Set User password
        api_response = api_instance.set_user_password(user_id, set_user_password_request)
        print("The response of UsersApi->set_user_password:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->set_user_password: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The identifier for the user | 
 **set_user_password_request** | [**SetUserPasswordRequest**](SetUserPasswordRequest.md)| Password details. | 

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
**200** | User successfully created. |  -  |
**400** | Error creating user. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user**
> UpdateUserResponse update_user(id, update_user_request)

Update user

Update a user record.

<div>
  <code>update:users</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.update_user_request import UpdateUserRequest
from kinde_sdk.models.update_user_response import UpdateUserResponse
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
    api_instance = kinde_sdk.UsersApi(api_client)
    id = 'id_example' # str | The user's id.
    update_user_request = kinde_sdk.UpdateUserRequest() # UpdateUserRequest | The user to update.

    try:
        # Update user
        api_response = api_instance.update_user(id, update_user_request)
        print("The response of UsersApi->update_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->update_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| The user&#39;s id. | 
 **update_user_request** | [**UpdateUserRequest**](UpdateUserRequest.md)| The user to update. | 

### Return type

[**UpdateUserResponse**](UpdateUserResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_feature_flag_override**
> SuccessResponse update_user_feature_flag_override(user_id, feature_flag_key, value)

Update User Feature Flag Override

Update user feature flag override.

<div>
  <code>update:user_feature_flags</code>
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'user_id_example' # str | The identifier for the user
    feature_flag_key = 'feature_flag_key_example' # str | The identifier for the feature flag
    value = 'value_example' # str | Override value

    try:
        # Update User Feature Flag Override
        api_response = api_instance.update_user_feature_flag_override(user_id, feature_flag_key, value)
        print("The response of UsersApi->update_user_feature_flag_override:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->update_user_feature_flag_override: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The identifier for the user | 
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

# **update_user_properties**
> SuccessResponse update_user_properties(user_id, update_organization_properties_request)

Update Property values

Update property values.

<div>
  <code>update:user_properties</code>
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'user_id_example' # str | The identifier for the user
    update_organization_properties_request = kinde_sdk.UpdateOrganizationPropertiesRequest() # UpdateOrganizationPropertiesRequest | Properties to update.

    try:
        # Update Property values
        api_response = api_instance.update_user_properties(user_id, update_organization_properties_request)
        print("The response of UsersApi->update_user_properties:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->update_user_properties: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The identifier for the user | 
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

# **update_user_property**
> SuccessResponse update_user_property(user_id, property_key, value)

Update Property value

Update property value.

<div>
  <code>update:user_properties</code>
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
    api_instance = kinde_sdk.UsersApi(api_client)
    user_id = 'user_id_example' # str | The identifier for the user
    property_key = 'property_key_example' # str | The identifier for the property
    value = 'value_example' # str | The new property value

    try:
        # Update Property value
        api_response = api_instance.update_user_property(user_id, property_key, value)
        print("The response of UsersApi->update_user_property:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->update_user_property: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **str**| The identifier for the user | 
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

