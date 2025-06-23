# kinde_sdk.ConnectedAppsApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_connected_app_auth_url**](ConnectedAppsApi.md#get_connected_app_auth_url) | **GET** /api/v1/connected_apps/auth_url | Get Connected App URL
[**get_connected_app_token**](ConnectedAppsApi.md#get_connected_app_token) | **GET** /api/v1/connected_apps/token | Get Connected App Token
[**revoke_connected_app_token**](ConnectedAppsApi.md#revoke_connected_app_token) | **POST** /api/v1/connected_apps/revoke | Revoke Connected App Token


# **get_connected_app_auth_url**
> ConnectedAppsAuthUrl get_connected_app_auth_url(key_code_ref, user_id=user_id, org_code=org_code, override_callback_url=override_callback_url)

Get Connected App URL

Get a URL that authenticates and authorizes a user to a third-party connected app.

<div>
  <code>read:connected_apps</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.connected_apps_auth_url import ConnectedAppsAuthUrl
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
    api_instance = kinde_sdk.ConnectedAppsApi(api_client)
    key_code_ref = 'key_code_ref_example' # str | The unique key code reference of the connected app to authenticate against.
    user_id = 'user_id_example' # str | The id of the user that needs to authenticate to the third-party connected app. (optional)
    org_code = 'org_code_example' # str | The code of the Kinde organization that needs to authenticate to the third-party connected app. (optional)
    override_callback_url = 'override_callback_url_example' # str | A URL that overrides the default callback URL setup in your connected app configuration (optional)

    try:
        # Get Connected App URL
        api_response = api_instance.get_connected_app_auth_url(key_code_ref, user_id=user_id, org_code=org_code, override_callback_url=override_callback_url)
        print("The response of ConnectedAppsApi->get_connected_app_auth_url:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectedAppsApi->get_connected_app_auth_url: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key_code_ref** | **str**| The unique key code reference of the connected app to authenticate against. | 
 **user_id** | **str**| The id of the user that needs to authenticate to the third-party connected app. | [optional] 
 **org_code** | **str**| The code of the Kinde organization that needs to authenticate to the third-party connected app. | [optional] 
 **override_callback_url** | **str**| A URL that overrides the default callback URL setup in your connected app configuration | [optional] 

### Return type

[**ConnectedAppsAuthUrl**](ConnectedAppsAuthUrl.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A URL that can be used to authenticate and a session id to identify this authentication session. |  -  |
**400** | Error retrieving connected app auth url. |  -  |
**403** | Invalid credentials. |  -  |
**404** | Error retrieving connected app auth url. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_connected_app_token**
> ConnectedAppsAccessToken get_connected_app_token(session_id)

Get Connected App Token

Get an access token that can be used to call the third-party provider linked to the connected app.

<div>
  <code>read:connected_apps</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.connected_apps_access_token import ConnectedAppsAccessToken
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
    api_instance = kinde_sdk.ConnectedAppsApi(api_client)
    session_id = 'session_id_example' # str | The unique sesssion id representing the login session of a user.

    try:
        # Get Connected App Token
        api_response = api_instance.get_connected_app_token(session_id)
        print("The response of ConnectedAppsApi->get_connected_app_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectedAppsApi->get_connected_app_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| The unique sesssion id representing the login session of a user. | 

### Return type

[**ConnectedAppsAccessToken**](ConnectedAppsAccessToken.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/json; charset=utf-8

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | An access token that can be used to query a third-party provider, as well as the token&#39;s expiry time. |  -  |
**400** | The session id provided points to an invalid session. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **revoke_connected_app_token**
> SuccessResponse revoke_connected_app_token(session_id)

Revoke Connected App Token

Revoke the tokens linked to the connected app session.

<div>
  <code>create:connected_apps</code>
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
    api_instance = kinde_sdk.ConnectedAppsApi(api_client)
    session_id = 'session_id_example' # str | The unique sesssion id representing the login session of a user.

    try:
        # Revoke Connected App Token
        api_response = api_instance.revoke_connected_app_token(session_id)
        print("The response of ConnectedAppsApi->revoke_connected_app_token:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ConnectedAppsApi->revoke_connected_app_token: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **session_id** | **str**| The unique sesssion id representing the login session of a user. | 

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
**200** | An access token that can be used to query a third-party provider, as well as the token&#39;s expiry time. |  -  |
**400** | Bad request. |  -  |
**403** | Invalid credentials. |  -  |
**405** | Invalid HTTP method used. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

