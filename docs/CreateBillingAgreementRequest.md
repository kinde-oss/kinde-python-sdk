# CreateBillingAgreementRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customer_id** | **str** | The ID of the billing customer to create a new agreement for | 
**plan_code** | **str** | The code of the billing plan the new agreement will be based on | 
**is_invoice_now** | **bool** | Generate a final invoice for any un-invoiced metered usage. | [optional] 
**is_prorate** | **bool** | Generate a proration invoice item that credits remaining unused features. | [optional] 

## Example

```python
from kinde_sdk.models.create_billing_agreement_request import CreateBillingAgreementRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateBillingAgreementRequest from a JSON string
create_billing_agreement_request_instance = CreateBillingAgreementRequest.from_json(json)
# print the JSON string representation of the object
print(CreateBillingAgreementRequest.to_json())

# convert the object into a dict
create_billing_agreement_request_dict = create_billing_agreement_request_instance.to_dict()
# create an instance of CreateBillingAgreementRequest from a dict
create_billing_agreement_request_from_dict = CreateBillingAgreementRequest.from_dict(create_billing_agreement_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


