# GetBillingAgreementsResponseAgreementsInnerEntitlementsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feature_code** | **str** | The feature code of the feature corresponding to this entitlement | [optional] 
**entitlement_id** | **str** | The friendly id of an entitlement | [optional] 

## Example

```python
from kinde_sdk.models.get_billing_agreements_response_agreements_inner_entitlements_inner import GetBillingAgreementsResponseAgreementsInnerEntitlementsInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetBillingAgreementsResponseAgreementsInnerEntitlementsInner from a JSON string
get_billing_agreements_response_agreements_inner_entitlements_inner_instance = GetBillingAgreementsResponseAgreementsInnerEntitlementsInner.from_json(json)
# print the JSON string representation of the object
print(GetBillingAgreementsResponseAgreementsInnerEntitlementsInner.to_json())

# convert the object into a dict
get_billing_agreements_response_agreements_inner_entitlements_inner_dict = get_billing_agreements_response_agreements_inner_entitlements_inner_instance.to_dict()
# create an instance of GetBillingAgreementsResponseAgreementsInnerEntitlementsInner from a dict
get_billing_agreements_response_agreements_inner_entitlements_inner_from_dict = GetBillingAgreementsResponseAgreementsInnerEntitlementsInner.from_dict(get_billing_agreements_response_agreements_inner_entitlements_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


