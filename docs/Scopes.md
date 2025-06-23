# Scopes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Scope ID. | [optional] 
**key** | **str** | Scope key. | [optional] 
**description** | **str** | Description of scope. | [optional] 
**api_id** | **str** | API ID. | [optional] 

## Example

```python
from kinde_sdk.models.scopes import Scopes

# TODO update the JSON string below
json = "{}"
# create an instance of Scopes from a JSON string
scopes_instance = Scopes.from_json(json)
# print the JSON string representation of the object
print(Scopes.to_json())

# convert the object into a dict
scopes_dict = scopes_instance.to_dict()
# create an instance of Scopes from a dict
scopes_from_dict = Scopes.from_dict(scopes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


