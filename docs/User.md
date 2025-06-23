# User


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique ID of the user in Kinde. | [optional] 
**provided_id** | **str** | External ID for user. | [optional] 
**preferred_email** | **str** | Default email address of the user in Kinde. | [optional] 
**phone** | **str** | User&#39;s primary phone number. | [optional] 
**username** | **str** | Primary username of the user in Kinde. | [optional] 
**last_name** | **str** | User&#39;s last name. | [optional] 
**first_name** | **str** | User&#39;s first name. | [optional] 
**is_suspended** | **bool** | Whether the user is currently suspended or not. | [optional] 
**picture** | **str** | User&#39;s profile picture URL. | [optional] 
**total_sign_ins** | **int** | Total number of user sign ins. | [optional] 
**failed_sign_ins** | **int** | Number of consecutive failed user sign ins. | [optional] 
**last_signed_in** | **str** | Last sign in date in ISO 8601 format. | [optional] 
**created_on** | **str** | Date of user creation in ISO 8601 format. | [optional] 
**organizations** | **List[str]** | Array of organizations a user belongs to. | [optional] 
**identities** | [**List[UserIdentitiesInner]**](UserIdentitiesInner.md) | Array of identities belonging to the user. | [optional] 

## Example

```python
from kinde_sdk.models.user import User

# TODO update the JSON string below
json = "{}"
# create an instance of User from a JSON string
user_instance = User.from_json(json)
# print the JSON string representation of the object
print(User.to_json())

# convert the object into a dict
user_dict = user_instance.to_dict()
# create an instance of User from a dict
user_from_dict = User.from_dict(user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


