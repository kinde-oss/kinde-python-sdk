# NotFoundResponseErrors


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** |  | [optional] 
**message** | **str** |  | [optional] 

## Example

```python
from kinde_sdk.models.not_found_response_errors import NotFoundResponseErrors

# TODO update the JSON string below
json = "{}"
# create an instance of NotFoundResponseErrors from a JSON string
not_found_response_errors_instance = NotFoundResponseErrors.from_json(json)
# print the JSON string representation of the object
print(NotFoundResponseErrors.to_json())

# convert the object into a dict
not_found_response_errors_dict = not_found_response_errors_instance.to_dict()
# create an instance of NotFoundResponseErrors from a dict
not_found_response_errors_from_dict = NotFoundResponseErrors.from_dict(not_found_response_errors_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


