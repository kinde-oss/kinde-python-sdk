# GetApiScopeResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**scope** | [**GetApiScopesResponseScopesInner**](GetApiScopesResponseScopesInner.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_api_scope_response import GetApiScopeResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetApiScopeResponse from a JSON string
get_api_scope_response_instance = GetApiScopeResponse.from_json(json)
# print the JSON string representation of the object
print(GetApiScopeResponse.to_json())

# convert the object into a dict
get_api_scope_response_dict = get_api_scope_response_instance.to_dict()
# create an instance of GetApiScopeResponse from a dict
get_api_scope_response_from_dict = GetApiScopeResponse.from_dict(get_api_scope_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


