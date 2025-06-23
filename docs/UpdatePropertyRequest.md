# UpdatePropertyRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the property. | 
**description** | **str** | Description of the property purpose. | [optional] 
**is_private** | **bool** | Whether the property can be included in id and access tokens. | 
**category_id** | **str** | Which category the property belongs to. | 

## Example

```python
from kinde_sdk.models.update_property_request import UpdatePropertyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdatePropertyRequest from a JSON string
update_property_request_instance = UpdatePropertyRequest.from_json(json)
# print the JSON string representation of the object
print(UpdatePropertyRequest.to_json())

# convert the object into a dict
update_property_request_dict = update_property_request_instance.to_dict()
# create an instance of UpdatePropertyRequest from a dict
update_property_request_from_dict = UpdatePropertyRequest.from_dict(update_property_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


