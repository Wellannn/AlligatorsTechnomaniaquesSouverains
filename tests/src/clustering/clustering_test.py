import unittest
from src.clustering.clustering import Clustering
from src.domain.user import User


class TestClustering(unittest.TestCase):
    def setUp(self):
        self.users = [
            User("Alice", "Smith", "asmith", "alice@example.com"),
            User("Bob", "Jones", "bjones", "bob@example.com"),
            User("Charlie", "Lee", "clee", "charlie@example.com"),
            User("Diana", "Khan", "dkhan", "diana@example.com"),
            User("Ethan", "Wong", "ewong", "ethan@example.com"),
            User("Fiona", "Müller", "fmueller", "fiona@example.com"),
            User("George", "O'Neill", "goneill", "george@example.com"),
            User("Hannah", "Kim", "hkim", "hannah@example.com"),
            User("Isaac", "Nguyen", "inguyen", "isaac@example.com"),
            User("Julia", "Fernandez", "jfernandez", "julia@example.com"),
        ]
        self.preferences = {
            self.users[0]: [self.users[1], self.users[2], self.users[3]],
            self.users[1]: [self.users[0], self.users[4], self.users[5]],
            self.users[2]: [self.users[3], self.users[0], self.users[6]],
            self.users[3]: [self.users[0], self.users[1], self.users[2]],
            self.users[4]: [self.users[1], self.users[6], self.users[7]],
            self.users[5]: [self.users[4], self.users[2], self.users[8]],
            self.users[6]: [self.users[4], self.users[5], self.users[9]],
            self.users[7]: [self.users[6], self.users[5], self.users[0]],
            self.users[8]: [self.users[7], self.users[1], self.users[2]],
            self.users[9]: [self.users[8], self.users[3], self.users[4]],
        }

    def test_cluster_group_count(self):
        groups, total_score = Clustering.cluster(self.preferences, group_size=3)
        # There are 10 users, so expect 4 groups: 2 of size 3, 2 of size 2 (or 3,3,2,2)
        group_sizes = sorted([len(g) for g in groups], reverse=True)
        self.assertEqual(sum(group_sizes), 10)
        self.assertIn(group_sizes, ([3,3,2,2], [3,3,3,1]))

    def test_cluster_no_duplicate_users(self):
        groups, total_score = Clustering.cluster(self.preferences, group_size=3)
        all_users = [u for group in groups for u in group]
        self.assertEqual(len(all_users), len(set(all_users)))

    def test_affinity_score_positive(self):
        groups, total_score = Clustering.cluster(self.preferences, group_size=3)
        self.assertTrue(total_score > 0)

    def test_group_members_are_users(self):
        groups, total_score = Clustering.cluster(self.preferences, group_size=3)
        for group in groups:
            for member in group:
                self.assertIsInstance(member, User)

    def test_balanced_group_sizes(self):
        # Test with 8 users and group size 3 (should be 2 groups of 3, 1 group of 2)
        prefs = {u: self.preferences[u] for u in self.users[:8]}
        groups, _ = Clustering.cluster(prefs, group_size=3)
        sizes = sorted([len(g) for g in groups], reverse=True)
        self.assertEqual(sizes, [3,3,2])

if __name__ == "__main__":
    unittest.main()
