# GetUserMfaResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | [optional] 
**code** | **str** |  | [optional] 
**mfa** | [**GetUserMfaResponseMfa**](GetUserMfaResponseMfa.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_user_mfa_response import GetUserMfaResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserMfaResponse from a JSON string
get_user_mfa_response_instance = GetUserMfaResponse.from_json(json)
# print the JSON string representation of the object
print(GetUserMfaResponse.to_json())

# convert the object into a dict
get_user_mfa_response_dict = get_user_mfa_response_instance.to_dict()
# create an instance of GetUserMfaResponse from a dict
get_user_mfa_response_from_dict = GetUserMfaResponse.from_dict(get_user_mfa_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


