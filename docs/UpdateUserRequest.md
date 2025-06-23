# UpdateUserRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**given_name** | **str** | User&#39;s first name. | [optional] 
**family_name** | **str** | User&#39;s last name. | [optional] 
**picture** | **str** | The user&#39;s profile picture. | [optional] 
**is_suspended** | **bool** | Whether the user is currently suspended or not. | [optional] 
**is_password_reset_requested** | **bool** | Prompt the user to change their password on next sign in. | [optional] 
**provided_id** | **str** | An external id to reference the user. | [optional] 

## Example

```python
from kinde_sdk.models.update_user_request import UpdateUserRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserRequest from a JSON string
update_user_request_instance = UpdateUserRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateUserRequest.to_json())

# convert the object into a dict
update_user_request_dict = update_user_request_instance.to_dict()
# create an instance of UpdateUserRequest from a dict
update_user_request_from_dict = UpdateUserRequest.from_dict(update_user_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


