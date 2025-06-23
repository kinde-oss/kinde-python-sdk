# CreateWebhookResponseWebhook


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**endpoint** | **str** |  | [optional] 

## Example

```python
from kinde_sdk.models.create_webhook_response_webhook import CreateWebhookResponseWebhook

# TODO update the JSON string below
json = "{}"
# create an instance of CreateWebhookResponseWebhook from a JSON string
create_webhook_response_webhook_instance = CreateWebhookResponseWebhook.from_json(json)
# print the JSON string representation of the object
print(CreateWebhookResponseWebhook.to_json())

# convert the object into a dict
create_webhook_response_webhook_dict = create_webhook_response_webhook_instance.to_dict()
# create an instance of CreateWebhookResponseWebhook from a dict
create_webhook_response_webhook_from_dict = CreateWebhookResponseWebhook.from_dict(create_webhook_response_webhook_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


