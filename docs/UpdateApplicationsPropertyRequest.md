# UpdateApplicationsPropertyRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | [**UpdateApplicationsPropertyRequestValue**](UpdateApplicationsPropertyRequestValue.md) |  | 

## Example

```python
from kinde_sdk.models.update_applications_property_request import UpdateApplicationsPropertyRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateApplicationsPropertyRequest from a JSON string
update_applications_property_request_instance = UpdateApplicationsPropertyRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateApplicationsPropertyRequest.to_json())

# convert the object into a dict
update_applications_property_request_dict = update_applications_property_request_instance.to_dict()
# create an instance of UpdateApplicationsPropertyRequest from a dict
update_applications_property_request_from_dict = UpdateApplicationsPropertyRequest.from_dict(update_applications_property_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


