# UpdateOrganizationUsersRequestUsersInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The users id. | [optional] 
**operation** | **str** | Optional operation, set to &#39;delete&#39; to remove the user from the organization. | [optional] 
**roles** | **List[str]** | Role keys to assign to the user. | [optional] 
**permissions** | **List[str]** | Permission keys to assign to the user. | [optional] 

## Example

```python
from kinde_sdk.models.update_organization_users_request_users_inner import UpdateOrganizationUsersRequestUsersInner

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateOrganizationUsersRequestUsersInner from a JSON string
update_organization_users_request_users_inner_instance = UpdateOrganizationUsersRequestUsersInner.from_json(json)
# print the JSON string representation of the object
print(UpdateOrganizationUsersRequestUsersInner.to_json())

# convert the object into a dict
update_organization_users_request_users_inner_dict = update_organization_users_request_users_inner_instance.to_dict()
# create an instance of UpdateOrganizationUsersRequestUsersInner from a dict
update_organization_users_request_users_inner_from_dict = UpdateOrganizationUsersRequestUsersInner.from_dict(update_organization_users_request_users_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


