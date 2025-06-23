# CreatePropertyRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the property. | 
**description** | **str** | Description of the property purpose. | [optional] 
**key** | **str** | The property identifier to use in code. | 
**type** | **str** | The property type. | 
**context** | **str** | The context that the property applies to. | 
**is_private** | **bool** | Whether the property can be included in id and access tokens. | 
**category_id** | **str** | Which category the property belongs to. | 

## Example

```python
from kinde_sdk.models.create_property_request import CreatePropertyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePropertyRequest from a JSON string
create_property_request_instance = CreatePropertyRequest.from_json(json)
# print the JSON string representation of the object
print(CreatePropertyRequest.to_json())

# convert the object into a dict
create_property_request_dict = create_property_request_instance.to_dict()
# create an instance of CreatePropertyRequest from a dict
create_property_request_from_dict = CreatePropertyRequest.from_dict(create_property_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


