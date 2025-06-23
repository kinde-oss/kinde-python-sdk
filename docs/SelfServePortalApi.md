# kinde_sdk.SelfServePortalApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_portal_link**](SelfServePortalApi.md#get_portal_link) | **GET** /account_api/v1/get_portal_link | Get self-serve portal link


# **get_portal_link**
> GetPortalLink get_portal_link(subnav=subnav, return_url=return_url)

Get self-serve portal link

Returns a link to the self-serve portal for the authenticated user. The user can use this link to manage their account, update their profile, and view their entitlements.


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_portal_link import GetPortalLink
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
    api_instance = kinde_sdk.SelfServePortalApi(api_client)
    subnav = 'subnav_example' # str | The area of the portal you want the user to land on (optional)
    return_url = 'return_url_example' # str | The URL to redirect the user to after they have completed their actions in the portal. (optional)

    try:
        # Get self-serve portal link
        api_response = api_instance.get_portal_link(subnav=subnav, return_url=return_url)
        print("The response of SelfServePortalApi->get_portal_link:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SelfServePortalApi->get_portal_link: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subnav** | **str**| The area of the portal you want the user to land on | [optional] 
 **return_url** | **str**| The URL to redirect the user to after they have completed their actions in the portal. | [optional] 

### Return type

[**GetPortalLink**](GetPortalLink.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully generated the portal link |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

