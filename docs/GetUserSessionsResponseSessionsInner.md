# GetUserSessionsResponseSessionsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **str** | The unique identifier of the user associated with the session. | [optional] 
**org_code** | **str** | The organization code associated with the session, if applicable. | [optional] 
**client_id** | **str** | The client ID used to initiate the session. | [optional] 
**expires_on** | **datetime** | The timestamp indicating when the session will expire. | [optional] 
**session_id** | **str** | The unique identifier of the session. | [optional] 
**started_on** | **datetime** | The timestamp when the session was initiated. | [optional] 
**updated_on** | **datetime** | The timestamp of the last update to the session. | [optional] 
**connection_id** | **str** | The identifier of the connection through which the session was established. | [optional] 
**last_ip_address** | **str** | The last known IP address of the user during this session. | [optional] 
**last_user_agent** | **str** | The last known user agent (browser or app) used during this session. | [optional] 
**initial_ip_address** | **str** | The IP address from which the session was initially started. | [optional] 
**initial_user_agent** | **str** | The user agent (browser or app) used when the session was first created. | [optional] 

## Example

```python
from kinde_sdk.models.get_user_sessions_response_sessions_inner import GetUserSessionsResponseSessionsInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserSessionsResponseSessionsInner from a JSON string
get_user_sessions_response_sessions_inner_instance = GetUserSessionsResponseSessionsInner.from_json(json)
# print the JSON string representation of the object
print(GetUserSessionsResponseSessionsInner.to_json())

# convert the object into a dict
get_user_sessions_response_sessions_inner_dict = get_user_sessions_response_sessions_inner_instance.to_dict()
# create an instance of GetUserSessionsResponseSessionsInner from a dict
get_user_sessions_response_sessions_inner_from_dict = GetUserSessionsResponseSessionsInner.from_dict(get_user_sessions_response_sessions_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


