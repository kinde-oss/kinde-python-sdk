# DeleteApiResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | [optional] 
**code** | **str** |  | [optional] 

## Example

```python
from kinde_sdk.models.delete_api_response import DeleteApiResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteApiResponse from a JSON string
delete_api_response_instance = DeleteApiResponse.from_json(json)
# print the JSON string representation of the object
print(DeleteApiResponse.to_json())

# convert the object into a dict
delete_api_response_dict = delete_api_response_instance.to_dict()
# create an instance of DeleteApiResponse from a dict
delete_api_response_from_dict = DeleteApiResponse.from_dict(delete_api_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


