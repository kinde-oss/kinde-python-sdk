# GetApisResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**next_token** | **str** | Pagination token. | [optional] 
**apis** | [**List[GetApisResponseApisInner]**](GetApisResponseApisInner.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_apis_response import GetApisResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetApisResponse from a JSON string
get_apis_response_instance = GetApisResponse.from_json(json)
# print the JSON string representation of the object
print(GetApisResponse.to_json())

# convert the object into a dict
get_apis_response_dict = get_apis_response_instance.to_dict()
# create an instance of GetApisResponse from a dict
get_apis_response_from_dict = GetApisResponse.from_dict(get_apis_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


