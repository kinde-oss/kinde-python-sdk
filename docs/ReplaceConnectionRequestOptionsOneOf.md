# ReplaceConnectionRequestOptionsOneOf

Azure AD connection options.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_id** | **str** | Client ID. | [optional] 
**client_secret** | **str** | Client secret. | [optional] 
**home_realm_domains** | **List[str]** | List of domains to limit authentication. | [optional] 
**entra_id_domain** | **str** | Domain for Entra ID. | [optional] 
**is_use_common_endpoint** | **bool** | Use https://login.windows.net/common instead of a default endpoint. | [optional] 
**is_sync_user_profile_on_login** | **bool** | Sync user profile data with IDP. | [optional] 
**is_retrieve_provider_user_groups** | **bool** | Include user group info from MS Entra ID. | [optional] 
**is_extended_attributes_required** | **bool** | Include additional user profile information. | [optional] 

## Example

```python
from kinde_sdk.models.replace_connection_request_options_one_of import ReplaceConnectionRequestOptionsOneOf

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceConnectionRequestOptionsOneOf from a JSON string
replace_connection_request_options_one_of_instance = ReplaceConnectionRequestOptionsOneOf.from_json(json)
# print the JSON string representation of the object
print(ReplaceConnectionRequestOptionsOneOf.to_json())

# convert the object into a dict
replace_connection_request_options_one_of_dict = replace_connection_request_options_one_of_instance.to_dict()
# create an instance of ReplaceConnectionRequestOptionsOneOf from a dict
replace_connection_request_options_one_of_from_dict = ReplaceConnectionRequestOptionsOneOf.from_dict(replace_connection_request_options_one_of_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


