# ReadEnvLogoResponseLogosInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of logo (light or dark). | [optional] 
**file_name** | **str** | The name of the logo file. | [optional] 

## Example

```python
from kinde_sdk.models.read_env_logo_response_logos_inner import ReadEnvLogoResponseLogosInner

# TODO update the JSON string below
json = "{}"
# create an instance of ReadEnvLogoResponseLogosInner from a JSON string
read_env_logo_response_logos_inner_instance = ReadEnvLogoResponseLogosInner.from_json(json)
# print the JSON string representation of the object
print(ReadEnvLogoResponseLogosInner.to_json())

# convert the object into a dict
read_env_logo_response_logos_inner_dict = read_env_logo_response_logos_inner_instance.to_dict()
# create an instance of ReadEnvLogoResponseLogosInner from a dict
read_env_logo_response_logos_inner_from_dict = ReadEnvLogoResponseLogosInner.from_dict(read_env_logo_response_logos_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


