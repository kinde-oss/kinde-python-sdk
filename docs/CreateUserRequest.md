# CreateUserRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**profile** | [**CreateUserRequestProfile**](CreateUserRequestProfile.md) |  | [optional] 
**organization_code** | **str** | The unique code associated with the organization you want the user to join. | [optional] 
**provided_id** | **str** | An external id to reference the user. | [optional] 
**identities** | [**List[CreateUserRequestIdentitiesInner]**](CreateUserRequestIdentitiesInner.md) | Array of identities to assign to the created user | [optional] 

## Example

```python
from kinde_sdk.models.create_user_request import CreateUserRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateUserRequest from a JSON string
create_user_request_instance = CreateUserRequest.from_json(json)
# print the JSON string representation of the object
print(CreateUserRequest.to_json())

# convert the object into a dict
create_user_request_dict = create_user_request_instance.to_dict()
# create an instance of CreateUserRequest from a dict
create_user_request_from_dict = CreateUserRequest.from_dict(create_user_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


