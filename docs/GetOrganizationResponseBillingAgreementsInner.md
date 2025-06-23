# GetOrganizationResponseBillingAgreementsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**plan_code** | **str** | The code of the plan from which this agreement is taken from | [optional] 
**agreement_id** | **str** | The id of the billing agreement in Kinde | [optional] 

## Example

```python
from kinde_sdk.models.get_organization_response_billing_agreements_inner import GetOrganizationResponseBillingAgreementsInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganizationResponseBillingAgreementsInner from a JSON string
get_organization_response_billing_agreements_inner_instance = GetOrganizationResponseBillingAgreementsInner.from_json(json)
# print the JSON string representation of the object
print(GetOrganizationResponseBillingAgreementsInner.to_json())

# convert the object into a dict
get_organization_response_billing_agreements_inner_dict = get_organization_response_billing_agreements_inner_instance.to_dict()
# create an instance of GetOrganizationResponseBillingAgreementsInner from a dict
get_organization_response_billing_agreements_inner_from_dict = GetOrganizationResponseBillingAgreementsInner.from_dict(get_organization_response_billing_agreements_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


