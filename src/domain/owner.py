from src.domain.user import User


class Owner(User):
    def __init__(self, username, email, status, firstname, lastname):
        super().__init__(firstname, lastname, username, email)
        self.status= status
