from kinde_sdk.paths.api_v1_user.get import ApiForget
from kinde_sdk.paths.api_v1_user.post import ApiForpost
from kinde_sdk.paths.api_v1_user.delete import ApiFordelete
from kinde_sdk.paths.api_v1_user.patch import ApiForpatch


class ApiV1User(
    ApiForget,
    ApiForpost,
    ApiFordelete,
    ApiForpatch,
):
    pass
