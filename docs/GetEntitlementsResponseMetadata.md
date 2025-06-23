# GetEntitlementsResponseMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**has_more** | **bool** | Whether more records exist. | [optional] 
**next_page_starting_after** | **str** | The ID of the last record on the current page. | [optional] 

## Example

```python
from kinde_sdk.models.get_entitlements_response_metadata import GetEntitlementsResponseMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of GetEntitlementsResponseMetadata from a JSON string
get_entitlements_response_metadata_instance = GetEntitlementsResponseMetadata.from_json(json)
# print the JSON string representation of the object
print(GetEntitlementsResponseMetadata.to_json())

# convert the object into a dict
get_entitlements_response_metadata_dict = get_entitlements_response_metadata_instance.to_dict()
# create an instance of GetEntitlementsResponseMetadata from a dict
get_entitlements_response_metadata_from_dict = GetEntitlementsResponseMetadata.from_dict(get_entitlements_response_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


