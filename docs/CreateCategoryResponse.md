# CreateCategoryResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | [optional] 
**code** | **str** |  | [optional] 
**category** | [**CreateCategoryResponseCategory**](CreateCategoryResponseCategory.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_category_response import CreateCategoryResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCategoryResponse from a JSON string
create_category_response_instance = CreateCategoryResponse.from_json(json)
# print the JSON string representation of the object
print(CreateCategoryResponse.to_json())

# convert the object into a dict
create_category_response_dict = create_category_response_instance.to_dict()
# create an instance of CreateCategoryResponse from a dict
create_category_response_from_dict = CreateCategoryResponse.from_dict(create_category_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


