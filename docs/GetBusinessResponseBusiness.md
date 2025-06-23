# GetBusinessResponseBusiness


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | The unique ID for the business. | [optional] 
**name** | **str** | Your business&#39;s name. | [optional] 
**phone** | **str** | Phone number associated with business. | [optional] 
**email** | **str** | Email address associated with business. | [optional] 
**industry** | **str** | The industry your business is in. | [optional] 
**timezone** | **str** | The timezone your business is in. | [optional] 
**privacy_url** | **str** | Your Privacy policy URL. | [optional] 
**terms_url** | **str** | Your Terms and Conditions URL. | [optional] 
**has_clickwrap** | **bool** | Whether your business uses clickwrap agreements. | [optional] 
**has_kinde_branding** | **bool** | Whether your business shows Kinde branding. | [optional] 
**created_on** | **str** | Date of business creation in ISO 8601 format. | [optional] 

## Example

```python
from kinde_sdk.models.get_business_response_business import GetBusinessResponseBusiness

# TODO update the JSON string below
json = "{}"
# create an instance of GetBusinessResponseBusiness from a JSON string
get_business_response_business_instance = GetBusinessResponseBusiness.from_json(json)
# print the JSON string representation of the object
print(GetBusinessResponseBusiness.to_json())

# convert the object into a dict
get_business_response_business_dict = get_business_response_business_instance.to_dict()
# create an instance of GetBusinessResponseBusiness from a dict
get_business_response_business_from_dict = GetBusinessResponseBusiness.from_dict(get_business_response_business_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


