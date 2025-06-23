# RoleScopesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**scopes** | [**List[Scopes]**](Scopes.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.role_scopes_response import RoleScopesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RoleScopesResponse from a JSON string
role_scopes_response_instance = RoleScopesResponse.from_json(json)
# print the JSON string representation of the object
print(RoleScopesResponse.to_json())

# convert the object into a dict
role_scopes_response_dict = role_scopes_response_instance.to_dict()
# create an instance of RoleScopesResponse from a dict
role_scopes_response_from_dict = RoleScopesResponse.from_dict(role_scopes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


