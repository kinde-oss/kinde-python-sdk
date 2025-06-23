# CreateFeatureFlagRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the flag. | 
**description** | **str** | Description of the flag purpose. | [optional] 
**key** | **str** | The flag identifier to use in code. | 
**type** | **str** | The variable type. | 
**allow_override_level** | **str** | Allow the flag to be overridden at a different level. | [optional] 
**default_value** | **str** | Default value for the flag used by environments and organizations. | 

## Example

```python
from kinde_sdk.models.create_feature_flag_request import CreateFeatureFlagRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFeatureFlagRequest from a JSON string
create_feature_flag_request_instance = CreateFeatureFlagRequest.from_json(json)
# print the JSON string representation of the object
print(CreateFeatureFlagRequest.to_json())

# convert the object into a dict
create_feature_flag_request_dict = create_feature_flag_request_instance.to_dict()
# create an instance of CreateFeatureFlagRequest from a dict
create_feature_flag_request_from_dict = CreateFeatureFlagRequest.from_dict(create_feature_flag_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


