# GetApiResponseApiApplicationsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Client ID of the application. | [optional] 
**name** | **str** | The application&#39;s name. | [optional] 
**type** | **str** | The application&#39;s type. | [optional] 
**is_active** | **bool** | Whether or not the application is authorized to access the API | [optional] 

## Example

```python
from kinde_sdk.models.get_api_response_api_applications_inner import GetApiResponseApiApplicationsInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetApiResponseApiApplicationsInner from a JSON string
get_api_response_api_applications_inner_instance = GetApiResponseApiApplicationsInner.from_json(json)
# print the JSON string representation of the object
print(GetApiResponseApiApplicationsInner.to_json())

# convert the object into a dict
get_api_response_api_applications_inner_dict = get_api_response_api_applications_inner_instance.to_dict()
# create an instance of GetApiResponseApiApplicationsInner from a dict
get_api_response_api_applications_inner_from_dict = GetApiResponseApiApplicationsInner.from_dict(get_api_response_api_applications_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


