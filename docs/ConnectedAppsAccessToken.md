# ConnectedAppsAccessToken


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_token** | **str** | The access token to access a third-party provider. | [optional] 
**access_token_expiry** | **str** | The date and time that the access token expires. | [optional] 

## Example

```python
from kinde_sdk.models.connected_apps_access_token import ConnectedAppsAccessToken

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectedAppsAccessToken from a JSON string
connected_apps_access_token_instance = ConnectedAppsAccessToken.from_json(json)
# print the JSON string representation of the object
print(ConnectedAppsAccessToken.to_json())

# convert the object into a dict
connected_apps_access_token_dict = connected_apps_access_token_instance.to_dict()
# create an instance of ConnectedAppsAccessToken from a dict
connected_apps_access_token_from_dict = ConnectedAppsAccessToken.from_dict(connected_apps_access_token_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


