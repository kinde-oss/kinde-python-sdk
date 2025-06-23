# UserIdentitiesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | [optional] 
**identity** | **str** |  | [optional] 

## Example

```python
from kinde_sdk.models.user_identities_inner import UserIdentitiesInner

# TODO update the JSON string below
json = "{}"
# create an instance of UserIdentitiesInner from a JSON string
user_identities_inner_instance = UserIdentitiesInner.from_json(json)
# print the JSON string representation of the object
print(UserIdentitiesInner.to_json())

# convert the object into a dict
user_identities_inner_dict = user_identities_inner_instance.to_dict()
# create an instance of UserIdentitiesInner from a dict
user_identities_inner_from_dict = UserIdentitiesInner.from_dict(user_identities_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


