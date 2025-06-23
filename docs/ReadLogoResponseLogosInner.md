# ReadLogoResponseLogosInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The type of logo (light or dark). | [optional] 
**file_name** | **str** | The name of the logo file. | [optional] 
**path** | **str** | The relative path to the logo file. | [optional] 

## Example

```python
from kinde_sdk.models.read_logo_response_logos_inner import ReadLogoResponseLogosInner

# TODO update the JSON string below
json = "{}"
# create an instance of ReadLogoResponseLogosInner from a JSON string
read_logo_response_logos_inner_instance = ReadLogoResponseLogosInner.from_json(json)
# print the JSON string representation of the object
print(ReadLogoResponseLogosInner.to_json())

# convert the object into a dict
read_logo_response_logos_inner_dict = read_logo_response_logos_inner_instance.to_dict()
# create an instance of ReadLogoResponseLogosInner from a dict
read_logo_response_logos_inner_from_dict = ReadLogoResponseLogosInner.from_dict(read_logo_response_logos_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


