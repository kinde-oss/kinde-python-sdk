# UpdateRolePermissionsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | [**List[UpdateRolePermissionsRequestPermissionsInner]**](UpdateRolePermissionsRequestPermissionsInner.md) | Permissions to add or remove from the role. | [optional] 

## Example

```python
from kinde_sdk.models.update_role_permissions_request import UpdateRolePermissionsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateRolePermissionsRequest from a JSON string
update_role_permissions_request_instance = UpdateRolePermissionsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateRolePermissionsRequest.to_json())

# convert the object into a dict
update_role_permissions_request_dict = update_role_permissions_request_instance.to_dict()
# create an instance of UpdateRolePermissionsRequest from a dict
update_role_permissions_request_from_dict = UpdateRolePermissionsRequest.from_dict(update_role_permissions_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


