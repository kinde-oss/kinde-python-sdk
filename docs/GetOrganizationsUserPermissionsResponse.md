# GetOrganizationsUserPermissionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**permissions** | [**List[OrganizationUserPermission]**](OrganizationUserPermission.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_organizations_user_permissions_response import GetOrganizationsUserPermissionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganizationsUserPermissionsResponse from a JSON string
get_organizations_user_permissions_response_instance = GetOrganizationsUserPermissionsResponse.from_json(json)
# print the JSON string representation of the object
print(GetOrganizationsUserPermissionsResponse.to_json())

# convert the object into a dict
get_organizations_user_permissions_response_dict = get_organizations_user_permissions_response_instance.to_dict()
# create an instance of GetOrganizationsUserPermissionsResponse from a dict
get_organizations_user_permissions_response_from_dict = GetOrganizationsUserPermissionsResponse.from_dict(get_organizations_user_permissions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


