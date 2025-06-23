# GetOrganizationsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**organizations** | [**List[OrganizationItemSchema]**](OrganizationItemSchema.md) |  | [optional] 
**next_token** | **str** | Pagination token. | [optional] 

## Example

```python
from kinde_sdk.models.get_organizations_response import GetOrganizationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetOrganizationsResponse from a JSON string
get_organizations_response_instance = GetOrganizationsResponse.from_json(json)
# print the JSON string representation of the object
print(GetOrganizationsResponse.to_json())

# convert the object into a dict
get_organizations_response_dict = get_organizations_response_instance.to_dict()
# create an instance of GetOrganizationsResponse from a dict
get_organizations_response_from_dict = GetOrganizationsResponse.from_dict(get_organizations_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


