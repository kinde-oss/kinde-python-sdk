# GetOrganizationUsersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**organization_users** | [**List[OrganizationUser]**](OrganizationUser.md) |  | [optional] 
**next_token** | **str** | Pagination token. | [optional] 

## Example

```python
from kinde_sdk.models.get_organization_users_response import GetOrganizationUsersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganizationUsersResponse from a JSON string
get_organization_users_response_instance = GetOrganizationUsersResponse.from_json(json)
# print the JSON string representation of the object
print(GetOrganizationUsersResponse.to_json())

# convert the object into a dict
get_organization_users_response_dict = get_organization_users_response_instance.to_dict()
# create an instance of GetOrganizationUsersResponse from a dict
get_organization_users_response_from_dict = GetOrganizationUsersResponse.from_dict(get_organization_users_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


