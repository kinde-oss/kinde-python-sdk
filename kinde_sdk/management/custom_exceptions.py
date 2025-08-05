"""
Custom Kinde-specific exceptions for the management SDK.

This module contains exceptions that are specific to Kinde's SDK functionality
and are not part of the OpenAPI-generated code. These exceptions will not be
overwritten during the generation process.
"""


class KindeException(Exception):
    """Base exception for all Kinde SDK exceptions."""
    pass


class KindeConfigurationException(KindeException):
    """Raised when there is a configuration error."""
    pass


class KindeLoginException(KindeException):
    """Raised when there is an error during the login process."""
    pass


class KindeTokenException(KindeException):
    """Raised when there is an error with token operations."""
    pass


class KindeRetrieveException(KindeException):
    """Raised when there is an error retrieving data."""
    pass 