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

class ApiValueError(KindeException):
    """Raised when there is an error with API values."""
    pass

class ApiTypeError(KindeException):
    """Raised when there is a type error with API values."""
    pass