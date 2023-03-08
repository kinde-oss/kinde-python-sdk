from kinde_sdk.paths.api_v1_organization_users.get import ApiForget
from kinde_sdk.paths.api_v1_organization_users.post import ApiForpost
from kinde_sdk.paths.api_v1_organization_users.patch import ApiForpatch


class ApiV1OrganizationUsers(
    ApiForget,
    ApiForpost,
    ApiForpatch,
):
    pass
