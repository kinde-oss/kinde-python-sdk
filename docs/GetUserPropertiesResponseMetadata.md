# GetUserPropertiesResponseMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**has_more** | **bool** | Whether more records exist. | [optional] 
**next_page_starting_after** | **str** | The ID of the last record on the current page. | [optional] 

## Example

```python
from kinde_sdk.models.get_user_properties_response_metadata import GetUserPropertiesResponseMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of GetUserPropertiesResponseMetadata from a JSON string
get_user_properties_response_metadata_instance = GetUserPropertiesResponseMetadata.from_json(json)
# print the JSON string representation of the object
print(GetUserPropertiesResponseMetadata.to_json())

# convert the object into a dict
get_user_properties_response_metadata_dict = get_user_properties_response_metadata_instance.to_dict()
# create an instance of GetUserPropertiesResponseMetadata from a dict
get_user_properties_response_metadata_from_dict = GetUserPropertiesResponseMetadata.from_dict(get_user_properties_response_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


