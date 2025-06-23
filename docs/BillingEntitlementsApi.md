# kinde_sdk.BillingEntitlementsApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_billing_entitlements**](BillingEntitlementsApi.md#get_billing_entitlements) | **GET** /api/v1/billing/entitlements | Get billing entitlements


# **get_billing_entitlements**
> GetBillingEntitlementsResponse get_billing_entitlements(customer_id, page_size=page_size, starting_after=starting_after, ending_before=ending_before, max_value=max_value, expand=expand)

Get billing entitlements

Returns all the entitlements a billing customer currently has access to

<div>
  <code>read:billing_entitlements</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_billing_entitlements_response import GetBillingEntitlementsResponse
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
    api_instance = kinde_sdk.BillingEntitlementsApi(api_client)
    customer_id = 'customer_id_example' # str | The ID of the billing customer to retrieve entitlements for
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    starting_after = 'starting_after_example' # str | The ID of the billing entitlement to start after. (optional)
    ending_before = 'ending_before_example' # str | The ID of the billing entitlement to end before. (optional)
    max_value = 'max_value_example' # str | When the maximum limit of an entitlement is null, this value is returned as the maximum limit (optional)
    expand = 'expand_example' # str | Specify additional plan data to retrieve. Use \"plans\". (optional)

    try:
        # Get billing entitlements
        api_response = api_instance.get_billing_entitlements(customer_id, page_size=page_size, starting_after=starting_after, ending_before=ending_before, max_value=max_value, expand=expand)
        print("The response of BillingEntitlementsApi->get_billing_entitlements:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BillingEntitlementsApi->get_billing_entitlements: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **str**| The ID of the billing customer to retrieve entitlements for | 
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **starting_after** | **str**| The ID of the billing entitlement to start after. | [optional] 
 **ending_before** | **str**| The ID of the billing entitlement to end before. | [optional] 
 **max_value** | **str**| When the maximum limit of an entitlement is null, this value is returned as the maximum limit | [optional] 
 **expand** | **str**| Specify additional plan data to retrieve. Use \&quot;plans\&quot;. | [optional] 

### Return type

[**GetBillingEntitlementsResponse**](GetBillingEntitlementsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Billing entitlements successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

