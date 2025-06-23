# kinde_sdk.CallbacksApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_logout_redirect_urls**](CallbacksApi.md#add_logout_redirect_urls) | **POST** /api/v1/applications/{app_id}/auth_logout_urls | Add logout redirect URLs
[**add_redirect_callback_urls**](CallbacksApi.md#add_redirect_callback_urls) | **POST** /api/v1/applications/{app_id}/auth_redirect_urls | Add Redirect Callback URLs
[**delete_callback_urls**](CallbacksApi.md#delete_callback_urls) | **DELETE** /api/v1/applications/{app_id}/auth_redirect_urls | Delete Callback URLs
[**delete_logout_urls**](CallbacksApi.md#delete_logout_urls) | **DELETE** /api/v1/applications/{app_id}/auth_logout_urls | Delete Logout URLs
[**get_callback_urls**](CallbacksApi.md#get_callback_urls) | **GET** /api/v1/applications/{app_id}/auth_redirect_urls | List Callback URLs
[**get_logout_urls**](CallbacksApi.md#get_logout_urls) | **GET** /api/v1/applications/{app_id}/auth_logout_urls | List logout URLs
[**replace_logout_redirect_urls**](CallbacksApi.md#replace_logout_redirect_urls) | **PUT** /api/v1/applications/{app_id}/auth_logout_urls | Replace logout redirect URls
[**replace_redirect_callback_urls**](CallbacksApi.md#replace_redirect_callback_urls) | **PUT** /api/v1/applications/{app_id}/auth_redirect_urls | Replace Redirect Callback URLs


# **add_logout_redirect_urls**
> SuccessResponse add_logout_redirect_urls(app_id, replace_logout_redirect_urls_request)

Add logout redirect URLs

Add additional logout redirect URLs.

<div>
  <code>create:application_logout_uris</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.replace_logout_redirect_urls_request import ReplaceLogoutRedirectURLsRequest
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
    api_instance = kinde_sdk.CallbacksApi(api_client)
    app_id = 'app_id_example' # str | The identifier for the application.
    replace_logout_redirect_urls_request = kinde_sdk.ReplaceLogoutRedirectURLsRequest() # ReplaceLogoutRedirectURLsRequest | Callback details.

    try:
        # Add logout redirect URLs
        api_response = api_instance.add_logout_redirect_urls(app_id, replace_logout_redirect_urls_request)
        print("The response of CallbacksApi->add_logout_redirect_urls:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CallbacksApi->add_logout_redirect_urls: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| The identifier for the application. | 
 **replace_logout_redirect_urls_request** | [**ReplaceLogoutRedirectURLsRequest**](ReplaceLogoutRedirectURLsRequest.md)| Callback details. | 

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
**200** | Logout URLs successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_redirect_callback_urls**
> SuccessResponse add_redirect_callback_urls(app_id, replace_redirect_callback_urls_request)

Add Redirect Callback URLs

Add additional redirect callback URLs.

<div>
  <code>create:applications_redirect_uris</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.replace_redirect_callback_urls_request import ReplaceRedirectCallbackURLsRequest
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
    api_instance = kinde_sdk.CallbacksApi(api_client)
    app_id = 'app_id_example' # str | The identifier for the application.
    replace_redirect_callback_urls_request = kinde_sdk.ReplaceRedirectCallbackURLsRequest() # ReplaceRedirectCallbackURLsRequest | Callback details.

    try:
        # Add Redirect Callback URLs
        api_response = api_instance.add_redirect_callback_urls(app_id, replace_redirect_callback_urls_request)
        print("The response of CallbacksApi->add_redirect_callback_urls:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CallbacksApi->add_redirect_callback_urls: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| The identifier for the application. | 
 **replace_redirect_callback_urls_request** | [**ReplaceRedirectCallbackURLsRequest**](ReplaceRedirectCallbackURLsRequest.md)| Callback details. | 

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
**200** | Callbacks successfully updated |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_callback_urls**
> SuccessResponse delete_callback_urls(app_id, urls)

Delete Callback URLs

Delete callback URLs.

<div>
  <code>delete:applications_redirect_uris</code>
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
    api_instance = kinde_sdk.CallbacksApi(api_client)
    app_id = 'app_id_example' # str | The identifier for the application.
    urls = 'urls_example' # str | Urls to delete, comma separated and url encoded.

    try:
        # Delete Callback URLs
        api_response = api_instance.delete_callback_urls(app_id, urls)
        print("The response of CallbacksApi->delete_callback_urls:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CallbacksApi->delete_callback_urls: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| The identifier for the application. | 
 **urls** | **str**| Urls to delete, comma separated and url encoded. | 

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
**200** | Callback URLs successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_logout_urls**
> SuccessResponse delete_logout_urls(app_id, urls)

Delete Logout URLs

Delete logout URLs.

<div>
  <code>delete:application_logout_uris</code>
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
    api_instance = kinde_sdk.CallbacksApi(api_client)
    app_id = 'app_id_example' # str | The identifier for the application.
    urls = 'urls_example' # str | Urls to delete, comma separated and url encoded.

    try:
        # Delete Logout URLs
        api_response = api_instance.delete_logout_urls(app_id, urls)
        print("The response of CallbacksApi->delete_logout_urls:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CallbacksApi->delete_logout_urls: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| The identifier for the application. | 
 **urls** | **str**| Urls to delete, comma separated and url encoded. | 

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
**200** | Logout URLs successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_callback_urls**
> RedirectCallbackUrls get_callback_urls(app_id)

List Callback URLs

Returns an application's redirect callback URLs.

<div>
  <code>read:applications_redirect_uris</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.redirect_callback_urls import RedirectCallbackUrls
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
    api_instance = kinde_sdk.CallbacksApi(api_client)
    app_id = 'app_id_example' # str | The identifier for the application.

    try:
        # List Callback URLs
        api_response = api_instance.get_callback_urls(app_id)
        print("The response of CallbacksApi->get_callback_urls:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CallbacksApi->get_callback_urls: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| The identifier for the application. | 

### Return type

[**RedirectCallbackUrls**](RedirectCallbackUrls.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Callback URLs successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_logout_urls**
> LogoutRedirectUrls get_logout_urls(app_id)

List logout URLs

Returns an application's logout redirect URLs.

<div>
  <code>read:application_logout_uris</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.logout_redirect_urls import LogoutRedirectUrls
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
    api_instance = kinde_sdk.CallbacksApi(api_client)
    app_id = 'app_id_example' # str | The identifier for the application.

    try:
        # List logout URLs
        api_response = api_instance.get_logout_urls(app_id)
        print("The response of CallbacksApi->get_logout_urls:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CallbacksApi->get_logout_urls: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| The identifier for the application. | 

### Return type

[**LogoutRedirectUrls**](LogoutRedirectUrls.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Logout URLs successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_logout_redirect_urls**
> SuccessResponse replace_logout_redirect_urls(app_id, replace_logout_redirect_urls_request)

Replace logout redirect URls

Replace all logout redirect URLs.

<div>
  <code>update:application_logout_uris</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.replace_logout_redirect_urls_request import ReplaceLogoutRedirectURLsRequest
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
    api_instance = kinde_sdk.CallbacksApi(api_client)
    app_id = 'app_id_example' # str | The identifier for the application.
    replace_logout_redirect_urls_request = kinde_sdk.ReplaceLogoutRedirectURLsRequest() # ReplaceLogoutRedirectURLsRequest | Callback details.

    try:
        # Replace logout redirect URls
        api_response = api_instance.replace_logout_redirect_urls(app_id, replace_logout_redirect_urls_request)
        print("The response of CallbacksApi->replace_logout_redirect_urls:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CallbacksApi->replace_logout_redirect_urls: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| The identifier for the application. | 
 **replace_logout_redirect_urls_request** | [**ReplaceLogoutRedirectURLsRequest**](ReplaceLogoutRedirectURLsRequest.md)| Callback details. | 

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
**200** | Logout URLs successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_redirect_callback_urls**
> SuccessResponse replace_redirect_callback_urls(app_id, replace_redirect_callback_urls_request)

Replace Redirect Callback URLs

Replace all redirect callback URLs.

<div>
  <code>update:applications_redirect_uris</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.replace_redirect_callback_urls_request import ReplaceRedirectCallbackURLsRequest
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
    api_instance = kinde_sdk.CallbacksApi(api_client)
    app_id = 'app_id_example' # str | The identifier for the application.
    replace_redirect_callback_urls_request = kinde_sdk.ReplaceRedirectCallbackURLsRequest() # ReplaceRedirectCallbackURLsRequest | Callback details.

    try:
        # Replace Redirect Callback URLs
        api_response = api_instance.replace_redirect_callback_urls(app_id, replace_redirect_callback_urls_request)
        print("The response of CallbacksApi->replace_redirect_callback_urls:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CallbacksApi->replace_redirect_callback_urls: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | **str**| The identifier for the application. | 
 **replace_redirect_callback_urls_request** | [**ReplaceRedirectCallbackURLsRequest**](ReplaceRedirectCallbackURLsRequest.md)| Callback details. | 

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
**200** | Callbacks successfully updated |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

