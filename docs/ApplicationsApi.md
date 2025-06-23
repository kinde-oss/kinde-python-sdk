# kinde_sdk.ApplicationsApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_application**](ApplicationsApi.md#create_application) | **POST** /api/v1/applications | Create application
[**delete_application**](ApplicationsApi.md#delete_application) | **DELETE** /api/v1/applications/{application_id} | Delete application
[**enable_connection**](ApplicationsApi.md#enable_connection) | **POST** /api/v1/applications/{application_id}/connections/{connection_id} | Enable connection
[**get_application**](ApplicationsApi.md#get_application) | **GET** /api/v1/applications/{application_id} | Get application
[**get_application_connections**](ApplicationsApi.md#get_application_connections) | **GET** /api/v1/applications/{application_id}/connections | Get connections
[**get_application_property_values**](ApplicationsApi.md#get_application_property_values) | **GET** /api/v1/applications/{application_id}/properties | Get property values
[**get_applications**](ApplicationsApi.md#get_applications) | **GET** /api/v1/applications | Get applications
[**remove_connection**](ApplicationsApi.md#remove_connection) | **DELETE** /api/v1/applications/{application_id}/connections/{connection_id} | Remove connection
[**update_application**](ApplicationsApi.md#update_application) | **PATCH** /api/v1/applications/{application_id} | Update Application
[**update_application_tokens**](ApplicationsApi.md#update_application_tokens) | **PATCH** /api/v1/applications/{application_id}/tokens | Update application tokens
[**update_applications_property**](ApplicationsApi.md#update_applications_property) | **PUT** /api/v1/applications/{application_id}/properties/{property_key} | Update property


# **create_application**
> CreateApplicationResponse create_application(create_application_request)

Create application

Create a new client.

<div>
  <code>create:applications</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_application_request import CreateApplicationRequest
from kinde_sdk.models.create_application_response import CreateApplicationResponse
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    create_application_request = kinde_sdk.CreateApplicationRequest() # CreateApplicationRequest | 

    try:
        # Create application
        api_response = api_instance.create_application(create_application_request)
        print("The response of ApplicationsApi->create_application:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->create_application: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_application_request** | [**CreateApplicationRequest**](CreateApplicationRequest.md)|  | 

### Return type

[**CreateApplicationResponse**](CreateApplicationResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Application successfully created. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_application**
> SuccessResponse delete_application(application_id)

Delete application

Delete a client / application.

<div>
  <code>delete:applications</code>
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    application_id = '20bbffaa4c5e492a962273039d4ae18b' # str | The identifier for the application.

    try:
        # Delete application
        api_response = api_instance.delete_application(application_id)
        print("The response of ApplicationsApi->delete_application:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->delete_application: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **str**| The identifier for the application. | 

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
**200** | Application successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enable_connection**
> enable_connection(application_id, connection_id)

Enable connection

Enable an auth connection for an application.

<div>
  <code>create:application_connections</code>
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    application_id = '20bbffaa4c5e492a962273039d4ae18b' # str | The identifier/client ID for the application.
    connection_id = 'conn_0192c16abb53b44277e597d31877ba5b' # str | The identifier for the connection.

    try:
        # Enable connection
        api_instance.enable_connection(application_id, connection_id)
    except Exception as e:
        print("Exception when calling ApplicationsApi->enable_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **str**| The identifier/client ID for the application. | 
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

# **get_application**
> GetApplicationResponse get_application(application_id)

Get application

Gets an application given the application's ID.

<div>
  <code>read:applications</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_application_response import GetApplicationResponse
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    application_id = '20bbffaa4c5e492a962273039d4ae18b' # str | The identifier for the application.

    try:
        # Get application
        api_response = api_instance.get_application(application_id)
        print("The response of ApplicationsApi->get_application:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->get_application: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **str**| The identifier for the application. | 

### Return type

[**GetApplicationResponse**](GetApplicationResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Application successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_application_connections**
> GetConnectionsResponse get_application_connections(application_id)

Get connections

Gets all connections for an application.

<div>
  <code>read:application_connections</code>
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    application_id = '20bbffaa4c5e492a962273039d4ae18b' # str | The identifier/client ID for the application.

    try:
        # Get connections
        api_response = api_instance.get_application_connections(application_id)
        print("The response of ApplicationsApi->get_application_connections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->get_application_connections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **str**| The identifier/client ID for the application. | 

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
**200** | Application connections successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_application_property_values**
> GetPropertyValuesResponse get_application_property_values(application_id)

Get property values

Gets properties for an application by client ID.

<div>
  <code>read:application_properties</code>
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    application_id = '3b0b5c6c8fcc464fab397f4969b5f482' # str | The application's ID / client ID.

    try:
        # Get property values
        api_response = api_instance.get_application_property_values(application_id)
        print("The response of ApplicationsApi->get_application_property_values:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->get_application_property_values: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **str**| The application&#39;s ID / client ID. | 

### Return type

[**GetPropertyValuesResponse**](GetPropertyValuesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Properties successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_applications**
> GetApplicationsResponse get_applications(sort=sort, page_size=page_size, next_token=next_token)

Get applications

Get a list of applications / clients.

<div>
  <code>read:applications</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_applications_response import GetApplicationsResponse
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    sort = 'sort_example' # str | Field and order to sort the result by. (optional)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    next_token = 'next_token_example' # str | A string to get the next page of results if there are more results. (optional)

    try:
        # Get applications
        api_response = api_instance.get_applications(sort=sort, page_size=page_size, next_token=next_token)
        print("The response of ApplicationsApi->get_applications:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->get_applications: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sort** | **str**| Field and order to sort the result by. | [optional] 
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **next_token** | **str**| A string to get the next page of results if there are more results. | [optional] 

### Return type

[**GetApplicationsResponse**](GetApplicationsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A successful response with a list of applications or an empty list. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_connection**
> SuccessResponse remove_connection(application_id, connection_id)

Remove connection

Turn off an auth connection for an application

<div>
  <code>delete:application_connections</code>
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    application_id = '20bbffaa4c5e492a962273039d4ae18b' # str | The identifier/client ID for the application.
    connection_id = 'conn_0192c16abb53b44277e597d31877ba5b' # str | The identifier for the connection.

    try:
        # Remove connection
        api_response = api_instance.remove_connection(application_id, connection_id)
        print("The response of ApplicationsApi->remove_connection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->remove_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **str**| The identifier/client ID for the application. | 
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

# **update_application**
> update_application(application_id, update_application_request=update_application_request)

Update Application

Updates a client's settings. For more information, read [Applications in Kinde](https://docs.kinde.com/build/applications/about-applications)

<div>
  <code>update:applications</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.update_application_request import UpdateApplicationRequest
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    application_id = '20bbffaa4c5e492a962273039d4ae18b' # str | The identifier for the application.
    update_application_request = kinde_sdk.UpdateApplicationRequest() # UpdateApplicationRequest | Application details. (optional)

    try:
        # Update Application
        api_instance.update_application(application_id, update_application_request=update_application_request)
    except Exception as e:
        print("Exception when calling ApplicationsApi->update_application: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **str**| The identifier for the application. | 
 **update_application_request** | [**UpdateApplicationRequest**](UpdateApplicationRequest.md)| Application details. | [optional] 

### Return type

void (empty response body)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Application successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_application_tokens**
> SuccessResponse update_application_tokens(application_id, update_application_tokens_request)

Update application tokens

Configure tokens for an application.
  <div>
    <code>update:application_tokens</code>
  </div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_application_tokens_request import UpdateApplicationTokensRequest
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    application_id = '20bbffaa4c5e492a962273039d4ae18b' # str | The identifier/client ID for the application.
    update_application_tokens_request = kinde_sdk.UpdateApplicationTokensRequest() # UpdateApplicationTokensRequest | Application tokens.

    try:
        # Update application tokens
        api_response = api_instance.update_application_tokens(application_id, update_application_tokens_request)
        print("The response of ApplicationsApi->update_application_tokens:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->update_application_tokens: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **str**| The identifier/client ID for the application. | 
 **update_application_tokens_request** | [**UpdateApplicationTokensRequest**](UpdateApplicationTokensRequest.md)| Application tokens. | 

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
**200** | Application tokens successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_applications_property**
> SuccessResponse update_applications_property(application_id, property_key, update_applications_property_request)

Update property

Update application property value.

<div>
  <code>update:application_properties</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_applications_property_request import UpdateApplicationsPropertyRequest
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
    api_instance = kinde_sdk.ApplicationsApi(api_client)
    application_id = '3b0b5c6c8fcc464fab397f4969b5f482' # str | The application's ID / client ID.
    property_key = 'kp_some_key' # str | The property's key.
    update_applications_property_request = kinde_sdk.UpdateApplicationsPropertyRequest() # UpdateApplicationsPropertyRequest | 

    try:
        # Update property
        api_response = api_instance.update_applications_property(application_id, property_key, update_applications_property_request)
        print("The response of ApplicationsApi->update_applications_property:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApplicationsApi->update_applications_property: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **application_id** | **str**| The application&#39;s ID / client ID. | 
 **property_key** | **str**| The property&#39;s key. | 
 **update_applications_property_request** | [**UpdateApplicationsPropertyRequest**](UpdateApplicationsPropertyRequest.md)|  | 

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
**200** | Property successfully updated |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

