# GetUserPropertiesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**GetUserPropertiesResponseData**](GetUserPropertiesResponseData.md) |  | [optional] 
**metadata** | [**GetUserPropertiesResponseMetadata**](GetUserPropertiesResponseMetadata.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_user_properties_response import GetUserPropertiesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserPropertiesResponse from a JSON string
get_user_properties_response_instance = GetUserPropertiesResponse.from_json(json)
# print the JSON string representation of the object
print(GetUserPropertiesResponse.to_json())

# convert the object into a dict
get_user_properties_response_dict = get_user_properties_response_instance.to_dict()
# create an instance of GetUserPropertiesResponse from a dict
get_user_properties_response_from_dict = GetUserPropertiesResponse.from_dict(get_user_properties_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


