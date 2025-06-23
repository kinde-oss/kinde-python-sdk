# GetBillingAgreementsResponseAgreementsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The friendly id of an agreement | [optional] 
**plan_code** | **str** | The plan code the billing customer is subscribed to | [optional] 
**expires_on** | **datetime** | The date the agreement expired (and was no longer active) | [optional] 
**billing_group_id** | **str** | The friendly id of the billing group this agreement&#39;s plan is part of | [optional] 
**entitlements** | [**List[GetBillingAgreementsResponseAgreementsInnerEntitlementsInner]**](GetBillingAgreementsResponseAgreementsInnerEntitlementsInner.md) | A list of billing entitlements that is part of this agreement | [optional] 

## Example

```python
from kinde_sdk.models.get_billing_agreements_response_agreements_inner import GetBillingAgreementsResponseAgreementsInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetBillingAgreementsResponseAgreementsInner from a JSON string
get_billing_agreements_response_agreements_inner_instance = GetBillingAgreementsResponseAgreementsInner.from_json(json)
# print the JSON string representation of the object
print(GetBillingAgreementsResponseAgreementsInner.to_json())

# convert the object into a dict
get_billing_agreements_response_agreements_inner_dict = get_billing_agreements_response_agreements_inner_instance.to_dict()
# create an instance of GetBillingAgreementsResponseAgreementsInner from a dict
get_billing_agreements_response_agreements_inner_from_dict = GetBillingAgreementsResponseAgreementsInner.from_dict(get_billing_agreements_response_agreements_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


