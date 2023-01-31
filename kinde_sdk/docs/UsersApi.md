# kinde_sdk.UsersApi

All URIs are relative to *https://app.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_user**](UsersApi.md#create_user) | **POST** /api/v1/user | Creates a user record


# **create_user**
> CreateUser200Response create_user()

Creates a user record

Creates a user record and optionally zero or more identities for the user. An example identity could be the email address of the user

### Example

* OAuth Authentication (OAuth2):
* OAuth Authentication (OAuth2):
* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import time
import kinde_sdk
from kinde_sdk.api import users_api
from kinde_sdk.model.create_user200_response import CreateUser200Response
from kinde_sdk.model.create_user_request import CreateUserRequest
from pprint import pprint
# Defining the host is optional and defaults to https://app.kinde.com
# See configuration.py for a list of all supported configuration parameters.
configuration = kinde_sdk.Configuration(
    host = "https://app.kinde.com"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure OAuth2 access token for authorization: OAuth2
configuration = kinde_sdk.Configuration(
    host = "https://app.kinde.com"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: OAuth2
configuration = kinde_sdk.Configuration(
    host = "https://app.kinde.com"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)

# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = users_api.UsersApi(api_client)
    create_user_request = CreateUserRequest(
        profile=CreateUserRequestProfile(
            given_name="given_name_example",
            family_name="family_name_example",
        ),
        identities=[
            CreateUserRequestIdentitiesInner(
                type="type_example",
                details=CreateUserRequestIdentitiesInnerDetails(
                    email="email_example",
                ),
            ),
        ],
    ) # CreateUserRequest | The details of the user to create (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Creates a user record
        api_response = api_instance.create_user(create_user_request=create_user_request)
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling UsersApi->create_user: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_user_request** | [**CreateUserRequest**](CreateUserRequest.md)| The details of the user to create | [optional]

### Return type

[**CreateUser200Response**](CreateUser200Response.md)

### Authorization

[OAuth2](../README.md#OAuth2), [OAuth2](../README.md#OAuth2), [kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully created a new user |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)
