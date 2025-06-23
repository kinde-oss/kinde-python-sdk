# SetUserPasswordRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hashed_password** | **str** | The hashed password. | 
**hashing_method** | **str** | The hashing method or algorithm used to encrypt the user’s password. Default is bcrypt. | [optional] 
**salt** | **str** | Extra characters added to passwords to make them stronger. Not required for bcrypt. | [optional] 
**salt_position** | **str** | Position of salt in password string. Not required for bcrypt. | [optional] 
**is_temporary_password** | **bool** | The user will be prompted to set a new password after entering this one. | [optional] 

## Example

```python
from kinde_sdk.models.set_user_password_request import SetUserPasswordRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SetUserPasswordRequest from a JSON string
set_user_password_request_instance = SetUserPasswordRequest.from_json(json)
# print the JSON string representation of the object
print(SetUserPasswordRequest.to_json())

# convert the object into a dict
set_user_password_request_dict = set_user_password_request_instance.to_dict()
# create an instance of SetUserPasswordRequest from a dict
set_user_password_request_from_dict = SetUserPasswordRequest.from_dict(set_user_password_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


