# ReadLogoResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**logos** | [**List[ReadLogoResponseLogosInner]**](ReadLogoResponseLogosInner.md) | A list of logos. | [optional] 
**message** | **str** | Response message. | [optional] 

## Example

```python
from kinde_sdk.models.read_logo_response import ReadLogoResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReadLogoResponse from a JSON string
read_logo_response_instance = ReadLogoResponse.from_json(json)
# print the JSON string representation of the object
print(ReadLogoResponse.to_json())

# convert the object into a dict
read_logo_response_dict = read_logo_response_instance.to_dict()
# create an instance of ReadLogoResponse from a dict
read_logo_response_from_dict = ReadLogoResponse.from_dict(read_logo_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


