# ReadEnvLogoResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**logos** | [**List[ReadEnvLogoResponseLogosInner]**](ReadEnvLogoResponseLogosInner.md) | A list of logos. | [optional] 
**message** | **str** | Response message. | [optional] 

## Example

```python
from kinde_sdk.models.read_env_logo_response import ReadEnvLogoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReadEnvLogoResponse from a JSON string
read_env_logo_response_instance = ReadEnvLogoResponse.from_json(json)
# print the JSON string representation of the object
print(ReadEnvLogoResponse.to_json())

# convert the object into a dict
read_env_logo_response_dict = read_env_logo_response_instance.to_dict()
# create an instance of ReadEnvLogoResponse from a dict
read_env_logo_response_from_dict = ReadEnvLogoResponse.from_dict(read_env_logo_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


