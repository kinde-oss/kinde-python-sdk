# GetEnvironmentFeatureFlagsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**feature_flags** | [**Dict[str, GetOrganizationFeatureFlagsResponseFeatureFlagsValue]**](GetOrganizationFeatureFlagsResponseFeatureFlagsValue.md) | The environment&#39;s feature flag settings. | [optional] 
**next_token** | **str** | Pagination token. | [optional] 

## Example

```python
from kinde_sdk.models.get_environment_feature_flags_response import GetEnvironmentFeatureFlagsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetEnvironmentFeatureFlagsResponse from a JSON string
get_environment_feature_flags_response_instance = GetEnvironmentFeatureFlagsResponse.from_json(json)
# print the JSON string representation of the object
print(GetEnvironmentFeatureFlagsResponse.to_json())

# convert the object into a dict
get_environment_feature_flags_response_dict = get_environment_feature_flags_response_instance.to_dict()
# create an instance of GetEnvironmentFeatureFlagsResponse from a dict
get_environment_feature_flags_response_from_dict = GetEnvironmentFeatureFlagsResponse.from_dict(get_environment_feature_flags_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


