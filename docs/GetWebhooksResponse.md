# GetWebhooksResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**webhooks** | [**List[Webhook]**](Webhook.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_webhooks_response import GetWebhooksResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetWebhooksResponse from a JSON string
get_webhooks_response_instance = GetWebhooksResponse.from_json(json)
# print the JSON string representation of the object
print(GetWebhooksResponse.to_json())

# convert the object into a dict
get_webhooks_response_dict = get_webhooks_response_instance.to_dict()
# create an instance of GetWebhooksResponse from a dict
get_webhooks_response_from_dict = GetWebhooksResponse.from_dict(get_webhooks_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


