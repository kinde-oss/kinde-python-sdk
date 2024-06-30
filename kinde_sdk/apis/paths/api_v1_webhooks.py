from kinde_sdk.paths.api_v1_webhooks.get import ApiForget
from kinde_sdk.paths.api_v1_webhooks.post import ApiForpost
from kinde_sdk.paths.api_v1_webhooks.patch import ApiForpatch


class ApiV1Webhooks(
    ApiForget,
    ApiForpost,
    ApiForpatch,
):
    pass
