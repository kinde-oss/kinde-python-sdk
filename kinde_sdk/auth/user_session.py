from .token_manager import TokenManager
import threading
import time
from typing import Dict, Any, Optional
from kinde_sdk.core.storage.storage_manager import StorageManager

# Revision of a session that was stored before revisions existed
_NO_REVISION = (0, 0.0)


class UserSession:
    def __init__(self):
        self.user_sessions = {}  # Store user-specific session data
        self.lock = threading.Lock()  # Add a lock for thread safety
        self.storage_manager = StorageManager()  # Use the provided storage backend

    def set_user_data(self, user_id: str, user_info: Dict[str, Any], token_data: Dict[str, Any], replace_tokens: bool = False):
        """
        Store user session details and associate tokens.

        Args:
            replace_tokens: If True, the stored access, ID and refresh tokens
                are all replaced by ``token_data`` instead of merged with it.
        """
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

            # Save again whenever the token manager refreshes its tokens
            self._persist_token_changes(user_id)
            
            # Set tokens in token manager
            if replace_tokens:
                self.user_sessions[user_id]["token_manager"].set_tokens(token_data, replace=True)
            else:
                self.user_sessions[user_id]["token_manager"].set_tokens(token_data)
            
            # Save to persistent storage, as a new revision of the session's tokens
            self._save_to_storage(user_id, tokens_changed=True)
    
    def _save_to_storage(self, user_id: str, tokens_changed: bool = False):
        """
        Save session data to storage.

        Args:
            tokens_changed: True when the tokens are new (a callback or a
                refresh), which gives them a revision later than any seen so far.
        """
        session_data = self.user_sessions.get(user_id)
        if session_data:
            token_manager = session_data["token_manager"]
            if tokens_changed:
                token_manager.revision = self._next_revision(user_id, token_manager)

            # We need to serialize the session data
            # Token manager can't be directly serialized
            serialized_data = {
                "user_info": session_data["user_info"],
                "tokens": token_manager.tokens,
            }
            revision = self._as_revision(getattr(token_manager, "revision", None))
            if revision is not None:
                serialized_data["revision"] = list(revision)
            # Store with user: prefix to make it user-specific but device-independent
            # if you want device-specific sessions, remove the "user:" prefix
            self.storage_manager.setItems(user_id, serialized_data)

    def _persist_token_changes(self, user_id: str):
        """Save the session whenever its token manager stores new tokens (e.g. a refresh)."""
        token_manager = self.user_sessions[user_id]["token_manager"]
        token_manager.on_tokens_changed = lambda: self._save_to_storage(user_id, tokens_changed=True)

    @staticmethod
    def _as_revision(value: Any) -> Optional[tuple]:
        """
        Read a revision: ``(counter, saved_at)``, compared in that order.

        The counter orders changes that followed one another, whichever process
        made them and whatever its clock says. The time only settles a tie
        between two processes that changed the tokens at the same moment.
        """
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            return None
        counter, saved_at = value
        if isinstance(counter, bool) or not isinstance(counter, int):
            return None
        if isinstance(saved_at, bool) or not isinstance(saved_at, (int, float)):
            return None
        return (counter, float(saved_at))

    def _stored_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """The stored session for a user, if it holds tokens."""
        session_data = self.storage_manager.get(user_id)
        if not isinstance(session_data, dict):
            return None
        tokens = session_data.get("tokens")
        if not isinstance(tokens, dict) or "access_token" not in tokens:
            return None
        return session_data

    def _stored_revision(self, stored_session: Optional[Dict[str, Any]]) -> tuple:
        if stored_session is None:
            return _NO_REVISION
        return self._as_revision(stored_session.get("revision")) or _NO_REVISION

    def _next_revision(self, user_id: str, token_manager: TokenManager) -> tuple:
        """A revision later than the cached one and the stored one."""
        cached = self._as_revision(getattr(token_manager, "revision", None)) or _NO_REVISION
        stored = self._stored_revision(self._stored_session(user_id))
        return (max(cached[0], stored[0]) + 1, time.time())

    def _sync_with_storage(self, user_id: str):
        """
        Reconcile a session cached in this process with the stored session.

        Both can be out of date. Another process may have stored newer tokens
        (a step-up, a refresh, a later sign-in). And the store may hold older
        ones: session backends write a request's whole session back when it
        ends, and a cookie session is whatever cookie the request carried, so
        a request that began before the tokens changed puts the old ones back.

        The revision saved with the tokens decides. Newer stored tokens are
        adopted. Older stored tokens are never adopted, and are overwritten
        with the current ones. Tokens changed in memory without being saved
        are left alone.
        """
        token_manager = self.user_sessions[user_id]["token_manager"]
        stored_session = self._stored_session(user_id)
        if stored_session is None:
            return

        stored_revision = self._stored_revision(stored_session)
        cached_revision = self._as_revision(getattr(token_manager, "revision", None))
        if cached_revision is None:
            # Nothing to compare with yet: keep the cached tokens
            token_manager.revision = stored_revision
        elif stored_revision > cached_revision:
            with token_manager.lock:
                token_manager.tokens = dict(stored_session["tokens"])
                token_manager.revision = stored_revision
        elif stored_revision < cached_revision:
            self._save_to_storage(user_id)

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
            
        # Set tokens. The token manager is shared by every session object in
        # this process, so it may already hold newer tokens than this stored
        # session, which can be an older copy (see _sync_with_storage).
        stored_revision = self._stored_revision(session_data)
        cached_revision = self._as_revision(getattr(token_manager, "revision", None))
        if cached_revision is None or not token_manager.tokens or stored_revision >= cached_revision:
            token_manager.tokens = tokens
            token_manager.revision = stored_revision
        
        # Store in memory
        self.user_sessions[user_id] = {
            "user_info": user_info,
            "token_manager": token_manager,
        }

        # Save again whenever the token manager refreshes its tokens
        self._persist_token_changes(user_id)
        
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
            else:
                # Another process may have replaced the session's tokens
                self._sync_with_storage(user_id)
                    
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