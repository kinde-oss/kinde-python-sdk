# ReplaceMFARequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**policy** | **str** | Specifies whether MFA is required, optional, or not enforced. | 
**enabled_factors** | **List[str]** | The MFA methods to enable. | 

## Example

```python
from kinde_sdk.models.replace_mfa_request import ReplaceMFARequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceMFARequest from a JSON string
replace_mfa_request_instance = ReplaceMFARequest.from_json(json)
# print the JSON string representation of the object
print(ReplaceMFARequest.to_json())

# convert the object into a dict
replace_mfa_request_dict = replace_mfa_request_instance.to_dict()
# create an instance of ReplaceMFARequest from a dict
replace_mfa_request_from_dict = ReplaceMFARequest.from_dict(replace_mfa_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


