from typing import Optional

from src.auth.password_utils import Password
from src.domain.owner import Owner
from src.domain.student import Student
from src.domain.teacher import Teacher
from src.service import storage_service
from src.service.storage_service import *
from src.service.storage_service import StorageService


class AuthService:
    """
    Service responsible for user authentication and account management.
    """

    def __init__(self, storage: StorageService) -> None:
        """
        Initializes the authentication service with a given storage backend.
        Args:
            storage: A storage object with methods like get_user_by_username(), 
                     is_user_exist(), save_user(), update_user(), etc.
        Returns:
            None
        """
        self.storage = storage

    def login_user(self, username: str, password: str) -> str:
        """
        Authenticates a user with their username and password.
        Args:
            username (str): The user's login identifier.
            password (str): The plain-text password to verify.
        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        user, status = self.storage.get_user_by_username(username)
        if user is None:
            return False
        if not user:
            print("L'utilisateur n'existe pas")
            return False

        hashed_password = Password.hash_password(password)

        if hashed_password in user.password_hashes :
            return status

        raise ValueError("Invalid username or password")

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
        user, status = self.storage.get_user_by_username(username)

        if user is not None:
            raise ValueError("Username already exists")

        password = Password.generate_password()
        hashed_password = Password.hash_password(password)
        print(password)

        if status == "student":
            user = Student(username=username, email=email, status=status, firstname=firstname, lastname=lastname)
        elif status == "teacher":
            user = Teacher(username=username, email=email, status=status, firstname=firstname, lastname=lastname)
        elif status == "owner":
            user = Owner(username=username, email=email, status=status, firstname=firstname, lastname=lastname)
        else:
            user = User(firstname=firstname, lastname=lastname, username=username, email=email)

        user.password_hashes.append(hashed_password)

        self.storage.create_user(user)
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

if __name__ == "__main__":
    # Example usage
    storage = storage_service.StorageService()
    auth_service = AuthService(storage)

    # Create a new user
    password = auth_service.create_user("el-mousin", "Lucien", "Mousin", "el.mousin@lacatho.fr", "teacher")