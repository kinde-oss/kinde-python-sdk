# GetRolesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**roles** | [**List[Roles]**](Roles.md) |  | [optional] 
**next_token** | **str** | Pagination token. | [optional] 

## Example

```python
from kinde_sdk.models.get_roles_response import GetRolesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetRolesResponse from a JSON string
get_roles_response_instance = GetRolesResponse.from_json(json)
# print the JSON string representation of the object
print(GetRolesResponse.to_json())

# convert the object into a dict
get_roles_response_dict = get_roles_response_instance.to_dict()
# create an instance of GetRolesResponse from a dict
get_roles_response_from_dict = GetRolesResponse.from_dict(get_roles_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


