# TokenErrorResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** | Error. | [optional] 
**error_description** | **str** | The error description. | [optional] 

## Example

```python
from kinde_sdk.models.token_error_response import TokenErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TokenErrorResponse from a JSON string
token_error_response_instance = TokenErrorResponse.from_json(json)
# print the JSON string representation of the object
print(TokenErrorResponse.to_json())

# convert the object into a dict
token_error_response_dict = token_error_response_instance.to_dict()
# create an instance of TokenErrorResponse from a dict
token_error_response_from_dict = TokenErrorResponse.from_dict(token_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


