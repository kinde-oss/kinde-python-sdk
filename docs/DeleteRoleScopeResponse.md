# DeleteRoleScopeResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 

## Example

```python
from kinde_sdk.models.delete_role_scope_response import DeleteRoleScopeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteRoleScopeResponse from a JSON string
delete_role_scope_response_instance = DeleteRoleScopeResponse.from_json(json)
# print the JSON string representation of the object
print(DeleteRoleScopeResponse.to_json())

# convert the object into a dict
delete_role_scope_response_dict = delete_role_scope_response_instance.to_dict()
# create an instance of DeleteRoleScopeResponse from a dict
delete_role_scope_response_from_dict = DeleteRoleScopeResponse.from_dict(delete_role_scope_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


