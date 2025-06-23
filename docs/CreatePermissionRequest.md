# CreatePermissionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The permission&#39;s name. | [optional] 
**description** | **str** | The permission&#39;s description. | [optional] 
**key** | **str** | The permission identifier to use in code. | [optional] 

## Example

```python
from kinde_sdk.models.create_permission_request import CreatePermissionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreatePermissionRequest from a JSON string
create_permission_request_instance = CreatePermissionRequest.from_json(json)
# print the JSON string representation of the object
print(CreatePermissionRequest.to_json())

# convert the object into a dict
create_permission_request_dict = create_permission_request_instance.to_dict()
# create an instance of CreatePermissionRequest from a dict
create_permission_request_from_dict = CreatePermissionRequest.from_dict(create_permission_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


