import unittest
from src.domain.student import Student

class TestStudentInit(unittest.TestCase):
    def test_init_with_all_arguments(self):
        student = Student(username="jdoe", email="jdoe@example.com", status="active", firstname="John", lastname="Doe")
        self.assertEqual(student.username, "jdoe")
        self.assertEqual(student.email, "jdoe@example.com")
        self.assertEqual(student.status, "active")
        self.assertEqual(student.firstname, "John")
        self.assertEqual(student.lastname, "Doe")

    def test_init_with_default_names(self):
        student = Student(username="asmith", email="asmith@example.com", status="inactive")
        self.assertEqual(student.username, "asmith")
        self.assertEqual(student.email, "asmith@example.com")
        self.assertEqual(student.status, "inactive")
        self.assertEqual(student.firstname, "")
        self.assertEqual(student.lastname, "")

    def test_status_assignment(self):
        student = Student(username="bwayne", email="bwayne@example.com", status="graduated")
        self.assertEqual(student.status, "graduated")

if __name__ == "__main__":
    unittest.main()