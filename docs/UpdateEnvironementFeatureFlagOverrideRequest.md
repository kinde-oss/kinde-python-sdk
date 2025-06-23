# UpdateEnvironementFeatureFlagOverrideRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** | The flag override value. | 

## Example

```python
from kinde_sdk.models.update_environement_feature_flag_override_request import UpdateEnvironementFeatureFlagOverrideRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateEnvironementFeatureFlagOverrideRequest from a JSON string
update_environement_feature_flag_override_request_instance = UpdateEnvironementFeatureFlagOverrideRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateEnvironementFeatureFlagOverrideRequest.to_json())

# convert the object into a dict
update_environement_feature_flag_override_request_dict = update_environement_feature_flag_override_request_instance.to_dict()
# create an instance of UpdateEnvironementFeatureFlagOverrideRequest from a dict
update_environement_feature_flag_override_request_from_dict = UpdateEnvironementFeatureFlagOverrideRequest.from_dict(update_environement_feature_flag_override_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


