# GetOrganizationFeatureFlagsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**feature_flags** | [**Dict[str, GetOrganizationFeatureFlagsResponseFeatureFlagsValue]**](GetOrganizationFeatureFlagsResponseFeatureFlagsValue.md) | The environment&#39;s feature flag settings. | [optional] 

## Example

```python
from kinde_sdk.models.get_organization_feature_flags_response import GetOrganizationFeatureFlagsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganizationFeatureFlagsResponse from a JSON string
get_organization_feature_flags_response_instance = GetOrganizationFeatureFlagsResponse.from_json(json)
# print the JSON string representation of the object
print(GetOrganizationFeatureFlagsResponse.to_json())

# convert the object into a dict
get_organization_feature_flags_response_dict = get_organization_feature_flags_response_instance.to_dict()
# create an instance of GetOrganizationFeatureFlagsResponse from a dict
get_organization_feature_flags_response_from_dict = GetOrganizationFeatureFlagsResponse.from_dict(get_organization_feature_flags_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


