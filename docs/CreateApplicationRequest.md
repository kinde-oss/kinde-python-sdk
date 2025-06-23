# CreateApplicationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The application&#39;s name. | 
**type** | **str** | The application&#39;s type. Use &#x60;reg&#x60; for regular server rendered applications, &#x60;spa&#x60; for single-page applications, and &#x60;m2m&#x60; for machine-to-machine applications. | 

## Example

```python
from kinde_sdk.models.create_application_request import CreateApplicationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateApplicationRequest from a JSON string
create_application_request_instance = CreateApplicationRequest.from_json(json)
# print the JSON string representation of the object
print(CreateApplicationRequest.to_json())

# convert the object into a dict
create_application_request_dict = create_application_request_instance.to_dict()
# create an instance of CreateApplicationRequest from a dict
create_application_request_from_dict = CreateApplicationRequest.from_dict(create_application_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


