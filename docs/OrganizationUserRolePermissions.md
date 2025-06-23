# OrganizationUserRolePermissions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**role** | **str** |  | [optional] 
**permissions** | [**OrganizationUserRolePermissionsPermissions**](OrganizationUserRolePermissionsPermissions.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.organization_user_role_permissions import OrganizationUserRolePermissions

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationUserRolePermissions from a JSON string
organization_user_role_permissions_instance = OrganizationUserRolePermissions.from_json(json)
# print the JSON string representation of the object
print(OrganizationUserRolePermissions.to_json())

# convert the object into a dict
organization_user_role_permissions_dict = organization_user_role_permissions_instance.to_dict()
# create an instance of OrganizationUserRolePermissions from a dict
organization_user_role_permissions_from_dict = OrganizationUserRolePermissions.from_dict(organization_user_role_permissions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


