class UserSession:
    def __init__(self):
        self.user_data = {}

    def set_user_data(self, user_info):
        """
        Store user session details.
        """
        self.user_data = user_info

    def get_user_data(self):
        """
        Retrieve stored user session details.
        """
        return self.user_data

    def is_authenticated(self):
        """
        Check if the user is authenticated.
        """
        return bool(self.user_data)
