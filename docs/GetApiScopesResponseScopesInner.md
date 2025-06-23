# GetApiScopesResponseScopesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique ID of the API scope. | [optional] 
**key** | **str** | The scope&#39;s reference key. | [optional] 
**description** | **str** | Explanation of the scope purpose. | [optional] 

## Example

```python
from kinde_sdk.models.get_api_scopes_response_scopes_inner import GetApiScopesResponseScopesInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetApiScopesResponseScopesInner from a JSON string
get_api_scopes_response_scopes_inner_instance = GetApiScopesResponseScopesInner.from_json(json)
# print the JSON string representation of the object
print(GetApiScopesResponseScopesInner.to_json())

# convert the object into a dict
get_api_scopes_response_scopes_inner_dict = get_api_scopes_response_scopes_inner_instance.to_dict()
# create an instance of GetApiScopesResponseScopesInner from a dict
get_api_scopes_response_scopes_inner_from_dict = GetApiScopesResponseScopesInner.from_dict(get_api_scopes_response_scopes_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


