# GetIndustriesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**industries** | [**List[GetIndustriesResponseIndustriesInner]**](GetIndustriesResponseIndustriesInner.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_industries_response import GetIndustriesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetIndustriesResponse from a JSON string
get_industries_response_instance = GetIndustriesResponse.from_json(json)
# print the JSON string representation of the object
print(GetIndustriesResponse.to_json())

# convert the object into a dict
get_industries_response_dict = get_industries_response_instance.to_dict()
# create an instance of GetIndustriesResponse from a dict
get_industries_response_from_dict = GetIndustriesResponse.from_dict(get_industries_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


