import secrets
import hashlib
import base64
import logging
import requests
from typing import Dict, Union, Any, Optional

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