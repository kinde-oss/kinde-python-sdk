# ReplaceRedirectCallbackURLsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**urls** | **List[str]** | Array of callback urls. | [optional] 

## Example

```python
from kinde_sdk.models.replace_redirect_callback_urls_request import ReplaceRedirectCallbackURLsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceRedirectCallbackURLsRequest from a JSON string
replace_redirect_callback_urls_request_instance = ReplaceRedirectCallbackURLsRequest.from_json(json)
# print the JSON string representation of the object
print(ReplaceRedirectCallbackURLsRequest.to_json())

# convert the object into a dict
replace_redirect_callback_urls_request_dict = replace_redirect_callback_urls_request_instance.to_dict()
# create an instance of ReplaceRedirectCallbackURLsRequest from a dict
replace_redirect_callback_urls_request_from_dict = ReplaceRedirectCallbackURLsRequest.from_dict(replace_redirect_callback_urls_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


