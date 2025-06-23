# AddAPIsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the API. (1-64 characters). | 
**audience** | **str** | A unique identifier for the API - commonly the URL. This value will be used as the &#x60;audience&#x60; parameter in authorization claims. (1-64 characters) | 

## Example

```python
from kinde_sdk.models.add_apis_request import AddAPIsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddAPIsRequest from a JSON string
add_apis_request_instance = AddAPIsRequest.from_json(json)
# print the JSON string representation of the object
print(AddAPIsRequest.to_json())

# convert the object into a dict
add_apis_request_dict = add_apis_request_instance.to_dict()
# create an instance of AddAPIsRequest from a dict
add_apis_request_from_dict = AddAPIsRequest.from_dict(add_apis_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


