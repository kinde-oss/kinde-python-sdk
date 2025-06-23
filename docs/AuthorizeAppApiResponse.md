# AuthorizeAppApiResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | [optional] 
**code** | **str** |  | [optional] 
**applications_disconnected** | **List[str]** |  | [optional] 
**applications_connected** | **List[str]** |  | [optional] 

## Example

```python
from kinde_sdk.models.authorize_app_api_response import AuthorizeAppApiResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AuthorizeAppApiResponse from a JSON string
authorize_app_api_response_instance = AuthorizeAppApiResponse.from_json(json)
# print the JSON string representation of the object
print(AuthorizeAppApiResponse.to_json())

# convert the object into a dict
authorize_app_api_response_dict = authorize_app_api_response_instance.to_dict()
# create an instance of AuthorizeAppApiResponse from a dict
authorize_app_api_response_from_dict = AuthorizeAppApiResponse.from_dict(authorize_app_api_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


