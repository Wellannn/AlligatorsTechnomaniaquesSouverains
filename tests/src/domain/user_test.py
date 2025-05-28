import unittest
from src.domain.user import User

class TestUserInit(unittest.TestCase):
    def test_init_default_values(self):
        user = User()
        self.assertIsInstance(user.id, str)
        self.assertNotEqual(user.id, "")
        self.assertEqual(user.firstname, "")
        self.assertEqual(user.lastname, "")
        self.assertEqual(user.username, "")
        self.assertEqual(user.email, "")
        self.assertEqual(user.password_hashes, [])

    def test_init_with_values(self):
        user = User(firstname="John", lastname="Doe", username="jdoe", email="john@example.com")
        self.assertIsInstance(user.id, str)
        self.assertEqual(user.firstname, "John")
        self.assertEqual(user.lastname, "Doe")
        self.assertEqual(user.username, "jdoe")
        self.assertEqual(user.email, "john@example.com")
        self.assertEqual(user.password_hashes, [])

    def test_unique_id(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)
