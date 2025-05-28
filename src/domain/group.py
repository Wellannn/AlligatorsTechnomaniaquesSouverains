import uuid


class Group:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.users = []

    def add_user(self, user):
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user):
        if user in self.users:
            self.users.remove(user)

    def get_users(self):
        return self.users

    def __repr__(self):
        user_names = [user.username for user in self.users]
        return f"Group({self.group_id}): {user_names}"