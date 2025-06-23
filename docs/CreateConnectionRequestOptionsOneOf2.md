# CreateConnectionRequestOptionsOneOf2

SAML connection options (e.g., Cloudflare SAML).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**home_realm_domains** | **List[str]** | List of domains to restrict authentication. | [optional] 
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
**is_auto_join_organization_enabled** | **bool** | Users automatically join organization when using this connection. | [optional] 

## Example

```python
from kinde_sdk.models.create_connection_request_options_one_of2 import CreateConnectionRequestOptionsOneOf2

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConnectionRequestOptionsOneOf2 from a JSON string
create_connection_request_options_one_of2_instance = CreateConnectionRequestOptionsOneOf2.from_json(json)
# print the JSON string representation of the object
print(CreateConnectionRequestOptionsOneOf2.to_json())

# convert the object into a dict
create_connection_request_options_one_of2_dict = create_connection_request_options_one_of2_instance.to_dict()
# create an instance of CreateConnectionRequestOptionsOneOf2 from a dict
create_connection_request_options_one_of2_from_dict = CreateConnectionRequestOptionsOneOf2.from_dict(create_connection_request_options_one_of2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


