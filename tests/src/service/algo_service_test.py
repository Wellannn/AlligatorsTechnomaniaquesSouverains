import unittest
from unittest.mock import MagicMock
from src.service.algo_service import AlgoService
from src.domain.user import User

class TestAlgoService(unittest.TestCase):
    def setUp(self):
        self.user1 = User("Alice")
        self.user2 = User("Bob")
        self.user3 = User("Charlie")
        self.user4 = User("Diana")
        self.preferences = {
            self.user1: {self.user2: 5, self.user3: 3},
            self.user2: {self.user1: 4, self.user3: 2},
            self.user3: {self.user1: 1, self.user2: 2},
            self.user4: {self.user1: 2}
        }

    def test_cluster_users_calls_clustering(self):
        service = AlgoService(self.preferences)
        service.clustering = MagicMock()
        service.clustering.cluster_users.return_value = [[self.user1, self.user2], [self.user3, self.user4]]
        result = service.cluster_users(2)
        service.clustering.cluster_users.assert_called_once_with(self.preferences, 2)
        self.assertEqual(result, [[self.user1, self.user2], [self.user3, self.user4]])

    def test_cluster_users_empty_preferences(self):
        service = AlgoService({})
        service.clustering = MagicMock()
        service.clustering.cluster_users.return_value = []
        result = service.cluster_users(2)
        service.clustering.cluster_users.assert_called_once_with({}, 2)
        self.assertEqual(result, [])

    def test_cluster_users_group_size_one(self):
        service = AlgoService(self.preferences)
        service.clustering = MagicMock()
        service.clustering.cluster_users.return_value = [[self.user1], [self.user2], [self.user3], [self.user4]]
        result = service.cluster_users(1)
        service.clustering.cluster_users.assert_called_once_with(self.preferences, 1)
        self.assertEqual(result, [[self.user1], [self.user2], [self.user3], [self.user4]])

if __name__ == "__main__":
    unittest.main()
