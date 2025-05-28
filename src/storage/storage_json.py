import os
import json
from datetime import datetime

from src.domain.student import Student
from src.domain.vote import Vote


class StorageJSON:
    def __init__(self, filename):
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

    def save_user(self, user_id, user_data):
        self._save_entry('users', user_id, user_data)

    def get_users(self):
        return self._get_category('users')

    def save_vote(self, vote_id, vote_data):
        self._save_entry('votes', vote_id, vote_data)

    def get_votes(self):
        return self._get_category('votes')

    def get_vote_by_id(self, vote_id):
        votes = self.get_votes()
        return votes.get(vote_id)

    def get_groups(self):
        return self._get_category('groups')

    def get_group_by_id(self, group_id):
        groups = self.get_groups()
        return groups.get(group_id)

    def get_user_by_username(self, username):
        users = self.get_users()
        for user in users.values():
            if user.get('username') == username:
                return user
        return None

    def _get_category(self, category):
        data = self._read()
        return data.get(category, {})

    def _save_entry(self, category, entry_id, entry_data):
        def serialize(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, dict):
                return {k: serialize(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [serialize(item) for item in obj]
            else:
                return obj

        data = self._read()
        if category not in data:
            data[category] = {}
        serialized_data = serialize(entry_data.__dict__ if hasattr(entry_data, '__dict__') else entry_data)
        if entry_id in data[category]:
            # Entry already exists, overwrite it with new data
            data[category][entry_id] = serialized_data
        else:
            data[category][entry_id] = serialized_data
        self._write(data)

    def _read(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def _write(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def delete_user(self, user_id):
        self._delete_entry('users', user_id)

    def delete_vote(self, vote_id):
        self._delete_entry('votes', vote_id)

    def _delete_entry(self, category, entry_id):
        data = self._read()
        if category in data and entry_id in data[category]:
            del data[category][entry_id]
            self._write(data)

    def save_group(self, group_id, group_data):
        self._save_entry('groups', group_id, group_data)

    def delete_group(self, group_id):
        self._delete_entry('groups', group_id)