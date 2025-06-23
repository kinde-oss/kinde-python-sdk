# UpdateIdentityRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_primary** | **bool** | Whether the identity is the primary for it&#39;s type | [optional] 

## Example

```python
from kinde_sdk.models.update_identity_request import UpdateIdentityRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateIdentityRequest from a JSON string
update_identity_request_instance = UpdateIdentityRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateIdentityRequest.to_json())

# convert the object into a dict
update_identity_request_dict = update_identity_request_instance.to_dict()
# create an instance of UpdateIdentityRequest from a dict
update_identity_request_from_dict = UpdateIdentityRequest.from_dict(update_identity_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


