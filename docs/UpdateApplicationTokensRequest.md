# UpdateApplicationTokensRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_token_lifetime** | **int** | The lifetime of an access token in seconds. | [optional] 
**refresh_token_lifetime** | **int** | The lifetime of a refresh token in seconds. | [optional] 
**id_token_lifetime** | **int** | The lifetime of an ID token in seconds. | [optional] 
**authenticated_session_lifetime** | **int** | The lifetime of an authenticated session in seconds. | [optional] 
**is_hasura_mapping_enabled** | **bool** | Enable or disable Hasura mapping. | [optional] 

## Example

```python
from kinde_sdk.models.update_application_tokens_request import UpdateApplicationTokensRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateApplicationTokensRequest from a JSON string
update_application_tokens_request_instance = UpdateApplicationTokensRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateApplicationTokensRequest.to_json())

# convert the object into a dict
update_application_tokens_request_dict = update_application_tokens_request_instance.to_dict()
# create an instance of UpdateApplicationTokensRequest from a dict
update_application_tokens_request_from_dict = UpdateApplicationTokensRequest.from_dict(update_application_tokens_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


