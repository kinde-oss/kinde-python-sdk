# GetIdentitiesResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**identities** | [**List[Identity]**](Identity.md) |  | [optional] 
**has_more** | **bool** | Whether more records exist. | [optional] 

## Example

```python
from kinde_sdk.models.get_identities_response import GetIdentitiesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetIdentitiesResponse from a JSON string
get_identities_response_instance = GetIdentitiesResponse.from_json(json)
# print the JSON string representation of the object
print(GetIdentitiesResponse.to_json())

# convert the object into a dict
get_identities_response_dict = get_identities_response_instance.to_dict()
# create an instance of GetIdentitiesResponse from a dict
get_identities_response_from_dict = GetIdentitiesResponse.from_dict(get_identities_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


