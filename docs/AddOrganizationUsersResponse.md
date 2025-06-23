# AddOrganizationUsersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**users_added** | **List[str]** |  | [optional] 

## Example

```python
from kinde_sdk.models.add_organization_users_response import AddOrganizationUsersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AddOrganizationUsersResponse from a JSON string
add_organization_users_response_instance = AddOrganizationUsersResponse.from_json(json)
# print the JSON string representation of the object
print(AddOrganizationUsersResponse.to_json())

# convert the object into a dict
add_organization_users_response_dict = add_organization_users_response_instance.to_dict()
# create an instance of AddOrganizationUsersResponse from a dict
add_organization_users_response_from_dict = AddOrganizationUsersResponse.from_dict(add_organization_users_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


