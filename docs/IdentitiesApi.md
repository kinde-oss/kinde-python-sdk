# kinde_sdk.IdentitiesApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_identity**](IdentitiesApi.md#delete_identity) | **DELETE** /api/v1/identities/{identity_id} | Delete identity
[**get_identity**](IdentitiesApi.md#get_identity) | **GET** /api/v1/identities/{identity_id} | Get identity
[**update_identity**](IdentitiesApi.md#update_identity) | **PATCH** /api/v1/identities/{identity_id} | Update identity


# **delete_identity**
> SuccessResponse delete_identity(identity_id)

Delete identity

Delete identity by ID.

<div>
  <code>delete:identities</code>
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
    api_instance = kinde_sdk.IdentitiesApi(api_client)
    identity_id = 'identity_id_example' # str | The unique identifier for the identity.

    try:
        # Delete identity
        api_response = api_instance.delete_identity(identity_id)
        print("The response of IdentitiesApi->delete_identity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IdentitiesApi->delete_identity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identity_id** | **str**| The unique identifier for the identity. | 

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
**200** | Identity successfully deleted. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_identity**
> Identity get_identity(identity_id)

Get identity

Returns an identity by ID

<div>
  <code>read:identities</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.identity import Identity
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
    api_instance = kinde_sdk.IdentitiesApi(api_client)
    identity_id = 'identity_id_example' # str | The unique identifier for the identity.

    try:
        # Get identity
        api_response = api_instance.get_identity(identity_id)
        print("The response of IdentitiesApi->get_identity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IdentitiesApi->get_identity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identity_id** | **str**| The unique identifier for the identity. | 

### Return type

[**Identity**](Identity.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Identity successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_identity**
> SuccessResponse update_identity(identity_id, update_identity_request)

Update identity

Update identity by ID.

<div>
  <code>update:identities</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_identity_request import UpdateIdentityRequest
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
    api_instance = kinde_sdk.IdentitiesApi(api_client)
    identity_id = 'identity_id_example' # str | The unique identifier for the identity.
    update_identity_request = kinde_sdk.UpdateIdentityRequest() # UpdateIdentityRequest | The fields of the identity to update.

    try:
        # Update identity
        api_response = api_instance.update_identity(identity_id, update_identity_request)
        print("The response of IdentitiesApi->update_identity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IdentitiesApi->update_identity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identity_id** | **str**| The unique identifier for the identity. | 
 **update_identity_request** | [**UpdateIdentityRequest**](UpdateIdentityRequest.md)| The fields of the identity to update. | 

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
**200** | Identity successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

