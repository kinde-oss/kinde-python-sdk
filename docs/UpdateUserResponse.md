# UpdateUserResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique ID of the user in Kinde. | [optional] 
**given_name** | **str** | User&#39;s first name. | [optional] 
**family_name** | **str** | User&#39;s last name. | [optional] 
**email** | **str** | User&#39;s preferred email. | [optional] 
**is_suspended** | **bool** | Whether the user is currently suspended or not. | [optional] 
**is_password_reset_requested** | **bool** | Whether a password reset has been requested. | [optional] 
**picture** | **str** | User&#39;s profile picture URL. | [optional] 

## Example

```python
from kinde_sdk.models.update_user_response import UpdateUserResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserResponse from a JSON string
update_user_response_instance = UpdateUserResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateUserResponse.to_json())

# convert the object into a dict
update_user_response_dict = update_user_response_instance.to_dict()
# create an instance of UpdateUserResponse from a dict
update_user_response_from_dict = UpdateUserResponse.from_dict(update_user_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


