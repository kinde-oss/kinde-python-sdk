# GetOrganizationsUserRolesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**roles** | [**List[OrganizationUserRole]**](OrganizationUserRole.md) |  | [optional] 
**next_token** | **str** | Pagination token. | [optional] 

## Example

```python
from kinde_sdk.models.get_organizations_user_roles_response import GetOrganizationsUserRolesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganizationsUserRolesResponse from a JSON string
get_organizations_user_roles_response_instance = GetOrganizationsUserRolesResponse.from_json(json)
# print the JSON string representation of the object
print(GetOrganizationsUserRolesResponse.to_json())

# convert the object into a dict
get_organizations_user_roles_response_dict = get_organizations_user_roles_response_instance.to_dict()
# create an instance of GetOrganizationsUserRolesResponse from a dict
get_organizations_user_roles_response_from_dict = GetOrganizationsUserRolesResponse.from_dict(get_organizations_user_roles_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


