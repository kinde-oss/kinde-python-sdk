from .framework.flask_framework import FlaskFramework
from kinde_sdk.core.framework.framework_factory import FrameworkFactory
from kinde_sdk.core.storage.storage_factory import StorageFactory
from .storage.flask_storage_factory import FlaskStorageFactory

# Register the Flask framework
FrameworkFactory.register_framework("flask", FlaskFramework)
StorageFactory.register_framework_factory("flask", FlaskStorageFactory) 

__all__ = ['FlaskFramework'] 