# GetUserRolesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**GetUserRolesResponseData**](GetUserRolesResponseData.md) |  | [optional] 
**metadata** | [**GetUserRolesResponseMetadata**](GetUserRolesResponseMetadata.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_user_roles_response import GetUserRolesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserRolesResponse from a JSON string
get_user_roles_response_instance = GetUserRolesResponse.from_json(json)
# print the JSON string representation of the object
print(GetUserRolesResponse.to_json())

# convert the object into a dict
get_user_roles_response_dict = get_user_roles_response_instance.to_dict()
# create an instance of GetUserRolesResponse from a dict
get_user_roles_response_from_dict = GetUserRolesResponse.from_dict(get_user_roles_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


