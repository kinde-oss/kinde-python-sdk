# UserIdentity


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of identity object created. | [optional] 
**result** | [**UserIdentityResult**](UserIdentityResult.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.user_identity import UserIdentity

# TODO update the JSON string below
json = "{}"
# create an instance of UserIdentity from a JSON string
user_identity_instance = UserIdentity.from_json(json)
# print the JSON string representation of the object
print(UserIdentity.to_json())

# convert the object into a dict
user_identity_dict = user_identity_instance.to_dict()
# create an instance of UserIdentity from a dict
user_identity_from_dict = UserIdentity.from_dict(user_identity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


