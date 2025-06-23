# GetUserPermissionsResponseDataPermissionsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The friendly ID of a permission | [optional] 
**name** | **str** | The name of the permission | [optional] 
**key** | **str** | The key of the permission | [optional] 

## Example

```python
from kinde_sdk.models.get_user_permissions_response_data_permissions_inner import GetUserPermissionsResponseDataPermissionsInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserPermissionsResponseDataPermissionsInner from a JSON string
get_user_permissions_response_data_permissions_inner_instance = GetUserPermissionsResponseDataPermissionsInner.from_json(json)
# print the JSON string representation of the object
print(GetUserPermissionsResponseDataPermissionsInner.to_json())

# convert the object into a dict
get_user_permissions_response_data_permissions_inner_dict = get_user_permissions_response_data_permissions_inner_instance.to_dict()
# create an instance of GetUserPermissionsResponseDataPermissionsInner from a dict
get_user_permissions_response_data_permissions_inner_from_dict = GetUserPermissionsResponseDataPermissionsInner.from_dict(get_user_permissions_response_data_permissions_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


