# kinde_sdk.PropertyCategoriesApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_category**](PropertyCategoriesApi.md#create_category) | **POST** /api/v1/property_categories | Create Category
[**get_categories**](PropertyCategoriesApi.md#get_categories) | **GET** /api/v1/property_categories | List categories
[**update_category**](PropertyCategoriesApi.md#update_category) | **PUT** /api/v1/property_categories/{category_id} | Update Category


# **create_category**
> CreateCategoryResponse create_category(create_category_request)

Create Category

Create category.

<div>
  <code>create:property_categories</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_category_request import CreateCategoryRequest
from kinde_sdk.models.create_category_response import CreateCategoryResponse
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
    api_instance = kinde_sdk.PropertyCategoriesApi(api_client)
    create_category_request = kinde_sdk.CreateCategoryRequest() # CreateCategoryRequest | Category details.

    try:
        # Create Category
        api_response = api_instance.create_category(create_category_request)
        print("The response of PropertyCategoriesApi->create_category:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PropertyCategoriesApi->create_category: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_category_request** | [**CreateCategoryRequest**](CreateCategoryRequest.md)| Category details. | 

### Return type

[**CreateCategoryResponse**](CreateCategoryResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Category successfully created |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_categories**
> GetCategoriesResponse get_categories(page_size=page_size, starting_after=starting_after, ending_before=ending_before, context=context)

List categories

Returns a list of categories.

<div>
  <code>read:property_categories</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_categories_response import GetCategoriesResponse
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
    api_instance = kinde_sdk.PropertyCategoriesApi(api_client)
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    starting_after = 'starting_after_example' # str | The ID of the category to start after. (optional)
    ending_before = 'ending_before_example' # str | The ID of the category to end before. (optional)
    context = 'context_example' # str | Filter the results by User or Organization context (optional)

    try:
        # List categories
        api_response = api_instance.get_categories(page_size=page_size, starting_after=starting_after, ending_before=ending_before, context=context)
        print("The response of PropertyCategoriesApi->get_categories:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PropertyCategoriesApi->get_categories: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **starting_after** | **str**| The ID of the category to start after. | [optional] 
 **ending_before** | **str**| The ID of the category to end before. | [optional] 
 **context** | **str**| Filter the results by User or Organization context | [optional] 

### Return type

[**GetCategoriesResponse**](GetCategoriesResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Categories successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_category**
> SuccessResponse update_category(category_id, update_category_request)

Update Category

Update category.

<div>
  <code>update:property_categories</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.success_response import SuccessResponse
from kinde_sdk.models.update_category_request import UpdateCategoryRequest
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
    api_instance = kinde_sdk.PropertyCategoriesApi(api_client)
    category_id = 'category_id_example' # str | The unique identifier for the category.
    update_category_request = kinde_sdk.UpdateCategoryRequest() # UpdateCategoryRequest | The fields of the category to update.

    try:
        # Update Category
        api_response = api_instance.update_category(category_id, update_category_request)
        print("The response of PropertyCategoriesApi->update_category:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PropertyCategoriesApi->update_category: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category_id** | **str**| The unique identifier for the category. | 
 **update_category_request** | [**UpdateCategoryRequest**](UpdateCategoryRequest.md)| The fields of the category to update. | 

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
**200** | category successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

