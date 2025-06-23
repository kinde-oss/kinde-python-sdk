# CreateRolesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**role** | [**CreateRolesResponseRole**](CreateRolesResponseRole.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_roles_response import CreateRolesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateRolesResponse from a JSON string
create_roles_response_instance = CreateRolesResponse.from_json(json)
# print the JSON string representation of the object
print(CreateRolesResponse.to_json())

# convert the object into a dict
create_roles_response_dict = create_roles_response_instance.to_dict()
# create an instance of CreateRolesResponse from a dict
create_roles_response_from_dict = CreateRolesResponse.from_dict(create_roles_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


