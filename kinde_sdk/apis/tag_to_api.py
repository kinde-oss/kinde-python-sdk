import typing_extensions

from kinde_sdk.apis.tags import TagValues
from kinde_sdk.apis.tags.o_auth_api import OAuthApi
from kinde_sdk.apis.tags.apis_api import APIsApi
from kinde_sdk.apis.tags.applications_api import ApplicationsApi
from kinde_sdk.apis.tags.business_api import BusinessApi
from kinde_sdk.apis.tags.industries_api import IndustriesApi
from kinde_sdk.apis.tags.timezones_api import TimezonesApi
from kinde_sdk.apis.tags.callbacks_api import CallbacksApi
from kinde_sdk.apis.tags.connected_apps_api import ConnectedAppsApi
from kinde_sdk.apis.tags.connections_api import ConnectionsApi
from kinde_sdk.apis.tags.environments_api import EnvironmentsApi
from kinde_sdk.apis.tags.feature_flags_api import FeatureFlagsApi
from kinde_sdk.apis.tags.organizations_api import OrganizationsApi
from kinde_sdk.apis.tags.permissions_api import PermissionsApi
from kinde_sdk.apis.tags.properties_api import PropertiesApi
from kinde_sdk.apis.tags.property_categories_api import PropertyCategoriesApi
from kinde_sdk.apis.tags.roles_api import RolesApi
from kinde_sdk.apis.tags.subscribers_api import SubscribersApi
from kinde_sdk.apis.tags.users_api import UsersApi
from kinde_sdk.apis.tags.webhooks_api import WebhooksApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.OAUTH: OAuthApi,
        TagValues.APIS: APIsApi,
        TagValues.APPLICATIONS: ApplicationsApi,
        TagValues.BUSINESS: BusinessApi,
        TagValues.INDUSTRIES: IndustriesApi,
        TagValues.TIMEZONES: TimezonesApi,
        TagValues.CALLBACKS: CallbacksApi,
        TagValues.CONNECTED_APPS: ConnectedAppsApi,
        TagValues.CONNECTIONS: ConnectionsApi,
        TagValues.ENVIRONMENTS: EnvironmentsApi,
        TagValues.FEATURE_FLAGS: FeatureFlagsApi,
        TagValues.ORGANIZATIONS: OrganizationsApi,
        TagValues.PERMISSIONS: PermissionsApi,
        TagValues.PROPERTIES: PropertiesApi,
        TagValues.PROPERTY_CATEGORIES: PropertyCategoriesApi,
        TagValues.ROLES: RolesApi,
        TagValues.SUBSCRIBERS: SubscribersApi,
        TagValues.USERS: UsersApi,
        TagValues.WEBHOOKS: WebhooksApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.OAUTH: OAuthApi,
        TagValues.APIS: APIsApi,
        TagValues.APPLICATIONS: ApplicationsApi,
        TagValues.BUSINESS: BusinessApi,
        TagValues.INDUSTRIES: IndustriesApi,
        TagValues.TIMEZONES: TimezonesApi,
        TagValues.CALLBACKS: CallbacksApi,
        TagValues.CONNECTED_APPS: ConnectedAppsApi,
        TagValues.CONNECTIONS: ConnectionsApi,
        TagValues.ENVIRONMENTS: EnvironmentsApi,
        TagValues.FEATURE_FLAGS: FeatureFlagsApi,
        TagValues.ORGANIZATIONS: OrganizationsApi,
        TagValues.PERMISSIONS: PermissionsApi,
        TagValues.PROPERTIES: PropertiesApi,
        TagValues.PROPERTY_CATEGORIES: PropertyCategoriesApi,
        TagValues.ROLES: RolesApi,
        TagValues.SUBSCRIBERS: SubscribersApi,
        TagValues.USERS: UsersApi,
        TagValues.WEBHOOKS: WebhooksApi,
    }
)
