# GetUserPermissionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**GetUserPermissionsResponseData**](GetUserPermissionsResponseData.md) |  | [optional] 
**metadata** | [**GetUserPermissionsResponseMetadata**](GetUserPermissionsResponseMetadata.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_user_permissions_response import GetUserPermissionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserPermissionsResponse from a JSON string
get_user_permissions_response_instance = GetUserPermissionsResponse.from_json(json)
# print the JSON string representation of the object
print(GetUserPermissionsResponse.to_json())

# convert the object into a dict
get_user_permissions_response_dict = get_user_permissions_response_instance.to_dict()
# create an instance of GetUserPermissionsResponse from a dict
get_user_permissions_response_from_dict = GetUserPermissionsResponse.from_dict(get_user_permissions_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


