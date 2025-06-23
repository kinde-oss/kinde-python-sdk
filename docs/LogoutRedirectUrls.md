# LogoutRedirectUrls


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**logout_urls** | **List[str]** | An application&#39;s logout URLs. | [optional] 
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 

## Example

```python
from kinde_sdk.models.logout_redirect_urls import LogoutRedirectUrls

# TODO update the JSON string below
json = "{}"
# create an instance of LogoutRedirectUrls from a JSON string
logout_redirect_urls_instance = LogoutRedirectUrls.from_json(json)
# print the JSON string representation of the object
print(LogoutRedirectUrls.to_json())

# convert the object into a dict
logout_redirect_urls_dict = logout_redirect_urls_instance.to_dict()
# create an instance of LogoutRedirectUrls from a dict
logout_redirect_urls_from_dict = LogoutRedirectUrls.from_dict(logout_redirect_urls_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


