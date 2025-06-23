# kinde_sdk.BillingAgreementsApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_billing_agreement**](BillingAgreementsApi.md#create_billing_agreement) | **POST** /api/v1/billing/agreements | Create billing agreement
[**get_billing_agreements**](BillingAgreementsApi.md#get_billing_agreements) | **GET** /api/v1/billing/agreements | Get billing agreements


# **create_billing_agreement**
> SuccessResponse create_billing_agreement(create_billing_agreement_request)

Create billing agreement

Creates a new billing agreement based on the plan code passed, and cancels the customer's existing agreements

<div>
  <code>create:billing_agreements</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_billing_agreement_request import CreateBillingAgreementRequest
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
    api_instance = kinde_sdk.BillingAgreementsApi(api_client)
    create_billing_agreement_request = kinde_sdk.CreateBillingAgreementRequest() # CreateBillingAgreementRequest | New agreement request values

    try:
        # Create billing agreement
        api_response = api_instance.create_billing_agreement(create_billing_agreement_request)
        print("The response of BillingAgreementsApi->create_billing_agreement:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BillingAgreementsApi->create_billing_agreement: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_billing_agreement_request** | [**CreateBillingAgreementRequest**](CreateBillingAgreementRequest.md)| New agreement request values | 

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
**200** | Billing agreement successfully changed |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_billing_agreements**
> GetBillingAgreementsResponse get_billing_agreements(customer_id, page_size=page_size, starting_after=starting_after, ending_before=ending_before, feature_code=feature_code)

Get billing agreements

Returns all the agreements a billing customer currently has access to

<div>
  <code>read:billing_agreements</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.get_billing_agreements_response import GetBillingAgreementsResponse
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
    api_instance = kinde_sdk.BillingAgreementsApi(api_client)
    customer_id = 'customer_0195ac80a14c2ca2cec97d026d864de0' # str | The ID of the billing customer to retrieve agreements for
    page_size = 56 # int | Number of results per page. Defaults to 10 if parameter not sent. (optional)
    starting_after = 'starting_after_example' # str | The ID of the billing agreement to start after. (optional)
    ending_before = 'ending_before_example' # str | The ID of the billing agreement to end before. (optional)
    feature_code = 'feature_code_example' # str | The feature code to filter by agreements only containing that feature (optional)

    try:
        # Get billing agreements
        api_response = api_instance.get_billing_agreements(customer_id, page_size=page_size, starting_after=starting_after, ending_before=ending_before, feature_code=feature_code)
        print("The response of BillingAgreementsApi->get_billing_agreements:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BillingAgreementsApi->get_billing_agreements: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **str**| The ID of the billing customer to retrieve agreements for | 
 **page_size** | **int**| Number of results per page. Defaults to 10 if parameter not sent. | [optional] 
 **starting_after** | **str**| The ID of the billing agreement to start after. | [optional] 
 **ending_before** | **str**| The ID of the billing agreement to end before. | [optional] 
 **feature_code** | **str**| The feature code to filter by agreements only containing that feature | [optional] 

### Return type

[**GetBillingAgreementsResponse**](GetBillingAgreementsResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json; charset=utf-8, application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Billing agreements successfully retrieved. |  -  |
**400** | Invalid request. |  -  |
**403** | Invalid credentials. |  -  |
**429** | Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

