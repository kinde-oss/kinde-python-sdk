# ReplaceConnectionRequestOptionsOneOf1

SAML connection options (e.g., Cloudflare SAML).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**home_realm_domains** | **List[str]** | List of domains to restrict authentication. | [optional] 
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
from kinde_sdk.models.replace_connection_request_options_one_of1 import ReplaceConnectionRequestOptionsOneOf1

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceConnectionRequestOptionsOneOf1 from a JSON string
replace_connection_request_options_one_of1_instance = ReplaceConnectionRequestOptionsOneOf1.from_json(json)
# print the JSON string representation of the object
print(ReplaceConnectionRequestOptionsOneOf1.to_json())

# convert the object into a dict
replace_connection_request_options_one_of1_dict = replace_connection_request_options_one_of1_instance.to_dict()
# create an instance of ReplaceConnectionRequestOptionsOneOf1 from a dict
replace_connection_request_options_one_of1_from_dict = ReplaceConnectionRequestOptionsOneOf1.from_dict(replace_connection_request_options_one_of1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


