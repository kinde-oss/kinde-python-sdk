# kinde_sdk.BillingApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_entitlements**](BillingApi.md#get_entitlements) | **GET** /account_api/v1/entitlements | Get entitlements


# **get_entitlements**
> GetEntitlementsResponse get_entitlements(page_size=page_size, starting_after=starting_after)

Get entitlements

Returns all the entitlements a the user currently has access to


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_entitlements_response import GetEntitlementsResponse
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
    api_instance = kinde_sdk.BillingApi(api_client)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    starting_after = 'entitlement_1234567890abcdef' # str | The ID of the entitlement to start after. (optional)

    try:
        # Get entitlements
        api_response = api_instance.get_entitlements(page_size=page_size, starting_after=starting_after)
        print("The response of BillingApi->get_entitlements:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BillingApi->get_entitlements: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **starting_after** | **str**| The ID of the entitlement to start after. | [optional] 

### Return type

[**GetEntitlementsResponse**](GetEntitlementsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Billing entitlements successfully retrieved. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

