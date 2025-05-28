from typing import Optional, Dict, Any
from src.domain.group import Group
from src.domain.user import User
from src.domain.vote import Vote
from src.storage.storage_json import StorageJSON


class StorageService:
    """
    Service class that acts as a wrapper over the storage layer (StorageJSON).
    It provides high-level methods for user, vote, and group data management.
    """

    def __init__(self, filename: str = "data.json") -> None:
        """
        Initializes the storage service with the provided JSON file.
        Args:
            filename (str): Path to the JSON file for persistent storage.
        Returns:
            None
        """
        self.storage = StorageJSON(filename)

    def is_user_exist(self, username: str) -> bool:
        """
        Checks whether a user with the given username exists.
        Args:
            username (str): The username to check.
        Returns:
            bool: True if the user exists, False otherwise.
        """
        return self.get_user(username) is not None

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a user's data based on their username.
        Args:
            username (str): The username of the user.
        Returns:
            Optional[Dict[str, Any]]: A dictionary of user data or None if not found.
        """
        return self.storage.get_user_by_username(username)

    def get_all_users(self) -> Dict[str, Any]:
        """
        Retrieves all users from storage.
        Returns:
            Dict[str, Any]: A dictionary of all users with user IDs as keys.
        """
        return self.storage.get_users()

    def create_user(self, user: User) -> None:
        """
        Stores a new user in storage.
        Args:
            user (User): The user object to store.
        """
        self.storage.save_user(user_id=user.id, user_data=user.__dict__)

    def update_user(self, user: User) -> None:
        """
        Updates an existing user in storage.
        Args:
            user (User): The user object with updated data.
        """
        self.create_user(user)

    def delete_user(self, user: User) -> None:
        """
        Deletes a user from storage.
        Args:
            user (User): The user to be deleted.
        """
        self.storage.delete_user(user.id)

    def create_vote(self, vote: Vote) -> None:
        """
        Stores a new vote in storage.
        Args:
            vote (Vote): The vote object to store.
        """
        self.storage.save_vote(vote.id, vote.__dict__)

    def get_vote(self, vote_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a vote from storage by ID.
        Args:
            vote_id (str): The ID of the vote.
        Returns:
            Optional[Dict[str, Any]]: The vote data if found, otherwise None.
        """
        votes = self.storage.get_votes()
        return votes.get(vote_id)

    def get_all_votes(self) -> Dict[str, Any]:
        """
        Retrieves all votes from storage.
        Returns:
            Dict[str, Any]: A dictionary of all vote data.
        """
        return self.storage.get_votes()

    def update_vote(self, vote: Vote) -> None:
        """
        Updates an existing vote in storage.
        Args:
            vote (Vote): The vote object with updated data.
        """
        self.storage.save_vote(vote.id, vote.__dict__)

    def delete_vote(self, vote_id: str) -> None:
        """
        Deletes a vote from storage.
        Args:
            vote_id (str): The ID of the vote to delete.
        Returns:
            None
        """
        self.storage.delete_vote(vote_id)

    def save_generated_group(self, groups: Group) -> None:
        """
        Saves the generated groups for a vote.
        Args:
            groups (Group): The group object containing the generated group data.
        """
        self.storage.save_group(groups.id, groups.__dict__)

    def get_group_by_id(self, group: Group) -> Optional[Dict[str, Any]]:
        """
        Retrieves group data associated with a vote.
        Args:
            group (Group): The group object whose ID is used for lookup.
        Returns:
            Optional[Dict[str, Any]]: The group data if found, otherwise None.
        """
        return self.storage.get_group_by_id(group.id)