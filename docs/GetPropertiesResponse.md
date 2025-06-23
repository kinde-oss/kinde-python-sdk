# GetPropertiesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**properties** | [**List[ModelProperty]**](ModelProperty.md) |  | [optional] 
**has_more** | **bool** | Whether more records exist. | [optional] 

## Example

```python
from kinde_sdk.models.get_properties_response import GetPropertiesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPropertiesResponse from a JSON string
get_properties_response_instance = GetPropertiesResponse.from_json(json)
# print the JSON string representation of the object
print(GetPropertiesResponse.to_json())

# convert the object into a dict
get_properties_response_dict = get_properties_response_instance.to_dict()
# create an instance of GetPropertiesResponse from a dict
get_properties_response_from_dict = GetPropertiesResponse.from_dict(get_properties_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


