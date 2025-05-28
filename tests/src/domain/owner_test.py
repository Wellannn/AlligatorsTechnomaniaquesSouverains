import unittest
from src.domain.owner import Owner

class TestOwnerInit(unittest.TestCase):
    def test_owner_init_with_all_fields(self):
        owner = Owner(username="owner1", email="owner1@example.com", status="active", firstname="John", lastname="Doe")
        self.assertEqual(owner.username, "owner1")
        self.assertEqual(owner.email, "owner1@example.com")
        self.assertEqual(owner.status, "active")
        self.assertEqual(owner.firstname, "John")
        self.assertEqual(owner.lastname, "Doe")

    def test_owner_init_with_defaults(self):
        owner = Owner(username="owner2", email="owner2@example.com", status="inactive")
        self.assertEqual(owner.username, "owner2")
        self.assertEqual(owner.email, "owner2@example.com")
        self.assertEqual(owner.status, "inactive")
        self.assertEqual(owner.firstname, "")
        self.assertEqual(owner.lastname, "")

    def test_owner_status_assignment(self):
        owner = Owner(username="owner3", email="owner3@example.com", status="pending")
        self.assertEqual(owner.status, "pending")

if __name__ == "__main__":
    unittest.main()