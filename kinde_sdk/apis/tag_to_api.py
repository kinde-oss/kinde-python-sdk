import typing_extensions

from kinde_sdk.apis.tags import TagValues
from kinde_sdk.apis.tags.users_api import UsersApi
from kinde_sdk.apis.tags.connected_apps_api import ConnectedAppsApi
from kinde_sdk.apis.tags.environments_api import EnvironmentsApi
from kinde_sdk.apis.tags.feature_flags_api import FeatureFlagsApi
from kinde_sdk.apis.tags.o_auth_api import OAuthApi
from kinde_sdk.apis.tags.organizations_api import OrganizationsApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.USERS: UsersApi,
        TagValues.CONNECTED_APPS: ConnectedAppsApi,
        TagValues.ENVIRONMENTS: EnvironmentsApi,
        TagValues.FEATURE_FLAGS: FeatureFlagsApi,
        TagValues.OAUTH: OAuthApi,
        TagValues.ORGANIZATIONS: OrganizationsApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.USERS: UsersApi,
        TagValues.CONNECTED_APPS: ConnectedAppsApi,
        TagValues.ENVIRONMENTS: EnvironmentsApi,
        TagValues.FEATURE_FLAGS: FeatureFlagsApi,
        TagValues.OAUTH: OAuthApi,
        TagValues.ORGANIZATIONS: OrganizationsApi,
    }
)
