# kinde_sdk.FeatureFlagsApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_feature_flag**](FeatureFlagsApi.md#create_feature_flag) | **POST** /api/v1/feature_flags | Create Feature Flag
[**delete_feature_flag**](FeatureFlagsApi.md#delete_feature_flag) | **DELETE** /api/v1/feature_flags/{feature_flag_key} | Delete Feature Flag
[**update_feature_flag**](FeatureFlagsApi.md#update_feature_flag) | **PUT** /api/v1/feature_flags/{feature_flag_key} | Replace Feature Flag


# **create_feature_flag**
> SuccessResponse create_feature_flag(create_feature_flag_request)

Create Feature Flag

Create feature flag.

<div>
  <code>create:feature_flags</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_feature_flag_request import CreateFeatureFlagRequest
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
    api_instance = kinde_sdk.FeatureFlagsApi(api_client)
    create_feature_flag_request = kinde_sdk.CreateFeatureFlagRequest() # CreateFeatureFlagRequest | Flag details.

    try:
        # Create Feature Flag
        api_response = api_instance.create_feature_flag(create_feature_flag_request)
        print("The response of FeatureFlagsApi->create_feature_flag:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeatureFlagsApi->create_feature_flag: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_feature_flag_request** | [**CreateFeatureFlagRequest**](CreateFeatureFlagRequest.md)| Flag details. | 

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
**201** | Feature flag successfully created |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_feature_flag**
> SuccessResponse delete_feature_flag(feature_flag_key)

Delete Feature Flag

Delete feature flag

<div>
  <code>delete:feature_flags</code>
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
    api_instance = kinde_sdk.FeatureFlagsApi(api_client)
    feature_flag_key = 'feature_flag_key_example' # str | The identifier for the feature flag.

    try:
        # Delete Feature Flag
        api_response = api_instance.delete_feature_flag(feature_flag_key)
        print("The response of FeatureFlagsApi->delete_feature_flag:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeatureFlagsApi->delete_feature_flag: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_flag_key** | **str**| The identifier for the feature flag. | 

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
**200** | Feature flag successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_feature_flag**
> SuccessResponse update_feature_flag(feature_flag_key, name, description, type, allow_override_level, default_value)

Replace Feature Flag

Update feature flag.

<div>
  <code>update:feature_flags</code>
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
    api_instance = kinde_sdk.FeatureFlagsApi(api_client)
    feature_flag_key = 'feature_flag_key_example' # str | The key identifier for the feature flag.
    name = 'name_example' # str | The name of the flag.
    description = 'description_example' # str | Description of the flag purpose.
    type = 'type_example' # str | The variable type
    allow_override_level = 'allow_override_level_example' # str | Allow the flag to be overridden at a different level.
    default_value = 'default_value_example' # str | Default value for the flag used by environments and organizations.

    try:
        # Replace Feature Flag
        api_response = api_instance.update_feature_flag(feature_flag_key, name, description, type, allow_override_level, default_value)
        print("The response of FeatureFlagsApi->update_feature_flag:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FeatureFlagsApi->update_feature_flag: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **feature_flag_key** | **str**| The key identifier for the feature flag. | 
 **name** | **str**| The name of the flag. | 
 **description** | **str**| Description of the flag purpose. | 
 **type** | **str**| The variable type | 
 **allow_override_level** | **str**| Allow the flag to be overridden at a different level. | 
 **default_value** | **str**| Default value for the flag used by environments and organizations. | 

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
**200** | Feature flag successfully updated. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

