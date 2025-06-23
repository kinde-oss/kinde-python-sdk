# OrganizationUserPermission


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**key** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**roles** | [**List[OrganizationUserPermissionRolesInner]**](OrganizationUserPermissionRolesInner.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.organization_user_permission import OrganizationUserPermission

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationUserPermission from a JSON string
organization_user_permission_instance = OrganizationUserPermission.from_json(json)
# print the JSON string representation of the object
print(OrganizationUserPermission.to_json())

# convert the object into a dict
organization_user_permission_dict = organization_user_permission_instance.to_dict()
# create an instance of OrganizationUserPermission from a dict
organization_user_permission_from_dict = OrganizationUserPermission.from_dict(organization_user_permission_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


