from .token_manager import TokenManager
import threading
import time
from typing import Dict, Any, Optional
from kinde_sdk.core.storage.storage_manager import StorageManager

class UserSession:
    def __init__(self):
        self.user_sessions = {}  # Store user-specific session data
        self.lock = threading.Lock()  # Add a lock for thread safety
        self.storage_manager = StorageManager()  # Use the provided storage backend

    def set_user_data(self, user_id: str, user_info: Dict[str, Any], token_data: Dict[str, Any]):
        """Store user session details and associate tokens."""
        with self.lock:  # Acquire the lock
            if user_id not in self.user_sessions:
                # Create new token manager
                token_manager = TokenManager(
                    user_id, 
                    user_info["client_id"], 
                    user_info.get("client_secret"),  # May be None for PKCE flow
                    user_info["token_url"]
                )
                
                # Set redirect URI if available
                if "redirect_uri" in user_info:
                    token_manager.set_redirect_uri(user_info["redirect_uri"])
                
                self.user_sessions[user_id] = {
                    "user_info": user_info,
                    "token_manager": token_manager
                }
            else:
                # Update existing user info
                self.user_sessions[user_id]["user_info"] = user_info
            
            # Set tokens in token manager
            self.user_sessions[user_id]["token_manager"].set_tokens(token_data)
            
            # Save to persistent storage
            self._save_to_storage(user_id)
    
    def _save_to_storage(self, user_id: str):
        """Save session data to storage."""
        session_data = self.user_sessions.get(user_id)
        if session_data:
            # We need to serialize the session data
            # Token manager can't be directly serialized
            serialized_data = {
                "user_info": session_data["user_info"],
                "tokens": session_data["token_manager"].tokens,
            }
            # Store with user: prefix to make it user-specific but device-independent
            # if you want device-specific sessions, remove the "user:" prefix
            self.storage_manager.setItems(user_id, serialized_data)

    def reset(self):
        """Reset all session data - useful for testing"""
        with self.lock:
            self.user_sessions = {}
            # Also reset the TokenManager instances
            from .token_manager import TokenManager
            TokenManager.reset_instances()


    def _load_from_storage(self, user_id: str) -> bool:
        """Load session data from storage if not already in memory."""
        if user_id in self.user_sessions:
            return True
            
        session_data = self.storage_manager.get(user_id)
        if not session_data:
            return False
            
        # Verify we have all the required data
        user_info = session_data.get("user_info", {})
        tokens = session_data.get("tokens", {})
        
        # Ensure we have all essential data
        if (not user_info or not tokens or 
            "client_id" not in user_info or 
            "token_url" not in user_info or
            "access_token" not in tokens):
            return False
            
        
        token_manager = TokenManager(
            user_id,
            user_info.get("client_id"),
            user_info.get("client_secret"),
            user_info.get("token_url")
        )
        
        # Set redirect URI if available
        if "redirect_uri" in user_info:
            token_manager.set_redirect_uri(user_info["redirect_uri"])
            
        # Set tokens
        token_manager.tokens = tokens
        
        # Store in memory
        self.user_sessions[user_id] = {
            "user_info": user_info,
            "token_manager": token_manager
        }
        
        return True

    def get_user_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored user session details."""
        with self.lock:
            # Try to load from storage if not in memory
            if user_id not in self.user_sessions:
                if not self._load_from_storage(user_id):
                    return None
                    
            return self.user_sessions.get(user_id, {}).get("user_info")

    def get_token_manager(self, user_id: str) -> Optional[TokenManager]:
        """Get the token manager for a user."""
        with self.lock:
            # Try to load from storage if not in memory
            if user_id not in self.user_sessions:
                if not self._load_from_storage(user_id):
                    return None
                    
            return self.user_sessions.get(user_id, {}).get("token_manager")


    def is_authenticated(self, user_id: str) -> bool:
        """Check if the user is authenticated with a valid token."""
        token_manager = self.get_token_manager(user_id)
        if not token_manager:
            return False
        
        try:
            # Try to get a valid access token
            # This will handle refreshing if needed
            access_token = token_manager.get_access_token()
            return access_token is not None and len(access_token) > 0
        except ValueError:
            # Token is expired and cannot be refreshed
            return False
        except Exception:
            # Any other error means authentication failed
            return False

    def logout(self, user_id: str) -> None:
        """Clear user session and tokens."""
        with self.lock:
            # Try to load from storage if not in memory
            if user_id not in self.user_sessions:
                if not self._load_from_storage(user_id):
                    return  # No session to clear
            
            # Revoke token if possible
            token_manager = self.user_sessions.get(user_id, {}).get("token_manager")
            if token_manager:
                try:
                    token_manager.revoke_token()
                except Exception:
                    pass  # Best effort
            
            # Delete from memory
            if user_id in self.user_sessions:
                del self.user_sessions[user_id]
                
            # Delete from storage
            self.storage_manager.clear_device_data()

    def cleanup_expired_sessions(self) -> None:
        """Remove expired sessions from memory and storage."""
        with self.lock:
            current_time = time.time()
            expired_users = []
            
            # Check all in-memory sessions
            for user_id, session in self.user_sessions.items():
                token_manager = session.get("token_manager")
                if not token_manager:
                    expired_users.append(user_id)
                    continue
                    
                tokens = token_manager.tokens
                if not tokens or tokens.get("expires_at", 0) < current_time:
                    # If there's a refresh token, we can keep the session
                    if "refresh_token" not in tokens:
                        expired_users.append(user_id)
            
            # Remove expired sessions
            for user_id in expired_users:
                if user_id in self.user_sessions:
                    del self.user_sessions[user_id]
                # self.storage.delete(user_id)
                self.storage_manager.delete(user_id)