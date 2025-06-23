# CreateConnectionRequestOptionsOneOf1

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
**is_auto_join_organization_enabled** | **bool** | Users automatically join organization when using this connection. | [optional] 

## Example

```python
from kinde_sdk.models.create_connection_request_options_one_of1 import CreateConnectionRequestOptionsOneOf1

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConnectionRequestOptionsOneOf1 from a JSON string
create_connection_request_options_one_of1_instance = CreateConnectionRequestOptionsOneOf1.from_json(json)
# print the JSON string representation of the object
print(CreateConnectionRequestOptionsOneOf1.to_json())

# convert the object into a dict
create_connection_request_options_one_of1_dict = create_connection_request_options_one_of1_instance.to_dict()
# create an instance of CreateConnectionRequestOptionsOneOf1 from a dict
create_connection_request_options_one_of1_from_dict = CreateConnectionRequestOptionsOneOf1.from_dict(create_connection_request_options_one_of1_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


