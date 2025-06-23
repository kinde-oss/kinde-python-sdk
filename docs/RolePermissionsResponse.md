# RolePermissionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**permissions** | [**List[Permissions]**](Permissions.md) |  | [optional] 
**next_token** | **str** | Pagination token. | [optional] 

## Example

```python
from kinde_sdk.models.role_permissions_response import RolePermissionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RolePermissionsResponse from a JSON string
role_permissions_response_instance = RolePermissionsResponse.from_json(json)
# print the JSON string representation of the object
print(RolePermissionsResponse.to_json())

# convert the object into a dict
role_permissions_response_dict = role_permissions_response_instance.to_dict()
# create an instance of RolePermissionsResponse from a dict
role_permissions_response_from_dict = RolePermissionsResponse.from_dict(role_permissions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


