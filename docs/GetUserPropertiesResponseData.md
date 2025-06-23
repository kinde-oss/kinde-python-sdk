# GetUserPropertiesResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | [**List[GetUserPropertiesResponseDataPropertiesInner]**](GetUserPropertiesResponseDataPropertiesInner.md) | A list of properties | [optional] 

## Example

```python
from kinde_sdk.models.get_user_properties_response_data import GetUserPropertiesResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserPropertiesResponseData from a JSON string
get_user_properties_response_data_instance = GetUserPropertiesResponseData.from_json(json)
# print the JSON string representation of the object
print(GetUserPropertiesResponseData.to_json())

# convert the object into a dict
get_user_properties_response_data_dict = get_user_properties_response_data_instance.to_dict()
# create an instance of GetUserPropertiesResponseData from a dict
get_user_properties_response_data_from_dict = GetUserPropertiesResponseData.from_dict(get_user_properties_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


