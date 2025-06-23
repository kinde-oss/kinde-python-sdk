# UpdateCategoryRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the category. | [optional] 

## Example

```python
from kinde_sdk.models.update_category_request import UpdateCategoryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateCategoryRequest from a JSON string
update_category_request_instance = UpdateCategoryRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateCategoryRequest.to_json())

# convert the object into a dict
update_category_request_dict = update_category_request_instance.to_dict()
# create an instance of UpdateCategoryRequest from a dict
update_category_request_from_dict = UpdateCategoryRequest.from_dict(update_category_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


