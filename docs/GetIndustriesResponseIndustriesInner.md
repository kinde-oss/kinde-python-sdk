# GetIndustriesResponseIndustriesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | The unique key for the industry. | [optional] 
**name** | **str** | The display name for the industry. | [optional] 

## Example

```python
from kinde_sdk.models.get_industries_response_industries_inner import GetIndustriesResponseIndustriesInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetIndustriesResponseIndustriesInner from a JSON string
get_industries_response_industries_inner_instance = GetIndustriesResponseIndustriesInner.from_json(json)
# print the JSON string representation of the object
print(GetIndustriesResponseIndustriesInner.to_json())

# convert the object into a dict
get_industries_response_industries_inner_dict = get_industries_response_industries_inner_instance.to_dict()
# create an instance of GetIndustriesResponseIndustriesInner from a dict
get_industries_response_industries_inner_from_dict = GetIndustriesResponseIndustriesInner.from_dict(get_industries_response_industries_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


