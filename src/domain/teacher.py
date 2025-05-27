from src.domain.user import User


class Teacher(User):
    def __init__(self, firstname, lastname, username, email, status):
        super().__init__(firstname, lastname, username, email)
        self.status = status
