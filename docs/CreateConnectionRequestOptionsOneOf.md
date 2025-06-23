# CreateConnectionRequestOptionsOneOf

Social connection options (e.g., Google SSO).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_id** | **str** | OAuth client ID. | [optional] 
**client_secret** | **str** | OAuth client secret. | [optional] 
**is_use_custom_domain** | **bool** | Use custom domain callback URL. | [optional] 

## Example

```python
from kinde_sdk.models.create_connection_request_options_one_of import CreateConnectionRequestOptionsOneOf

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConnectionRequestOptionsOneOf from a JSON string
create_connection_request_options_one_of_instance = CreateConnectionRequestOptionsOneOf.from_json(json)
# print the JSON string representation of the object
print(CreateConnectionRequestOptionsOneOf.to_json())

# convert the object into a dict
create_connection_request_options_one_of_dict = create_connection_request_options_one_of_instance.to_dict()
# create an instance of CreateConnectionRequestOptionsOneOf from a dict
create_connection_request_options_one_of_from_dict = CreateConnectionRequestOptionsOneOf.from_dict(create_connection_request_options_one_of_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


