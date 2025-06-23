# CreateUserRequestIdentitiesInner

The result of the user creation operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of identity to create, e.g. email, username, or phone. | [optional] 
**is_verified** | **bool** | Set whether an email or phone identity is verified or not. | [optional] 
**details** | [**CreateUserRequestIdentitiesInnerDetails**](CreateUserRequestIdentitiesInnerDetails.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_user_request_identities_inner import CreateUserRequestIdentitiesInner

# TODO update the JSON string below
json = "{}"
# create an instance of CreateUserRequestIdentitiesInner from a JSON string
create_user_request_identities_inner_instance = CreateUserRequestIdentitiesInner.from_json(json)
# print the JSON string representation of the object
print(CreateUserRequestIdentitiesInner.to_json())

# convert the object into a dict
create_user_request_identities_inner_dict = create_user_request_identities_inner_instance.to_dict()
# create an instance of CreateUserRequestIdentitiesInner from a dict
create_user_request_identities_inner_from_dict = CreateUserRequestIdentitiesInner.from_dict(create_user_request_identities_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


