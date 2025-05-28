import uuid
from src.domain.user import User


class Group:
    """
    Represents a group of users.
    Each group has a unique identifier and can contain multiple users.
    """
    def __init__(self) -> None:
        """
        Initializes a new group with a unique identifier.
        Returns:
            None
        """
        self.id = str(uuid.uuid4())
        self.users = []

    def add_user(self, user: User) -> None:
        """
        Adds a user to the group.
        Args:
            user (User): The user to add to the group.
        Returns:
            None
        """
        if user not in self.users:
            self.users.append(user)

    def remove_user(self, user: User) -> None:
        """
        Removes a user from the group.
        Args:
            user (User): The user to remove from the group.
        Returns:
            None
        """
        if user in self.users:
            self.users.remove(user)

    def get_users(self) -> list:
        """
        Returns a list of users in the group.
        Returns:
            list: A list of User objects in the group.
        """
        return self.users

    def __repr__(self) -> str:
        """
        Returns a string representation of the group, including its ID and user names.
        Returns:
            str: A string representation of the group.
        """
        user_names = [user.username for user in self.users]
        return f"Group({self.group_id}): {user_names}"