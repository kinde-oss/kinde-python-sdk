# UpdateOrganizationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The organization&#39;s name. | [optional] 
**external_id** | **str** | The organization&#39;s ID. | [optional] 
**background_color** | **str** | The organization&#39;s brand settings - background color. | [optional] 
**button_color** | **str** | The organization&#39;s brand settings - button color. | [optional] 
**button_text_color** | **str** | The organization&#39;s brand settings - button text color. | [optional] 
**link_color** | **str** | The organization&#39;s brand settings - link color. | [optional] 
**background_color_dark** | **str** | The organization&#39;s brand settings - dark mode background color. | [optional] 
**button_color_dark** | **str** | The organization&#39;s brand settings - dark mode button color. | [optional] 
**button_text_color_dark** | **str** | The organization&#39;s brand settings - dark mode button text color. | [optional] 
**link_color_dark** | **str** | The organization&#39;s brand settings - dark mode link color. | [optional] 
**theme_code** | **str** | The organization&#39;s brand settings - theme/mode. | [optional] 
**handle** | **str** | The organization&#39;s handle. | [optional] 
**is_allow_registrations** | **bool** | Deprecated - Use &#39;is_auto_membership_enabled&#39; instead. | [optional] 
**is_auto_join_domain_list** | **bool** | Users can sign up to this organization. | [optional] 
**allowed_domains** | **List[str]** | Domains allowed for self-sign up to this environment. | [optional] 
**is_enable_advanced_orgs** | **bool** | Activate advanced organization features. | [optional] 
**is_enforce_mfa** | **bool** | Enforce MFA for all users in this organization. | [optional] 
**sender_name** | **str** | The name of the organization that will be used in emails | [optional] 
**sender_email** | **str** | The email address that will be used in emails. Requires custom SMTP to be set up. | [optional] 

## Example

```python
from kinde_sdk.models.update_organization_request import UpdateOrganizationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateOrganizationRequest from a JSON string
update_organization_request_instance = UpdateOrganizationRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateOrganizationRequest.to_json())

# convert the object into a dict
update_organization_request_dict = update_organization_request_instance.to_dict()
# create an instance of UpdateOrganizationRequest from a dict
update_organization_request_from_dict = UpdateOrganizationRequest.from_dict(update_organization_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


