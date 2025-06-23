# GetEntitlementsResponseDataPlansInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | A unique code for the plan | [optional] 
**subscribed_on** | **datetime** | The date the user subscribed to the plan | [optional] 

## Example

```python
from kinde_sdk.models.get_entitlements_response_data_plans_inner import GetEntitlementsResponseDataPlansInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetEntitlementsResponseDataPlansInner from a JSON string
get_entitlements_response_data_plans_inner_instance = GetEntitlementsResponseDataPlansInner.from_json(json)
# print the JSON string representation of the object
print(GetEntitlementsResponseDataPlansInner.to_json())

# convert the object into a dict
get_entitlements_response_data_plans_inner_dict = get_entitlements_response_data_plans_inner_instance.to_dict()
# create an instance of GetEntitlementsResponseDataPlansInner from a dict
get_entitlements_response_data_plans_inner_from_dict = GetEntitlementsResponseDataPlansInner.from_dict(get_entitlements_response_data_plans_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


