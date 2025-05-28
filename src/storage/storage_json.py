import os
import json
from typing import Any, Dict, Optional
from datetime import datetime


class StorageJSON:
    """
    A class to manage persistent JSON-based storage for users, votes, and groups.
    """

    def __init__(self, filename: str) -> None:
        """
        Initializes the storage file. Creates an empty JSON structure if the file is missing or corrupted.
        Args:
            filename (str): The path to the JSON file where data will be stored.
        Returns:
            None
        Raises:
            FileNotFoundError: If the file cannot be created or accessed.
            json.JSONDecodeError: If the file is not a valid JSON.
        """
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)
        else:
            with open(self.filename, 'r+') as f:
                try:
                    json.load(f)
                except json.JSONDecodeError:
                    f.seek(0)
                    json.dump({}, f)
                    f.truncate()

    def save_user(self, user_id: str, user_data: Any) -> None:
        """
        Saves or updates a user by ID.
        Args:
            user_id (str): Unique identifier for the user.
            user_data (Any): Data associated with the user, can be a dict or any serializable object.
        Returns:
            None
        """
        self._save_entry('users', user_id, user_data)

    def get_users(self) -> Dict[str, Any]:
        """
        Returns all stored users.
        Returns:
            Dict[str, Any]: A dictionary of user IDs mapped to their data.
        """
        return self._get_category('users')

    def save_vote(self, vote_id: str, vote_data: Any) -> None:
        """
        Saves or updates a vote by ID.
        Args:
            vote_id (str): Unique identifier for the vote.
            vote_data (Any): Data associated with the vote, can be a dict or any serializable object.
        Returns:
            None
        """
        self._save_entry('votes', vote_id, vote_data)

    def get_votes(self) -> Dict[str, Any]:
        """
        Returns all stored votes.
        Returns:
            Dict[str, Any]: A dictionary of vote IDs mapped to their data.
        """
        return self._get_category('votes')

    def get_vote_by_id(self, vote_id: str) -> Optional[Dict[str, Any]]:
        """
        Returns a vote by ID, or None if not found.
        Args:
            vote_id (str): Unique identifier for the vote.
        Returns:
            Optional[Dict[str, Any]]: The vote data if found, otherwise None.
        """
        return self.get_votes().get(vote_id)

    def get_groups(self) -> Dict[str, Any]:
        """
        Returns all stored groups.
        Returns:
            Dict[str, Any]: A dictionary of group IDs mapped to their data.
        """
        return self._get_category('groups')

    def get_group_by_id(self, group_id: str) -> Optional[Dict[str, Any]]:
        """
        Returns a group by ID, or None if not found.
        Args:
            group_id (str): Unique identifier for the group.
        Returns:
            Optional[Dict[str, Any]]: The group data if found, otherwise None.
        """
        return self.get_groups().get(group_id)

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Returns a user by username, or None if not found.
        Args:
            username (str): The username of the user to find.
        Returns:
            Optional[Dict[str, Any]]: The user data if found, otherwise None.
        """
        users = self.get_users()
        for user in users.values():
            if user.get('username') == username:
                return user
        return None

    def _get_category(self, category: str) -> Dict[str, Any]:
        """
        Returns all entries in a given category (users, votes, groups).
        Args:
            category (str): The category to retrieve (e.g., 'users', 'votes', 'groups').
        Returns:
            Dict[str, Any]: A dictionary of entries in the specified category.
        """
        data = self._read()
        return data.get(category, {})

    def _save_entry(self, category: str, entry_id: str, entry_data: Any) -> None:
        """
        Saves or updates an entry in a specified category.
        Args:
            category (str): The category to save the entry in (e.g., 'users', 'votes', 'groups').
            entry_id (str): Unique identifier for the entry.
            entry_data (Any): Data associated with the entry, can be a dict or any serializable object.
        Returns:
            None
        """
        def serialize(obj: Any) -> Any:
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            elif hasattr(obj, '__dict__'):
                return serialize(obj.__dict__)
            return obj

        data = self._read()
        if category not in data:
            data[category] = {}

        data[category][entry_id] = serialize(entry_data)
        self._write(data)

    def _read(self) -> Dict[str, Any]:
        """
        Reads the JSON file and returns its content as a dictionary.
        Returns:
            Dict[str, Any]: The content of the JSON file.
        """
        with open(self.filename, 'r') as f:
            return json.load(f)

    def _write(self, data: Dict[str, Any]) -> None:
        """
        Writes the given data to the JSON file.
        Args:
            data (Dict[str, Any]): The data to write to the file.
        Returns:
            None
        """
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def delete_user(self, user_id: str) -> None:
        """
        Deletes a user by ID.
        Args:
            user_id (str): Unique identifier for the user to delete.
        Returns:
            None
        """
        self._delete_entry('users', user_id)

    def delete_vote(self, vote_id: str) -> None:
        """
        Deletes a vote by ID.
        Args:
            vote_id (str): Unique identifier for the vote to delete.
        Returns:
            None
        """
        self._delete_entry('votes', vote_id)

    def delete_group(self, group_id: str) -> None:
        """
        Deletes a group by ID.
        Args:
            group_id (str): Unique identifier for the group to delete.
        Returns:
            None
        """
        self._delete_entry('groups', group_id)

    def _delete_entry(self, category: str, entry_id: str) -> None:
        """
        Deletes an entry from a specified category.
        Args:
            category (str): The category from which to delete the entry (e.g., 'users', 'votes', 'groups').
            entry_id (str): Unique identifier for the entry to delete.
        Returns:
            None
        """
        data = self._read()
        if category in data and entry_id in data[category]:
            del data[category][entry_id]
            self._write(data)
