from src.domain.user import User


class Student(User):
    """
    Represents a student in the system.
    Inherits from User and includes an additional status attribute.
    """
    
    def __init__(self, username: str, email: str, status: str, firstname: str = "", lastname: str = "") -> None:
        """
        Initializes a new student with a username, email, status, and optional first and last names.
        Args:
            username (str): The username of the student.
            email (str): The email address of the student.
            status (str): The status of the student (e.g., "active", "inactive").
            firstname (str): The first name of the student (default is an empty string).
            lastname (str): The last name of the student (default is an empty string).
        Returns:
            None
        """
        super().__init__(firstname, lastname, username, email)
        self.status = status
