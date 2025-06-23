# UpdateOrganizationPropertiesRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | **object** | Property keys and values | 

## Example

```python
from kinde_sdk.models.update_organization_properties_request import UpdateOrganizationPropertiesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateOrganizationPropertiesRequest from a JSON string
update_organization_properties_request_instance = UpdateOrganizationPropertiesRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateOrganizationPropertiesRequest.to_json())

# convert the object into a dict
update_organization_properties_request_dict = update_organization_properties_request_instance.to_dict()
# create an instance of UpdateOrganizationPropertiesRequest from a dict
update_organization_properties_request_from_dict = UpdateOrganizationPropertiesRequest.from_dict(update_organization_properties_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


