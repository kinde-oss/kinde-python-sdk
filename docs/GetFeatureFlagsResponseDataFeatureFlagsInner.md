# GetFeatureFlagsResponseDataFeatureFlagsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The friendly ID of an flag | [optional] 
**name** | **str** | The name of the flag | [optional] 
**key** | **str** | The key of the flag | [optional] 
**type** | **str** | The type of the flag | [optional] 
**value** | [**StringBooleanIntegerObject**](StringBooleanIntegerObject.md) | The value of the flag | [optional] 

## Example

```python
from kinde_sdk.models.get_feature_flags_response_data_feature_flags_inner import GetFeatureFlagsResponseDataFeatureFlagsInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeatureFlagsResponseDataFeatureFlagsInner from a JSON string
get_feature_flags_response_data_feature_flags_inner_instance = GetFeatureFlagsResponseDataFeatureFlagsInner.from_json(json)
# print the JSON string representation of the object
print(GetFeatureFlagsResponseDataFeatureFlagsInner.to_json())

# convert the object into a dict
get_feature_flags_response_data_feature_flags_inner_dict = get_feature_flags_response_data_feature_flags_inner_instance.to_dict()
# create an instance of GetFeatureFlagsResponseDataFeatureFlagsInner from a dict
get_feature_flags_response_data_feature_flags_inner_from_dict = GetFeatureFlagsResponseDataFeatureFlagsInner.from_dict(get_feature_flags_response_data_feature_flags_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


