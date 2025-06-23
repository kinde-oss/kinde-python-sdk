# GetOrganizationResponseBilling

The billing information if the organization is a billing customer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**billing_customer_id** | **str** |  | [optional] 
**agreements** | [**List[GetOrganizationResponseBillingAgreementsInner]**](GetOrganizationResponseBillingAgreementsInner.md) | The billing agreements the billing customer is currently subscribed to | [optional] 

## Example

```python
from kinde_sdk.models.get_organization_response_billing import GetOrganizationResponseBilling

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganizationResponseBilling from a JSON string
get_organization_response_billing_instance = GetOrganizationResponseBilling.from_json(json)
# print the JSON string representation of the object
print(GetOrganizationResponseBilling.to_json())

# convert the object into a dict
get_organization_response_billing_dict = get_organization_response_billing_instance.to_dict()
# create an instance of GetOrganizationResponseBilling from a dict
get_organization_response_billing_from_dict = GetOrganizationResponseBilling.from_dict(get_organization_response_billing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


