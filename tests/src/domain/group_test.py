import unittest
from src.domain.user import User
from src.domain.group import Group


class TestGroupGetUsers(unittest.TestCase):
    def setUp(self):
        self.group = Group()
        self.user1 = User("alice")
        self.user2 = User("bob")

    def test_get_users_empty(self):
        self.assertEqual(self.group.get_users(), [])

    def test_get_users_after_adding_one_user(self):
        self.group.add_user(self.user1)
        self.assertEqual(self.group.get_users(), [self.user1])

    def test_get_users_after_adding_multiple_users(self):
        self.group.add_user(self.user1)
        self.group.add_user(self.user2)
        self.assertEqual(self.group.get_users(), [self.user1, self.user2])

    def test_get_users_after_removing_user(self):
        self.group.add_user(self.user1)
        self.group.add_user(self.user2)
        self.group.remove_user(self.user1)
        self.assertEqual(self.group.get_users(), [self.user2])

    def test_get_users_does_not_duplicate_users(self):
        self.group.add_user(self.user1)
        self.group.add_user(self.user1)
        self.assertEqual(self.group.get_users(), [self.user1])

if __name__ == "__main__":
    unittest.main()
