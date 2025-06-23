# kinde_sdk.BusinessApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_business**](BusinessApi.md#get_business) | **GET** /api/v1/business | Get business
[**update_business**](BusinessApi.md#update_business) | **PATCH** /api/v1/business | Update business


# **get_business**
> GetBusinessResponse get_business()

Get business

Get your business details.

<div>
  <code>read:businesses</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_business_response import GetBusinessResponse
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
    api_instance = kinde_sdk.BusinessApi(api_client)

    try:
        # Get business
        api_response = api_instance.get_business()
        print("The response of BusinessApi->get_business:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BusinessApi->get_business: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetBusinessResponse**](GetBusinessResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Your business details. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_business**
> SuccessResponse update_business(update_business_request)

Update business

Update your business details.

<div>
  <code>update:businesses</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_business_request import UpdateBusinessRequest
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
    api_instance = kinde_sdk.BusinessApi(api_client)
    update_business_request = kinde_sdk.UpdateBusinessRequest() # UpdateBusinessRequest | The business details to update.

    try:
        # Update business
        api_response = api_instance.update_business(update_business_request)
        print("The response of BusinessApi->update_business:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BusinessApi->update_business: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_business_request** | [**UpdateBusinessRequest**](UpdateBusinessRequest.md)| The business details to update. | 

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
**200** | Business successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

