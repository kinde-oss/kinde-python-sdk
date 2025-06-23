# UpdateBusinessRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**business_name** | **str** | The name of the business. | [optional] 
**email** | **str** | The email address of the business. | [optional] 
**industry_key** | **str** | The key of the industry of your business. Can be retrieved from the /industries endpoint. | [optional] 
**is_click_wrap** | **bool** | Whether the business is using clickwrap agreements. | [optional] 
**is_show_kinde_branding** | **bool** | Whether the business is showing Kinde branding. Requires a paid plan. | [optional] 
**kinde_perk_code** | **str** | The Kinde perk code for the business. | [optional] 
**phone** | **str** | The phone number of the business. | [optional] 
**privacy_url** | **str** | The URL to the business&#39;s privacy policy. | [optional] 
**terms_url** | **str** | The URL to the business&#39;s terms of service. | [optional] 
**timezone_key** | **str** | The key of the timezone of your business. Can be retrieved from the /timezones endpoint. | [optional] 

## Example

```python
from kinde_sdk.models.update_business_request import UpdateBusinessRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateBusinessRequest from a JSON string
update_business_request_instance = UpdateBusinessRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateBusinessRequest.to_json())

# convert the object into a dict
update_business_request_dict = update_business_request_instance.to_dict()
# create an instance of UpdateBusinessRequest from a dict
update_business_request_from_dict = UpdateBusinessRequest.from_dict(update_business_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


