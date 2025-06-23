# CreateIdentityResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | [optional] 
**code** | **str** |  | [optional] 
**identity** | [**CreateIdentityResponseIdentity**](CreateIdentityResponseIdentity.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_identity_response import CreateIdentityResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIdentityResponse from a JSON string
create_identity_response_instance = CreateIdentityResponse.from_json(json)
# print the JSON string representation of the object
print(CreateIdentityResponse.to_json())

# convert the object into a dict
create_identity_response_dict = create_identity_response_instance.to_dict()
# create an instance of CreateIdentityResponse from a dict
create_identity_response_from_dict = CreateIdentityResponse.from_dict(create_identity_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


