# GetApiResponseApiScopesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the scope. | [optional] 
**key** | **str** | The reference key for the scope. | [optional] 

## Example

```python
from kinde_sdk.models.get_api_response_api_scopes_inner import GetApiResponseApiScopesInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetApiResponseApiScopesInner from a JSON string
get_api_response_api_scopes_inner_instance = GetApiResponseApiScopesInner.from_json(json)
# print the JSON string representation of the object
print(GetApiResponseApiScopesInner.to_json())

# convert the object into a dict
get_api_response_api_scopes_inner_dict = get_api_response_api_scopes_inner_instance.to_dict()
# create an instance of GetApiResponseApiScopesInner from a dict
get_api_response_api_scopes_inner_from_dict = GetApiResponseApiScopesInner.from_dict(get_api_response_api_scopes_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


