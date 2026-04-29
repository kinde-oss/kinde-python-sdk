"""Single source of truth for the Kinde Python SDK version.

This module is intentionally minimal: it must not import anything else,
so it can be safely imported from any sub-package's ``__init__`` without
risking a circular import with ``kinde_sdk/__init__.py``.

The OpenAPI-generated ``kinde_sdk/management/__init__.py`` and
``kinde_sdk/frontend/__init__.py`` re-export this attribute, so all three
namespaces report the same version. The generator scripts
(``generate_management_sdk.py`` and ``generate_frontend_sdk.py``) read
this value to set the OpenAPI Generator's ``packageVersion``.

Bump this string on every release; nothing else needs touching.
"""

__version__ = "2.2.0"
