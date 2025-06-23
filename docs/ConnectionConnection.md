# ConnectionConnection


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**display_name** | **str** |  | [optional] 
**strategy** | **str** |  | [optional] 

## Example

```python
from kinde_sdk.models.connection_connection import ConnectionConnection

# TODO update the JSON string below
json = "{}"
# create an instance of ConnectionConnection from a JSON string
connection_connection_instance = ConnectionConnection.from_json(json)
# print the JSON string representation of the object
print(ConnectionConnection.to_json())

# convert the object into a dict
connection_connection_dict = connection_connection_instance.to_dict()
# create an instance of ConnectionConnection from a dict
connection_connection_from_dict = ConnectionConnection.from_dict(connection_connection_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


