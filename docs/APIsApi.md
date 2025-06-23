# kinde_sdk.APIsApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_api_application_scope**](APIsApi.md#add_api_application_scope) | **POST** /api/v1/apis/{api_id}/applications/{application_id}/scopes/{scope_id} | Add scope to API application
[**add_api_scope**](APIsApi.md#add_api_scope) | **POST** /api/v1/apis/{api_id}/scopes | Create API scope
[**add_apis**](APIsApi.md#add_apis) | **POST** /api/v1/apis | Create API
[**delete_api**](APIsApi.md#delete_api) | **DELETE** /api/v1/apis/{api_id} | Delete API
[**delete_api_appliation_scope**](APIsApi.md#delete_api_appliation_scope) | **DELETE** /api/v1/apis/{api_id}/applications/{application_id}/scopes/{scope_id} | Delete API application scope
[**delete_api_scope**](APIsApi.md#delete_api_scope) | **DELETE** /api/v1/apis/{api_id}/scopes/{scope_id} | Delete API scope
[**get_api**](APIsApi.md#get_api) | **GET** /api/v1/apis/{api_id} | Get API
[**get_api_scope**](APIsApi.md#get_api_scope) | **GET** /api/v1/apis/{api_id}/scopes/{scope_id} | Get API scope
[**get_api_scopes**](APIsApi.md#get_api_scopes) | **GET** /api/v1/apis/{api_id}/scopes | Get API scopes
[**get_apis**](APIsApi.md#get_apis) | **GET** /api/v1/apis | Get APIs
[**update_api_applications**](APIsApi.md#update_api_applications) | **PATCH** /api/v1/apis/{api_id}/applications | Authorize API applications
[**update_api_scope**](APIsApi.md#update_api_scope) | **PATCH** /api/v1/apis/{api_id}/scopes/{scope_id} | Update API scope


# **add_api_application_scope**
> add_api_application_scope(api_id, application_id, scope_id)

Add scope to API application

Add a scope to an API application.

<div>
  <code>create:api_application_scopes</code>
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
    api_instance = kinde_sdk.APIsApi(api_client)
    api_id = '838f208d006a482dbd8cdb79a9889f68' # str | API ID
    application_id = '7643b487c97545aab79257fd13a1085a' # str | Application ID
    scope_id = 'api_scope_019391daf58d87d8a7213419c016ac95' # str | Scope ID

    try:
        # Add scope to API application
        api_instance.add_api_application_scope(api_id, application_id, scope_id)
    except Exception as e:
        print("Exception when calling APIsApi->add_api_application_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **str**| API ID | 
 **application_id** | **str**| Application ID | 
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
**200** | API scope successfully added to API application |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_api_scope**
> CreateApiScopesResponse add_api_scope(api_id, add_api_scope_request)

Create API scope

Create a new API scope.

<div>
  <code>create:api_scopes</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.add_api_scope_request import AddAPIScopeRequest
from kinde_sdk.models.create_api_scopes_response import CreateApiScopesResponse
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
    api_instance = kinde_sdk.APIsApi(api_client)
    api_id = '838f208d006a482dbd8cdb79a9889f68' # str | API ID
    add_api_scope_request = kinde_sdk.AddAPIScopeRequest() # AddAPIScopeRequest | 

    try:
        # Create API scope
        api_response = api_instance.add_api_scope(api_id, add_api_scope_request)
        print("The response of APIsApi->add_api_scope:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APIsApi->add_api_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **str**| API ID | 
 **add_api_scope_request** | [**AddAPIScopeRequest**](AddAPIScopeRequest.md)|  | 

### Return type

[**CreateApiScopesResponse**](CreateApiScopesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | API scopes successfully created |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **add_apis**
> CreateApisResponse add_apis(add_apis_request)

Create API

Register a new API. For more information read [Register and manage APIs](https://docs.kinde.com/developer-tools/your-apis/register-manage-apis/).

<div>
  <code>create:apis</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.add_apis_request import AddAPIsRequest
from kinde_sdk.models.create_apis_response import CreateApisResponse
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
    api_instance = kinde_sdk.APIsApi(api_client)
    add_apis_request = kinde_sdk.AddAPIsRequest() # AddAPIsRequest | 

    try:
        # Create API
        api_response = api_instance.add_apis(add_apis_request)
        print("The response of APIsApi->add_apis:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APIsApi->add_apis: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **add_apis_request** | [**AddAPIsRequest**](AddAPIsRequest.md)|  | 

### Return type

[**CreateApisResponse**](CreateApisResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | APIs successfully updated |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_api**
> DeleteApiResponse delete_api(api_id)

Delete API

Delete an API you previously created.

<div>
  <code>delete:apis</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.delete_api_response import DeleteApiResponse
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
    api_instance = kinde_sdk.APIsApi(api_client)
    api_id = '7ccd126599aa422a771abcb341596881' # str | The API's ID.

    try:
        # Delete API
        api_response = api_instance.delete_api(api_id)
        print("The response of APIsApi->delete_api:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APIsApi->delete_api: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **str**| The API&#39;s ID. | 

### Return type

[**DeleteApiResponse**](DeleteApiResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | API successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_api_appliation_scope**
> delete_api_appliation_scope(api_id, application_id, scope_id)

Delete API application scope

Delete an API application scope you previously created.

<div>
  <code>delete:apis_application_scopes</code>
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
    api_instance = kinde_sdk.APIsApi(api_client)
    api_id = '838f208d006a482dbd8cdb79a9889f68' # str | API ID
    application_id = '7643b487c97545aab79257fd13a1085a' # str | Application ID
    scope_id = 'api_scope_019391daf58d87d8a7213419c016ac95' # str | Scope ID

    try:
        # Delete API application scope
        api_instance.delete_api_appliation_scope(api_id, application_id, scope_id)
    except Exception as e:
        print("Exception when calling APIsApi->delete_api_appliation_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **str**| API ID | 
 **application_id** | **str**| Application ID | 
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
**200** | API scope successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_api_scope**
> delete_api_scope(api_id, scope_id)

Delete API scope

Delete an API scope you previously created.

<div>
  <code>delete:apis_scopes</code>
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
    api_instance = kinde_sdk.APIsApi(api_client)
    api_id = '838f208d006a482dbd8cdb79a9889f68' # str | API ID
    scope_id = 'api_scope_019391daf58d87d8a7213419c016ac95' # str | Scope ID

    try:
        # Delete API scope
        api_instance.delete_api_scope(api_id, scope_id)
    except Exception as e:
        print("Exception when calling APIsApi->delete_api_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
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
**200** | API scope successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api**
> GetApiResponse get_api(api_id)

Get API

Retrieve API details by ID.

<div>
  <code>read:apis</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_api_response import GetApiResponse
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
    api_instance = kinde_sdk.APIsApi(api_client)
    api_id = '7ccd126599aa422a771abcb341596881' # str | The API's ID.

    try:
        # Get API
        api_response = api_instance.get_api(api_id)
        print("The response of APIsApi->get_api:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APIsApi->get_api: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **str**| The API&#39;s ID. | 

### Return type

[**GetApiResponse**](GetApiResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | API successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_scope**
> GetApiScopeResponse get_api_scope(api_id, scope_id)

Get API scope

Retrieve API scope by API ID.

<div>
  <code>read:api_scopes</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_api_scope_response import GetApiScopeResponse
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
    api_instance = kinde_sdk.APIsApi(api_client)
    api_id = '838f208d006a482dbd8cdb79a9889f68' # str | API ID
    scope_id = 'api_scope_019391daf58d87d8a7213419c016ac95' # str | Scope ID

    try:
        # Get API scope
        api_response = api_instance.get_api_scope(api_id, scope_id)
        print("The response of APIsApi->get_api_scope:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APIsApi->get_api_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **str**| API ID | 
 **scope_id** | **str**| Scope ID | 

### Return type

[**GetApiScopeResponse**](GetApiScopeResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | API scope successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_scopes**
> GetApiScopesResponse get_api_scopes(api_id)

Get API scopes

Retrieve API scopes by API ID.

<div>
  <code>read:api_scopes</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_api_scopes_response import GetApiScopesResponse
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
    api_instance = kinde_sdk.APIsApi(api_client)
    api_id = '838f208d006a482dbd8cdb79a9889f68' # str | API ID

    try:
        # Get API scopes
        api_response = api_instance.get_api_scopes(api_id)
        print("The response of APIsApi->get_api_scopes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APIsApi->get_api_scopes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **str**| API ID | 

### Return type

[**GetApiScopesResponse**](GetApiScopesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | API scopes successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_apis**
> GetApisResponse get_apis(expand=expand)

Get APIs

Returns a list of your APIs. The APIs are returned sorted by name.

<div>
  <code>read:apis</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_apis_response import GetApisResponse
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
    api_instance = kinde_sdk.APIsApi(api_client)
    expand = 'expand_example' # str | Specify additional data to retrieve. Use \"scopes\". (optional)

    try:
        # Get APIs
        api_response = api_instance.get_apis(expand=expand)
        print("The response of APIsApi->get_apis:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APIsApi->get_apis: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **expand** | **str**| Specify additional data to retrieve. Use \&quot;scopes\&quot;. | [optional] 

### Return type

[**GetApisResponse**](GetApisResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of APIs. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_api_applications**
> AuthorizeAppApiResponse update_api_applications(api_id, update_api_applications_request)

Authorize API applications

Authorize applications to be allowed to request access tokens for an API

<div>
  <code>update:apis</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.authorize_app_api_response import AuthorizeAppApiResponse
from kinde_sdk.models.update_api_applications_request import UpdateAPIApplicationsRequest
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
    api_instance = kinde_sdk.APIsApi(api_client)
    api_id = '7ccd126599aa422a771abcb341596881' # str | The API's ID.
    update_api_applications_request = kinde_sdk.UpdateAPIApplicationsRequest() # UpdateAPIApplicationsRequest | The applications you want to authorize.

    try:
        # Authorize API applications
        api_response = api_instance.update_api_applications(api_id, update_api_applications_request)
        print("The response of APIsApi->update_api_applications:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APIsApi->update_api_applications: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **str**| The API&#39;s ID. | 
 **update_api_applications_request** | [**UpdateAPIApplicationsRequest**](UpdateAPIApplicationsRequest.md)| The applications you want to authorize. | 

### Return type

[**AuthorizeAppApiResponse**](AuthorizeAppApiResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Authorized applications updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_api_scope**
> update_api_scope(api_id, scope_id, update_api_scope_request)

Update API scope

Update an API scope.

<div>
  <code>update:api_scopes</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.update_api_scope_request import UpdateAPIScopeRequest
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
    api_instance = kinde_sdk.APIsApi(api_client)
    api_id = '838f208d006a482dbd8cdb79a9889f68' # str | API ID
    scope_id = 'api_scope_019391daf58d87d8a7213419c016ac95' # str | Scope ID
    update_api_scope_request = kinde_sdk.UpdateAPIScopeRequest() # UpdateAPIScopeRequest | 

    try:
        # Update API scope
        api_instance.update_api_scope(api_id, scope_id, update_api_scope_request)
    except Exception as e:
        print("Exception when calling APIsApi->update_api_scope: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **api_id** | **str**| API ID | 
 **scope_id** | **str**| Scope ID | 
 **update_api_scope_request** | [**UpdateAPIScopeRequest**](UpdateAPIScopeRequest.md)|  | 

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
**200** | API scope successfully updated |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

