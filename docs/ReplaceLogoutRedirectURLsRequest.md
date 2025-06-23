# ReplaceLogoutRedirectURLsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**urls** | **List[str]** | Array of logout urls. | [optional] 

## Example

```python
from kinde_sdk.models.replace_logout_redirect_urls_request import ReplaceLogoutRedirectURLsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceLogoutRedirectURLsRequest from a JSON string
replace_logout_redirect_urls_request_instance = ReplaceLogoutRedirectURLsRequest.from_json(json)
# print the JSON string representation of the object
print(ReplaceLogoutRedirectURLsRequest.to_json())

# convert the object into a dict
replace_logout_redirect_urls_request_dict = replace_logout_redirect_urls_request_instance.to_dict()
# create an instance of ReplaceLogoutRedirectURLsRequest from a dict
replace_logout_redirect_urls_request_from_dict = ReplaceLogoutRedirectURLsRequest.from_dict(replace_logout_redirect_urls_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


