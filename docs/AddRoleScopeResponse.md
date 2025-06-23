# AddRoleScopeResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 

## Example

```python
from kinde_sdk.models.add_role_scope_response import AddRoleScopeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AddRoleScopeResponse from a JSON string
add_role_scope_response_instance = AddRoleScopeResponse.from_json(json)
# print the JSON string representation of the object
print(AddRoleScopeResponse.to_json())

# convert the object into a dict
add_role_scope_response_dict = add_role_scope_response_instance.to_dict()
# create an instance of AddRoleScopeResponse from a dict
add_role_scope_response_from_dict = AddRoleScopeResponse.from_dict(add_role_scope_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


