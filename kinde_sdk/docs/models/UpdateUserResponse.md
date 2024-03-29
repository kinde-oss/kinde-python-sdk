# kinde_sdk.model.update_user_response.UpdateUserResponse

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Unique id of the user in Kinde. | [optional] 
**given_name** | str,  | str,  | User&#x27;s first name. | [optional] 
**family_name** | str,  | str,  | User&#x27;s last name. | [optional] 
**email** | str,  | str,  | User&#x27;s preferred email. | [optional] 
**is_suspended** | bool,  | BoolClass,  | Whether the user is currently suspended or not. | [optional] 
**is_password_reset_requested** | bool,  | BoolClass,  | Whether a password reset has been requested. | [optional] 
**picture** | str,  | str,  | User&#x27;s profile picture URL. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

