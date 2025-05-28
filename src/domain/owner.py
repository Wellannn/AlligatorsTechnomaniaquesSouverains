from src.domain.user import User


class Owner(User):
    """
    Represents an owner of a system.
    Inherits from User and includes an additional status attribute.
    """
    def __init__(self, username: str, email: str, status: str, firstname: str = "", lastname: str = "") -> None:
        """
        Initializes a new owner with a username, email, status, and optional first and last names.
        Args:
            username (str): The username of the owner.
            email (str): The email address of the owner.
            status (str): The status of the owner (e.g., "active", "inactive").
            firstname (str): The first name of the owner (default is an empty string).
            lastname (str): The last name of the owner (default is an empty string).
        Returns:
            None
        """
        super().__init__(firstname, lastname, username, email)
        self.status = status
