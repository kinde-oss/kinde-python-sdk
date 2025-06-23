# ReplaceConnectionRequestOptions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_id** | **str** | Client ID. | [optional] 
**client_secret** | **str** | Client secret. | [optional] 
**is_use_custom_domain** | **bool** | Use custom domain callback URL. | [optional] 
**home_realm_domains** | **List[str]** | List of domains to restrict authentication. | [optional] 
**entra_id_domain** | **str** | Domain for Entra ID. | [optional] 
**is_use_common_endpoint** | **bool** | Use https://login.windows.net/common instead of a default endpoint. | [optional] 
**is_sync_user_profile_on_login** | **bool** | Sync user profile data with IDP. | [optional] 
**is_retrieve_provider_user_groups** | **bool** | Include user group info from MS Entra ID. | [optional] 
**is_extended_attributes_required** | **bool** | Include additional user profile information. | [optional] 
**saml_entity_id** | **str** | SAML Entity ID. | [optional] 
**saml_acs_url** | **str** | Assertion Consumer Service URL. | [optional] 
**saml_idp_metadata_url** | **str** | URL for the IdP metadata. | [optional] 
**saml_email_key_attr** | **str** | Attribute key for the user’s email. | [optional] 
**saml_first_name_key_attr** | **str** | Attribute key for the user’s first name. | [optional] 
**saml_last_name_key_attr** | **str** | Attribute key for the user’s last name. | [optional] 
**is_create_missing_user** | **bool** | Create user if they don’t exist. | [optional] 
**saml_signing_certificate** | **str** | Certificate for signing SAML requests. | [optional] 
**saml_signing_private_key** | **str** | Private key associated with the signing certificate. | [optional] 

## Example

```python
from kinde_sdk.models.replace_connection_request_options import ReplaceConnectionRequestOptions

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceConnectionRequestOptions from a JSON string
replace_connection_request_options_instance = ReplaceConnectionRequestOptions.from_json(json)
# print the JSON string representation of the object
print(ReplaceConnectionRequestOptions.to_json())

# convert the object into a dict
replace_connection_request_options_dict = replace_connection_request_options_instance.to_dict()
# create an instance of ReplaceConnectionRequestOptions from a dict
replace_connection_request_options_from_dict = ReplaceConnectionRequestOptions.from_dict(replace_connection_request_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


