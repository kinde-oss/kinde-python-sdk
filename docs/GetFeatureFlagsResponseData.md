# GetFeatureFlagsResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_flags** | [**List[GetFeatureFlagsResponseDataFeatureFlagsInner]**](GetFeatureFlagsResponseDataFeatureFlagsInner.md) | A list of feature flags | [optional] 

## Example

```python
from kinde_sdk.models.get_feature_flags_response_data import GetFeatureFlagsResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeatureFlagsResponseData from a JSON string
get_feature_flags_response_data_instance = GetFeatureFlagsResponseData.from_json(json)
# print the JSON string representation of the object
print(GetFeatureFlagsResponseData.to_json())

# convert the object into a dict
get_feature_flags_response_data_dict = get_feature_flags_response_data_instance.to_dict()
# create an instance of GetFeatureFlagsResponseData from a dict
get_feature_flags_response_data_from_dict = GetFeatureFlagsResponseData.from_dict(get_feature_flags_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


