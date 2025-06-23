# UpdateWebHookRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_types** | **List[str]** | Array of event type keys | [optional] 
**name** | **str** | The webhook name | [optional] 
**description** | **str** | The webhook description | [optional] 

## Example

```python
from kinde_sdk.models.update_web_hook_request import UpdateWebHookRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateWebHookRequest from a JSON string
update_web_hook_request_instance = UpdateWebHookRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateWebHookRequest.to_json())

# convert the object into a dict
update_web_hook_request_dict = update_web_hook_request_instance.to_dict()
# create an instance of UpdateWebHookRequest from a dict
update_web_hook_request_from_dict = UpdateWebHookRequest.from_dict(update_web_hook_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


