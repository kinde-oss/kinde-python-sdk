# UserIdentityResult

The result of the user creation operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created** | **bool** | True if the user identity was successfully created. | [optional] 

## Example

```python
from kinde_sdk.models.user_identity_result import UserIdentityResult

# TODO update the JSON string below
json = "{}"
# create an instance of UserIdentityResult from a JSON string
user_identity_result_instance = UserIdentityResult.from_json(json)
# print the JSON string representation of the object
print(UserIdentityResult.to_json())

# convert the object into a dict
user_identity_result_dict = user_identity_result_instance.to_dict()
# create an instance of UserIdentityResult from a dict
user_identity_result_from_dict = UserIdentityResult.from_dict(user_identity_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


