# UpdateRolePermissionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** |  | [optional] 
**message** | **str** |  | [optional] 
**permissions_added** | **List[str]** |  | [optional] 
**permissions_removed** | **List[str]** |  | [optional] 

## Example

```python
from kinde_sdk.models.update_role_permissions_response import UpdateRolePermissionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateRolePermissionsResponse from a JSON string
update_role_permissions_response_instance = UpdateRolePermissionsResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateRolePermissionsResponse.to_json())

# convert the object into a dict
update_role_permissions_response_dict = update_role_permissions_response_instance.to_dict()
# create an instance of UpdateRolePermissionsResponse from a dict
update_role_permissions_response_from_dict = UpdateRolePermissionsResponse.from_dict(update_role_permissions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


