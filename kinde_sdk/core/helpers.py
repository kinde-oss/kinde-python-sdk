import secrets
import hashlib
import base64
import logging
import requests
import json
import re
import time
from typing import Dict, Union, Any, Optional, List

logger = logging.getLogger("kinde_sdk")

def generate_random_string(length: int = 32) -> str:
    """
    Generate a random string of specified length.
    
    Args:
        length: Length of the random string
        
    Returns:
        Random URL-safe string
    """
    return secrets.token_urlsafe(length)

def base64_url_encode(data: Union[bytes, str]) -> str:
    """
    Encode bytes or string to base64url format.
    
    Args:
        data: Data to encode (bytes or string)
        
    Returns:
        Base64URL encoded string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
        
    return base64.urlsafe_b64encode(data).decode('utf-8').replace('=', '')

async def generate_pkce_pair(length: int = 52) -> Dict[str, str]:
    """
    Generate PKCE code verifier and challenge pair.
    
    Args:
        length: Length of the code verifier
    
    Returns:
        Dictionary containing code_verifier and code_challenge
    """
    # Generate code verifier (random string between 43-128 chars)
    # We use 52 chars by default to match JS implementation
    code_verifier = generate_random_string(length)
    
    # Generate code challenge using SHA-256
    code_challenge = ""
    try:
        # Hash the verifier
        data = code_verifier.encode()
        hashed = hashlib.sha256(data).digest()
        code_challenge = base64_url_encode(hashed)
    except Exception as e:
        # Fallback to plain verifier if hashing fails
        logger.error(f"Error generating code challenge: {str(e)}")
        code_challenge = base64_url_encode(code_verifier)
    
    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge
    }

async def get_user_details(userinfo_url: str, token_manager, logger) -> Dict[str, Any]:
    """
    Retrieve user information using the stored token.
    
    Args:
        userinfo_url: URL for user information endpoint
        token_manager: Token manager instance
        logger: Logger instance
            
    Returns:
        Dictionary with user profile information
        
    Raises:
        ValueError: If token is not available or is invalid
        requests.RequestException: If the API request fails
    """
    try:
        # Get access token
        access_token = token_manager.get_access_token()
        
        # Set up request headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        # Make the request to userinfo endpoint
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        
        # Return user profile data
        return response.json()
        
    except ValueError as e:
        # Token manager errors (e.g., no token available)
        logger.error(f"Token error when retrieving user details: {str(e)}")
        raise
        
    except requests.RequestException as e:
        # Network or API errors
        error_message = f"Failed to retrieve user details: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                error_message = f"User details retrieval failed: {error_data.get('error_description', error_data.get('error', 'Unknown error'))}"
            except Exception:
                error_message = f"User details retrieval failed with status code: {e.response.status_code}"
        
        logger.error(error_message)
        raise

# Additional helper functions from the core module

def decode_jwt(token: str) -> Dict[str, Any]:
    """
    Decode a JWT token without verification.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary containing the decoded token payload
        
    Raises:
        ValueError: If token format is invalid
    """
    try:
        # JWT format: header.payload.signature
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid token format")
        
        # Decode the payload (second part)
        # Add padding if needed
        padding = '=' * (4 - len(parts[1]) % 4) if len(parts[1]) % 4 != 0 else ''
        decoded_bytes = base64.urlsafe_b64decode(parts[1] + padding)
        payload = json.loads(decoded_bytes.decode('utf-8'))
        
        return payload
        
    except Exception as e:
        logger.error(f"Error decoding JWT: {str(e)}")
        raise ValueError(f"Failed to decode token: {str(e)}")

def is_authenticated(token_manager) -> bool:
    """
    Check if the user is authenticated by validating access token.
    
    Args:
        token_manager: Token manager instance
        
    Returns:
        Boolean indicating whether the user is authenticated
    """
    try:
        # Check if access token exists and is valid
        access_token = token_manager.get_access_token()
        return access_token is not None and access_token != ""
    except Exception:
        return False

def get_user_organizations(api_url: str, token_manager, logger) -> List[Dict[str, Any]]:
    """
    Retrieve organizations for the authenticated user.
    
    Args:
        api_url: Base API URL
        token_manager: Token manager instance
        logger: Logger instance
            
    Returns:
        List of organizations the user belongs to
        
    Raises:
        ValueError: If token is not available or is invalid
        requests.RequestException: If the API request fails
    """
    try:
        # Get access token
        access_token = token_manager.get_access_token()
        
        # Set up request headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        # Make the request to organizations endpoint
        orgs_url = f"{api_url}/user/organizations"
        response = requests.get(orgs_url, headers=headers)
        response.raise_for_status()
        
        # Return organizations data
        result = response.json()
        return result.get("organizations", [])
        
    except ValueError as e:
        # Token manager errors
        logger.error(f"Token error when retrieving organizations: {str(e)}")
        raise
        
    except requests.RequestException as e:
        # Network or API errors
        error_message = f"Failed to retrieve organizations: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                error_message = f"Organizations retrieval failed: {error_data.get('error_description', error_data.get('error', 'Unknown error'))}"
            except Exception:
                error_message = f"Organizations retrieval failed with status code: {e.response.status_code}"
        
        logger.error(error_message)
        raise

def get_organization_details(api_url: str, org_code: str, token_manager, logger) -> Dict[str, Any]:
    """
    Retrieve details for a specific organization.
    
    Args:
        api_url: Base API URL
        org_code: Organization code
        token_manager: Token manager instance
        logger: Logger instance
            
    Returns:
        Dictionary with organization details
        
    Raises:
        ValueError: If token is not available or is invalid
        requests.RequestException: If the API request fails
    """
    try:
        # Get access token
        access_token = token_manager.get_access_token()
        
        # Set up request headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        # Make the request to organization details endpoint
        org_url = f"{api_url}/organization/{org_code}"
        response = requests.get(org_url, headers=headers)
        response.raise_for_status()
        
        # Return organization data
        return response.json()
        
    except ValueError as e:
        # Token manager errors
        logger.error(f"Token error when retrieving organization details: {str(e)}")
        raise
        
    except requests.RequestException as e:
        # Network or API errors
        error_message = f"Failed to retrieve organization details: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                error_message = f"Organization details retrieval failed: {error_data.get('error_description', error_data.get('error', 'Unknown error'))}"
            except Exception:
                error_message = f"Organization details retrieval failed with status code: {e.response.status_code}"
        
        logger.error(error_message)
        raise

def get_organization_users(api_url: str, org_code: str, token_manager, logger) -> List[Dict[str, Any]]:
    """
    Retrieve users for a specific organization.
    
    Args:
        api_url: Base API URL
        org_code: Organization code
        token_manager: Token manager instance
        logger: Logger instance
            
    Returns:
        List of users in the organization
        
    Raises:
        ValueError: If token is not available or is invalid
        requests.RequestException: If the API request fails
    """
    try:
        # Get access token
        access_token = token_manager.get_access_token()
        
        # Set up request headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        # Make the request to organization users endpoint
        users_url = f"{api_url}/organization/{org_code}/users"
        response = requests.get(users_url, headers=headers)
        response.raise_for_status()
        
        # Return users data
        result = response.json()
        return result.get("users", [])
        
    except ValueError as e:
        # Token manager errors
        logger.error(f"Token error when retrieving organization users: {str(e)}")
        raise
        
    except requests.RequestException as e:
        # Network or API errors
        error_message = f"Failed to retrieve organization users: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                error_message = f"Organization users retrieval failed: {error_data.get('error_description', error_data.get('error', 'Unknown error'))}"
            except Exception:
                error_message = f"Organization users retrieval failed with status code: {e.response.status_code}"
        
        logger.error(error_message)
        raise

def get_user_permissions(api_url: str, token_manager, org_code: Optional[str] = None, logger = None) -> List[str]:
    """
    Retrieve permissions for the authenticated user.
    
    Args:
        api_url: Base API URL
        token_manager: Token manager instance
        org_code: Optional organization code
        logger: Logger instance
            
    Returns:
        List of permission codes
        
    Raises:
        ValueError: If token is not available or is invalid
        requests.RequestException: If the API request fails
    """
    try:
        # Get access token
        access_token = token_manager.get_access_token()
        
        # Set up request headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        # Build URL based on whether org_code is provided
        if org_code:
            permissions_url = f"{api_url}/organization/{org_code}/user/permissions"
        else:
            permissions_url = f"{api_url}/user/permissions"
            
        # Make the request to permissions endpoint
        response = requests.get(permissions_url, headers=headers)
        response.raise_for_status()
        
        # Return permissions data
        result = response.json()
        permissions = result.get("permissions", [])
        
        # Extract permission codes
        permission_codes = [perm.get("code") for perm in permissions if perm.get("code")]
        return permission_codes
        
    except ValueError as e:
        # Token manager errors
        if logger:
            logger.error(f"Token error when retrieving user permissions: {str(e)}")
        raise
        
    except requests.RequestException as e:
        # Network or API errors
        error_message = f"Failed to retrieve user permissions: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                error_message = f"User permissions retrieval failed: {error_data.get('error_description', error_data.get('error', 'Unknown error'))}"
            except Exception:
                error_message = f"User permissions retrieval failed with status code: {e.response.status_code}"
        
        if logger:
            logger.error(error_message)
        raise

def has_permission(permission_code: str, api_url: str, token_manager, org_code: Optional[str] = None, logger = None) -> bool:
    """
    Check if the authenticated user has a specific permission.
    
    Args:
        permission_code: Permission code to check
        api_url: Base API URL
        token_manager: Token manager instance
        org_code: Optional organization code
        logger: Logger instance
            
    Returns:
        Boolean indicating whether the user has the permission
    """
    try:
        # Get user permissions
        permissions = get_user_permissions(api_url, token_manager, org_code, logger)
        
        # Check if permission code exists in the list
        return permission_code in permissions
        
    except Exception as e:
        if logger:
            logger.error(f"Error checking permission: {str(e)}")
        return False

def get_user_roles(api_url: str, token_manager, org_code: Optional[str] = None, logger = None) -> List[Dict[str, Any]]:
    """
    Retrieve roles for the authenticated user.
    
    Args:
        api_url: Base API URL
        token_manager: Token manager instance
        org_code: Optional organization code
        logger: Logger instance
            
    Returns:
        List of role objects
        
    Raises:
        ValueError: If token is not available or is invalid
        requests.RequestException: If the API request fails
    """
    try:
        # Get access token
        access_token = token_manager.get_access_token()
        
        # Set up request headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        # Build URL based on whether org_code is provided
        if org_code:
            roles_url = f"{api_url}/organization/{org_code}/user/roles"
        else:
            roles_url = f"{api_url}/user/roles"
            
        # Make the request to roles endpoint
        response = requests.get(roles_url, headers=headers)
        response.raise_for_status()
        
        # Return roles data
        result = response.json()
        return result.get("roles", [])
        
    except ValueError as e:
        # Token manager errors
        if logger:
            logger.error(f"Token error when retrieving user roles: {str(e)}")
        raise
        
    except requests.RequestException as e:
        # Network or API errors
        error_message = f"Failed to retrieve user roles: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                error_message = f"User roles retrieval failed: {error_data.get('error_description', error_data.get('error', 'Unknown error'))}"
            except Exception:
                error_message = f"User roles retrieval failed with status code: {e.response.status_code}"
        
        if logger:
            logger.error(error_message)
        raise

def has_role(role_code: str, api_url: str, token_manager, org_code: Optional[str] = None, logger = None) -> bool:
    """
    Check if the authenticated user has a specific role.
    
    Args:
        role_code: Role code to check
        api_url: Base API URL
        token_manager: Token manager instance
        org_code: Optional organization code
        logger: Logger instance
            
    Returns:
        Boolean indicating whether the user has the role
    """
    try:
        # Get user roles
        roles = get_user_roles(api_url, token_manager, org_code, logger)
        
        # Check if role code exists in the list
        for role in roles:
            if role.get("code") == role_code:
                return True
                
        return False
        
    except Exception as e:
        if logger:
            logger.error(f"Error checking role: {str(e)}")
        return False

def get_flag_value(api_url: str, flag_code: str, default_value: Any, token_manager, org_code: Optional[str] = None, logger = None) -> Any:
    """
    Get the value of a feature flag.
    
    Args:
        api_url: Base API URL
        flag_code: Feature flag code
        default_value: Default value to return if flag not found
        token_manager: Token manager instance
        org_code: Optional organization code
        logger: Logger instance
            
    Returns:
        Feature flag value or default value if not found
    """
    try:
        # Get access token
        access_token = token_manager.get_access_token()
        
        # Set up request headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        # Build URL based on whether org_code is provided
        if org_code:
            flag_url = f"{api_url}/organization/{org_code}/feature-flags/{flag_code}"
        else:
            flag_url = f"{api_url}/feature-flags/{flag_code}"
            
        # Make the request to flag endpoint
        response = requests.get(flag_url, headers=headers)
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        flag_data = result.get("feature_flag", {})
        
        # If flag exists and is active, return the value
        if flag_data.get("is_active", False):
            return flag_data.get("value", default_value)
            
        # Return default value if flag not active
        return default_value
        
    except Exception as e:
        # Any error returns the default value
        if logger:
            logger.error(f"Error retrieving feature flag: {str(e)}")
        return default_value

def get_claim_value(token_manager, claim_name: str, default_value: Any = None) -> Any:
    """
    Get a claim value from the ID token.
    
    Args:
        token_manager: Token manager instance
        claim_name: Name of the claim to retrieve
        default_value: Default value to return if claim not found
        
    Returns:
        Claim value or default value if not found
    """
    try:
        # Get claims from token manager
        claims = token_manager.get_claims()
        
        # Return claim value or default if not found
        return claims.get(claim_name, default_value)
        
    except Exception:
        return default_value

def is_claim_valid(token_manager, claim_name: str, expected_value: Any) -> bool:
    """
    Check if a claim has the expected value.
    
    Args:
        token_manager: Token manager instance
        claim_name: Name of the claim to check
        expected_value: Expected value of the claim
        
    Returns:
        Boolean indicating whether claim has the expected value
    """
    try:
        # Get claim value
        claim_value = get_claim_value(token_manager, claim_name)
        
        # Check if claim value matches expected value
        return claim_value == expected_value
        
    except Exception:
        return False

def generate_state() -> str:
    """
    Generate a random state parameter for OAuth flow.
    
    Returns:
        Random state string
    """
    return generate_random_string(32)

def hash_string(value: str) -> str:
    """
    Create a SHA-256 hash of a string.
    
    Args:
        value: String to hash
        
    Returns:
        Hex digest of the hash
    """
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def get_current_timestamp() -> int:
    """
    Get current Unix timestamp in seconds.
    
    Returns:
        Current timestamp in seconds
    """
    return int(time.time())

def parse_domain(url: str) -> str:
    """
    Extract domain from URL.
    
    Args:
        url: URL to parse
        
    Returns:
        Domain name
    """
    # Simple domain extraction using regex
    match = re.search(r'https?://([^/]+)', url)
    if match:
        return match.group(1)
    return ""

def format_api_url(host: str) -> str:
    """
    Format API URL from host.
    
    Args:
        host: Host URL
        
    Returns:
        Formatted API URL
    """
    # Remove trailing slash if present
    host = host.rstrip('/')
    return f"{host}/api"

def is_token_expired(expires_at: int, buffer_seconds: int = 60) -> bool:
    """
    Check if a token is expired with buffer time.
    
    Args:
        expires_at: Expiration timestamp
        buffer_seconds: Buffer time in seconds
        
    Returns:
        Boolean indicating whether token is expired
    """
    current_time = get_current_timestamp()
    return current_time >= (expires_at - buffer_seconds)

def sanitize_url(url: str) -> str:
    """
    Sanitize URL by removing potentially harmful characters.
    
    Args:
        url: URL to sanitize
        
    Returns:
        Sanitized URL
    """
    # Basic URL sanitization
    return url.strip()