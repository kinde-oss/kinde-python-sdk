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

class KindeTokenPersistenceException(KindeTokenException):
    """Raised when tokens were refreshed but could not be saved. The refreshed tokens
    are kept, `access_token` is still valid, and the save is retried on the next call."""
    def __init__(self, message: str, access_token: str = None):
        super().__init__(message)
        self.access_token = access_token

class KindeRetrieveException(KindeException):
    """Raised when there is an error retrieving data."""
    pass 

class ApiValueError(KindeException):
    """Raised when there is an error with API values."""
    pass

class ApiTypeError(KindeException):
    """Raised when there is a type error with API values."""
    pass