# GetCategoriesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**categories** | [**List[Category]**](Category.md) |  | [optional] 
**has_more** | **bool** | Whether more records exist. | [optional] 

## Example

```python
from kinde_sdk.models.get_categories_response import GetCategoriesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetCategoriesResponse from a JSON string
get_categories_response_instance = GetCategoriesResponse.from_json(json)
# print the JSON string representation of the object
print(GetCategoriesResponse.to_json())

# convert the object into a dict
get_categories_response_dict = get_categories_response_instance.to_dict()
# create an instance of GetCategoriesResponse from a dict
get_categories_response_from_dict = GetCategoriesResponse.from_dict(get_categories_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


