<a name="__pageTop"></a>
# kinde_sdk.apis.tags.subscribers_api.SubscribersApi

All URIs are relative to *https://app.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_subscriber**](#create_subscriber) | **post** /api/v1/subscribers | Create Subscriber
[**get_subscriber**](#get_subscriber) | **get** /api/v1/subscribers/{subscriber_id} | Get Subscriber
[**get_subscribers**](#get_subscribers) | **get** /api/v1/subscribers | List Subscribers

# **create_subscriber**
<a name="create_subscriber"></a>
> CreateSubscriberSuccessResponse create_subscriber(first_namelast_nameemail)

Create Subscriber

Create subscriber.

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import subscribers_api
from kinde_sdk.model.create_subscriber_success_response import CreateSubscriberSuccessResponse
from kinde_sdk.model.error_response import ErrorResponse
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

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = subscribers_api.SubscribersApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'first_name': "first_name_example",
        'last_name': "last_name_example",
        'email': "email_example",
    }
    try:
        # Create Subscriber
        api_response = api_instance.create_subscriber(
            query_params=query_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling SubscribersApi->create_subscriber: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
first_name | FirstNameSchema | | 
last_name | LastNameSchema | | 
email | EmailSchema | | 


# FirstNameSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# LastNameSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, str,  | NoneClass, str,  |  | 

# EmailSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, str,  | NoneClass, str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_subscriber.ApiResponseFor201) | Subscriber successfully created
400 | [ApiResponseFor400](#create_subscriber.ApiResponseFor400) | Invalid request.
403 | [ApiResponseFor403](#create_subscriber.ApiResponseFor403) | Invalid credentials.

#### create_subscriber.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**CreateSubscriberSuccessResponse**](../../models/CreateSubscriberSuccessResponse.md) |  | 


#### create_subscriber.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### create_subscriber.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_subscriber**
<a name="get_subscriber"></a>
> GetSubscriberResponse get_subscriber(subscriber_id)

Get Subscriber

Retrieve a subscriber record. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import subscribers_api
from kinde_sdk.model.get_subscriber_response import GetSubscriberResponse
from kinde_sdk.model.error_response import ErrorResponse
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

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = subscribers_api.SubscribersApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'subscriber_id': "subscriber_id_example",
    }
    try:
        # Get Subscriber
        api_response = api_instance.get_subscriber(
            path_params=path_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling SubscribersApi->get_subscriber: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
subscriber_id | SubscriberIdSchema | | 

# SubscriberIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_subscriber.ApiResponseFor200) | Subscriber successfully retrieved.
400 | [ApiResponseFor400](#get_subscriber.ApiResponseFor400) | Bad request.
403 | [ApiResponseFor403](#get_subscriber.ApiResponseFor403) | Invalid credentials.

#### get_subscriber.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**GetSubscriberResponse**](../../models/GetSubscriberResponse.md) |  | 


#### get_subscriber.ApiResponseFor400
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor400ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor400ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


#### get_subscriber.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_subscribers**
<a name="get_subscribers"></a>
> GetSubscribersResponse get_subscribers()

List Subscribers

The returned list can be sorted by full name or email address in ascending or descending order. The number of records to return at a time can also be controlled using the `page_size` query string parameter. 

### Example

* Bearer (JWT) Authentication (kindeBearerAuth):
```python
import kinde_sdk
from kinde_sdk.apis.tags import subscribers_api
from kinde_sdk.model.get_subscribers_response import GetSubscribersResponse
from kinde_sdk.model.error_response import ErrorResponse
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

# Configure Bearer authorization (JWT): kindeBearerAuth
configuration = kinde_sdk.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with kinde_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = subscribers_api.SubscribersApi(api_client)

    # example passing only optional values
    query_params = {
        'sort': "name_asc",
        'page_size': 1,
        'next_token': "next_token_example",
    }
    try:
        # List Subscribers
        api_response = api_instance.get_subscribers(
            query_params=query_params,
        )
        pprint(api_response)
    except kinde_sdk.ApiException as e:
        print("Exception when calling SubscribersApi->get_subscribers: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json; charset&#x3D;utf-8', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
sort | SortSchema | | optional
page_size | PageSizeSchema | | optional
next_token | NextTokenSchema | | optional


# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, str,  | NoneClass, str,  |  | must be one of ["name_asc", "name_desc", "email_asc", "email_desc", ] 

# PageSizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, decimal.Decimal, int,  | NoneClass, decimal.Decimal,  |  | 

# NextTokenSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None, str,  | NoneClass, str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_subscribers.ApiResponseFor200) | Subscriber successfully retrieved.
403 | [ApiResponseFor403](#get_subscribers.ApiResponseFor403) | Bad request.

#### get_subscribers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**GetSubscribersResponse**](../../models/GetSubscribersResponse.md) |  | 


#### get_subscribers.ApiResponseFor403
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor403ResponseBodyApplicationJsonCharsetutf8, ] |  |
headers | Unset | headers were not defined |

# SchemaFor403ResponseBodyApplicationJsonCharsetutf8
Type | Description  | Notes
------------- | ------------- | -------------
[**ErrorResponse**](../../models/ErrorResponse.md) |  | 


### Authorization

[kindeBearerAuth](../../../README.md#kindeBearerAuth)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

