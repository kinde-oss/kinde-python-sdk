# ApiResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**result** | **str** | The result of the api operation. | [optional] 

## Example

```python
from kinde_sdk.models.api_result import ApiResult

# TODO update the JSON string below
json = "{}"
# create an instance of ApiResult from a JSON string
api_result_instance = ApiResult.from_json(json)
# print the JSON string representation of the object
print(ApiResult.to_json())

# convert the object into a dict
api_result_dict = api_result_instance.to_dict()
# create an instance of ApiResult from a dict
api_result_from_dict = ApiResult.from_dict(api_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


