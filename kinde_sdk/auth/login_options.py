class LoginOptions:
    """Login options constants for OAuth authentication."""
    
    # Standard OAuth parameters
    RESPONSE_TYPE = "response_type"
    REDIRECT_URI = "redirect_uri"
    SCOPE = "scope"
    AUDIENCE = "audience"
    STATE = "state"
    NONCE = "nonce"
    CODE_CHALLENGE = "code_challenge"
    CODE_CHALLENGE_METHOD = "code_challenge_method"
    
    # Organization parameters
    ORG_CODE = "org_code"
    ORG_NAME = "org_name"
    IS_CREATE_ORG = "is_create_org"
    
    # User experience parameters
    PROMPT = "prompt"
    LANG = "lang"
    LOGIN_HINT = "login_hint"
    CONNECTION_ID = "connection_id"
    REDIRECT_URL = "redirect_url"
    HAS_SUCCESS_PAGE = "has_success_page"
    WORKFLOW_DEPLOYMENT_ID = "workflow_deployment_id"
    PLAN_INTEREST = "plan_interest"
    
    # Additional parameters container
    AUTH_PARAMS = "auth_params"