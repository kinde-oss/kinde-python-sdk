# GetOrganizationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | The unique identifier for the organization. | [optional] 
**name** | **str** | The organization&#39;s name. | [optional] 
**handle** | **str** | A unique handle for the organization - can be used for dynamic callback urls. | [optional] 
**is_default** | **bool** | Whether the organization is the default organization. | [optional] 
**external_id** | **str** | The organization&#39;s external identifier - commonly used when migrating from or mapping to other systems. | [optional] 
**is_auto_membership_enabled** | **bool** | If users become members of this organization when the org code is supplied during authentication. | [optional] 
**logo** | **str** | The organization&#39;s logo URL. | [optional] 
**logo_dark** | **str** | The organization&#39;s logo URL to be used for dark themes. | [optional] 
**favicon_svg** | **str** | The organization&#39;s SVG favicon URL. Optimal format for most browsers | [optional] 
**favicon_fallback** | **str** | The favicon URL to be used as a fallback in browsers that don’t support SVG, add a PNG | [optional] 
**link_color** | [**GetEnvironmentResponseEnvironmentLinkColor**](GetEnvironmentResponseEnvironmentLinkColor.md) |  | [optional] 
**background_color** | [**GetEnvironmentResponseEnvironmentBackgroundColor**](GetEnvironmentResponseEnvironmentBackgroundColor.md) |  | [optional] 
**button_color** | [**GetEnvironmentResponseEnvironmentLinkColor**](GetEnvironmentResponseEnvironmentLinkColor.md) |  | [optional] 
**button_text_color** | [**GetEnvironmentResponseEnvironmentBackgroundColor**](GetEnvironmentResponseEnvironmentBackgroundColor.md) |  | [optional] 
**link_color_dark** | [**GetEnvironmentResponseEnvironmentLinkColor**](GetEnvironmentResponseEnvironmentLinkColor.md) |  | [optional] 
**background_color_dark** | [**GetEnvironmentResponseEnvironmentLinkColor**](GetEnvironmentResponseEnvironmentLinkColor.md) |  | [optional] 
**button_text_color_dark** | [**GetEnvironmentResponseEnvironmentLinkColor**](GetEnvironmentResponseEnvironmentLinkColor.md) |  | [optional] 
**button_color_dark** | [**GetEnvironmentResponseEnvironmentLinkColor**](GetEnvironmentResponseEnvironmentLinkColor.md) |  | [optional] 
**button_border_radius** | **int** | The border radius for buttons. Value is px, Kinde transforms to rem for rendering | [optional] 
**card_border_radius** | **int** | The border radius for cards. Value is px, Kinde transforms to rem for rendering | [optional] 
**input_border_radius** | **int** | The border radius for inputs. Value is px, Kinde transforms to rem for rendering | [optional] 
**theme_code** | **str** | Whether the environment is forced into light mode, dark mode or user preference | [optional] 
**color_scheme** | **str** | The color scheme for the environment used for meta tags based on the theme code | [optional] 
**created_on** | **str** | Date of organization creation in ISO 8601 format. | [optional] 
**is_allow_registrations** | **bool** | Deprecated - Use &#39;is_auto_membership_enabled&#39; instead | [optional] 
**sender_name** | **str** | The name of the organization that will be used in emails | [optional] 
**sender_email** | **str** | The email address that will be used in emails. Requires custom SMTP to be set up. | [optional] 
**billing** | [**GetOrganizationResponseBilling**](GetOrganizationResponseBilling.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_organization_response import GetOrganizationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganizationResponse from a JSON string
get_organization_response_instance = GetOrganizationResponse.from_json(json)
# print the JSON string representation of the object
print(GetOrganizationResponse.to_json())

# convert the object into a dict
get_organization_response_dict = get_organization_response_instance.to_dict()
# create an instance of GetOrganizationResponse from a dict
get_organization_response_from_dict = GetOrganizationResponse.from_dict(get_organization_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


