# OrganizationUserRole


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**key** | **str** |  | [optional] 
**name** | **str** |  | [optional] 

## Example

```python
from kinde_sdk.models.organization_user_role import OrganizationUserRole

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationUserRole from a JSON string
organization_user_role_instance = OrganizationUserRole.from_json(json)
# print the JSON string representation of the object
print(OrganizationUserRole.to_json())

# convert the object into a dict
organization_user_role_dict = organization_user_role_instance.to_dict()
# create an instance of OrganizationUserRole from a dict
organization_user_role_from_dict = OrganizationUserRole.from_dict(organization_user_role_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


