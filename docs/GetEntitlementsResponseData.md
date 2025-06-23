# GetEntitlementsResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**org_code** | **str** | The organization code the entitlements are associated with. | [optional] 
**plans** | [**List[GetEntitlementsResponseDataPlansInner]**](GetEntitlementsResponseDataPlansInner.md) | A list of plans the user is subscribed to | [optional] 
**entitlements** | [**List[GetEntitlementsResponseDataEntitlementsInner]**](GetEntitlementsResponseDataEntitlementsInner.md) | A list of entitlements | [optional] 

## Example

```python
from kinde_sdk.models.get_entitlements_response_data import GetEntitlementsResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of GetEntitlementsResponseData from a JSON string
get_entitlements_response_data_instance = GetEntitlementsResponseData.from_json(json)
# print the JSON string representation of the object
print(GetEntitlementsResponseData.to_json())

# convert the object into a dict
get_entitlements_response_data_dict = get_entitlements_response_data_instance.to_dict()
# create an instance of GetEntitlementsResponseData from a dict
get_entitlements_response_data_from_dict = GetEntitlementsResponseData.from_dict(get_entitlements_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


