# GetUserRolesResponseDataRolesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The friendly ID of a role | [optional] 
**name** | **str** | The name of the role | [optional] 
**key** | **str** | The key of the role | [optional] 

## Example

```python
from kinde_sdk.models.get_user_roles_response_data_roles_inner import GetUserRolesResponseDataRolesInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserRolesResponseDataRolesInner from a JSON string
get_user_roles_response_data_roles_inner_instance = GetUserRolesResponseDataRolesInner.from_json(json)
# print the JSON string representation of the object
print(GetUserRolesResponseDataRolesInner.to_json())

# convert the object into a dict
get_user_roles_response_data_roles_inner_dict = get_user_roles_response_data_roles_inner_instance.to_dict()
# create an instance of GetUserRolesResponseDataRolesInner from a dict
get_user_roles_response_data_roles_inner_from_dict = GetUserRolesResponseDataRolesInner.from_dict(get_user_roles_response_data_roles_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


