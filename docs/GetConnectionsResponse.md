# GetConnectionsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**connections** | [**List[Connection]**](Connection.md) |  | [optional] 
**has_more** | **bool** | Whether more records exist. | [optional] 

## Example

```python
from kinde_sdk.models.get_connections_response import GetConnectionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetConnectionsResponse from a JSON string
get_connections_response_instance = GetConnectionsResponse.from_json(json)
# print the JSON string representation of the object
print(GetConnectionsResponse.to_json())

# convert the object into a dict
get_connections_response_dict = get_connections_response_instance.to_dict()
# create an instance of GetConnectionsResponse from a dict
get_connections_response_from_dict = GetConnectionsResponse.from_dict(get_connections_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


