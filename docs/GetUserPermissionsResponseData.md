# GetUserPermissionsResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_code** | **str** | The organization code the roles are associated with. | [optional] 
**permissions** | [**List[GetUserPermissionsResponseDataPermissionsInner]**](GetUserPermissionsResponseDataPermissionsInner.md) | A list of permissions | [optional] 

## Example

```python
from kinde_sdk.models.get_user_permissions_response_data import GetUserPermissionsResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserPermissionsResponseData from a JSON string
get_user_permissions_response_data_instance = GetUserPermissionsResponseData.from_json(json)
# print the JSON string representation of the object
print(GetUserPermissionsResponseData.to_json())

# convert the object into a dict
get_user_permissions_response_data_dict = get_user_permissions_response_data_instance.to_dict()
# create an instance of GetUserPermissionsResponseData from a dict
get_user_permissions_response_data_from_dict = GetUserPermissionsResponseData.from_dict(get_user_permissions_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


