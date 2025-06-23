# kinde_sdk.OAuthApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_user_profile_v2**](OAuthApi.md#get_user_profile_v2) | **GET** /oauth2/v2/user_profile | Get user profile
[**token_introspection**](OAuthApi.md#token_introspection) | **POST** /oauth2/introspect | Introspect
[**token_revocation**](OAuthApi.md#token_revocation) | **POST** /oauth2/revoke | Revoke token


# **get_user_profile_v2**
> UserProfileV2 get_user_profile_v2()

Get user profile

This endpoint returns a user's ID, names, profile picture URL and email of the currently logged in user.


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.user_profile_v2 import UserProfileV2
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
    api_instance = kinde_sdk.OAuthApi(api_client)

    try:
        # Get user profile
        api_response = api_instance.get_user_profile_v2()
        print("The response of OAuthApi->get_user_profile_v2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OAuthApi->get_user_profile_v2: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserProfileV2**](UserProfileV2.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Details of logged in user. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **token_introspection**
> TokenIntrospect token_introspection(token, token_type_hint=token_type_hint)

Introspect

Retrieve information about the provided token.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.token_introspect import TokenIntrospect
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
    api_instance = kinde_sdk.OAuthApi(api_client)
    token = 'token_example' # str | The token to be introspected.
    token_type_hint = 'token_type_hint_example' # str | A hint about the token type being queried in the request. (optional)

    try:
        # Introspect
        api_response = api_instance.token_introspection(token, token_type_hint=token_type_hint)
        print("The response of OAuthApi->token_introspection:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OAuthApi->token_introspection: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **token** | **str**| The token to be introspected. | 
 **token_type_hint** | **str**| A hint about the token type being queried in the request. | [optional] 

### Return type

[**TokenIntrospect**](TokenIntrospect.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Details of the token. |  -  |
**401** | Bad request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **token_revocation**
> token_revocation(client_id, token, client_secret=client_secret, token_type_hint=token_type_hint)

Revoke token

Use this endpoint to invalidate an access or refresh token. The token will no longer be valid for use.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
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
    api_instance = kinde_sdk.OAuthApi(api_client)
    client_id = 'client_id_example' # str | The `client_id` of your application.
    token = 'token_example' # str | The token to be revoked.
    client_secret = 'client_secret_example' # str | The `client_secret` of your application. Required for backend apps only. (optional)
    token_type_hint = 'token_type_hint_example' # str | The type of token to be revoked. (optional)

    try:
        # Revoke token
        api_instance.token_revocation(client_id, token, client_secret=client_secret, token_type_hint=token_type_hint)
    except Exception as e:
        print("Exception when calling OAuthApi->token_revocation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **client_id** | **str**| The &#x60;client_id&#x60; of your application. | 
 **token** | **str**| The token to be revoked. | 
 **client_secret** | **str**| The &#x60;client_secret&#x60; of your application. Required for backend apps only. | [optional] 
 **token_type_hint** | **str**| The type of token to be revoked. | [optional] 

### Return type

void (empty response body)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Token successfully revoked. |  -  |
**400** | Invalid request. |  -  |
**401** | Bad request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

