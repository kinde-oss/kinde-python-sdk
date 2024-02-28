import typing_extensions

from kinde_sdk.paths import PathValues
from kinde_sdk.apis.paths.oauth2_user_profile import Oauth2UserProfile
from kinde_sdk.apis.paths.oauth2_introspect import Oauth2Introspect
from kinde_sdk.apis.paths.oauth2_revoke import Oauth2Revoke
from kinde_sdk.apis.paths.oauth2_v2_user_profile import Oauth2V2UserProfile
from kinde_sdk.apis.paths.api_v1_apis import ApiV1Apis
from kinde_sdk.apis.paths.api_v1_apis_api_id import ApiV1ApisApiId
from kinde_sdk.apis.paths.api_v1_apis_api_id_applications import ApiV1ApisApiIdApplications
from kinde_sdk.apis.paths.api_v1_applications import ApiV1Applications
from kinde_sdk.apis.paths.api_v1_applications_application_id import ApiV1ApplicationsApplicationId
from kinde_sdk.apis.paths.api_v1_business import ApiV1Business
from kinde_sdk.apis.paths.api_v1_industries import ApiV1Industries
from kinde_sdk.apis.paths.api_v1_timezones import ApiV1Timezones
from kinde_sdk.apis.paths.api_v1_applications_app_id_auth_redirect_urls import ApiV1ApplicationsAppIdAuthRedirectUrls
from kinde_sdk.apis.paths.api_v1_applications_app_id_auth_logout_urls import ApiV1ApplicationsAppIdAuthLogoutUrls
from kinde_sdk.apis.paths.api_v1_connected_apps_auth_url import ApiV1ConnectedAppsAuthUrl
from kinde_sdk.apis.paths.api_v1_connected_apps_token import ApiV1ConnectedAppsToken
from kinde_sdk.apis.paths.api_v1_connected_apps_revoke import ApiV1ConnectedAppsRevoke
from kinde_sdk.apis.paths.api_v1_environment_feature_flags import ApiV1EnvironmentFeatureFlags
from kinde_sdk.apis.paths.api_v1_environment_feature_flags_feature_flag_key import ApiV1EnvironmentFeatureFlagsFeatureFlagKey
from kinde_sdk.apis.paths.api_v1_feature_flags import ApiV1FeatureFlags
from kinde_sdk.apis.paths.api_v1_feature_flags_feature_flag_key import ApiV1FeatureFlagsFeatureFlagKey
from kinde_sdk.apis.paths.api_v1_organization import ApiV1Organization
from kinde_sdk.apis.paths.api_v1_organization_org_code import ApiV1OrganizationOrgCode
from kinde_sdk.apis.paths.api_v1_organizations import ApiV1Organizations
from kinde_sdk.apis.paths.api_v1_organizations_org_code_users import ApiV1OrganizationsOrgCodeUsers
from kinde_sdk.apis.paths.api_v1_organizations_org_code_users_user_id_roles import ApiV1OrganizationsOrgCodeUsersUserIdRoles
from kinde_sdk.apis.paths.api_v1_organizations_org_code_users_user_id_roles_role_id import ApiV1OrganizationsOrgCodeUsersUserIdRolesRoleId
from kinde_sdk.apis.paths.api_v1_organizations_org_code_users_user_id_permissions import ApiV1OrganizationsOrgCodeUsersUserIdPermissions
from kinde_sdk.apis.paths.api_v1_organizations_org_code_users_user_id_permissions_permission_id import ApiV1OrganizationsOrgCodeUsersUserIdPermissionsPermissionId
from kinde_sdk.apis.paths.api_v1_organizations_org_code_users_user_id import ApiV1OrganizationsOrgCodeUsersUserId
from kinde_sdk.apis.paths.api_v1_organizations_org_code_feature_flags import ApiV1OrganizationsOrgCodeFeatureFlags
from kinde_sdk.apis.paths.api_v1_organizations_org_code_feature_flags_feature_flag_key import ApiV1OrganizationsOrgCodeFeatureFlagsFeatureFlagKey
from kinde_sdk.apis.paths.api_v1_permissions import ApiV1Permissions
from kinde_sdk.apis.paths.api_v1_permissions_permission_id import ApiV1PermissionsPermissionId
from kinde_sdk.apis.paths.api_v1_roles import ApiV1Roles
from kinde_sdk.apis.paths.api_v1_roles_role_id_permissions import ApiV1RolesRoleIdPermissions
from kinde_sdk.apis.paths.api_v1_roles_role_id_permissions_permission_id import ApiV1RolesRoleIdPermissionsPermissionId
from kinde_sdk.apis.paths.api_v1_roles_role_id import ApiV1RolesRoleId
from kinde_sdk.apis.paths.api_v1_subscribers import ApiV1Subscribers
from kinde_sdk.apis.paths.api_v1_subscribers_subscriber_id import ApiV1SubscribersSubscriberId
from kinde_sdk.apis.paths.api_v1_users import ApiV1Users
from kinde_sdk.apis.paths.api_v1_users_user_id_refresh_claims import ApiV1UsersUserIdRefreshClaims
from kinde_sdk.apis.paths.api_v1_user import ApiV1User
from kinde_sdk.apis.paths.api_v1_users_user_id_feature_flags_feature_flag_key import ApiV1UsersUserIdFeatureFlagsFeatureFlagKey

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.OAUTH2_USER_PROFILE: Oauth2UserProfile,
        PathValues.OAUTH2_INTROSPECT: Oauth2Introspect,
        PathValues.OAUTH2_REVOKE: Oauth2Revoke,
        PathValues.OAUTH2_V2_USER_PROFILE: Oauth2V2UserProfile,
        PathValues.API_V1_APIS: ApiV1Apis,
        PathValues.API_V1_APIS_API_ID: ApiV1ApisApiId,
        PathValues.API_V1_APIS_API_ID_APPLICATIONS: ApiV1ApisApiIdApplications,
        PathValues.API_V1_APPLICATIONS: ApiV1Applications,
        PathValues.API_V1_APPLICATIONS_APPLICATION_ID: ApiV1ApplicationsApplicationId,
        PathValues.API_V1_BUSINESS: ApiV1Business,
        PathValues.API_V1_INDUSTRIES: ApiV1Industries,
        PathValues.API_V1_TIMEZONES: ApiV1Timezones,
        PathValues.API_V1_APPLICATIONS_APP_ID_AUTH_REDIRECT_URLS: ApiV1ApplicationsAppIdAuthRedirectUrls,
        PathValues.API_V1_APPLICATIONS_APP_ID_AUTH_LOGOUT_URLS: ApiV1ApplicationsAppIdAuthLogoutUrls,
        PathValues.API_V1_CONNECTED_APPS_AUTH_URL: ApiV1ConnectedAppsAuthUrl,
        PathValues.API_V1_CONNECTED_APPS_TOKEN: ApiV1ConnectedAppsToken,
        PathValues.API_V1_CONNECTED_APPS_REVOKE: ApiV1ConnectedAppsRevoke,
        PathValues.API_V1_ENVIRONMENT_FEATURE_FLAGS: ApiV1EnvironmentFeatureFlags,
        PathValues.API_V1_ENVIRONMENT_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1EnvironmentFeatureFlagsFeatureFlagKey,
        PathValues.API_V1_FEATURE_FLAGS: ApiV1FeatureFlags,
        PathValues.API_V1_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1FeatureFlagsFeatureFlagKey,
        PathValues.API_V1_ORGANIZATION: ApiV1Organization,
        PathValues.API_V1_ORGANIZATION_ORG_CODE: ApiV1OrganizationOrgCode,
        PathValues.API_V1_ORGANIZATIONS: ApiV1Organizations,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS: ApiV1OrganizationsOrgCodeUsers,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS_USER_ID_ROLES: ApiV1OrganizationsOrgCodeUsersUserIdRoles,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS_USER_ID_ROLES_ROLE_ID: ApiV1OrganizationsOrgCodeUsersUserIdRolesRoleId,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS_USER_ID_PERMISSIONS: ApiV1OrganizationsOrgCodeUsersUserIdPermissions,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS_USER_ID_PERMISSIONS_PERMISSION_ID: ApiV1OrganizationsOrgCodeUsersUserIdPermissionsPermissionId,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS_USER_ID: ApiV1OrganizationsOrgCodeUsersUserId,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_FEATURE_FLAGS: ApiV1OrganizationsOrgCodeFeatureFlags,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1OrganizationsOrgCodeFeatureFlagsFeatureFlagKey,
        PathValues.API_V1_PERMISSIONS: ApiV1Permissions,
        PathValues.API_V1_PERMISSIONS_PERMISSION_ID: ApiV1PermissionsPermissionId,
        PathValues.API_V1_ROLES: ApiV1Roles,
        PathValues.API_V1_ROLES_ROLE_ID_PERMISSIONS: ApiV1RolesRoleIdPermissions,
        PathValues.API_V1_ROLES_ROLE_ID_PERMISSIONS_PERMISSION_ID: ApiV1RolesRoleIdPermissionsPermissionId,
        PathValues.API_V1_ROLES_ROLE_ID: ApiV1RolesRoleId,
        PathValues.API_V1_SUBSCRIBERS: ApiV1Subscribers,
        PathValues.API_V1_SUBSCRIBERS_SUBSCRIBER_ID: ApiV1SubscribersSubscriberId,
        PathValues.API_V1_USERS: ApiV1Users,
        PathValues.API_V1_USERS_USER_ID_REFRESH_CLAIMS: ApiV1UsersUserIdRefreshClaims,
        PathValues.API_V1_USER: ApiV1User,
        PathValues.API_V1_USERS_USER_ID_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1UsersUserIdFeatureFlagsFeatureFlagKey,
    }
)

