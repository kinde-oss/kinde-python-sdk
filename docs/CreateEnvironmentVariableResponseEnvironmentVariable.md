# CreateEnvironmentVariableResponseEnvironmentVariable


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique ID for the environment variable. | [optional] 

## Example

```python
from kinde_sdk.models.create_environment_variable_response_environment_variable import CreateEnvironmentVariableResponseEnvironmentVariable

# TODO update the JSON string below
json = "{}"
# create an instance of CreateEnvironmentVariableResponseEnvironmentVariable from a JSON string
create_environment_variable_response_environment_variable_instance = CreateEnvironmentVariableResponseEnvironmentVariable.from_json(json)
# print the JSON string representation of the object
print(CreateEnvironmentVariableResponseEnvironmentVariable.to_json())

# convert the object into a dict
create_environment_variable_response_environment_variable_dict = create_environment_variable_response_environment_variable_instance.to_dict()
# create an instance of CreateEnvironmentVariableResponseEnvironmentVariable from a dict
create_environment_variable_response_environment_variable_from_dict = CreateEnvironmentVariableResponseEnvironmentVariable.from_dict(create_environment_variable_response_environment_variable_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


