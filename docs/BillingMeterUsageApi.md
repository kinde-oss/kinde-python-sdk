# kinde_sdk.BillingMeterUsageApi

All URIs are relative to *https://your_kinde_subdomain.kinde.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_meter_usage_record**](BillingMeterUsageApi.md#create_meter_usage_record) | **POST** /api/v1/billing/meter_usage | Create meter usage record


# **create_meter_usage_record**
> CreateMeterUsageRecordResponse create_meter_usage_record(create_meter_usage_record_request)

Create meter usage record

Create a new meter usage record

<div>
  <code>create:meter_usage</code>
</div>


### Example

* Bearer (JWT) Authentication (kindeBearerAuth):

```python
import kinde_sdk
from kinde_sdk.models.create_meter_usage_record_request import CreateMeterUsageRecordRequest
from kinde_sdk.models.create_meter_usage_record_response import CreateMeterUsageRecordResponse
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
    api_instance = kinde_sdk.BillingMeterUsageApi(api_client)
    create_meter_usage_record_request = kinde_sdk.CreateMeterUsageRecordRequest() # CreateMeterUsageRecordRequest | Meter usage record

    try:
        # Create meter usage record
        api_response = api_instance.create_meter_usage_record(create_meter_usage_record_request)
        print("The response of BillingMeterUsageApi->create_meter_usage_record:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling BillingMeterUsageApi->create_meter_usage_record: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_meter_usage_record_request** | [**CreateMeterUsageRecordRequest**](CreateMeterUsageRecordRequest.md)| Meter usage record | 

### Return type

[**CreateMeterUsageRecordResponse**](CreateMeterUsageRecordResponse.md)

### Authorization

[kindeBearerAuth](../README.md#kindeBearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Meter usage record successfully created. |  -  |
**400** | Invalid request. |  -  |
**403** | Unauthorized - invalid credentials. |  -  |
**429** | Too many requests. Request was throttled. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

