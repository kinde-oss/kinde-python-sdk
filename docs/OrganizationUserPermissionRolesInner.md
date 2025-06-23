# OrganizationUserPermissionRolesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**key** | **str** |  | [optional] 

## Example

```python
from kinde_sdk.models.organization_user_permission_roles_inner import OrganizationUserPermissionRolesInner

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationUserPermissionRolesInner from a JSON string
organization_user_permission_roles_inner_instance = OrganizationUserPermissionRolesInner.from_json(json)
# print the JSON string representation of the object
print(OrganizationUserPermissionRolesInner.to_json())

# convert the object into a dict
organization_user_permission_roles_inner_dict = organization_user_permission_roles_inner_instance.to_dict()
# create an instance of OrganizationUserPermissionRolesInner from a dict
organization_user_permission_roles_inner_from_dict = OrganizationUserPermissionRolesInner.from_dict(organization_user_permission_roles_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


