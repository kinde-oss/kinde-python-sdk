# GetBillingEntitlementsResponseEntitlementsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The friendly id of an entitlement | [optional] 
**fixed_charge** | **int** | The price charged if this is an entitlement for a fixed charged | [optional] 
**price_name** | **str** | The name of the price associated with the entitlement | [optional] 
**unit_amount** | **int** | The price charged for this entitlement in cents | [optional] 
**feature_code** | **str** | The feature code of the feature corresponding to this entitlement | [optional] 
**feature_name** | **str** | The feature name of the feature corresponding to this entitlement | [optional] 
**entitlement_limit_max** | **int** | The maximum number of units of the feature the customer is entitled to | [optional] 
**entitlement_limit_min** | **int** | The minimum number of units of the feature the customer is entitled to | [optional] 

## Example

```python
from kinde_sdk.models.get_billing_entitlements_response_entitlements_inner import GetBillingEntitlementsResponseEntitlementsInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetBillingEntitlementsResponseEntitlementsInner from a JSON string
get_billing_entitlements_response_entitlements_inner_instance = GetBillingEntitlementsResponseEntitlementsInner.from_json(json)
# print the JSON string representation of the object
print(GetBillingEntitlementsResponseEntitlementsInner.to_json())

# convert the object into a dict
get_billing_entitlements_response_entitlements_inner_dict = get_billing_entitlements_response_entitlements_inner_instance.to_dict()
# create an instance of GetBillingEntitlementsResponseEntitlementsInner from a dict
get_billing_entitlements_response_entitlements_inner_from_dict = GetBillingEntitlementsResponseEntitlementsInner.from_dict(get_billing_entitlements_response_entitlements_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


