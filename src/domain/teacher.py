from src.domain.user import User


class Teacher(User):
    """
    Represents a teacher in the system.
    Inherits from User and includes an additional status attribute.
    """
    
    def __init__(self, username: str, email: str, status: str, firstname: str = "", lastname: str = "") -> None:
        """
        Initializes a new teacher with a username, email, status, and optional first and last names.
        Args:
            username (str): The username of the teacher.
            email (str): The email address of the teacher.
            status (str): The status of the teacher (e.g., "active", "inactive").
            firstname (str): The first name of the teacher (default is an empty string).
            lastname (str): The last name of the teacher (default is an empty string).
        Returns:
            None
        """
        super().__init__(firstname, lastname, username, email)
        self.status = status
