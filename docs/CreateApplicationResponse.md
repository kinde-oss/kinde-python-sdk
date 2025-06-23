# CreateApplicationResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**application** | [**CreateApplicationResponseApplication**](CreateApplicationResponseApplication.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_application_response import CreateApplicationResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateApplicationResponse from a JSON string
create_application_response_instance = CreateApplicationResponse.from_json(json)
# print the JSON string representation of the object
print(CreateApplicationResponse.to_json())

# convert the object into a dict
create_application_response_dict = create_application_response_instance.to_dict()
# create an instance of CreateApplicationResponse from a dict
create_application_response_from_dict = CreateApplicationResponse.from_dict(create_application_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


