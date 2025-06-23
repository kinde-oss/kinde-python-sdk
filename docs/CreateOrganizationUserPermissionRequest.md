# CreateOrganizationUserPermissionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permission_id** | **str** | The permission id. | [optional] 

## Example

```python
from kinde_sdk.models.create_organization_user_permission_request import CreateOrganizationUserPermissionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrganizationUserPermissionRequest from a JSON string
create_organization_user_permission_request_instance = CreateOrganizationUserPermissionRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOrganizationUserPermissionRequest.to_json())

# convert the object into a dict
create_organization_user_permission_request_dict = create_organization_user_permission_request_instance.to_dict()
# create an instance of CreateOrganizationUserPermissionRequest from a dict
create_organization_user_permission_request_from_dict = CreateOrganizationUserPermissionRequest.from_dict(create_organization_user_permission_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


