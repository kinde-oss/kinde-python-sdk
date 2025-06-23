# SubscribersSubscriber


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**full_name** | **str** |  | [optional] 
**first_name** | **str** |  | [optional] 
**last_name** | **str** |  | [optional] 

## Example

```python
from kinde_sdk.models.subscribers_subscriber import SubscribersSubscriber

# TODO update the JSON string below
json = "{}"
# create an instance of SubscribersSubscriber from a JSON string
subscribers_subscriber_instance = SubscribersSubscriber.from_json(json)
# print the JSON string representation of the object
print(SubscribersSubscriber.to_json())

# convert the object into a dict
subscribers_subscriber_dict = subscribers_subscriber_instance.to_dict()
# create an instance of SubscribersSubscriber from a dict
subscribers_subscriber_from_dict = SubscribersSubscriber.from_dict(subscribers_subscriber_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


