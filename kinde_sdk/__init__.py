"""
Kinde Python SDK
~~~~~~~~~~~~~~~

This is the Kinde Python SDK for interacting with the Kinde API.
"""

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.core.storage.storage_factory import StorageFactory
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.core.framework.framework_interface import FrameworkInterface
from kinde_sdk.core.framework.null_framework import NullFramework

__version__ = "2.1.0"

__all__ = [
    "OAuth",
    "TokenManager",
    "UserSession",
    "permissions",
    "claims",
    "profiles",
    "feature_flags"
    "StorageFactory",
    "FrameworkFactory",
    "FrameworkInterface",
    "NullFramework",
]
