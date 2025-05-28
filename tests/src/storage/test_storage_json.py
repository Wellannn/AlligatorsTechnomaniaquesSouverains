import os
import unittest

from src.domain.student import Student
from src.storage.storage_json import StorageJSON


class TestStorageJSON(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test_data.json'
        self.storage = StorageJSON(self.test_file)
        self.storage._write({})  # Reset file for isolation

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_delete_user(self):
        student = Student(username="deleteuser", email="delete@example.com", status="student", firstname="Delete", lastname="User")
        self.storage.save_user(student.id, student)
        users = self.storage.get_users()
        self.assertIn(student.id, users)

        self.storage.delete_user(student.id)
        users_after_delete = self.storage.get_users()
        self.assertNotIn(student.id, users_after_delete)

    def test_delete_user_nonexistent(self):
        # Should not raise an error
        try:
            self.storage.delete_user("nonexistent-id")
        except Exception as e:
            self.fail(f"delete_user raised an exception unexpectedly: {e}")

    def test_read_invalid_json(self):
        with open(self.test_file, 'w') as f:
            f.write('INVALID JSON')
        # Le fichier doit être réinitialisé sans exception
        storage = StorageJSON(self.test_file)
        data = storage._read()
        self.assertEqual(data, {})

    def test_get_user_by_username_not_found(self):
        result = self.storage.get_user_by_username("not_existing_user")
        self.assertIsNone(result)

    def test_get_from_empty_category(self):
        self.assertEqual(self.storage.get_votes(), {})
        self.assertEqual(self.storage.get_users(), {})

    def test_save_entry_with_non_serializable_object(self):
        class NonSerializable:
            pass
        with self.assertRaises(TypeError):
            self.storage._write({'users': {'bad_id': NonSerializable()}})

if __name__ == '__main__':
    unittest.main()
