# CreateOrganizationUserRoleRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**role_id** | **str** | The role id. | [optional] 

## Example

```python
from kinde_sdk.models.create_organization_user_role_request import CreateOrganizationUserRoleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrganizationUserRoleRequest from a JSON string
create_organization_user_role_request_instance = CreateOrganizationUserRoleRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOrganizationUserRoleRequest.to_json())

# convert the object into a dict
create_organization_user_role_request_dict = create_organization_user_role_request_instance.to_dict()
# create an instance of CreateOrganizationUserRoleRequest from a dict
create_organization_user_role_request_from_dict = CreateOrganizationUserRoleRequest.from_dict(create_organization_user_role_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


