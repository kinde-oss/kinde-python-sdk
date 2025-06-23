# CreateApplicationResponseApplication


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The application&#39;s identifier. | [optional] 
**client_id** | **str** | The application&#39;s client ID. | [optional] 
**client_secret** | **str** | The application&#39;s client secret. | [optional] 

## Example

```python
from kinde_sdk.models.create_application_response_application import CreateApplicationResponseApplication

# TODO update the JSON string below
json = "{}"
# create an instance of CreateApplicationResponseApplication from a JSON string
create_application_response_application_instance = CreateApplicationResponseApplication.from_json(json)
# print the JSON string representation of the object
print(CreateApplicationResponseApplication.to_json())

# convert the object into a dict
create_application_response_application_dict = create_application_response_application_instance.to_dict()
# create an instance of CreateApplicationResponseApplication from a dict
create_application_response_application_from_dict = CreateApplicationResponseApplication.from_dict(create_application_response_application_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


