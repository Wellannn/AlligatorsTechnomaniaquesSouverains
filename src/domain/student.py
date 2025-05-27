from src.domain.user import User


class Student(User):
    def __init__(self, username, email, student_id, status, firstname, lastname):
        super().__init__(firstname, lastname, username, email)
        self.status = status
