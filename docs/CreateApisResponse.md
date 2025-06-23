# CreateApisResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | A Kinde generated message. | [optional] 
**code** | **str** | A Kinde generated status code. | [optional] 
**api** | [**CreateApisResponseApi**](CreateApisResponseApi.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_apis_response import CreateApisResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateApisResponse from a JSON string
create_apis_response_instance = CreateApisResponse.from_json(json)
# print the JSON string representation of the object
print(CreateApisResponse.to_json())

# convert the object into a dict
create_apis_response_dict = create_apis_response_instance.to_dict()
# create an instance of CreateApisResponse from a dict
create_apis_response_from_dict = CreateApisResponse.from_dict(create_apis_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


