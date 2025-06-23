# GetBillingEntitlementsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**has_more** | **bool** | Whether more records exist. | [optional] 
**entitlements** | [**List[GetBillingEntitlementsResponseEntitlementsInner]**](GetBillingEntitlementsResponseEntitlementsInner.md) | A list of entitlements | [optional] 
**plans** | [**List[GetBillingEntitlementsResponsePlansInner]**](GetBillingEntitlementsResponsePlansInner.md) | A list of plans. | [optional] 

## Example

```python
from kinde_sdk.models.get_billing_entitlements_response import GetBillingEntitlementsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetBillingEntitlementsResponse from a JSON string
get_billing_entitlements_response_instance = GetBillingEntitlementsResponse.from_json(json)
# print the JSON string representation of the object
print(GetBillingEntitlementsResponse.to_json())

# convert the object into a dict
get_billing_entitlements_response_dict = get_billing_entitlements_response_instance.to_dict()
# create an instance of GetBillingEntitlementsResponse from a dict
get_billing_entitlements_response_from_dict = GetBillingEntitlementsResponse.from_dict(get_billing_entitlements_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


