# UpdateRolesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The role&#39;s name. | 
**description** | **str** | The role&#39;s description. | [optional] 
**key** | **str** | The role identifier to use in code. | 
**is_default_role** | **bool** | Set role as default for new users. | [optional] 

## Example

```python
from kinde_sdk.models.update_roles_request import UpdateRolesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateRolesRequest from a JSON string
update_roles_request_instance = UpdateRolesRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateRolesRequest.to_json())

# convert the object into a dict
update_roles_request_dict = update_roles_request_instance.to_dict()
# create an instance of UpdateRolesRequest from a dict
update_roles_request_from_dict = UpdateRolesRequest.from_dict(update_roles_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


