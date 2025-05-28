import unittest
from datetime import datetime, timedelta
from src.domain.vote import Vote


class TestVoteInit(unittest.TestCase):
    def setUp(self):
        self.title = "Project Vote"
        self.group_size = 4
        self.eligible_students = ["Alice", "Bob", "Charlie"]
        self.teachers = ["Prof. Smith", "Prof. Doe"]
        self.end_date = datetime.now() + timedelta(days=7)
        self.reliability_score = 0.85
        self.preference = {"Alice": ["Bob", "Charlie"]}

    def test_init_required_fields(self):
        vote = Vote(
            title=self.title,
            group_size=self.group_size,
            eligible_students=self.eligible_students,
            teachers=self.teachers,
            end_date=self.end_date
        )
        self.assertEqual(vote.title, self.title)
        self.assertEqual(vote.group_size, self.group_size)
        self.assertEqual(vote.eligible_students, self.eligible_students)
        self.assertEqual(vote.teachers, self.teachers)
        self.assertEqual(vote.end_date, self.end_date)
        self.assertEqual(vote.reliability_score, 0.0)
        self.assertEqual(vote.preferennces, {})
        self.assertIsInstance(vote.id, str)

    def test_init_with_all_fields(self):
        vote = Vote(
            title=self.title,
            group_size=self.group_size,
            eligible_students=self.eligible_students,
            teachers=self.teachers,
            end_date=self.end_date,
            reliability_score=self.reliability_score,
            preference=self.preference
        )
        self.assertEqual(vote.title, self.title)
        self.assertEqual(vote.group_size, self.group_size)
        self.assertEqual(vote.eligible_students, self.eligible_students)
        self.assertEqual(vote.teachers, self.teachers)
        self.assertEqual(vote.end_date, self.end_date)
        self.assertEqual(vote.reliability_score, self.reliability_score)
        self.assertEqual(vote.preferennces, self.preference)
        self.assertIsInstance(vote.id, str)

    def test_unique_id(self):
        vote1 = Vote(
            title=self.title,
            group_size=self.group_size,
            eligible_students=self.eligible_students,
            teachers=self.teachers,
            end_date=self.end_date
        )
        vote2 = Vote(
            title=self.title,
            group_size=self.group_size,
            eligible_students=self.eligible_students,
            teachers=self.teachers,
            end_date=self.end_date
        )
        self.assertNotEqual(vote1.id, vote2.id)

    def test_preference_default_is_empty_dict(self):
        vote = Vote(
            title=self.title,
            group_size=self.group_size,
            eligible_students=self.eligible_students,
            teachers=self.teachers,
            end_date=self.end_date
        )
        self.assertEqual(vote.preferennces, {})

if __name__ == "__main__":
    unittest.main()