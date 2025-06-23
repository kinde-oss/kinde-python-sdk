# CreateUserRequestProfile

Basic information required to create a user.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**given_name** | **str** | User&#39;s first name. | [optional] 
**family_name** | **str** | User&#39;s last name. | [optional] 
**picture** | **str** | The user&#39;s profile picture. | [optional] 

## Example

```python
from kinde_sdk.models.create_user_request_profile import CreateUserRequestProfile

# TODO update the JSON string below
json = "{}"
# create an instance of CreateUserRequestProfile from a JSON string
create_user_request_profile_instance = CreateUserRequestProfile.from_json(json)
# print the JSON string representation of the object
print(CreateUserRequestProfile.to_json())

# convert the object into a dict
create_user_request_profile_dict = create_user_request_profile_instance.to_dict()
# create an instance of CreateUserRequestProfile from a dict
create_user_request_profile_from_dict = CreateUserRequestProfile.from_dict(create_user_request_profile_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


