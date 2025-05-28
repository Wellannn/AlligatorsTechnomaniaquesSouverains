import uuid
import hashlib

class User:
    """
    Represents a user in the system.
    Each user has a unique identifier, username, first name, last name, email, and a list of password hashes for security.
    """
    def __init__(self, firstname: str = "", lastname: str = "", username: str = "", email: str = "") -> None:
        """
        Initializes a new user with a unique identifier, username, first name, last name, email, and an empty list of password hashes.
        
        Args:
            firstname (str): The first name of the user (default is an empty string).
            lastname (str): The last name of the user (default is an empty string).
            username (str): The username of the user (default is an empty string).
            email (str): The email address of the user (default is an empty string).
        
        Returns:
            None
        """
        self.id = str(uuid.uuid4())
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password_hashes = []

