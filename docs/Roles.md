# Roles


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The role&#39;s ID. | [optional] 
**key** | **str** | The role identifier to use in code. | [optional] 
**name** | **str** | The role&#39;s name. | [optional] 
**description** | **str** | The role&#39;s description. | [optional] 
**is_default_role** | **bool** | Whether the role is the default role. | [optional] 

## Example

```python
from kinde_sdk.models.roles import Roles

# TODO update the JSON string below
json = "{}"
# create an instance of Roles from a JSON string
roles_instance = Roles.from_json(json)
# print the JSON string representation of the object
print(Roles.to_json())

# convert the object into a dict
roles_dict = roles_instance.to_dict()
# create an instance of Roles from a dict
roles_from_dict = Roles.from_dict(roles_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


