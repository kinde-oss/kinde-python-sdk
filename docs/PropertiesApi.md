# kinde_sdk.PropertiesApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_property**](PropertiesApi.md#create_property) | **POST** /api/v1/properties | Create Property
[**delete_property**](PropertiesApi.md#delete_property) | **DELETE** /api/v1/properties/{property_id} | Delete Property
[**get_properties**](PropertiesApi.md#get_properties) | **GET** /api/v1/properties | List properties
[**get_user_properties**](PropertiesApi.md#get_user_properties) | **GET** /account_api/v1/properties | Get properties
[**update_property**](PropertiesApi.md#update_property) | **PUT** /api/v1/properties/{property_id} | Update Property


# **create_property**
> CreatePropertyResponse create_property(create_property_request)

Create Property

Create property.

<div>
  <code>create:properties</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_property_request import CreatePropertyRequest
from kinde_sdk.models.create_property_response import CreatePropertyResponse
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
    api_instance = kinde_sdk.PropertiesApi(api_client)
    create_property_request = kinde_sdk.CreatePropertyRequest() # CreatePropertyRequest | Property details.

    try:
        # Create Property
        api_response = api_instance.create_property(create_property_request)
        print("The response of PropertiesApi->create_property:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PropertiesApi->create_property: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_property_request** | [**CreatePropertyRequest**](CreatePropertyRequest.md)| Property details. | 

### Return type

[**CreatePropertyResponse**](CreatePropertyResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Property successfully created |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_property**
> SuccessResponse delete_property(property_id)

Delete Property

Delete property.

<div>
  <code>delete:properties</code>
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
    api_instance = kinde_sdk.PropertiesApi(api_client)
    property_id = 'property_id_example' # str | The unique identifier for the property.

    try:
        # Delete Property
        api_response = api_instance.delete_property(property_id)
        print("The response of PropertiesApi->delete_property:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PropertiesApi->delete_property: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **property_id** | **str**| The unique identifier for the property. | 

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
**200** | Property successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_properties**
> GetPropertiesResponse get_properties(page_size=page_size, starting_after=starting_after, ending_before=ending_before, context=context)

List properties

Returns a list of properties

<div>
  <code>read:properties</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_properties_response import GetPropertiesResponse
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
    api_instance = kinde_sdk.PropertiesApi(api_client)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    starting_after = 'starting_after_example' # str | The ID of the property to start after. (optional)
    ending_before = 'ending_before_example' # str | The ID of the property to end before. (optional)
    context = 'context_example' # str | Filter results by user,  organization or application context (optional)

    try:
        # List properties
        api_response = api_instance.get_properties(page_size=page_size, starting_after=starting_after, ending_before=ending_before, context=context)
        print("The response of PropertiesApi->get_properties:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PropertiesApi->get_properties: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **starting_after** | **str**| The ID of the property to start after. | [optional] 
 **ending_before** | **str**| The ID of the property to end before. | [optional] 
 **context** | **str**| Filter results by user,  organization or application context | [optional] 

### Return type

[**GetPropertiesResponse**](GetPropertiesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Properties successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_properties**
> GetUserPropertiesResponse get_user_properties(page_size=page_size, starting_after=starting_after)

Get properties

Returns all properties for the user


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_user_properties_response import GetUserPropertiesResponse
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
    api_instance = kinde_sdk.PropertiesApi(api_client)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    starting_after = 'prop_1234567890abcdef' # str | The ID of the property to start after. (optional)

    try:
        # Get properties
        api_response = api_instance.get_user_properties(page_size=page_size, starting_after=starting_after)
        print("The response of PropertiesApi->get_user_properties:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PropertiesApi->get_user_properties: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **starting_after** | **str**| The ID of the property to start after. | [optional] 

### Return type

[**GetUserPropertiesResponse**](GetUserPropertiesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Properties successfully retrieved. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_property**
> SuccessResponse update_property(property_id, update_property_request)

Update Property

Update property.

<div>
  <code>update:properties</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_property_request import UpdatePropertyRequest
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
    api_instance = kinde_sdk.PropertiesApi(api_client)
    property_id = 'property_id_example' # str | The unique identifier for the property.
    update_property_request = kinde_sdk.UpdatePropertyRequest() # UpdatePropertyRequest | The fields of the property to update.

    try:
        # Update Property
        api_response = api_instance.update_property(property_id, update_property_request)
        print("The response of PropertiesApi->update_property:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PropertiesApi->update_property: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **property_id** | **str**| The unique identifier for the property. | 
 **update_property_request** | [**UpdatePropertyRequest**](UpdatePropertyRequest.md)| The fields of the property to update. | 

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
**200** | Property successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

