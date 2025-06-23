# UpdateOrganizationUsersRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**users** | [**List[UpdateOrganizationUsersRequestUsersInner]**](UpdateOrganizationUsersRequestUsersInner.md) | Users to add, update or remove from the organization. | [optional] 

## Example

```python
from kinde_sdk.models.update_organization_users_request import UpdateOrganizationUsersRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateOrganizationUsersRequest from a JSON string
update_organization_users_request_instance = UpdateOrganizationUsersRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateOrganizationUsersRequest.to_json())

# convert the object into a dict
update_organization_users_request_dict = update_organization_users_request_instance.to_dict()
# create an instance of UpdateOrganizationUsersRequest from a dict
update_organization_users_request_from_dict = UpdateOrganizationUsersRequest.from_dict(update_organization_users_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


