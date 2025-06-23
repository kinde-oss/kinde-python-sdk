# OrganizationUser


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique ID for the user. | [optional] 
**email** | **str** | The user&#39;s email address. | [optional] 
**full_name** | **str** | The user&#39;s full name. | [optional] 
**last_name** | **str** | The user&#39;s last name. | [optional] 
**first_name** | **str** | The user&#39;s first name. | [optional] 
**picture** | **str** | The user&#39;s profile picture URL. | [optional] 
**joined_on** | **str** | The date the user joined the organization. | [optional] 
**last_accessed_on** | **str** | The date the user last accessed the organization. | [optional] 
**roles** | **List[str]** | The roles the user has in the organization. | [optional] 

## Example

```python
from kinde_sdk.models.organization_user import OrganizationUser

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationUser from a JSON string
organization_user_instance = OrganizationUser.from_json(json)
# print the JSON string representation of the object
print(OrganizationUser.to_json())

# convert the object into a dict
organization_user_dict = organization_user_instance.to_dict()
# create an instance of OrganizationUser from a dict
organization_user_from_dict = OrganizationUser.from_dict(organization_user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


