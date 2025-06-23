# AddAPIScopeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | The key reference for the scope (1-64 characters, no white space). | 
**description** | **str** | Description of the api scope purpose. | [optional] 

## Example

```python
from kinde_sdk.models.add_api_scope_request import AddAPIScopeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddAPIScopeRequest from a JSON string
add_api_scope_request_instance = AddAPIScopeRequest.from_json(json)
# print the JSON string representation of the object
print(AddAPIScopeRequest.to_json())

# convert the object into a dict
add_api_scope_request_dict = add_api_scope_request_instance.to_dict()
# create an instance of AddAPIScopeRequest from a dict
add_api_scope_request_from_dict = AddAPIScopeRequest.from_dict(add_api_scope_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


