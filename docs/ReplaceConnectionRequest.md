# ReplaceConnectionRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The internal name of the connection. | [optional] 
**display_name** | **str** | The public-facing name of the connection. | [optional] 
**enabled_applications** | **List[str]** | Client IDs of applications in which this connection is to be enabled. | [optional] 
**options** | [**ReplaceConnectionRequestOptions**](ReplaceConnectionRequestOptions.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.replace_connection_request import ReplaceConnectionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceConnectionRequest from a JSON string
replace_connection_request_instance = ReplaceConnectionRequest.from_json(json)
# print the JSON string representation of the object
print(ReplaceConnectionRequest.to_json())

# convert the object into a dict
replace_connection_request_dict = replace_connection_request_instance.to_dict()
# create an instance of ReplaceConnectionRequest from a dict
replace_connection_request_from_dict = ReplaceConnectionRequest.from_dict(replace_connection_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


