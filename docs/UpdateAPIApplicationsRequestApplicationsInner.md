# UpdateAPIApplicationsRequestApplicationsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The application&#39;s Client ID. | 
**operation** | **str** | Optional operation, set to &#39;delete&#39; to revoke authorization for the application. If not set, the application will be authorized. | [optional] 

## Example

```python
from kinde_sdk.models.update_api_applications_request_applications_inner import UpdateAPIApplicationsRequestApplicationsInner

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAPIApplicationsRequestApplicationsInner from a JSON string
update_api_applications_request_applications_inner_instance = UpdateAPIApplicationsRequestApplicationsInner.from_json(json)
# print the JSON string representation of the object
print(UpdateAPIApplicationsRequestApplicationsInner.to_json())

# convert the object into a dict
update_api_applications_request_applications_inner_dict = update_api_applications_request_applications_inner_instance.to_dict()
# create an instance of UpdateAPIApplicationsRequestApplicationsInner from a dict
update_api_applications_request_applications_inner_from_dict = UpdateAPIApplicationsRequestApplicationsInner.from_dict(update_api_applications_request_applications_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


