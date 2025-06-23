# GetApiResponseApi


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique ID of the API. | [optional] 
**name** | **str** | The API’s name. | [optional] 
**audience** | **str** | A unique identifier for the API - commonly the URL. This value will be used as the &#x60;audience&#x60; parameter in authorization claims. | [optional] 
**is_management_api** | **bool** | Whether or not it is the Kinde management API. | [optional] 
**scopes** | [**List[GetApiResponseApiScopesInner]**](GetApiResponseApiScopesInner.md) |  | [optional] 
**applications** | [**List[GetApiResponseApiApplicationsInner]**](GetApiResponseApiApplicationsInner.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_api_response_api import GetApiResponseApi

# TODO update the JSON string below
json = "{}"
# create an instance of GetApiResponseApi from a JSON string
get_api_response_api_instance = GetApiResponseApi.from_json(json)
# print the JSON string representation of the object
print(GetApiResponseApi.to_json())

# convert the object into a dict
get_api_response_api_dict = get_api_response_api_instance.to_dict()
# create an instance of GetApiResponseApi from a dict
get_api_response_api_from_dict = GetApiResponseApi.from_dict(get_api_response_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


