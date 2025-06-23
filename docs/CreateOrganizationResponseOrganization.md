# CreateOrganizationResponseOrganization


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | The organization&#39;s unique code. | [optional] 
**billing_customer_id** | **str** | The billing customer id if the organization was created with the is_create_billing_customer as true | [optional] 

## Example

```python
from kinde_sdk.models.create_organization_response_organization import CreateOrganizationResponseOrganization

# TODO update the JSON string below
json = "{}"
# create an instance of CreateOrganizationResponseOrganization from a JSON string
create_organization_response_organization_instance = CreateOrganizationResponseOrganization.from_json(json)
# print the JSON string representation of the object
print(CreateOrganizationResponseOrganization.to_json())

# convert the object into a dict
create_organization_response_organization_dict = create_organization_response_organization_instance.to_dict()
# create an instance of CreateOrganizationResponseOrganization from a dict
create_organization_response_organization_from_dict = CreateOrganizationResponseOrganization.from_dict(create_organization_response_organization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


