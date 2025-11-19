from .framework.fastapi_framework import FastAPIFramework
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.core.storage.storage_factory import StorageFactory
from .storage.fastapi_storage_factory import FastAPIStorageFactory

# Register the FastAPI framework
FrameworkFactory.register_framework("fastapi", FastAPIFramework)
StorageFactory.register_framework_factory("fastapi", FastAPIStorageFactory)

__all__ = ['FastAPIFramework'] 