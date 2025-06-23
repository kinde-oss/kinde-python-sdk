# GetRedirectCallbackUrlsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**redirect_urls** | [**List[RedirectCallbackUrls]**](RedirectCallbackUrls.md) | An application&#39;s redirect callback URLs. | [optional] 

## Example

```python
from kinde_sdk.models.get_redirect_callback_urls_response import GetRedirectCallbackUrlsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetRedirectCallbackUrlsResponse from a JSON string
get_redirect_callback_urls_response_instance = GetRedirectCallbackUrlsResponse.from_json(json)
# print the JSON string representation of the object
print(GetRedirectCallbackUrlsResponse.to_json())

# convert the object into a dict
get_redirect_callback_urls_response_dict = get_redirect_callback_urls_response_instance.to_dict()
# create an instance of GetRedirectCallbackUrlsResponse from a dict
get_redirect_callback_urls_response_from_dict = GetRedirectCallbackUrlsResponse.from_dict(get_redirect_callback_urls_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


