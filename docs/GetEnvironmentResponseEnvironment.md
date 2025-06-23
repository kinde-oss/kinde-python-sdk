# GetEnvironmentResponseEnvironment


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | The unique identifier for the environment. | [optional] 
**name** | **str** | The environment&#39;s name. | [optional] 
**hotjar_site_id** | **str** | Your HotJar site ID. | [optional] 
**google_analytics_tag** | **str** | Your Google Analytics tag. | [optional] 
**is_default** | **bool** | Whether the environment is the default. Typically this is your production environment. | [optional] 
**is_live** | **bool** | Whether the environment is live. | [optional] 
**kinde_domain** | **str** | Your domain on Kinde | [optional] 
**custom_domain** | **str** | Your custom domain for the environment | [optional] 
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
**created_on** | **str** | Date of environment creation in ISO 8601 format. | [optional] 

## Example

```python
from kinde_sdk.models.get_environment_response_environment import GetEnvironmentResponseEnvironment

# TODO update the JSON string below
json = "{}"
# create an instance of GetEnvironmentResponseEnvironment from a JSON string
get_environment_response_environment_instance = GetEnvironmentResponseEnvironment.from_json(json)
# print the JSON string representation of the object
print(GetEnvironmentResponseEnvironment.to_json())

# convert the object into a dict
get_environment_response_environment_dict = get_environment_response_environment_instance.to_dict()
# create an instance of GetEnvironmentResponseEnvironment from a dict
get_environment_response_environment_from_dict = GetEnvironmentResponseEnvironment.from_dict(get_environment_response_environment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


