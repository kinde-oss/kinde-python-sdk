# AddRoleScopeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scope_id** | **str** | The scope identifier. | 

## Example

```python
from kinde_sdk.models.add_role_scope_request import AddRoleScopeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddRoleScopeRequest from a JSON string
add_role_scope_request_instance = AddRoleScopeRequest.from_json(json)
# print the JSON string representation of the object
print(AddRoleScopeRequest.to_json())

# convert the object into a dict
add_role_scope_request_dict = add_role_scope_request_instance.to_dict()
# create an instance of AddRoleScopeRequest from a dict
add_role_scope_request_from_dict = AddRoleScopeRequest.from_dict(add_role_scope_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


