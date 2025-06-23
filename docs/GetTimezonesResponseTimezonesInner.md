# GetTimezonesResponseTimezonesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | The unique key for the timezone. | [optional] 
**name** | **str** | The display name for the timezone. | [optional] 

## Example

```python
from kinde_sdk.models.get_timezones_response_timezones_inner import GetTimezonesResponseTimezonesInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetTimezonesResponseTimezonesInner from a JSON string
get_timezones_response_timezones_inner_instance = GetTimezonesResponseTimezonesInner.from_json(json)
# print the JSON string representation of the object
print(GetTimezonesResponseTimezonesInner.to_json())

# convert the object into a dict
get_timezones_response_timezones_inner_dict = get_timezones_response_timezones_inner_instance.to_dict()
# create an instance of GetTimezonesResponseTimezonesInner from a dict
get_timezones_response_timezones_inner_from_dict = GetTimezonesResponseTimezonesInner.from_dict(get_timezones_response_timezones_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


