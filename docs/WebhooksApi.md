# kinde_sdk.WebhooksApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_web_hook**](WebhooksApi.md#create_web_hook) | **POST** /api/v1/webhooks | Create a Webhook
[**delete_web_hook**](WebhooksApi.md#delete_web_hook) | **DELETE** /api/v1/webhooks/{webhook_id} | Delete Webhook
[**get_event**](WebhooksApi.md#get_event) | **GET** /api/v1/events/{event_id} | Get Event
[**get_event_types**](WebhooksApi.md#get_event_types) | **GET** /api/v1/event_types | List Event Types
[**get_web_hooks**](WebhooksApi.md#get_web_hooks) | **GET** /api/v1/webhooks | List Webhooks
[**update_web_hook**](WebhooksApi.md#update_web_hook) | **PATCH** /api/v1/webhooks/{webhook_id} | Update a Webhook


# **create_web_hook**
> CreateWebhookResponse create_web_hook(create_web_hook_request)

Create a Webhook

Create a webhook

<div>
  <code>create:webhooks</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_web_hook_request import CreateWebHookRequest
from kinde_sdk.models.create_webhook_response import CreateWebhookResponse
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
    api_instance = kinde_sdk.WebhooksApi(api_client)
    create_web_hook_request = kinde_sdk.CreateWebHookRequest() # CreateWebHookRequest | Webhook request specification.

    try:
        # Create a Webhook
        api_response = api_instance.create_web_hook(create_web_hook_request)
        print("The response of WebhooksApi->create_web_hook:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->create_web_hook: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_web_hook_request** | [**CreateWebHookRequest**](CreateWebHookRequest.md)| Webhook request specification. | 

### Return type

[**CreateWebhookResponse**](CreateWebhookResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Webhook successfully created. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_web_hook**
> DeleteWebhookResponse delete_web_hook(webhook_id)

Delete Webhook

Delete webhook

<div>
  <code>delete:webhooks</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.delete_webhook_response import DeleteWebhookResponse
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
    api_instance = kinde_sdk.WebhooksApi(api_client)
    webhook_id = 'webhook_id_example' # str | The webhook id.

    try:
        # Delete Webhook
        api_response = api_instance.delete_web_hook(webhook_id)
        print("The response of WebhooksApi->delete_web_hook:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->delete_web_hook: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **webhook_id** | **str**| The webhook id. | 

### Return type

[**DeleteWebhookResponse**](DeleteWebhookResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Webhook successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_event**
> GetEventResponse get_event(event_id)

Get Event

Returns an event

<div>
  <code>read:events</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_event_response import GetEventResponse
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
    api_instance = kinde_sdk.WebhooksApi(api_client)
    event_id = 'event_id_example' # str | The event id.

    try:
        # Get Event
        api_response = api_instance.get_event(event_id)
        print("The response of WebhooksApi->get_event:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->get_event: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **event_id** | **str**| The event id. | 

### Return type

[**GetEventResponse**](GetEventResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Event successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_event_types**
> GetEventTypesResponse get_event_types()

List Event Types

Returns a list event type definitions

<div>
  <code>read:event_types</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_event_types_response import GetEventTypesResponse
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
    api_instance = kinde_sdk.WebhooksApi(api_client)

    try:
        # List Event Types
        api_response = api_instance.get_event_types()
        print("The response of WebhooksApi->get_event_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->get_event_types: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetEventTypesResponse**](GetEventTypesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Event types successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_web_hooks**
> GetWebhooksResponse get_web_hooks()

List Webhooks

List webhooks

<div>
  <code>read:webhooks</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_webhooks_response import GetWebhooksResponse
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
    api_instance = kinde_sdk.WebhooksApi(api_client)

    try:
        # List Webhooks
        api_response = api_instance.get_web_hooks()
        print("The response of WebhooksApi->get_web_hooks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->get_web_hooks: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetWebhooksResponse**](GetWebhooksResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Webhook list successfully returned. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_web_hook**
> UpdateWebhookResponse update_web_hook(webhook_id, update_web_hook_request)

Update a Webhook

Update a webhook

<div>
  <code>update:webhooks</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.update_web_hook_request import UpdateWebHookRequest
from kinde_sdk.models.update_webhook_response import UpdateWebhookResponse
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
    api_instance = kinde_sdk.WebhooksApi(api_client)
    webhook_id = 'webhook_id_example' # str | The webhook id.
    update_web_hook_request = kinde_sdk.UpdateWebHookRequest() # UpdateWebHookRequest | Update webhook request specification.

    try:
        # Update a Webhook
        api_response = api_instance.update_web_hook(webhook_id, update_web_hook_request)
        print("The response of WebhooksApi->update_web_hook:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->update_web_hook: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **webhook_id** | **str**| The webhook id. | 
 **update_web_hook_request** | [**UpdateWebHookRequest**](UpdateWebHookRequest.md)| Update webhook request specification. | 

### Return type

[**UpdateWebhookResponse**](UpdateWebhookResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Webhook successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

