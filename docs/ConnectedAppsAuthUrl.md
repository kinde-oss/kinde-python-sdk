# ConnectedAppsAuthUrl


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**url** | **str** | A URL that is used to authenticate an end-user against a connected app. | [optional] 
**session_id** | **str** | A unique identifier for the login session. | [optional] 

## Example

```python
from kinde_sdk.models.connected_apps_auth_url import ConnectedAppsAuthUrl

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectedAppsAuthUrl from a JSON string
connected_apps_auth_url_instance = ConnectedAppsAuthUrl.from_json(json)
# print the JSON string representation of the object
print(ConnectedAppsAuthUrl.to_json())

# convert the object into a dict
connected_apps_auth_url_dict = connected_apps_auth_url_instance.to_dict()
# create an instance of ConnectedAppsAuthUrl from a dict
connected_apps_auth_url_from_dict = ConnectedAppsAuthUrl.from_dict(connected_apps_auth_url_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


