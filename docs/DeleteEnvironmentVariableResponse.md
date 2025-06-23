# DeleteEnvironmentVariableResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | A Kinde generated message. | [optional] 
**code** | **str** | A Kinde generated status code. | [optional] 

## Example

```python
from kinde_sdk.models.delete_environment_variable_response import DeleteEnvironmentVariableResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteEnvironmentVariableResponse from a JSON string
delete_environment_variable_response_instance = DeleteEnvironmentVariableResponse.from_json(json)
# print the JSON string representation of the object
print(DeleteEnvironmentVariableResponse.to_json())

# convert the object into a dict
delete_environment_variable_response_dict = delete_environment_variable_response_instance.to_dict()
# create an instance of DeleteEnvironmentVariableResponse from a dict
delete_environment_variable_response_from_dict = DeleteEnvironmentVariableResponse.from_dict(delete_environment_variable_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


