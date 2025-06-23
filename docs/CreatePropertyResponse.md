# CreatePropertyResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | [optional] 
**code** | **str** |  | [optional] 
**var_property** | [**CreatePropertyResponseProperty**](CreatePropertyResponseProperty.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_property_response import CreatePropertyResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePropertyResponse from a JSON string
create_property_response_instance = CreatePropertyResponse.from_json(json)
# print the JSON string representation of the object
print(CreatePropertyResponse.to_json())

# convert the object into a dict
create_property_response_dict = create_property_response_instance.to_dict()
# create an instance of CreatePropertyResponse from a dict
create_property_response_from_dict = CreatePropertyResponse.from_dict(create_property_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


