# RedirectCallbackUrls


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**redirect_urls** | **List[str]** | An application&#39;s redirect URLs. | [optional] 

## Example

```python
from kinde_sdk.models.redirect_callback_urls import RedirectCallbackUrls

# TODO update the JSON string below
json = "{}"
# create an instance of RedirectCallbackUrls from a JSON string
redirect_callback_urls_instance = RedirectCallbackUrls.from_json(json)
# print the JSON string representation of the object
print(RedirectCallbackUrls.to_json())

# convert the object into a dict
redirect_callback_urls_dict = redirect_callback_urls_instance.to_dict()
# create an instance of RedirectCallbackUrls from a dict
redirect_callback_urls_from_dict = RedirectCallbackUrls.from_dict(redirect_callback_urls_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


