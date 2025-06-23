# GetUserRolesResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_code** | **str** | The organization code the roles are associated with. | [optional] 
**roles** | [**List[GetUserRolesResponseDataRolesInner]**](GetUserRolesResponseDataRolesInner.md) | A list of roles | [optional] 

## Example

```python
from kinde_sdk.models.get_user_roles_response_data import GetUserRolesResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserRolesResponseData from a JSON string
get_user_roles_response_data_instance = GetUserRolesResponseData.from_json(json)
# print the JSON string representation of the object
print(GetUserRolesResponseData.to_json())

# convert the object into a dict
get_user_roles_response_data_dict = get_user_roles_response_data_instance.to_dict()
# create an instance of GetUserRolesResponseData from a dict
get_user_roles_response_data_from_dict = GetUserRolesResponseData.from_dict(get_user_roles_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


