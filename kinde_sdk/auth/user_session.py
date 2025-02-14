from .token_manager import TokenManager

class UserSession:
    def __init__(self):
        self.user_sessions = {}  # Store user-specific session data

    def set_user_data(self, user_id, user_info, token_data):
        """ Store user session details and associate tokens. """
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                "user_info": user_info,
                "token_manager": TokenManager(user_id, user_info["client_id"], user_info["client_secret"], user_info["token_url"])
            }
        self.user_sessions[user_id]["user_info"] = user_info
        self.user_sessions[user_id]["token_manager"].set_tokens(
            token_data["access_token"],
            token_data["refresh_token"],
            token_data["expires_in"]
        )

    def get_user_data(self, user_id):
        """ Retrieve stored user session details. """
        return self.user_sessions.get(user_id, {}).get("user_info")

    def is_authenticated(self, user_id):
        """ Check if the user is authenticated. """
        token_manager = self.user_sessions.get(user_id, {}).get("token_manager")
        return bool(token_manager and token_manager.get_access_token())

    def logout(self, user_id):
        """ Clear user session and tokens. """
        if user_id in self.user_sessions:
            self.user_sessions[user_id]["token_manager"].revoke_token()
            del self.user_sessions[user_id]
