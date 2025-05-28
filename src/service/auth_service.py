from typing import Optional
from src.auth.password_utils import Password
from src.domain.user import User
from src.domain.student import Student
from src.domain.teacher import Teacher
from src.domain.owner import Owner
import storage_service


class AuthService:
    """
    Service responsible for user authentication and account management.
    """

    def __init__(self, storage: storage_service.StorageService) -> None:
        """
        Initializes the authentication service with a given storage backend.
        Args:
            storage: A storage object with methods like get_user_by_username(), 
                     is_user_exist(), save_user(), update_user(), etc.
        Returns:
            None
        """
        self.storage = storage

    def login_user(self, username: str, password: str) -> bool:
        """
        Authenticates a user with their username and password.
        Args:
            username (str): The user's login identifier.
            password (str): The plain-text password to verify.
        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        user_data = self.storage.get_user_by_username(username)
        if not user_data:
            return False

        hashed_password = Password.hash_password(password)
        return hashed_password in user_data.get('password_hashes', [])

    def create_user(
        self,
        username: str,
        firstname: str,
        lastname: str,
        email: str,
        status: str
    ) -> Optional[str]:
        """
        Creates a new user and stores it in the system with a generated password.
        Args:
            username (str): The user's login identifier.
            firstname (str): First name of the user.
            lastname (str): Last name of the user.
            email (str): Email address.
            status (str): The user's role or account type 
                          (e.g., "student", "teacher", "owner").
        Returns:
            Optional[str]: The generated password if creation succeeds, None otherwise.
        """
        if self.storage.is_user_exist(username):
            return None

        password = Password.generate_password()
        hashed_password = Password.hash_password(password)

        if status == "student":
            user = Student(username, email, status, firstname, lastname)
        elif status == "teacher":
            user = Teacher(firstname, lastname, username, email, status)
        elif status == "owner":
            user = Owner(username, email, status, firstname, lastname)
        else:
            user = User(firstname, lastname, username, email)

        user.password_hashes.append(hashed_password)

        self.storage.save_user(user.id, user)
        return password

    def change_password(
        self,
        username: str,
        old_password: str,
        new_password: str
    ) -> bool:
        """
        Changes the user's password if the old password is valid.
        Args:
            username (str): The user's login identifier.
            old_password (str): The current password.
            new_password (str): The new password to set.
        Returns:
            bool: True if the password was changed successfully, False otherwise.
        """
        if not self.login_user(username, old_password):
            return False

        user = self.storage.get_user_by_username(username)
        new_hashed = Password.hash_password(new_password)
        user['password_hashes'].append(new_hashed)

        self.storage.update_user(user)
        return True
