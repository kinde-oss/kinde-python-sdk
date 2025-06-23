# kinde_sdk.ConnectionsApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_connection**](ConnectionsApi.md#create_connection) | **POST** /api/v1/connections | Create Connection
[**delete_connection**](ConnectionsApi.md#delete_connection) | **DELETE** /api/v1/connections/{connection_id} | Delete Connection
[**get_connection**](ConnectionsApi.md#get_connection) | **GET** /api/v1/connections/{connection_id} | Get Connection
[**get_connections**](ConnectionsApi.md#get_connections) | **GET** /api/v1/connections | Get connections
[**replace_connection**](ConnectionsApi.md#replace_connection) | **PUT** /api/v1/connections/{connection_id} | Replace Connection
[**update_connection**](ConnectionsApi.md#update_connection) | **PATCH** /api/v1/connections/{connection_id} | Update Connection


# **create_connection**
> CreateConnectionResponse create_connection(create_connection_request)

Create Connection

Create Connection.

<div>
  <code>create:connections</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_connection_request import CreateConnectionRequest
from kinde_sdk.models.create_connection_response import CreateConnectionResponse
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
    api_instance = kinde_sdk.ConnectionsApi(api_client)
    create_connection_request = kinde_sdk.CreateConnectionRequest() # CreateConnectionRequest | Connection details.

    try:
        # Create Connection
        api_response = api_instance.create_connection(create_connection_request)
        print("The response of ConnectionsApi->create_connection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->create_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_connection_request** | [**CreateConnectionRequest**](CreateConnectionRequest.md)| Connection details. | 

### Return type

[**CreateConnectionResponse**](CreateConnectionResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Connection successfully created. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_connection**
> SuccessResponse delete_connection(connection_id)

Delete Connection

Delete connection.

<div>
  <code>delete:connections</code>
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
    api_instance = kinde_sdk.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | The identifier for the connection.

    try:
        # Delete Connection
        api_response = api_instance.delete_connection(connection_id)
        print("The response of ConnectionsApi->delete_connection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->delete_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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
**200** | Connection successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**404** | The specified resource was not found |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connection**
> Connection get_connection(connection_id)

Get Connection

Get Connection.

<div>
  <code>read:connections</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.connection import Connection
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
    api_instance = kinde_sdk.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | The unique identifier for the connection.

    try:
        # Get Connection
        api_response = api_instance.get_connection(connection_id)
        print("The response of ConnectionsApi->get_connection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->get_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| The unique identifier for the connection. | 

### Return type

[**Connection**](Connection.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Connection successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connections**
> GetConnectionsResponse get_connections(page_size=page_size, home_realm_domain=home_realm_domain, starting_after=starting_after, ending_before=ending_before)

Get connections

Returns a list of authentication connections. Optionally you can filter this by a home realm domain.

<div>
  <code>read:connections</code>
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
    api_instance = kinde_sdk.ConnectionsApi(api_client)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    home_realm_domain = 'myapp.com' # str | Filter the results by the home realm domain. (optional)
    starting_after = 'starting_after_example' # str | The ID of the connection to start after. (optional)
    ending_before = 'ending_before_example' # str | The ID of the connection to end before. (optional)

    try:
        # Get connections
        api_response = api_instance.get_connections(page_size=page_size, home_realm_domain=home_realm_domain, starting_after=starting_after, ending_before=ending_before)
        print("The response of ConnectionsApi->get_connections:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->get_connections: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **home_realm_domain** | **str**| Filter the results by the home realm domain. | [optional] 
 **starting_after** | **str**| The ID of the connection to start after. | [optional] 
 **ending_before** | **str**| The ID of the connection to end before. | [optional] 

### Return type

[**GetConnectionsResponse**](GetConnectionsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Connections successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_connection**
> SuccessResponse replace_connection(connection_id, replace_connection_request)

Replace Connection

Replace Connection Config.

<div>
  <code>update:connections</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.replace_connection_request import ReplaceConnectionRequest
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
    api_instance = kinde_sdk.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | The unique identifier for the connection.
    replace_connection_request = kinde_sdk.ReplaceConnectionRequest() # ReplaceConnectionRequest | The complete connection configuration to replace the existing one.

    try:
        # Replace Connection
        api_response = api_instance.replace_connection(connection_id, replace_connection_request)
        print("The response of ConnectionsApi->replace_connection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->replace_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| The unique identifier for the connection. | 
 **replace_connection_request** | [**ReplaceConnectionRequest**](ReplaceConnectionRequest.md)| The complete connection configuration to replace the existing one. | 

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
**200** | Connection successfully updated |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**404** | The specified resource was not found |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_connection**
> SuccessResponse update_connection(connection_id, update_connection_request)

Update Connection

Update Connection.

<div>
  <code>update:connections</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_connection_request import UpdateConnectionRequest
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
    api_instance = kinde_sdk.ConnectionsApi(api_client)
    connection_id = 'connection_id_example' # str | The unique identifier for the connection.
    update_connection_request = kinde_sdk.UpdateConnectionRequest() # UpdateConnectionRequest | The fields of the connection to update.

    try:
        # Update Connection
        api_response = api_instance.update_connection(connection_id, update_connection_request)
        print("The response of ConnectionsApi->update_connection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectionsApi->update_connection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **connection_id** | **str**| The unique identifier for the connection. | 
 **update_connection_request** | [**UpdateConnectionRequest**](UpdateConnectionRequest.md)| The fields of the connection to update. | 

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
**200** | Connection successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**404** | The specified resource was not found |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

