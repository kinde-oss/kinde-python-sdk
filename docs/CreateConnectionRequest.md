# CreateConnectionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The internal name of the connection. | [optional] 
**display_name** | **str** | The public facing name of the connection. | [optional] 
**strategy** | **str** | The identity provider identifier for the connection. | [optional] 
**enabled_applications** | **List[str]** | Client IDs of applications in which this connection is to be enabled. | [optional] 
**organization_code** | **str** | Enterprise connections only - the code for organization that manages this connection. | [optional] 
**options** | [**CreateConnectionRequestOptions**](CreateConnectionRequestOptions.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_connection_request import CreateConnectionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConnectionRequest from a JSON string
create_connection_request_instance = CreateConnectionRequest.from_json(json)
# print the JSON string representation of the object
print(CreateConnectionRequest.to_json())

# convert the object into a dict
create_connection_request_dict = create_connection_request_instance.to_dict()
# create an instance of CreateConnectionRequest from a dict
create_connection_request_from_dict = CreateConnectionRequest.from_dict(create_connection_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


