# CreateUserRequestIdentitiesInnerDetails

Additional details required to create the user.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | The email address of the user. | [optional] 
**phone** | **str** | The phone number of the user. | [optional] 
**phone_country_id** | **str** | The country code for the phone number. | [optional] 
**username** | **str** | The username of the user. | [optional] 

## Example

```python
from kinde_sdk.models.create_user_request_identities_inner_details import CreateUserRequestIdentitiesInnerDetails

# TODO update the JSON string below
json = "{}"
# create an instance of CreateUserRequestIdentitiesInnerDetails from a JSON string
create_user_request_identities_inner_details_instance = CreateUserRequestIdentitiesInnerDetails.from_json(json)
# print the JSON string representation of the object
print(CreateUserRequestIdentitiesInnerDetails.to_json())

# convert the object into a dict
create_user_request_identities_inner_details_dict = create_user_request_identities_inner_details_instance.to_dict()
# create an instance of CreateUserRequestIdentitiesInnerDetails from a dict
create_user_request_identities_inner_details_from_dict = CreateUserRequestIdentitiesInnerDetails.from_dict(create_user_request_identities_inner_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


