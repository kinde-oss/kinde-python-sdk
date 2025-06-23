# GetApisResponseApisInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The unique ID for the API. | [optional] 
**name** | **str** | The API’s name. | [optional] 
**audience** | **str** | A unique identifier for the API - commonly the URL. This value will be used as the &#x60;audience&#x60; parameter in authorization claims. | [optional] 
**is_management_api** | **bool** | Whether or not it is the Kinde management API. | [optional] 
**scopes** | [**List[GetApisResponseApisInnerScopesInner]**](GetApisResponseApisInnerScopesInner.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_apis_response_apis_inner import GetApisResponseApisInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetApisResponseApisInner from a JSON string
get_apis_response_apis_inner_instance = GetApisResponseApisInner.from_json(json)
# print the JSON string representation of the object
print(GetApisResponseApisInner.to_json())

# convert the object into a dict
get_apis_response_apis_inner_dict = get_apis_response_apis_inner_instance.to_dict()
# create an instance of GetApisResponseApisInner from a dict
get_apis_response_apis_inner_from_dict = GetApisResponseApisInner.from_dict(get_apis_response_apis_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


