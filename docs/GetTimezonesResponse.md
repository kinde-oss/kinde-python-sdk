# GetTimezonesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**timezones** | [**List[GetTimezonesResponseTimezonesInner]**](GetTimezonesResponseTimezonesInner.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_timezones_response import GetTimezonesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetTimezonesResponse from a JSON string
get_timezones_response_instance = GetTimezonesResponse.from_json(json)
# print the JSON string representation of the object
print(GetTimezonesResponse.to_json())

# convert the object into a dict
get_timezones_response_dict = get_timezones_response_instance.to_dict()
# create an instance of GetTimezonesResponse from a dict
get_timezones_response_from_dict = GetTimezonesResponse.from_dict(get_timezones_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


