# SearchUsersResponseResultsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique ID of the user in Kinde. | [optional] 
**provided_id** | **str** | External ID for user. | [optional] 
**email** | **str** | Default email address of the user in Kinde. | [optional] 
**username** | **str** | Primary username of the user in Kinde. | [optional] 
**last_name** | **str** | User&#39;s last name. | [optional] 
**first_name** | **str** | User&#39;s first name. | [optional] 
**is_suspended** | **bool** | Whether the user is currently suspended or not. | [optional] 
**picture** | **str** | User&#39;s profile picture URL. | [optional] 
**total_sign_ins** | **int** | Total number of user sign ins. | [optional] 
**failed_sign_ins** | **int** | Number of consecutive failed user sign ins. | [optional] 
**last_signed_in** | **str** | Last sign in date in ISO 8601 format. | [optional] 
**created_on** | **str** | Date of user creation in ISO 8601 format. | [optional] 
**organizations** | **List[str]** | Array of organizations a user belongs to. | [optional] 
**identities** | [**List[UserIdentitiesInner]**](UserIdentitiesInner.md) | Array of identities belonging to the user. | [optional] 
**properties** | **Dict[str, str]** | The user properties. | [optional] 

## Example

```python
from kinde_sdk.models.search_users_response_results_inner import SearchUsersResponseResultsInner

# TODO update the JSON string below
json = "{}"
# create an instance of SearchUsersResponseResultsInner from a JSON string
search_users_response_results_inner_instance = SearchUsersResponseResultsInner.from_json(json)
# print the JSON string representation of the object
print(SearchUsersResponseResultsInner.to_json())

# convert the object into a dict
search_users_response_results_inner_dict = search_users_response_results_inner_instance.to_dict()
# create an instance of SearchUsersResponseResultsInner from a dict
search_users_response_results_inner_from_dict = SearchUsersResponseResultsInner.from_dict(search_users_response_results_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


