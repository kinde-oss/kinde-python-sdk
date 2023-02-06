# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from kinde_sdk.api.o_auth_api import OAuthApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from kinde_sdk.api.o_auth_api import OAuthApi
from kinde_sdk.api.users_api import UsersApi
from kinde_sdk.api.users_api import UsersApi
