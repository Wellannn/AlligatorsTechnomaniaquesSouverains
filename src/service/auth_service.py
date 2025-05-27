from src.auth.password_utils import hash_password, generate_password
from src.domain.user import User
from src.domain.student import Student
from src.domain.teacher import Teacher
from src.domain.owner import Owner

class AuthService:
    def __init__(self, storage):
        self.storage = storage
    
    def login_user(self, username, password):
        """Check if user exists and password is correct"""
        user_data = self.storage.get_user_by_username(username)
        
        if not user_data:
            return False
        
        hashed_password = hash_password(password)
        return hashed_password in user_data.get('password_hashes', [])
    
    def create_user(self, username, firstname, lastname, email, status):
        """Create a new user with generated password"""
        if self.is_user_exist(username):
            return None
        
        password = generate_password()
        hashed_password = hash_password(password)
        
        # Create user object based on status
        if status == "student":
            user = Student(username, email, status, firstname, lastname)
        elif status == "teacher":
            user = Teacher(firstname, lastname, username, email, status)
        elif status == "owner":
            user = Owner(username, email, status, firstname, lastname)
        else:
            user = User(firstname, lastname, username, email)
        
        user.password_hashes.append(hashed_password)
        
        # Save to storage using user ID
        self.storage.save_user(user.id, user)
        
        return password
    
    def change_password(self, username, old_password, new_password):
        """Change user password"""
        if not self.login_user(username, old_password):
            return False
        
        user_data = self.storage.get_user_by_username(username)
        new_hashed = hash_password(new_password)
        user_data['password_hashes'].append(new_hashed)
        
        # Update user in storage
        self.storage.save_user(user_data['id'], user_data)
        return True
    
    def is_user_exist(self, username):
        """Check if user exists"""
        return self.storage.get_user_by_username(username) is not None