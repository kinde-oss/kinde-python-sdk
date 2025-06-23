# GetEventResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**event** | [**GetEventResponseEvent**](GetEventResponseEvent.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_event_response import GetEventResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetEventResponse from a JSON string
get_event_response_instance = GetEventResponse.from_json(json)
# print the JSON string representation of the object
print(GetEventResponse.to_json())

# convert the object into a dict
get_event_response_dict = get_event_response_instance.to_dict()
# create an instance of GetEventResponse from a dict
get_event_response_from_dict = GetEventResponse.from_dict(get_event_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


