# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from kinde_sdk.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    OAUTH2_USER_PROFILE = "/oauth2/user_profile"
    OAUTH2_V2_USER_PROFILE = "/oauth2/v2/user_profile"
    API_V1_USERS = "/api/v1/users"
    API_V1_USER = "/api/v1/user"
    API_V1_ORGANIZATION = "/api/v1/organization"
    API_V1_ORGANIZATIONS = "/api/v1/organizations"
    API_V1_ORGANIZATION_USERS = "/api/v1/organization/users"
    API_V1_CONNECTED_APPS_AUTH_URL = "/api/v1/connected_apps/auth_url"
    API_V1_CONNECTED_APPS_TOKEN = "/api/v1/connected_apps/token"
    API_V1_CONNECTED_APPS_REVOKE = "/api/v1/connected_apps/revoke"
    API_V1_FEATURE_FLAGS = "/api/v1/feature_flags"
    API_V1_FEATURE_FLAGS_FEATURE_FLAG_KEY = "/api/v1/feature_flags/{feature_flag_key}"
    API_V1_ORGANIZATIONS_ORG_CODE_FEATURE_FLAGS = "/api/v1/organizations/{org_code}/feature_flags"
    API_V1_ORGANIZATIONS_ORG_CODE_FEATURE_FLAGS_FEATURE_FLAG_KEY = "/api/v1/organizations/{org_code}/feature_flags/{feature_flag_key}"
    API_V1_ENVIRONMENT_FEATURE_FLAGS_ = "/api/v1/environment/feature_flags/"
    API_V1_ENVIRONMENT_FEATURE_FLAGS_FEATURE_FLAG_KEY = "/api/v1/environment/feature_flags/{feature_flag_key}"
