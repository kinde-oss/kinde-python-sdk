# CreateUserIdentityRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** | The email address, social identity, or username of the user. | [optional] 
**type** | **str** | The identity type | [optional] 
**phone_country_id** | **str** | The country code for the phone number, only required when identity type is &#39;phone&#39;. | [optional] 
**connection_id** | **str** | The social or enterprise connection ID, only required when identity type is &#39;social&#39; or &#39;enterprise&#39;. | [optional] 

## Example

```python
from kinde_sdk.models.create_user_identity_request import CreateUserIdentityRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateUserIdentityRequest from a JSON string
create_user_identity_request_instance = CreateUserIdentityRequest.from_json(json)
# print the JSON string representation of the object
print(CreateUserIdentityRequest.to_json())

# convert the object into a dict
create_user_identity_request_dict = create_user_identity_request_instance.to_dict()
# create an instance of CreateUserIdentityRequest from a dict
create_user_identity_request_from_dict = CreateUserIdentityRequest.from_dict(create_user_identity_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


