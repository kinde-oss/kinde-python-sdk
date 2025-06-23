# TokenIntrospect


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active** | **bool** | Indicates the status of the token. | [optional] 
**aud** | **List[str]** | Array of intended token recipients. | [optional] 
**client_id** | **str** | Identifier for the requesting client. | [optional] 
**exp** | **int** | Token expiration timestamp. | [optional] 
**iat** | **int** | Token issuance timestamp. | [optional] 

## Example

```python
from kinde_sdk.models.token_introspect import TokenIntrospect

# TODO update the JSON string below
json = "{}"
# create an instance of TokenIntrospect from a JSON string
token_introspect_instance = TokenIntrospect.from_json(json)
# print the JSON string representation of the object
print(TokenIntrospect.to_json())

# convert the object into a dict
token_introspect_dict = token_introspect_instance.to_dict()
# create an instance of TokenIntrospect from a dict
token_introspect_from_dict = TokenIntrospect.from_dict(token_introspect_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


