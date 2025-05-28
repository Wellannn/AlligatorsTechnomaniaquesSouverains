from src.domain.group import Group
from src.domain.user import User
from src.domain.vote import Vote
from src.storage.storage_json import StorageJSON

class StorageService:
    def __init__(self, filename="data.json"):
        self.storage = StorageJSON(filename)
    
    def is_user_exist(self, username):
        """Check if user exists"""
        return self.get_user(username) is not None
    
    def get_user(self, username):
        """Get user data by username"""
        return self.storage.get_user_by_username(username)
    
    def get_all_users(self):
        """Get all users"""
        return self.storage.get_users()
    
    def create_user(self, user: User):
        """Create new user"""
        self.storage.save_user(user_id= user.id, user_data= user.__dict__)
    
    def update_user(self, user: User):
        """Update user data"""
        self.create_user(user)
    
    def delete_user(self, user: User):
        """Delete user"""
        self.storage.delete_user(user.id)
    
    def create_vote(self, vote):
        """Create new vote"""
        self.storage.save_vote(vote.id, vote.__dict__)
    
    def get_vote(self, vote_id):
        """Get vote data"""
        votes = self.storage.get_votes()
        return votes.get(vote_id)
    
    def get_all_votes(self):
        """Get all votes"""
        return self.storage.get_votes()
    
    def update_vote(self, vote):
        """Update vote data"""
        self.storage.save_vote(vote.id, vote.__dict__)
    
    def delete_vote(self, vote_id):
        """Delete vote"""
        self.storage.delete_vote(vote_id)

    def save_generated_group(self, groups: Group):
        """Save generated groups for a vote"""
        self.storage.save_group(groups.id, groups.__dict__)

    def get_group_by_id(self, group: Group):
        """Get groups for a specific vote"""
        return self.storage.get_group_by_id(group.id)
