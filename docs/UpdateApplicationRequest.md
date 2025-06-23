# UpdateApplicationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The application&#39;s name. | [optional] 
**language_key** | **str** | The application&#39;s language key. | [optional] 
**logout_uris** | **List[str]** | The application&#39;s logout uris. | [optional] 
**redirect_uris** | **List[str]** | The application&#39;s redirect uris. | [optional] 
**login_uri** | **str** | The default login route for resolving session issues. | [optional] 
**homepage_uri** | **str** | The homepage link to your application. | [optional] 

## Example

```python
from kinde_sdk.models.update_application_request import UpdateApplicationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateApplicationRequest from a JSON string
update_application_request_instance = UpdateApplicationRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateApplicationRequest.to_json())

# convert the object into a dict
update_application_request_dict = update_application_request_instance.to_dict()
# create an instance of UpdateApplicationRequest from a dict
update_application_request_from_dict = UpdateApplicationRequest.from_dict(update_application_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


