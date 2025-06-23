# UpdateAPIApplicationsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**applications** | [**List[UpdateAPIApplicationsRequestApplicationsInner]**](UpdateAPIApplicationsRequestApplicationsInner.md) |  | 

## Example

```python
from kinde_sdk.models.update_api_applications_request import UpdateAPIApplicationsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAPIApplicationsRequest from a JSON string
update_api_applications_request_instance = UpdateAPIApplicationsRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateAPIApplicationsRequest.to_json())

# convert the object into a dict
update_api_applications_request_dict = update_api_applications_request_instance.to_dict()
# create an instance of UpdateAPIApplicationsRequest from a dict
update_api_applications_request_from_dict = UpdateAPIApplicationsRequest.from_dict(update_api_applications_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


