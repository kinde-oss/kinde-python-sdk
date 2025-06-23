# kinde_sdk.SearchApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**search_users**](SearchApi.md#search_users) | **GET** /api/v1/search/users | Search users


# **search_users**
> SearchUsersResponse search_users(page_size=page_size, query=query, properties=properties, starting_after=starting_after, ending_before=ending_before, expand=expand)

Search users

Search for users based on the provided query string. Set query to '*' to filter by other parameters only.
The number of records to return at a time can be controlled using the `page_size` query string parameter.

<div>
  <code>read:users</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.search_users_response import SearchUsersResponse
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
    api_instance = kinde_sdk.SearchApi(api_client)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    query = 'query_example' # str | Search the users by email or name. Use '*' to search all. (optional)
    properties = {'key': kinde_sdk.List[str]()} # Dict[str, List[str]] |  (optional)
    starting_after = 'starting_after_example' # str | The ID of the user to start after. (optional)
    ending_before = 'ending_before_example' # str | The ID of the user to end before. (optional)
    expand = 'expand_example' # str | Specify additional data to retrieve. Use \"organizations\" and/or \"identities\". (optional)

    try:
        # Search users
        api_response = api_instance.search_users(page_size=page_size, query=query, properties=properties, starting_after=starting_after, ending_before=ending_before, expand=expand)
        print("The response of SearchApi->search_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->search_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **query** | **str**| Search the users by email or name. Use &#39;*&#39; to search all. | [optional] 
 **properties** | [**Dict[str, List[str]]**](List[str].md)|  | [optional] 
 **starting_after** | **str**| The ID of the user to start after. | [optional] 
 **ending_before** | **str**| The ID of the user to end before. | [optional] 
 **expand** | **str**| Specify additional data to retrieve. Use \&quot;organizations\&quot; and/or \&quot;identities\&quot;. | [optional] 

### Return type

[**SearchUsersResponse**](SearchUsersResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Users successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

