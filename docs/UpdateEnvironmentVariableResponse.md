# UpdateEnvironmentVariableResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | A Kinde generated message. | [optional] 
**code** | **str** | A Kinde generated status code. | [optional] 

## Example

```python
from kinde_sdk.models.update_environment_variable_response import UpdateEnvironmentVariableResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateEnvironmentVariableResponse from a JSON string
update_environment_variable_response_instance = UpdateEnvironmentVariableResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateEnvironmentVariableResponse.to_json())

# convert the object into a dict
update_environment_variable_response_dict = update_environment_variable_response_instance.to_dict()
# create an instance of UpdateEnvironmentVariableResponse from a dict
update_environment_variable_response_from_dict = UpdateEnvironmentVariableResponse.from_dict(update_environment_variable_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


