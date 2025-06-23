# GetSubscribersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**subscribers** | [**List[SubscribersSubscriber]**](SubscribersSubscriber.md) |  | [optional] 
**next_token** | **str** | Pagination token. | [optional] 

## Example

```python
from kinde_sdk.models.get_subscribers_response import GetSubscribersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetSubscribersResponse from a JSON string
get_subscribers_response_instance = GetSubscribersResponse.from_json(json)
# print the JSON string representation of the object
print(GetSubscribersResponse.to_json())

# convert the object into a dict
get_subscribers_response_dict = get_subscribers_response_instance.to_dict()
# create an instance of GetSubscribersResponse from a dict
get_subscribers_response_from_dict = GetSubscribersResponse.from_dict(get_subscribers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


