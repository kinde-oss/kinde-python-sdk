from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import requests
from dotenv import load_dotenv
from kinde_sdk.management.management_token_manager import ManagementTokenManager
from kinde_sdk.management import ManagementClient
from typing import Dict, Any
import time

import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Kinde Management Token Example with Introspection")

# Security scheme for bearer token
security = HTTPBearer()

# Extract, introspect, and validate management token from header
def get_management_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> ManagementTokenManager:
    logger.debug("Starting token validation")
    bearer_token = credentials.credentials
    logger.debug(f"Received bearer token (first 20 chars): {bearer_token[:20]}...")
    
    # SDK config from env
    domain = os.getenv("KINDE_HOST", "https://app.kinde.com")
    logger.debug(f"Raw domain from env: {domain}")
    if domain.startswith(('http://', 'https://')):
        domain = domain.split('://', 1)[1]
    logger.debug(f"Normalized domain: {domain}")
    client_id = os.getenv("KINDE_MANAGEMENT_CLIENT_ID")
    client_secret = os.getenv("KINDE_MANAGEMENT_CLIENT_SECRET")
    logger.debug(f"Client ID: {client_id}")
    # Not logging secret for security
    
    if not all([domain, client_id, client_secret]):
        logger.error("Missing Kinde management credentials")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Missing Kinde management credentials in environment"
        )
    
    try:
        token_manager = ManagementTokenManager(
            domain=domain,
            client_id=client_id,
            client_secret=client_secret
        )
        logger.debug(f"ManagementTokenManager instantiated {bearer_token}")
        
        introspection_result = token_manager.validate_and_set_via_introspection(bearer_token)
        logger.debug(f"Introspection result: {introspection_result}")
        
        access_token = token_manager.get_access_token()
        if not access_token:
            logger.error("No access token after introspection")
            raise ValueError("Invalid management token after introspection")
        logger.debug("Access token obtained successfully")
        
        return token_manager
    
    except ValueError as e:
        logger.error(f"ValueError in token validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.error(f"Exception in token validation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token introspection failed: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )

# Example route using the validated management token
@app.get("/management/users")
async def get_users(token_manager: ManagementTokenManager = Depends(get_management_token)):
    logger.debug("Entering get_users endpoint")
    try:
        # Create ManagementClient with the token manager
        management_client = ManagementClient(
            domain=token_manager.domain,
            client_id=token_manager.client_id,
            client_secret=token_manager.client_secret
        )
        logger.debug("ManagementClient created")
        
        # Fetch users (example API call)
        users_response = management_client.get_users()
        
        # Get the user count from the response
        user_count = len(users_response.users) if users_response.users else 0
        logger.debug(f"Fetched {user_count} users")
        
        return {
            "message": "Users fetched successfully",
            "user_count": user_count,
            "users": users_response.users if users_response.users else []  # In production, filter sensitive data
        }
    except Exception as e:
        logger.error(f"Error in get_users: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch users: {str(e)}"
        ) from e

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 