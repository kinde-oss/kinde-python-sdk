import typing_extensions

from kinde_sdk.paths import PathValues
from kinde_sdk.apis.paths.oauth2_user_profile import Oauth2UserProfile
from kinde_sdk.apis.paths.oauth2_v2_user_profile import Oauth2V2UserProfile
from kinde_sdk.apis.paths.api_v1_users import ApiV1Users
from kinde_sdk.apis.paths.api_v1_user import ApiV1User
from kinde_sdk.apis.paths.api_v1_organization import ApiV1Organization
from kinde_sdk.apis.paths.api_v1_organizations import ApiV1Organizations
from kinde_sdk.apis.paths.api_v1_organization_users import ApiV1OrganizationUsers
from kinde_sdk.apis.paths.api_v1_connected_apps_auth_url import ApiV1ConnectedAppsAuthUrl
from kinde_sdk.apis.paths.api_v1_connected_apps_token import ApiV1ConnectedAppsToken
from kinde_sdk.apis.paths.api_v1_connected_apps_revoke import ApiV1ConnectedAppsRevoke
from kinde_sdk.apis.paths.api_v1_feature_flags import ApiV1FeatureFlags
from kinde_sdk.apis.paths.api_v1_feature_flags_feature_flag_key import ApiV1FeatureFlagsFeatureFlagKey
from kinde_sdk.apis.paths.api_v1_organizations_org_code_feature_flags import ApiV1OrganizationsOrgCodeFeatureFlags
from kinde_sdk.apis.paths.api_v1_organizations_org_code_feature_flags_feature_flag_key import ApiV1OrganizationsOrgCodeFeatureFlagsFeatureFlagKey
from kinde_sdk.apis.paths.api_v1_environment_feature_flags_ import ApiV1EnvironmentFeatureFlags
from kinde_sdk.apis.paths.api_v1_environment_feature_flags_feature_flag_key import ApiV1EnvironmentFeatureFlagsFeatureFlagKey

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.OAUTH2_USER_PROFILE: Oauth2UserProfile,
        PathValues.OAUTH2_V2_USER_PROFILE: Oauth2V2UserProfile,
        PathValues.API_V1_USERS: ApiV1Users,
        PathValues.API_V1_USER: ApiV1User,
        PathValues.API_V1_ORGANIZATION: ApiV1Organization,
        PathValues.API_V1_ORGANIZATIONS: ApiV1Organizations,
        PathValues.API_V1_ORGANIZATION_USERS: ApiV1OrganizationUsers,
        PathValues.API_V1_CONNECTED_APPS_AUTH_URL: ApiV1ConnectedAppsAuthUrl,
        PathValues.API_V1_CONNECTED_APPS_TOKEN: ApiV1ConnectedAppsToken,
        PathValues.API_V1_CONNECTED_APPS_REVOKE: ApiV1ConnectedAppsRevoke,
        PathValues.API_V1_FEATURE_FLAGS: ApiV1FeatureFlags,
        PathValues.API_V1_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1FeatureFlagsFeatureFlagKey,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_FEATURE_FLAGS: ApiV1OrganizationsOrgCodeFeatureFlags,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1OrganizationsOrgCodeFeatureFlagsFeatureFlagKey,
        PathValues.API_V1_ENVIRONMENT_FEATURE_FLAGS_: ApiV1EnvironmentFeatureFlags,
        PathValues.API_V1_ENVIRONMENT_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1EnvironmentFeatureFlagsFeatureFlagKey,
    }
)

path_to_api = PathToApi(
    {
        PathValues.OAUTH2_USER_PROFILE: Oauth2UserProfile,
        PathValues.OAUTH2_V2_USER_PROFILE: Oauth2V2UserProfile,
        PathValues.API_V1_USERS: ApiV1Users,
        PathValues.API_V1_USER: ApiV1User,
        PathValues.API_V1_ORGANIZATION: ApiV1Organization,
        PathValues.API_V1_ORGANIZATIONS: ApiV1Organizations,
        PathValues.API_V1_ORGANIZATION_USERS: ApiV1OrganizationUsers,
        PathValues.API_V1_CONNECTED_APPS_AUTH_URL: ApiV1ConnectedAppsAuthUrl,
        PathValues.API_V1_CONNECTED_APPS_TOKEN: ApiV1ConnectedAppsToken,
        PathValues.API_V1_CONNECTED_APPS_REVOKE: ApiV1ConnectedAppsRevoke,
        PathValues.API_V1_FEATURE_FLAGS: ApiV1FeatureFlags,
        PathValues.API_V1_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1FeatureFlagsFeatureFlagKey,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_FEATURE_FLAGS: ApiV1OrganizationsOrgCodeFeatureFlags,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1OrganizationsOrgCodeFeatureFlagsFeatureFlagKey,
        PathValues.API_V1_ENVIRONMENT_FEATURE_FLAGS_: ApiV1EnvironmentFeatureFlags,
        PathValues.API_V1_ENVIRONMENT_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1EnvironmentFeatureFlagsFeatureFlagKey,
    }
)
