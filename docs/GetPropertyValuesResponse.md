# GetPropertyValuesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**properties** | [**List[PropertyValue]**](PropertyValue.md) |  | [optional] 
**next_token** | **str** | Pagination token. | [optional] 

## Example

```python
from kinde_sdk.models.get_property_values_response import GetPropertyValuesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPropertyValuesResponse from a JSON string
get_property_values_response_instance = GetPropertyValuesResponse.from_json(json)
# print the JSON string representation of the object
print(GetPropertyValuesResponse.to_json())

# convert the object into a dict
get_property_values_response_dict = get_property_values_response_instance.to_dict()
# create an instance of GetPropertyValuesResponse from a dict
get_property_values_response_from_dict = GetPropertyValuesResponse.from_dict(get_property_values_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


