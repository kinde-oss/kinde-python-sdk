# CreateEnvironmentVariableRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | The name of the environment variable (max 128 characters). | 
**value** | **str** | The value of the new environment variable (max 2048 characters). | 
**is_secret** | **bool** | Whether the environment variable is sensitive. Secrets are not-readable by you or your team after creation. | [optional] 

## Example

```python
from kinde_sdk.models.create_environment_variable_request import CreateEnvironmentVariableRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateEnvironmentVariableRequest from a JSON string
create_environment_variable_request_instance = CreateEnvironmentVariableRequest.from_json(json)
# print the JSON string representation of the object
print(CreateEnvironmentVariableRequest.to_json())

# convert the object into a dict
create_environment_variable_request_dict = create_environment_variable_request_instance.to_dict()
# create an instance of CreateEnvironmentVariableRequest from a dict
create_environment_variable_request_from_dict = CreateEnvironmentVariableRequest.from_dict(create_environment_variable_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


