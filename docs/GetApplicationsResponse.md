# GetApplicationsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**applications** | [**List[Applications]**](Applications.md) |  | [optional] 
**next_token** | **str** | Pagination token. | [optional] 

## Example

```python
from kinde_sdk.models.get_applications_response import GetApplicationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetApplicationsResponse from a JSON string
get_applications_response_instance = GetApplicationsResponse.from_json(json)
# print the JSON string representation of the object
print(GetApplicationsResponse.to_json())

# convert the object into a dict
get_applications_response_dict = get_applications_response_instance.to_dict()
# create an instance of GetApplicationsResponse from a dict
get_applications_response_from_dict = GetApplicationsResponse.from_dict(get_applications_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


