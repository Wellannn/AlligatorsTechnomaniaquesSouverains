import uuid


class User:
    def __init__(self, firstname, lastname, username, email):
        self.id = str(uuid.uuid4())
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

