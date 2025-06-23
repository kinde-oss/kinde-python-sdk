# kinde_sdk.FeatureFlagsApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_feature_flags**](FeatureFlagsApi.md#get_feature_flags) | **GET** /account_api/v1/feature_flags | Get feature flags


# **get_feature_flags**
> GetFeatureFlagsResponse get_feature_flags(page_size=page_size, starting_after=starting_after)

Get feature flags

Returns all the feature flags that affect the user


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_feature_flags_response import GetFeatureFlagsResponse
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
    api_instance = kinde_sdk.FeatureFlagsApi(api_client)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    starting_after = 'flag_1234567890abcdef' # str | The ID of the flag to start after. (optional)

    try:
        # Get feature flags
        api_response = api_instance.get_feature_flags(page_size=page_size, starting_after=starting_after)
        print("The response of FeatureFlagsApi->get_feature_flags:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeatureFlagsApi->get_feature_flags: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **starting_after** | **str**| The ID of the flag to start after. | [optional] 

### Return type

[**GetFeatureFlagsResponse**](GetFeatureFlagsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Feature flags successfully retrieved. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

