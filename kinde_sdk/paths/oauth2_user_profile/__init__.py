# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from kinde_sdk.paths.oauth2_user_profile import Api

from kinde_sdk.paths import PathValues

path = PathValues.OAUTH2_USER_PROFILE