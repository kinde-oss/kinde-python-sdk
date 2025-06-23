# GetPermissionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**permissions** | [**List[Permissions]**](Permissions.md) |  | [optional] 
**next_token** | **str** | Pagination token. | [optional] 

## Example

```python
from kinde_sdk.models.get_permissions_response import GetPermissionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetPermissionsResponse from a JSON string
get_permissions_response_instance = GetPermissionsResponse.from_json(json)
# print the JSON string representation of the object
print(GetPermissionsResponse.to_json())

# convert the object into a dict
get_permissions_response_dict = get_permissions_response_instance.to_dict()
# create an instance of GetPermissionsResponse from a dict
get_permissions_response_from_dict = GetPermissionsResponse.from_dict(get_permissions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


