# UpdateOrganizationUsersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | [optional] 
**code** | **str** |  | [optional] 
**users_added** | **List[str]** |  | [optional] 
**users_updated** | **List[str]** |  | [optional] 
**users_removed** | **List[str]** |  | [optional] 

## Example

```python
from kinde_sdk.models.update_organization_users_response import UpdateOrganizationUsersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateOrganizationUsersResponse from a JSON string
update_organization_users_response_instance = UpdateOrganizationUsersResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateOrganizationUsersResponse.to_json())

# convert the object into a dict
update_organization_users_response_dict = update_organization_users_response_instance.to_dict()
# create an instance of UpdateOrganizationUsersResponse from a dict
update_organization_users_response_from_dict = UpdateOrganizationUsersResponse.from_dict(update_organization_users_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


