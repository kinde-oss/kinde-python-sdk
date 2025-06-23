# GetApiResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**api** | [**GetApiResponseApi**](GetApiResponseApi.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_api_response import GetApiResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetApiResponse from a JSON string
get_api_response_instance = GetApiResponse.from_json(json)
# print the JSON string representation of the object
print(GetApiResponse.to_json())

# convert the object into a dict
get_api_response_dict = get_api_response_instance.to_dict()
# create an instance of GetApiResponse from a dict
get_api_response_from_dict = GetApiResponse.from_dict(get_api_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