path_to_api = PathToApi(
    {
        PathValues.OAUTH2_USER_PROFILE: Oauth2UserProfile,
        PathValues.OAUTH2_INTROSPECT: Oauth2Introspect,
        PathValues.OAUTH2_REVOKE: Oauth2Revoke,
        PathValues.OAUTH2_V2_USER_PROFILE: Oauth2V2UserProfile,
        PathValues.API_V1_APIS: ApiV1Apis,
        PathValues.API_V1_APIS_API_ID: ApiV1ApisApiId,
        PathValues.API_V1_APIS_API_ID_APPLICATIONS: ApiV1ApisApiIdApplications,
        PathValues.API_V1_APPLICATIONS: ApiV1Applications,
        PathValues.API_V1_APPLICATIONS_APPLICATION_ID: ApiV1ApplicationsApplicationId,
        PathValues.API_V1_BUSINESS: ApiV1Business,
        PathValues.API_V1_INDUSTRIES: ApiV1Industries,
        PathValues.API_V1_TIMEZONES: ApiV1Timezones,
        PathValues.API_V1_APPLICATIONS_APP_ID_AUTH_REDIRECT_URLS: ApiV1ApplicationsAppIdAuthRedirectUrls,
        PathValues.API_V1_APPLICATIONS_APP_ID_AUTH_LOGOUT_URLS: ApiV1ApplicationsAppIdAuthLogoutUrls,
        PathValues.API_V1_CONNECTED_APPS_AUTH_URL: ApiV1ConnectedAppsAuthUrl,
        PathValues.API_V1_CONNECTED_APPS_TOKEN: ApiV1ConnectedAppsToken,
        PathValues.API_V1_CONNECTED_APPS_REVOKE: ApiV1ConnectedAppsRevoke,
        PathValues.API_V1_ENVIRONMENT_FEATURE_FLAGS: ApiV1EnvironmentFeatureFlags,
        PathValues.API_V1_ENVIRONMENT_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1EnvironmentFeatureFlagsFeatureFlagKey,
        PathValues.API_V1_FEATURE_FLAGS: ApiV1FeatureFlags,
        PathValues.API_V1_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1FeatureFlagsFeatureFlagKey,
        PathValues.API_V1_ORGANIZATION: ApiV1Organization,
        PathValues.API_V1_ORGANIZATION_ORG_CODE: ApiV1OrganizationOrgCode,
        PathValues.API_V1_ORGANIZATIONS: ApiV1Organizations,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS: ApiV1OrganizationsOrgCodeUsers,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS_USER_ID_ROLES: ApiV1OrganizationsOrgCodeUsersUserIdRoles,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS_USER_ID_ROLES_ROLE_ID: ApiV1OrganizationsOrgCodeUsersUserIdRolesRoleId,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS_USER_ID_PERMISSIONS: ApiV1OrganizationsOrgCodeUsersUserIdPermissions,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS_USER_ID_PERMISSIONS_PERMISSION_ID: ApiV1OrganizationsOrgCodeUsersUserIdPermissionsPermissionId,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_USERS_USER_ID: ApiV1OrganizationsOrgCodeUsersUserId,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_FEATURE_FLAGS: ApiV1OrganizationsOrgCodeFeatureFlags,
        PathValues.API_V1_ORGANIZATIONS_ORG_CODE_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1OrganizationsOrgCodeFeatureFlagsFeatureFlagKey,
        PathValues.API_V1_PERMISSIONS: ApiV1Permissions,
        PathValues.API_V1_PERMISSIONS_PERMISSION_ID: ApiV1PermissionsPermissionId,
        PathValues.API_V1_ROLES: ApiV1Roles,
        PathValues.API_V1_ROLES_ROLE_ID_PERMISSIONS: ApiV1RolesRoleIdPermissions,
        PathValues.API_V1_ROLES_ROLE_ID_PERMISSIONS_PERMISSION_ID: ApiV1RolesRoleIdPermissionsPermissionId,
        PathValues.API_V1_ROLES_ROLE_ID: ApiV1RolesRoleId,
        PathValues.API_V1_SUBSCRIBERS: ApiV1Subscribers,
        PathValues.API_V1_SUBSCRIBERS_SUBSCRIBER_ID: ApiV1SubscribersSubscriberId,
        PathValues.API_V1_USERS: ApiV1Users,
        PathValues.API_V1_USERS_USER_ID_REFRESH_CLAIMS: ApiV1UsersUserIdRefreshClaims,
        PathValues.API_V1_USER: ApiV1User,
        PathValues.API_V1_USERS_USER_ID_FEATURE_FLAGS_FEATURE_FLAG_KEY: ApiV1UsersUserIdFeatureFlagsFeatureFlagKey,
    }
)
