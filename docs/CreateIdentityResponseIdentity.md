# CreateIdentityResponseIdentity


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The identity&#39;s ID. | [optional] 

## Example

```python
from kinde_sdk.models.create_identity_response_identity import CreateIdentityResponseIdentity

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIdentityResponseIdentity from a JSON string
create_identity_response_identity_instance = CreateIdentityResponseIdentity.from_json(json)
# print the JSON string representation of the object
print(CreateIdentityResponseIdentity.to_json())

# convert the object into a dict
create_identity_response_identity_dict = create_identity_response_identity_instance.to_dict()
# create an instance of CreateIdentityResponseIdentity from a dict
create_identity_response_identity_from_dict = CreateIdentityResponseIdentity.from_dict(create_identity_response_identity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


