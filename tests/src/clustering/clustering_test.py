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
            self.users[0]: {self.users[1]: 10, self.users[2]: 5, self.users[3]: 3},
            self.users[1]: {self.users[0]: 8, self.users[4]: 6, self.users[5]: 4},
            self.users[2]: {self.users[3]: 9, self.users[0]: 7, self.users[6]: 2},
            self.users[3]: {self.users[0]: 10, self.users[1]: 6, self.users[2]: 4},
            self.users[4]: {self.users[1]: 8, self.users[6]: 7, self.users[7]: 5},
            self.users[5]: {self.users[4]: 9, self.users[2]: 3, self.users[8]: 4},
            self.users[6]: {self.users[4]: 6, self.users[5]: 5, self.users[9]: 2},
            self.users[7]: {self.users[6]: 7, self.users[5]: 4, self.users[0]: 3},
            self.users[8]: {self.users[7]: 9, self.users[1]: 4, self.users[2]: 6},
            self.users[9]: {self.users[8]: 7, self.users[3]: 5, self.users[4]: 6},
        }

    def test_cluster_group_count(self):
        groups, total_score = Clustering.cluster(self.preferences, group_size=3)
        group_sizes = sorted([len(g) for g in groups], reverse=True)
        self.assertEqual(sum(group_sizes), 10)
        self.assertIn(group_sizes, ([3, 3, 2, 2], [3, 3, 3, 1]))

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
        # Test avec 8 utilisateurs
        prefs = {u: self.preferences[u] for u in self.users[:8]}
        groups, _ = Clustering.cluster(prefs, group_size=3)
        sizes = sorted([len(g) for g in groups], reverse=True)
        self.assertEqual(sizes, [3, 3, 2])

    def test_cluster_returns_expected_number_of_groups(self):
        groups, total_score = Clustering.cluster(self.preferences, group_size=4)
        self.assertTrue(2 <= len(groups) <= 4)
        self.assertEqual(sum(len(g) for g in groups), len(self.users))

    def test_cluster_handles_single_user(self):
        single_user = [User("Zoe", "Solo", "zsolo", "zoe@example.com")]
        prefs = {single_user[0]: {}}
        groups, total_score = Clustering.cluster(prefs, group_size=3)
        self.assertEqual(groups, [[single_user[0]]])
        self.assertEqual(total_score, 0)

    def test_cluster_handles_empty_preferences(self):
        groups, total_score = Clustering.cluster({}, group_size=3)
        self.assertEqual(groups, [])
        self.assertEqual(total_score, 0)

    def test_cluster_group_size_never_exceeds_max(self):
        groups, total_score = Clustering.cluster(self.preferences, group_size=3)
        for group in groups:
            self.assertLessEqual(len(group), 3)

    def test_cluster_affinity_score_consistency(self):
        groups, total_score = Clustering.cluster(self.preferences, group_size=3)
        matrix, user_list = Clustering._Clustering__build_affinity_matrix(self.preferences)
        manual_score = 0
        for group in groups:
            indices = [user_list.index(u) for u in group]
            manual_score += Clustering._Clustering__score_group(indices, matrix)
        self.assertEqual(total_score, manual_score)


if __name__ == "__main__":
    unittest.main()
