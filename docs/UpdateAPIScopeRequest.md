# UpdateAPIScopeRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Description of the api scope purpose. | [optional] 

## Example

```python
from kinde_sdk.models.update_api_scope_request import UpdateAPIScopeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateAPIScopeRequest from a JSON string
update_api_scope_request_instance = UpdateAPIScopeRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateAPIScopeRequest.to_json())

# convert the object into a dict
update_api_scope_request_dict = update_api_scope_request_instance.to_dict()
# create an instance of UpdateAPIScopeRequest from a dict
update_api_scope_request_from_dict = UpdateAPIScopeRequest.from_dict(update_api_scope_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


