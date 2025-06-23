# GetPortalLink


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | Unique URL to redirect the user to. | [optional] 

## Example

```python
from kinde_sdk.models.get_portal_link import GetPortalLink

# TODO update the JSON string below
json = "{}"
# create an instance of GetPortalLink from a JSON string
get_portal_link_instance = GetPortalLink.from_json(json)
# print the JSON string representation of the object
print(GetPortalLink.to_json())

# convert the object into a dict
get_portal_link_dict = get_portal_link_instance.to_dict()
# create an instance of GetPortalLink from a dict
get_portal_link_from_dict = GetPortalLink.from_dict(get_portal_link_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


