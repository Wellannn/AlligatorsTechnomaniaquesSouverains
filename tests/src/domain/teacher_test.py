import unittest
from src.domain.teacher import Teacher

class TestTeacherInit(unittest.TestCase):
    def test_init_with_all_arguments(self):
        teacher = Teacher(username="teach1", email="teach1@example.com", status="active", firstname="Alice", lastname="Smith")
        self.assertEqual(teacher.username, "teach1")
        self.assertEqual(teacher.email, "teach1@example.com")
        self.assertEqual(teacher.status, "active")
        self.assertEqual(teacher.firstname, "Alice")
        self.assertEqual(teacher.lastname, "Smith")

    def test_init_with_default_names(self):
        teacher = Teacher(username="teach2", email="teach2@example.com", status="inactive")
        self.assertEqual(teacher.username, "teach2")
        self.assertEqual(teacher.email, "teach2@example.com")
        self.assertEqual(teacher.status, "inactive")
        self.assertEqual(teacher.firstname, "")
        self.assertEqual(teacher.lastname, "")

    def test_status_assignment(self):
        teacher = Teacher(username="teach3", email="teach3@example.com", status="on_leave")
        self.assertEqual(teacher.status, "on_leave")

if __name__ == "__main__":
    unittest.main()