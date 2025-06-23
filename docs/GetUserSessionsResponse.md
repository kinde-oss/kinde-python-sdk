# GetUserSessionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** |  | [optional] 
**message** | **str** |  | [optional] 
**has_more** | **bool** |  | [optional] 
**sessions** | [**List[GetUserSessionsResponseSessionsInner]**](GetUserSessionsResponseSessionsInner.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_user_sessions_response import GetUserSessionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserSessionsResponse from a JSON string
get_user_sessions_response_instance = GetUserSessionsResponse.from_json(json)
# print the JSON string representation of the object
print(GetUserSessionsResponse.to_json())

# convert the object into a dict
get_user_sessions_response_dict = get_user_sessions_response_instance.to_dict()
# create an instance of GetUserSessionsResponse from a dict
get_user_sessions_response_from_dict = GetUserSessionsResponse.from_dict(get_user_sessions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


