# kinde_sdk.EnvironmentVariablesApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_environment_variable**](EnvironmentVariablesApi.md#create_environment_variable) | **POST** /api/v1/environment_variables | Create environment variable
[**delete_environment_variable**](EnvironmentVariablesApi.md#delete_environment_variable) | **DELETE** /api/v1/environment_variables/{variable_id} | Delete environment variable
[**get_environment_variable**](EnvironmentVariablesApi.md#get_environment_variable) | **GET** /api/v1/environment_variables/{variable_id} | Get environment variable
[**get_environment_variables**](EnvironmentVariablesApi.md#get_environment_variables) | **GET** /api/v1/environment_variables | Get environment variables
[**update_environment_variable**](EnvironmentVariablesApi.md#update_environment_variable) | **PATCH** /api/v1/environment_variables/{variable_id} | Update environment variable


# **create_environment_variable**
> CreateEnvironmentVariableResponse create_environment_variable(create_environment_variable_request)

Create environment variable

Create a new environment variable. This feature is in beta and admin UI is not yet available.

<div>
  <code>create:environment_variables</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_environment_variable_request import CreateEnvironmentVariableRequest
from kinde_sdk.models.create_environment_variable_response import CreateEnvironmentVariableResponse
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
    api_instance = kinde_sdk.EnvironmentVariablesApi(api_client)
    create_environment_variable_request = kinde_sdk.CreateEnvironmentVariableRequest() # CreateEnvironmentVariableRequest | The environment variable details.

    try:
        # Create environment variable
        api_response = api_instance.create_environment_variable(create_environment_variable_request)
        print("The response of EnvironmentVariablesApi->create_environment_variable:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EnvironmentVariablesApi->create_environment_variable: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_environment_variable_request** | [**CreateEnvironmentVariableRequest**](CreateEnvironmentVariableRequest.md)| The environment variable details. | 

### Return type

[**CreateEnvironmentVariableResponse**](CreateEnvironmentVariableResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Environment variable successfully created. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_environment_variable**
> DeleteEnvironmentVariableResponse delete_environment_variable(variable_id)

Delete environment variable

Delete an environment variable you previously created. This feature is in beta and admin UI is not yet available.

<div>
  <code>delete:environment_variables</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.delete_environment_variable_response import DeleteEnvironmentVariableResponse
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
    api_instance = kinde_sdk.EnvironmentVariablesApi(api_client)
    variable_id = 'env_var_0192b1941f125645fa15bf28a662a0b3' # str | The environment variable's ID.

    try:
        # Delete environment variable
        api_response = api_instance.delete_environment_variable(variable_id)
        print("The response of EnvironmentVariablesApi->delete_environment_variable:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EnvironmentVariablesApi->delete_environment_variable: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **variable_id** | **str**| The environment variable&#39;s ID. | 

### Return type

[**DeleteEnvironmentVariableResponse**](DeleteEnvironmentVariableResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment variable successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_environment_variable**
> GetEnvironmentVariableResponse get_environment_variable(variable_id)

Get environment variable

Retrieve environment variable details by ID. This feature is in beta and admin UI is not yet available.

<div>
  <code>read:environment_variables</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_environment_variable_response import GetEnvironmentVariableResponse
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
    api_instance = kinde_sdk.EnvironmentVariablesApi(api_client)
    variable_id = 'env_var_0192b1941f125645fa15bf28a662a0b3' # str | The environment variable's ID.

    try:
        # Get environment variable
        api_response = api_instance.get_environment_variable(variable_id)
        print("The response of EnvironmentVariablesApi->get_environment_variable:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EnvironmentVariablesApi->get_environment_variable: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **variable_id** | **str**| The environment variable&#39;s ID. | 

### Return type

[**GetEnvironmentVariableResponse**](GetEnvironmentVariableResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment variable successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_environment_variables**
> GetEnvironmentVariablesResponse get_environment_variables()

Get environment variables

Get environment variables. This feature is in beta and admin UI is not yet available.

<div>
  <code>read:environment_variables</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_environment_variables_response import GetEnvironmentVariablesResponse
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
    api_instance = kinde_sdk.EnvironmentVariablesApi(api_client)

    try:
        # Get environment variables
        api_response = api_instance.get_environment_variables()
        print("The response of EnvironmentVariablesApi->get_environment_variables:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EnvironmentVariablesApi->get_environment_variables: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetEnvironmentVariablesResponse**](GetEnvironmentVariablesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response with a list of environment variables or an empty list. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_environment_variable**
> UpdateEnvironmentVariableResponse update_environment_variable(variable_id, update_environment_variable_request)

Update environment variable

Update an environment variable you previously created. This feature is in beta and admin UI is not yet available.

<div>
  <code>update:environment_variables</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.update_environment_variable_request import UpdateEnvironmentVariableRequest
from kinde_sdk.models.update_environment_variable_response import UpdateEnvironmentVariableResponse
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
    api_instance = kinde_sdk.EnvironmentVariablesApi(api_client)
    variable_id = 'env_var_0192b1941f125645fa15bf28a662a0b3' # str | The environment variable's ID.
    update_environment_variable_request = kinde_sdk.UpdateEnvironmentVariableRequest() # UpdateEnvironmentVariableRequest | The new details for the environment variable

    try:
        # Update environment variable
        api_response = api_instance.update_environment_variable(variable_id, update_environment_variable_request)
        print("The response of EnvironmentVariablesApi->update_environment_variable:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EnvironmentVariablesApi->update_environment_variable: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **variable_id** | **str**| The environment variable&#39;s ID. | 
 **update_environment_variable_request** | [**UpdateEnvironmentVariableRequest**](UpdateEnvironmentVariableRequest.md)| The new details for the environment variable | 

### Return type

[**UpdateEnvironmentVariableResponse**](UpdateEnvironmentVariableResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Environment variable successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

