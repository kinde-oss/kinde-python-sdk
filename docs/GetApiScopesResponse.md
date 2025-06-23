# GetApiScopesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**scopes** | [**List[GetApiScopesResponseScopesInner]**](GetApiScopesResponseScopesInner.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_api_scopes_response import GetApiScopesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetApiScopesResponse from a JSON string
get_api_scopes_response_instance = GetApiScopesResponse.from_json(json)
# print the JSON string representation of the object
print(GetApiScopesResponse.to_json())

# convert the object into a dict
get_api_scopes_response_dict = get_api_scopes_response_instance.to_dict()
# create an instance of GetApiScopesResponse from a dict
get_api_scopes_response_from_dict = GetApiScopesResponse.from_dict(get_api_scopes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


