# GetBillingEntitlementsResponsePlansInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | The plan code the billing customer is subscribed to | [optional] 
**subscribed_on** | **datetime** |  | [optional] 

## Example

```python
from kinde_sdk.models.get_billing_entitlements_response_plans_inner import GetBillingEntitlementsResponsePlansInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetBillingEntitlementsResponsePlansInner from a JSON string
get_billing_entitlements_response_plans_inner_instance = GetBillingEntitlementsResponsePlansInner.from_json(json)
# print the JSON string representation of the object
print(GetBillingEntitlementsResponsePlansInner.to_json())

# convert the object into a dict
get_billing_entitlements_response_plans_inner_dict = get_billing_entitlements_response_plans_inner_instance.to_dict()
# create an instance of GetBillingEntitlementsResponsePlansInner from a dict
get_billing_entitlements_response_plans_inner_from_dict = GetBillingEntitlementsResponsePlansInner.from_dict(get_billing_entitlements_response_plans_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


