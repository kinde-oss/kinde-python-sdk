# AddOrganizationUsersRequestUsersInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The users id. | [optional] 
**roles** | **List[str]** | Role keys to assign to the user. | [optional] 
**permissions** | **List[str]** | Permission keys to assign to the user. | [optional] 

## Example

```python
from kinde_sdk.models.add_organization_users_request_users_inner import AddOrganizationUsersRequestUsersInner

# TODO update the JSON string below
json = "{}"
# create an instance of AddOrganizationUsersRequestUsersInner from a JSON string
add_organization_users_request_users_inner_instance = AddOrganizationUsersRequestUsersInner.from_json(json)
# print the JSON string representation of the object
print(AddOrganizationUsersRequestUsersInner.to_json())

# convert the object into a dict
add_organization_users_request_users_inner_dict = add_organization_users_request_users_inner_instance.to_dict()
# create an instance of AddOrganizationUsersRequestUsersInner from a dict
add_organization_users_request_users_inner_from_dict = AddOrganizationUsersRequestUsersInner.from_dict(add_organization_users_request_users_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


