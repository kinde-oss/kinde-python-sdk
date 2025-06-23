# kinde_sdk.TimezonesApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_timezones**](TimezonesApi.md#get_timezones) | **GET** /api/v1/timezones | Get timezones


# **get_timezones**
> GetTimezonesResponse get_timezones()

Get timezones

Get a list of timezones and associated timezone keys.

<div>
  <code>read:timezones</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_timezones_response import GetTimezonesResponse
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
    api_instance = kinde_sdk.TimezonesApi(api_client)

    try:
        # Get timezones
        api_response = api_instance.get_timezones()
        print("The response of TimezonesApi->get_timezones:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TimezonesApi->get_timezones: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetTimezonesResponse**](GetTimezonesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of timezones. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

