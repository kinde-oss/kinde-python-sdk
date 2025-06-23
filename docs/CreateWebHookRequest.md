# CreateWebHookRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**endpoint** | **str** | The webhook endpoint url | 
**event_types** | **List[str]** | Array of event type keys | 
**name** | **str** | The webhook name | 
**description** | **str** | The webhook description | [optional] 

## Example

```python
from kinde_sdk.models.create_web_hook_request import CreateWebHookRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateWebHookRequest from a JSON string
create_web_hook_request_instance = CreateWebHookRequest.from_json(json)
# print the JSON string representation of the object
print(CreateWebHookRequest.to_json())

# convert the object into a dict
create_web_hook_request_dict = create_web_hook_request_instance.to_dict()
# create an instance of CreateWebHookRequest from a dict
create_web_hook_request_from_dict = CreateWebHookRequest.from_dict(create_web_hook_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


