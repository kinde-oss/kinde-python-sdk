# GetEventResponseEvent


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**event_id** | **str** |  | [optional] 
**timestamp** | **int** | Timestamp in ISO 8601 format. | [optional] 
**data** | **object** | Event specific data object. | [optional] 

## Example

```python
from kinde_sdk.models.get_event_response_event import GetEventResponseEvent

# TODO update the JSON string below
json = "{}"
# create an instance of GetEventResponseEvent from a JSON string
get_event_response_event_instance = GetEventResponseEvent.from_json(json)
# print the JSON string representation of the object
print(GetEventResponseEvent.to_json())

# convert the object into a dict
get_event_response_event_dict = get_event_response_event_instance.to_dict()
# create an instance of GetEventResponseEvent from a dict
get_event_response_event_from_dict = GetEventResponseEvent.from_dict(get_event_response_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


