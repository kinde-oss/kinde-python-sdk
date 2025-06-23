# kinde_sdk.MFAApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**replace_mfa**](MFAApi.md#replace_mfa) | **PUT** /api/v1/mfa | Replace MFA Configuration


# **replace_mfa**
> SuccessResponse replace_mfa(replace_mfa_request)

Replace MFA Configuration

Replace MFA Configuration.

<div>
  <code>update:mfa</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.replace_mfa_request import ReplaceMFARequest
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
    api_instance = kinde_sdk.MFAApi(api_client)
    replace_mfa_request = kinde_sdk.ReplaceMFARequest() # ReplaceMFARequest | MFA details.

    try:
        # Replace MFA Configuration
        api_response = api_instance.replace_mfa(replace_mfa_request)
        print("The response of MFAApi->replace_mfa:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MFAApi->replace_mfa: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **replace_mfa_request** | [**ReplaceMFARequest**](ReplaceMFARequest.md)| MFA details. | 

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
**200** | MFA Configuration updated successfully. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

