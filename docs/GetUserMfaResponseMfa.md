# GetUserMfaResponseMfa


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The MFA&#39;s identifier. | [optional] 
**type** | **str** | The type of MFA (e.g. email, SMS, authenticator app). | [optional] 
**created_on** | **datetime** | The timestamp when the MFA was created. | [optional] 
**name** | **str** | The identifier used for MFA (e.g. email address, phone number). | [optional] 
**is_verified** | **bool** | Whether the MFA is verified or not. | [optional] 
**usage_count** | **int** | The number of times MFA has been used. | [optional] 
**last_used_on** | **datetime** | The timestamp when the MFA was last used. | [optional] 

## Example

```python
from kinde_sdk.models.get_user_mfa_response_mfa import GetUserMfaResponseMfa

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserMfaResponseMfa from a JSON string
get_user_mfa_response_mfa_instance = GetUserMfaResponseMfa.from_json(json)
# print the JSON string representation of the object
print(GetUserMfaResponseMfa.to_json())

# convert the object into a dict
get_user_mfa_response_mfa_dict = get_user_mfa_response_mfa_instance.to_dict()
# create an instance of GetUserMfaResponseMfa from a dict
get_user_mfa_response_mfa_from_dict = GetUserMfaResponseMfa.from_dict(get_user_mfa_response_mfa_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


