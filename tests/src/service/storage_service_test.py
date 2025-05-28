import unittest
from unittest.mock import MagicMock
from src.service.storage_service import StorageService
from src.domain.group import Group


class TestStorageServiceGetGroupById(unittest.TestCase):
    def setUp(self):
        self.storage_service = StorageService("test_data.json")
        self.storage_service.storage = MagicMock()

    def test_get_group_by_id_returns_group_data(self):
        group = Group(id="group123")
        expected_data = {"id": "group123", "name": "Test Group"}
        self.storage_service.storage.get_group_by_id.return_value = expected_data

        result = self.storage_service.get_group_by_id(group)

        self.storage_service.storage.get_group_by_id.assert_called_once_with("group123")
        self.assertEqual(result, expected_data)

    def test_get_group_by_id_returns_none_when_not_found(self):
        group = Group(id="nonexistent")
        self.storage_service.storage.get_group_by_id.return_value = None

        result = self.storage_service.get_group_by_id(group)

        self.storage_service.storage.get_group_by_id.assert_called_once_with("nonexistent")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()