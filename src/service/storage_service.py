from src.storage.storage_json import StorageJSON

class StorageService:
    def __init__(self, filename="data.json"):
        self.storage = StorageJSON(filename)
    
    def is_user_exist(self, username):
        """Check if user exists"""
        return self.storage.get_user_by_username(username) is not None
    
    def get_user(self, username):
        """Get user data by username"""
        return self.storage.get_user_by_username(username)
    
    def get_all_users(self):
        """Get all users"""
        return self.storage.get_users()
    
    def create_user(self, user_data):
        """Create new user"""
        self.storage.save_user(user_data['id'], user_data)
    
    def update_user(self, user_id, user_data):
        """Update user data"""
        self.storage.save_user(user_id, user_data)
    
    def delete_user(self, user_id):
        """Delete user"""
        self.storage.delete_user(user_id)
    
    def create_vote(self, vote):
        """Create new vote"""
        self.storage.save_vote(vote.id, vote)
    
    def get_vote(self, vote_id):
        """Get vote data"""
        votes = self.storage.get_votes()
        return votes.get(vote_id)
    
    def get_all_votes(self):
        """Get all votes"""
        return self.storage.get_votes()
    
    def update_vote(self, vote):
        """Update vote data"""
        self.storage.save_vote(vote.id, vote)
    
    def delete_vote(self, vote_id):
        """Delete vote"""
        self.storage.delete_vote(vote_id)
    
    def save_generated_group(self, vote_id, groups):
        """Save generated groups for a vote"""
        data = self.storage._read()
        if 'groups' not in data:
            data['groups'] = {}
        data['groups'][vote_id] = groups
        self.storage._write(data)
    
    def get_group_for_vote(self, vote_id):
        """Get groups for a specific vote"""
        data = self.storage._read()
        groups = data.get('groups', {})
        return groups.get(vote_id, [])