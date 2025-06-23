# kinde_sdk.SubscribersApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_subscriber**](SubscribersApi.md#create_subscriber) | **POST** /api/v1/subscribers | Create Subscriber
[**get_subscriber**](SubscribersApi.md#get_subscriber) | **GET** /api/v1/subscribers/{subscriber_id} | Get Subscriber
[**get_subscribers**](SubscribersApi.md#get_subscribers) | **GET** /api/v1/subscribers | List Subscribers


# **create_subscriber**
> CreateSubscriberSuccessResponse create_subscriber(first_name, last_name, email)

Create Subscriber

Create subscriber.

<div>
  <code>create:subscribers</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_subscriber_success_response import CreateSubscriberSuccessResponse
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
    api_instance = kinde_sdk.SubscribersApi(api_client)
    first_name = 'first_name_example' # str | Subscriber's first name.
    last_name = 'last_name_example' # str | Subscriber's last name.
    email = 'email_example' # str | The email address of the subscriber.

    try:
        # Create Subscriber
        api_response = api_instance.create_subscriber(first_name, last_name, email)
        print("The response of SubscribersApi->create_subscriber:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SubscribersApi->create_subscriber: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **first_name** | **str**| Subscriber&#39;s first name. | 
 **last_name** | **str**| Subscriber&#39;s last name. | 
 **email** | **str**| The email address of the subscriber. | 

### Return type

[**CreateSubscriberSuccessResponse**](CreateSubscriberSuccessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Subscriber successfully created |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subscriber**
> GetSubscriberResponse get_subscriber(subscriber_id)

Get Subscriber

Retrieve a subscriber record.

<div>
  <code>read:subscribers</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_subscriber_response import GetSubscriberResponse
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
    api_instance = kinde_sdk.SubscribersApi(api_client)
    subscriber_id = 'subscriber_id_example' # str | The subscriber's id.

    try:
        # Get Subscriber
        api_response = api_instance.get_subscriber(subscriber_id)
        print("The response of SubscribersApi->get_subscriber:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SubscribersApi->get_subscriber: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subscriber_id** | **str**| The subscriber&#39;s id. | 

### Return type

[**GetSubscriberResponse**](GetSubscriberResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Subscriber successfully retrieved. |  -  |
**400** | Bad request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_subscribers**
> GetSubscribersResponse get_subscribers(sort=sort, page_size=page_size, next_token=next_token)

List Subscribers

The returned list can be sorted by full name or email address
in ascending or descending order. The number of records to return at a time can also be controlled using the `page_size` query
string parameter.

<div>
  <code>read:subscribers</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_subscribers_response import GetSubscribersResponse
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
    api_instance = kinde_sdk.SubscribersApi(api_client)
    sort = 'sort_example' # str | Field and order to sort the result by. (optional)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    next_token = 'next_token_example' # str | A string to get the next page of results if there are more results. (optional)

    try:
        # List Subscribers
        api_response = api_instance.get_subscribers(sort=sort, page_size=page_size, next_token=next_token)
        print("The response of SubscribersApi->get_subscribers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SubscribersApi->get_subscribers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sort** | **str**| Field and order to sort the result by. | [optional] 
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **next_token** | **str**| A string to get the next page of results if there are more results. | [optional] 

### Return type

[**GetSubscribersResponse**](GetSubscribersResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Subscriber successfully retrieved. |  -  |
**403** | Bad request. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

