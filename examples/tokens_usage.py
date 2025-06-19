"""
Example demonstrating how to use the new tokens wrapper
to access the token manager directly.
"""

from kinde_sdk.auth import tokens

async def example_token_access():
    """
    Example showing how to access token manager functionality
    through the new tokens wrapper.
    """
    
    # Check if user is authenticated
    if tokens.is_authenticated():
        print("User is authenticated")
        
        # Get user ID
        user_id = tokens.get_user_id()
        print(f"User ID: {user_id}")
        
        # Get token manager for direct access
        token_manager = tokens.get_token_manager()
        if token_manager:
            # Access raw claims
            claims = token_manager.get_claims()
            print(f"User claims: {claims}")
            
            # Access specific tokens
            access_token = token_manager.tokens.get("access_token")
            id_token = token_manager.tokens.get("id_token")
            refresh_token = token_manager.tokens.get("refresh_token")
            
            print(f"Has access token: {access_token is not None}")
            print(f"Has ID token: {id_token is not None}")
            print(f"Has refresh token: {refresh_token is not None}")
        
        # Get token information summary
        token_info = tokens.get_token_info()
        print(f"Token info: {token_info}")
        
    else:
        print("User is not authenticated")

def example_sync_token_access():
    """
    Example showing synchronous access to token information.
    """
    
    # Get token information (this method is synchronous)
    token_info = tokens.get_token_info()
    
    if token_info["isAuthenticated"]:
        print(f"Authenticated user: {token_info['userId']}")
        print(f"Token status:")
        print(f"  - Access token: {'Yes' if token_info['hasAccessToken'] else 'No'}")
        print(f"  - ID token: {'Yes' if token_info['hasIdToken'] else 'No'}")
        print(f"  - Refresh token: {'Yes' if token_info['hasRefreshToken'] else 'No'}")
    else:
        print("No authenticated user")

if __name__ == "__main__":
    # Run synchronous example
    example_sync_token_access()
    
    # Run async example (would need to be in async context)
    # import asyncio
    # asyncio.run(example_token_access()) 