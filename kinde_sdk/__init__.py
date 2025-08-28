"""
Kinde Python SDK
~~~~~~~~~~~~~~~

This is the Kinde Python SDK for interacting with the Kinde API.

The SDK is organized into three main components:
- auth: Authentication and OAuth functionality
- core: Core utilities and framework support
- management: Management API client (separate module)

The SDK now supports both sync and async operations with consistent APIs.
"""

from kinde_sdk.auth.oauth import OAuth
from kinde_sdk.auth.async_oauth import AsyncOAuth
from kinde_sdk.auth.smart_oauth import SmartOAuth, create_oauth_client
from kinde_sdk.auth.token_manager import TokenManager
from kinde_sdk.auth.user_session import UserSession
from kinde_sdk.auth import permissions, claims, portals, feature_flags
from kinde_sdk.auth.async_claims import async_claims
from kinde_sdk.core.storage.storage_factory import StorageFactory
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.core.framework.framework_interface import FrameworkInterface
from kinde_sdk.core.framework.null_framework import NullFramework

__version__ = "2.1.0"

__all__ = [
    "OAuth",
    "AsyncOAuth", 
    "SmartOAuth",
    "create_oauth_client",
    "TokenManager",
    "UserSession",
    "permissions",
    "claims",
    "async_claims",
    "portals",
    "feature_flags",
    "StorageFactory",
    "FrameworkFactory",
    "FrameworkInterface",
    "NullFramework",
]
