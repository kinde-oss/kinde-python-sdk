# CreateEnvironmentVariableResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | A Kinde generated message. | [optional] 
**code** | **str** | A Kinde generated status code. | [optional] 
**environment_variable** | [**CreateEnvironmentVariableResponseEnvironmentVariable**](CreateEnvironmentVariableResponseEnvironmentVariable.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_environment_variable_response import CreateEnvironmentVariableResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateEnvironmentVariableResponse from a JSON string
create_environment_variable_response_instance = CreateEnvironmentVariableResponse.from_json(json)
# print the JSON string representation of the object
print(CreateEnvironmentVariableResponse.to_json())

# convert the object into a dict
create_environment_variable_response_dict = create_environment_variable_response_instance.to_dict()
# create an instance of CreateEnvironmentVariableResponse from a dict
create_environment_variable_response_from_dict = CreateEnvironmentVariableResponse.from_dict(create_environment_variable_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


