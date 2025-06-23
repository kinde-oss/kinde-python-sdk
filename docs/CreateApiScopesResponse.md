# CreateApiScopesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | A Kinde generated message. | [optional] 
**code** | **str** | A Kinde generated status code. | [optional] 
**scope** | [**CreateApiScopesResponseScope**](CreateApiScopesResponseScope.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_api_scopes_response import CreateApiScopesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateApiScopesResponse from a JSON string
create_api_scopes_response_instance = CreateApiScopesResponse.from_json(json)
# print the JSON string representation of the object
print(CreateApiScopesResponse.to_json())

# convert the object into a dict
create_api_scopes_response_dict = create_api_scopes_response_instance.to_dict()
# create an instance of CreateApiScopesResponse from a dict
create_api_scopes_response_from_dict = CreateApiScopesResponse.from_dict(create_api_scopes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


