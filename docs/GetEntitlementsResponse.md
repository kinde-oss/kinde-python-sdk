# GetEntitlementsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**GetEntitlementsResponseData**](GetEntitlementsResponseData.md) |  | [optional] 
**metadata** | [**GetEntitlementsResponseMetadata**](GetEntitlementsResponseMetadata.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_entitlements_response import GetEntitlementsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetEntitlementsResponse from a JSON string
get_entitlements_response_instance = GetEntitlementsResponse.from_json(json)
# print the JSON string representation of the object
print(GetEntitlementsResponse.to_json())

# convert the object into a dict
get_entitlements_response_dict = get_entitlements_response_instance.to_dict()
# create an instance of GetEntitlementsResponse from a dict
get_entitlements_response_from_dict = GetEntitlementsResponse.from_dict(get_entitlements_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


