# ReplaceOrganizationMFARequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**enabled_factors** | **List[str]** | The MFA methods to enable. | 

## Example

```python
from kinde_sdk.models.replace_organization_mfa_request import ReplaceOrganizationMFARequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceOrganizationMFARequest from a JSON string
replace_organization_mfa_request_instance = ReplaceOrganizationMFARequest.from_json(json)
# print the JSON string representation of the object
print(ReplaceOrganizationMFARequest.to_json())

# convert the object into a dict
replace_organization_mfa_request_dict = replace_organization_mfa_request_instance.to_dict()
# create an instance of ReplaceOrganizationMFARequest from a dict
replace_organization_mfa_request_from_dict = ReplaceOrganizationMFARequest.from_dict(replace_organization_mfa_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


