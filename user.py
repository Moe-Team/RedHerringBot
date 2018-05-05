class User:

    def __init__(self, username):
        self.username = username


class UserHandler:

    def __init__(self):
        self.users = {}
    
    def add_user(self, username):
        self.users[username] = User(username)
    
    def get_user(self, username):
        return self.users.get(username)


user_handler = UserHandler()
