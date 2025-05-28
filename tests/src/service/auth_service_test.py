import unittest
from unittest.mock import MagicMock, patch
from src.service.auth_service import AuthService


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.mock_storage = MagicMock()
        self.auth_service = AuthService(self.mock_storage)

    @patch('src.service.auth_service.Password')
    def test_login_user_success(self, mock_password):
        username = "testuser"
        password = "password123"
        hashed = "hashed_password"
        self.mock_storage.get_user_by_username.return_value = {
            'password_hashes': [hashed]
        }
        mock_password.hash_password.return_value = hashed

        result = self.auth_service.login_user(username, password)

        self.assertTrue(result)
        self.mock_storage.get_user_by_username.assert_called_once_with(username)
        mock_password.hash_password.assert_called_once_with(password)

    @patch('src.service.auth_service.Password')
    def test_login_user_failure_wrong_password(self, mock_password):
        username = "testuser"
        password = "wrongpassword"
        self.mock_storage.get_user_by_username.return_value = {
            'password_hashes': ["some_other_hash"]
        }
        mock_password.hash_password.return_value = "not_in_hashes"

        result = self.auth_service.login_user(username, password)

        self.assertFalse(result)

    def test_login_user_failure_no_user(self):
        self.mock_storage.get_user_by_username.return_value = None
        result = self.auth_service.login_user("nouser", "password")
        self.assertFalse(result)

    @patch('src.service.auth_service.Password')
    @patch('src.service.auth_service.Student')
    def test_create_user_student(self, mock_student, mock_password):
        self.mock_storage.is_user_exist.return_value = False
        mock_password.generate_password.return_value = "genpass"
        mock_password.hash_password.return_value = "hashed"
        mock_user = MagicMock()
        mock_user.password_hashes = []
        mock_user.id = "student_id"
        mock_student.return_value = mock_user

        password = self.auth_service.create_user(
            "studentuser", "John", "Doe", "john@example.com", "student"
        )

        self.assertEqual(password, "genpass")
        self.mock_storage.save_user.assert_called_once_with("student_id", mock_user)
        self.assertIn("hashed", mock_user.password_hashes)

    @patch('src.service.auth_service.Password')
    @patch('src.service.auth_service.Teacher')
    def test_create_user_teacher(self, mock_teacher, mock_password):
        self.mock_storage.is_user_exist.return_value = False
        mock_password.generate_password.return_value = "genpass"
        mock_password.hash_password.return_value = "hashed"
        mock_user = MagicMock()
        mock_user.password_hashes = []
        mock_user.id = "teacher_id"
        mock_teacher.return_value = mock_user

        password = self.auth_service.create_user(
            "teacheruser", "Jane", "Smith", "jane@example.com", "teacher"
        )

        self.assertEqual(password, "genpass")
        self.mock_storage.save_user.assert_called_once_with("teacher_id", mock_user)
        self.assertIn("hashed", mock_user.password_hashes)

    @patch('src.service.auth_service.Password')
    @patch('src.service.auth_service.Owner')
    def test_create_user_owner(self, mock_owner, mock_password):
        self.mock_storage.is_user_exist.return_value = False
        mock_password.generate_password.return_value = "genpass"
        mock_password.hash_password.return_value = "hashed"
        mock_user = MagicMock()
        mock_user.password_hashes = []
        mock_user.id = "owner_id"
        mock_owner.return_value = mock_user

        password = self.auth_service.create_user(
            "owneruser", "Alice", "Brown", "alice@example.com", "owner"
        )

        self.assertEqual(password, "genpass")
        self.mock_storage.save_user.assert_called_once_with("owner_id", mock_user)
        self.assertIn("hashed", mock_user.password_hashes)

    @patch('src.service.auth_service.Password')
    @patch('src.service.auth_service.User')
    def test_create_user_default(self, mock_user_class, mock_password):
        self.mock_storage.is_user_exist.return_value = False
        mock_password.generate_password.return_value = "genpass"
        mock_password.hash_password.return_value = "hashed"
        mock_user = MagicMock()
        mock_user.password_hashes = []
        mock_user.id = "user_id"
        mock_user_class.return_value = mock_user

        password = self.auth_service.create_user(
            "defaultuser", "Bob", "Marley", "bob@example.com", "unknown"
        )

        self.assertEqual(password, "genpass")
        self.mock_storage.save_user.assert_called_once_with("user_id", mock_user)
        self.assertIn("hashed", mock_user.password_hashes)

    def test_create_user_already_exists(self):
        self.mock_storage.is_user_exist.return_value = True
        password = self.auth_service.create_user(
            "existinguser", "First", "Last", "email@example.com", "student"
        )
        self.assertIsNone(password)
        self.mock_storage.save_user.assert_not_called()

    @patch('src.service.auth_service.Password')
    def test_change_password_success(self, mock_password):
        username = "user"
        old_password = "old"
        new_password = "new"
        user_data = {'password_hashes': ["old_hash"]}
        self.auth_service.login_user = MagicMock(return_value=True)
        self.mock_storage.get_user_by_username.return_value = user_data
        mock_password.hash_password.return_value = "new_hash"

        result = self.auth_service.change_password(username, old_password, new_password)

        self.assertTrue(result)
        self.assertIn("new_hash", user_data['password_hashes'])
        self.mock_storage.update_user.assert_called_once_with(user_data)

    def test_change_password_fail_wrong_old(self):
        self.auth_service.login_user = MagicMock(return_value=False)
        result = self.auth_service.change_password("user", "badold", "new")
        self.assertFalse(result)
        self.mock_storage.update_user.assert_not_called()

if __name__ == '__main__':
    unittest.main()
