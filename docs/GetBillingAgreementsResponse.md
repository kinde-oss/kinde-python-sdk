# GetBillingAgreementsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**has_more** | **bool** | Whether more records exist. | [optional] 
**agreements** | [**List[GetBillingAgreementsResponseAgreementsInner]**](GetBillingAgreementsResponseAgreementsInner.md) | A list of billing agreements | [optional] 

## Example

```python
from kinde_sdk.models.get_billing_agreements_response import GetBillingAgreementsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetBillingAgreementsResponse from a JSON string
get_billing_agreements_response_instance = GetBillingAgreementsResponse.from_json(json)
# print the JSON string representation of the object
print(GetBillingAgreementsResponse.to_json())

# convert the object into a dict
get_billing_agreements_response_dict = get_billing_agreements_response_instance.to_dict()
# create an instance of GetBillingAgreementsResponse from a dict
get_billing_agreements_response_from_dict = GetBillingAgreementsResponse.from_dict(get_billing_agreements_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


