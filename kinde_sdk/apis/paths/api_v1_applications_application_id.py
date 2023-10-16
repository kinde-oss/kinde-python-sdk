from kinde_sdk.paths.api_v1_applications_application_id.get import ApiForget
from kinde_sdk.paths.api_v1_applications_application_id.delete import ApiFordelete
from kinde_sdk.paths.api_v1_applications_application_id.patch import ApiForpatch


class ApiV1ApplicationsApplicationId(
    ApiForget,
    ApiFordelete,
    ApiForpatch,
):
    pass
