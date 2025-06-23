# CreateConnectionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** |  | [optional] 
**code** | **str** |  | [optional] 
**connection** | [**CreateConnectionResponseConnection**](CreateConnectionResponseConnection.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.create_connection_response import CreateConnectionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConnectionResponse from a JSON string
create_connection_response_instance = CreateConnectionResponse.from_json(json)
# print the JSON string representation of the object
print(CreateConnectionResponse.to_json())

# convert the object into a dict
create_connection_response_dict = create_connection_response_instance.to_dict()
# create an instance of CreateConnectionResponse from a dict
create_connection_response_from_dict = CreateConnectionResponse.from_dict(create_connection_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


