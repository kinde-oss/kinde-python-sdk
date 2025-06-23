# UpdateOrganizationSessionsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_use_org_sso_session_policy** | **bool** | Whether to use the organization&#39;s SSO session policy override. | [optional] 
**sso_session_persistence_mode** | **str** | Determines if the session should be persistent or not. | [optional] 
**is_use_org_authenticated_session_lifetime** | **bool** | Whether to apply the organization&#39;s authenticated session lifetime override. | [optional] 
**authenticated_session_lifetime** | **int** | Authenticated session lifetime in seconds. | [optional] 

## Example

```python
from kinde_sdk.models.update_organization_sessions_request import UpdateOrganizationSessionsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateOrganizationSessionsRequest from a JSON string
update_organization_sessions_request_instance = UpdateOrganizationSessionsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateOrganizationSessionsRequest.to_json())

# convert the object into a dict
update_organization_sessions_request_dict = update_organization_sessions_request_instance.to_dict()
# create an instance of UpdateOrganizationSessionsRequest from a dict
update_organization_sessions_request_from_dict = UpdateOrganizationSessionsRequest.from_dict(update_organization_sessions_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


