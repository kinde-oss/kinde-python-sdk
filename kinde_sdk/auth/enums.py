from enum import Enum

class GrantType(Enum):
    """OAuth grant types."""
    CLIENT_CREDENTIALS = "client_credentials"
    AUTHORIZATION_CODE = "authorization_code"
    AUTHORIZATION_CODE_WITH_PKCE = "authorization_code_with_pkce"

class IssuerRouteTypes(Enum):
    """Types of authentication routes."""
    LOGIN = "login"
    REGISTER = "register"

class PromptTypes(Enum):
    """Authentication prompt types."""
    CREATE = "create"
    LOGIN = "login"
    CONSENT = "consent"
    SELECT_ACCOUNT = "select_account"
    NONE = "none"