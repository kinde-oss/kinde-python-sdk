from .token_manager import TokenManager
import threading
from .storage_interface import StorageInterface

class UserSession:
    def __init__(self, storage: StorageInterface):
        self.user_sessions = {}  # Store user-specific session data
        self.lock = threading.Lock()  # Add a lock for thread safety
        self.storage = storage  # Use the provided storage backend

    def set_user_data(self, user_id, user_info, token_data):
        """Store user session details and associate tokens."""
        with self.lock:  # Acquire the lock
            if user_id not in self.user_sessions:
                self.user_sessions[user_id] = {
                    "user_info": user_info,
                    "token_manager": TokenManager(
                        user_id, user_info["client_id"], user_info["client_secret"], user_info["token_url"]
                    ),
                }
            self.user_sessions[user_id]["user_info"] = user_info
            self.user_sessions[user_id]["token_manager"].set_tokens(
                token_data["access_token"],
                token_data["refresh_token"],
                token_data["expires_in"],
            )
            self.storage.set(user_id, {"user_info": user_info, "token_manager": token_manager})

    def get_user_data(self, user_id):
        """ Retrieve stored user session details. """
        with self.lock:
            # return self.user_sessions.get(user_id, {}).get("user_info")
            session = self.storage.get(user_id)
            return session.get("user_info") if session else None

    def is_authenticated(self, user_id):
        """ Check if the user is authenticated. """
        with self.lock:
            token_manager = self.user_sessions.get(user_id, {}).get("token_manager")
            return bool(token_manager and token_manager.get_access_token())

    def logout(self, user_id):
        """ Clear user session and tokens. """
        with self.lock:
            if user_id in self.user_sessions:
                self.user_sessions[user_id]["token_manager"].revoke_token()
                del self.user_sessions[user_id]

    def cleanup_expired_sessions(self):
        """Remove expired sessions."""
        with self.lock:  # Acquire the lock
            current_time = time.time()
            expired_users = [
                user_id
                for user_id, session in self.user_sessions.items()
                if session["token_manager"].tokens.get("expires_at", 0) < current_time
            ]
            for user_id in expired_users:
                del self.user_sessions[user_id]