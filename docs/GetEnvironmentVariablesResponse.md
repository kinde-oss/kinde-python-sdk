# GetEnvironmentVariablesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**has_more** | **bool** | Whether more records exist. | [optional] 
**environment_variables** | [**List[EnvironmentVariable]**](EnvironmentVariable.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_environment_variables_response import GetEnvironmentVariablesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetEnvironmentVariablesResponse from a JSON string
get_environment_variables_response_instance = GetEnvironmentVariablesResponse.from_json(json)
# print the JSON string representation of the object
print(GetEnvironmentVariablesResponse.to_json())

# convert the object into a dict
get_environment_variables_response_dict = get_environment_variables_response_instance.to_dict()
# create an instance of GetEnvironmentVariablesResponse from a dict
get_environment_variables_response_from_dict = GetEnvironmentVariablesResponse.from_dict(get_environment_variables_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


