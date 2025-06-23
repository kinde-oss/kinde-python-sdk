# GetFeatureFlagsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**GetFeatureFlagsResponseData**](GetFeatureFlagsResponseData.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_feature_flags_response import GetFeatureFlagsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeatureFlagsResponse from a JSON string
get_feature_flags_response_instance = GetFeatureFlagsResponse.from_json(json)
# print the JSON string representation of the object
print(GetFeatureFlagsResponse.to_json())

# convert the object into a dict
get_feature_flags_response_dict = get_feature_flags_response_instance.to_dict()
# create an instance of GetFeatureFlagsResponse from a dict
get_feature_flags_response_from_dict = GetFeatureFlagsResponse.from_dict(get_feature_flags_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


