# CreateConnectionRequestOptions


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
**is_auto_join_organization_enabled** | **bool** | Users automatically join organization when using this connection. | [optional] 
**saml_entity_id** | **str** | SAML Entity ID. | [optional] 
**saml_acs_url** | **str** | Assertion Consumer Service URL. | [optional] 
**saml_idp_metadata_url** | **str** | URL for the IdP metadata. | [optional] 
**saml_sign_in_url** | **str** | Override the default SSO endpoint with a URL your IdP recognizes. | [optional] 
**saml_email_key_attr** | **str** | Attribute key for the user’s email. | [optional] 
**saml_first_name_key_attr** | **str** | Attribute key for the user’s first name. | [optional] 
**saml_last_name_key_attr** | **str** | Attribute key for the user’s last name. | [optional] 
**is_create_missing_user** | **bool** | Create user if they don’t exist. | [optional] 
**saml_signing_certificate** | **str** | Certificate for signing SAML requests. | [optional] 
**saml_signing_private_key** | **str** | Private key associated with the signing certificate. | [optional] 

## Example

```python
from kinde_sdk.models.create_connection_request_options import CreateConnectionRequestOptions

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConnectionRequestOptions from a JSON string
create_connection_request_options_instance = CreateConnectionRequestOptions.from_json(json)
# print the JSON string representation of the object
print(CreateConnectionRequestOptions.to_json())

# convert the object into a dict
create_connection_request_options_dict = create_connection_request_options_instance.to_dict()
# create an instance of CreateConnectionRequestOptions from a dict
create_connection_request_options_from_dict = CreateConnectionRequestOptions.from_dict(create_connection_request_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


