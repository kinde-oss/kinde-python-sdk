# GetSubscriberResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**subscribers** | [**List[Subscriber]**](Subscriber.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.get_subscriber_response import GetSubscriberResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetSubscriberResponse from a JSON string
get_subscriber_response_instance = GetSubscriberResponse.from_json(json)
# print the JSON string representation of the object
print(GetSubscriberResponse.to_json())

# convert the object into a dict
get_subscriber_response_dict = get_subscriber_response_instance.to_dict()
# create an instance of GetSubscriberResponse from a dict
get_subscriber_response_from_dict = GetSubscriberResponse.from_dict(get_subscriber_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


