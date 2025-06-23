# CreateMeterUsageRecordResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Response message. | [optional] 
**code** | **str** | Response code. | [optional] 

## Example

```python
from kinde_sdk.models.create_meter_usage_record_response import CreateMeterUsageRecordResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateMeterUsageRecordResponse from a JSON string
create_meter_usage_record_response_instance = CreateMeterUsageRecordResponse.from_json(json)
# print the JSON string representation of the object
print(CreateMeterUsageRecordResponse.to_json())

# convert the object into a dict
create_meter_usage_record_response_dict = create_meter_usage_record_response_instance.to_dict()
# create an instance of CreateMeterUsageRecordResponse from a dict
create_meter_usage_record_response_from_dict = CreateMeterUsageRecordResponse.from_dict(create_meter_usage_record_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


