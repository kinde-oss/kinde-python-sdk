class KindeException(Exception):
    """Base exception for all Kinde SDK exceptions."""
    pass

class KindeConfigurationException(KindeException):
    """Raised when there is a configuration error."""
    pass

class KindeLoginException(KindeException):
    """Raised when there is an error during the login process."""
    pass

class KindeCallbackError(KindeLoginException):
    """
    Raised when Kinde returns an OAuth error to the callback URL.

    Only raised after the ``state`` parameter has been validated. The user's
    existing session and tokens are left untouched.

    Attributes:
        error: The OAuth error code (e.g. ``"unmet_authentication_requirements"``).
        error_description: The ``error_description`` from the callback, or ``""``.
        state: The validated ``state`` from the callback.
        acr_values: The ``acr_values`` of the step-up request this answers, if known.
        max_age: The ``max_age`` of the step-up request this answers, if known.
    """

    error = None

    def __init__(self, error_description=None, state=None, error=None, acr_values=None, max_age=None):
        if error is not None:
            self.error = error
        self.error_description = error_description or ""
        self.state = state
        self.acr_values = acr_values
        self.max_age = max_age
        super().__init__(self.error_description or self.error or "Authorization failed")

class UnmetAuthenticationRequirementsError(KindeCallbackError):
    """
    Raised when the user cannot meet the requested authentication context
    (for example no enrolled MFA factor, or no passkey).

    This is a final answer: the same request gives the same error. Don't retry
    and don't redirect to login. Tell the user why instead.
    """

    error = "unmet_authentication_requirements"

class LoginRequiredError(KindeCallbackError):
    """
    Raised when a ``prompt=none`` request cannot complete without an
    interactive login. The app decides whether to start one.
    """

    error = "login_required"

# Callback errors that are raised as their own exception type.
CALLBACK_ERRORS = {
    UnmetAuthenticationRequirementsError.error: UnmetAuthenticationRequirementsError,
    LoginRequiredError.error: LoginRequiredError,
}

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