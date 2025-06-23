# OrganizationItemSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | The unique identifier for the organization. | [optional] 
**name** | **str** | The organization&#39;s name. | [optional] 
**handle** | **str** | A unique handle for the organization - can be used for dynamic callback urls. | [optional] 
**is_default** | **bool** | Whether the organization is the default organization. | [optional] 
**external_id** | **str** | The organization&#39;s external identifier - commonly used when migrating from or mapping to other systems. | [optional] 
**is_auto_membership_enabled** | **bool** | If users become members of this organization when the org code is supplied during authentication. | [optional] 

## Example

```python
from kinde_sdk.models.organization_item_schema import OrganizationItemSchema

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationItemSchema from a JSON string
organization_item_schema_instance = OrganizationItemSchema.from_json(json)
# print the JSON string representation of the object
print(OrganizationItemSchema.to_json())

# convert the object into a dict
organization_item_schema_dict = organization_item_schema_instance.to_dict()
# create an instance of OrganizationItemSchema from a dict
organization_item_schema_from_dict = OrganizationItemSchema.from_dict(organization_item_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


