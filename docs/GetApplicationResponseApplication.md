# GetApplicationResponseApplication


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The application&#39;s identifier. | [optional] 
**name** | **str** | The application&#39;s name. | [optional] 
**type** | **str** | The application&#39;s type. | [optional] 
**client_id** | **str** | The application&#39;s client ID. | [optional] 
**client_secret** | **str** | The application&#39;s client secret. | [optional] 
**login_uri** | **str** | The default login route for resolving session issues. | [optional] 
**homepage_uri** | **str** | The homepage link to your application. | [optional] 
**has_cancel_button** | **bool** | Whether the application has a cancel button to allow users to exit the auth flow [Beta]. | [optional] 

## Example

```python
from kinde_sdk.models.get_application_response_application import GetApplicationResponseApplication

# TODO update the JSON string below
json = "{}"
# create an instance of GetApplicationResponseApplication from a JSON string
get_application_response_application_instance = GetApplicationResponseApplication.from_json(json)
# print the JSON string representation of the object
print(GetApplicationResponseApplication.to_json())

# convert the object into a dict
get_application_response_application_dict = get_application_response_application_instance.to_dict()
# create an instance of GetApplicationResponseApplication from a dict
get_application_response_application_from_dict = GetApplicationResponseApplication.from_dict(get_application_response_application_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


