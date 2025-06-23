# UpdateRolePermissionsRequestPermissionsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The permission id. | [optional] 
**operation** | **str** | Optional operation, set to &#39;delete&#39; to remove the permission from the role. | [optional] 

## Example

```python
from kinde_sdk.models.update_role_permissions_request_permissions_inner import UpdateRolePermissionsRequestPermissionsInner

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateRolePermissionsRequestPermissionsInner from a JSON string
update_role_permissions_request_permissions_inner_instance = UpdateRolePermissionsRequestPermissionsInner.from_json(json)
# print the JSON string representation of the object
print(UpdateRolePermissionsRequestPermissionsInner.to_json())

# convert the object into a dict
update_role_permissions_request_permissions_inner_dict = update_role_permissions_request_permissions_inner_instance.to_dict()
# create an instance of UpdateRolePermissionsRequestPermissionsInner from a dict
update_role_permissions_request_permissions_inner_from_dict = UpdateRolePermissionsRequestPermissionsInner.from_dict(update_role_permissions_request_permissions_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


