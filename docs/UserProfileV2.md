# UserProfileV2


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sub** | **str** | Unique ID of the user in Kinde. | [optional] 
**provided_id** | **str** | Value of the user&#39;s ID in a third-party system when the user is imported into Kinde. | [optional] 
**name** | **str** | User&#39;s first and last name separated by a space. | [optional] 
**given_name** | **str** | User&#39;s first name. | [optional] 
**family_name** | **str** | User&#39;s last name. | [optional] 
**updated_at** | **int** | Date the user was last updated at (In Unix time). | [optional] 
**email** | **str** | User&#39;s email address if available. | [optional] 
**email_verified** | **bool** | Whether the user&#39;s email address has been verified. | [optional] 
**picture** | **str** | URL that point&#39;s to the user&#39;s picture or avatar | [optional] 
**preferred_username** | **str** | User&#39;s preferred username. | [optional] 
**id** | **str** | Unique ID of the user in Kinde | [optional] 

## Example

```python
from kinde_sdk.models.user_profile_v2 import UserProfileV2

# TODO update the JSON string below
json = "{}"
# create an instance of UserProfileV2 from a JSON string
user_profile_v2_instance = UserProfileV2.from_json(json)
# print the JSON string representation of the object
print(UserProfileV2.to_json())

# convert the object into a dict
user_profile_v2_dict = user_profile_v2_instance.to_dict()
# create an instance of UserProfileV2 from a dict
user_profile_v2_from_dict = UserProfileV2.from_dict(user_profile_v2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


