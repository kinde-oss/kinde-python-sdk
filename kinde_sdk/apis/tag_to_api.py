import typing_extensions

from kinde_sdk.apis.tags import TagValues
from kinde_sdk.apis.tags.users_api import UsersApi
from kinde_sdk.apis.tags.business_api import BusinessApi
from kinde_sdk.apis.tags.callbacks_api import CallbacksApi
from kinde_sdk.apis.tags.connected_apps_api import ConnectedAppsApi
from kinde_sdk.apis.tags.environments_api import EnvironmentsApi
from kinde_sdk.apis.tags.feature_flags_api import FeatureFlagsApi
from kinde_sdk.apis.tags.industries_api import IndustriesApi
from kinde_sdk.apis.tags.o_auth_api import OAuthApi
from kinde_sdk.apis.tags.organizations_api import OrganizationsApi
from kinde_sdk.apis.tags.permissions_api import PermissionsApi
from kinde_sdk.apis.tags.roles_api import RolesApi
from kinde_sdk.apis.tags.subscribers_api import SubscribersApi
from kinde_sdk.apis.tags.timezones_api import TimezonesApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.USERS: UsersApi,
        TagValues.BUSINESS: BusinessApi,
        TagValues.CALLBACKS: CallbacksApi,
        TagValues.CONNECTED_APPS: ConnectedAppsApi,
        TagValues.ENVIRONMENTS: EnvironmentsApi,
        TagValues.FEATURE_FLAGS: FeatureFlagsApi,
        TagValues.INDUSTRIES: IndustriesApi,
        TagValues.OAUTH: OAuthApi,
        TagValues.ORGANIZATIONS: OrganizationsApi,
        TagValues.PERMISSIONS: PermissionsApi,
        TagValues.ROLES: RolesApi,
        TagValues.SUBSCRIBERS: SubscribersApi,
        TagValues.TIMEZONES: TimezonesApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.USERS: UsersApi,
        TagValues.BUSINESS: BusinessApi,
        TagValues.CALLBACKS: CallbacksApi,
        TagValues.CONNECTED_APPS: ConnectedAppsApi,
        TagValues.ENVIRONMENTS: EnvironmentsApi,
        TagValues.FEATURE_FLAGS: FeatureFlagsApi,
        TagValues.INDUSTRIES: IndustriesApi,
        TagValues.OAUTH: OAuthApi,
        TagValues.ORGANIZATIONS: OrganizationsApi,
        TagValues.PERMISSIONS: PermissionsApi,
        TagValues.ROLES: RolesApi,
        TagValues.SUBSCRIBERS: SubscribersApi,
        TagValues.TIMEZONES: TimezonesApi,
    }
)
