# CreateMeterUsageRecordRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customer_agreement_id** | **str** | The billing agreement against which to record usage | 
**billing_feature_code** | **str** | The code of the feature within the agreement against which to record usage | 
**meter_value** | **str** | The value of usage to record | 
**meter_usage_timestamp** | **datetime** | The date and time the usage needs to be recorded for (defaults to current date/time) | [optional] 

## Example

```python
from kinde_sdk.models.create_meter_usage_record_request import CreateMeterUsageRecordRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateMeterUsageRecordRequest from a JSON string
create_meter_usage_record_request_instance = CreateMeterUsageRecordRequest.from_json(json)
# print the JSON string representation of the object
print(CreateMeterUsageRecordRequest.to_json())

# convert the object into a dict
create_meter_usage_record_request_dict = create_meter_usage_record_request_instance.to_dict()
# create an instance of CreateMeterUsageRecordRequest from a dict
create_meter_usage_record_request_from_dict = CreateMeterUsageRecordRequest.from_dict(create_meter_usage_record_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


