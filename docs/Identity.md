# Identity


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique ID for the identity | [optional] 
**type** | **str** | The type of identity | [optional] 
**is_confirmed** | **bool** | Whether the identity is confirmed | [optional] 
**created_on** | **str** | Date of user creation in ISO 8601 format | [optional] 
**last_login_on** | **str** | Date of last login in ISO 8601 format | [optional] 
**total_logins** | **int** |  | [optional] 
**name** | **str** | The value of the identity | [optional] 
**email** | **str** | The associated email of the identity | [optional] 
**is_primary** | **bool** | Whether the identity is the primary identity for the user | [optional] 

## Example

```python
from kinde_sdk.models.identity import Identity

# TODO update the JSON string below
json = "{}"
# create an instance of Identity from a JSON string
identity_instance = Identity.from_json(json)
# print the JSON string representation of the object
print(Identity.to_json())

# convert the object into a dict
identity_dict = identity_instance.to_dict()
# create an instance of Identity from a dict
identity_from_dict = Identity.from_dict(identity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


