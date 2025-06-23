# SearchUsersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | **str** | Response code. | [optional] 
**message** | **str** | Response message. | [optional] 
**results** | [**List[SearchUsersResponseResultsInner]**](SearchUsersResponseResultsInner.md) |  | [optional] 

## Example

```python
from kinde_sdk.models.search_users_response import SearchUsersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SearchUsersResponse from a JSON string
search_users_response_instance = SearchUsersResponse.from_json(json)
# print the JSON string representation of the object
print(SearchUsersResponse.to_json())

# convert the object into a dict
search_users_response_dict = search_users_response_instance.to_dict()
# create an instance of SearchUsersResponse from a dict
search_users_response_from_dict = SearchUsersResponse.from_dict(search_users_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


