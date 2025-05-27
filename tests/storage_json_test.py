import hashlib
import os
import unittest

from src.domain.student import Student
from src.domain.user import User
from src.storage.storage_json import StorageJSON


class TestUserPasswordHashing(unittest.TestCase):
    def setUp(self):
        self.user = User("John", "Doe", "johndoe", "john@example.com")

    def test_add_password_hashes(self):
        # Génère 12 mots de passe hachés
        all_hashes = []
        for i in range(12):
            pwd = f"password{i}"
            self.user.add_password(pwd)
            all_hashes.append(hashlib.sha256(pwd.encode()).hexdigest())

        # Vérifie qu'on n'a gardé que les 10 derniers
        self.assertEqual(self.user.password_hashes, all_hashes[2:])

    def test_password_is_hashed(self):
        self.user.add_password("my_secret")
        self.assertNotEqual(self.user.password_hashes[0], "my_secret")
        self.assertEqual(len(self.user.password_hashes[0]), 64)  # SHA-256 = 64 caractères hex

class TestStorageJSONPassword(unittest.TestCase):
    def setUp(self):
        self.filename = "test_storage.json"
        self.storage = StorageJSON(self.filename)
        self.student = Student("studentuser", "student@example.com", "stu123", "active", "Alice", "Smith")
        for i in range(10):
            self.student.add_password(f"pass{i}")
        self.storage.save_student("stu123", self.student)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_saved_passwords_length(self):
        students = self.storage.get_students()
        self.assertIn("stu123", students)
        self.assertEqual(len(students["stu123"]["password_hashes"]), 10)

if __name__ == '__main__':
    unittest.main()
