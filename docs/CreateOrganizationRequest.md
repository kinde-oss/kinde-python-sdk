# CreateOrganizationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The organization&#39;s name. | 
**feature_flags** | **Dict[str, str]** | The organization&#39;s feature flag settings. | [optional] 
**external_id** | **str** | The organization&#39;s external identifier - commonly used when migrating from or mapping to other systems. | [optional] 
**background_color** | **str** | The organization&#39;s brand settings - background color. | [optional] 
**button_color** | **str** | The organization&#39;s brand settings - button color. | [optional] 
**button_text_color** | **str** | The organization&#39;s brand settings - button text color. | [optional] 
**link_color** | **str** | The organization&#39;s brand settings - link color. | [optional] 
**background_color_dark** | **str** | The organization&#39;s brand settings - dark mode background color. | [optional] 
**button_color_dark** | **str** | The organization&#39;s brand settings - dark mode button color. | [optional] 
**button_text_color_dark** | **str** | The organization&#39;s brand settings - dark mode button text color. | [optional] 
**link_color_dark** | **str** | The organization&#39;s brand settings - dark mode link color. | [optional] 
**theme_code** | **str** | The organization&#39;s brand settings - theme/mode &#39;light&#39; | &#39;dark&#39; | &#39;user_preference&#39;. | [optional] 
**handle** | **str** | A unique handle for the organization - can be used for dynamic callback urls. | [optional] 
**is_allow_registrations** | **bool** | If users become members of this organization when the org code is supplied during authentication. | [optional] 
**sender_name** | **str** | The name of the organization that will be used in emails | [optional] 
**sender_email** | **str** | The email address that will be used in emails. Requires custom SMTP to be set up. | [optional] 
**is_create_billing_customer** | **bool** | If a billing customer is also created for this organization | [optional] 
**billing_email** | **str** | The email address used for billing purposes for the organization | [optional] 
**billing_plan_code** | **str** | The billing plan to put the customer on. If not specified, the default plan is used | [optional] 

## Example

```python
from kinde_sdk.models.create_organization_request import CreateOrganizationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrganizationRequest from a JSON string
create_organization_request_instance = CreateOrganizationRequest.from_json(json)
# print the JSON string representation of the object
print(CreateOrganizationRequest.to_json())

# convert the object into a dict
create_organization_request_dict = create_organization_request_instance.to_dict()
# create an instance of CreateOrganizationRequest from a dict
create_organization_request_from_dict = CreateOrganizationRequest.from_dict(create_organization_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


