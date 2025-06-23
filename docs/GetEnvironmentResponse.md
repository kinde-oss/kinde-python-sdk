# GetEnvironmentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**environment** | [**GetEnvironmentResponseEnvironment**](GetEnvironmentResponseEnvironment.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_environment_response import GetEnvironmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetEnvironmentResponse from a JSON string
get_environment_response_instance = GetEnvironmentResponse.from_json(json)
# print the JSON string representation of the object
print(GetEnvironmentResponse.to_json())

# convert the object into a dict
get_environment_response_dict = get_environment_response_instance.to_dict()
# create an instance of GetEnvironmentResponse from a dict
get_environment_response_from_dict = GetEnvironmentResponse.from_dict(get_environment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


