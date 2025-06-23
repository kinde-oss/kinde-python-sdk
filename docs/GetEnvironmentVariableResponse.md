# GetEnvironmentVariableResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**environment_variable** | [**EnvironmentVariable**](EnvironmentVariable.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_environment_variable_response import GetEnvironmentVariableResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetEnvironmentVariableResponse from a JSON string
get_environment_variable_response_instance = GetEnvironmentVariableResponse.from_json(json)
# print the JSON string representation of the object
print(GetEnvironmentVariableResponse.to_json())

# convert the object into a dict
get_environment_variable_response_dict = get_environment_variable_response_instance.to_dict()
# create an instance of GetEnvironmentVariableResponse from a dict
get_environment_variable_response_from_dict = GetEnvironmentVariableResponse.from_dict(get_environment_variable_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


