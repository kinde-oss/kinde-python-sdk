# GetUserPropertiesResponseDataPropertiesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The friendly ID of a property | [optional] 
**name** | **str** | The name of the property | [optional] 
**key** | **str** | The key of the property | [optional] 
**value** | [**StringBooleanInteger**](StringBooleanInteger.md) | The value of the property | [optional] 

## Example

```python
from kinde_sdk.models.get_user_properties_response_data_properties_inner import GetUserPropertiesResponseDataPropertiesInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserPropertiesResponseDataPropertiesInner from a JSON string
get_user_properties_response_data_properties_inner_instance = GetUserPropertiesResponseDataPropertiesInner.from_json(json)
# print the JSON string representation of the object
print(GetUserPropertiesResponseDataPropertiesInner.to_json())

# convert the object into a dict
get_user_properties_response_data_properties_inner_dict = get_user_properties_response_data_properties_inner_instance.to_dict()
# create an instance of GetUserPropertiesResponseDataPropertiesInner from a dict
get_user_properties_response_data_properties_inner_from_dict = GetUserPropertiesResponseDataPropertiesInner.from_dict(get_user_properties_response_data_properties_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


