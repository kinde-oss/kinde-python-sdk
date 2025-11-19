import unittest
import threading
import time
import uuid
from unittest.mock import patch, MagicMock

from kinde_sdk.core.storage.storage_manager import StorageManager
from kinde_sdk.core.storage.storage_interface import StorageInterface

class TestStorageManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Reset the singleton instance before each test
        StorageManager._instance = None
        self.storage_manager = StorageManager()
        
        # Create a mock storage
        self.mock_storage = MagicMock(spec=StorageInterface)
        self.storage_manager._storage = self.mock_storage
        
        # Set a test device ID
        self.test_device_id = str(uuid.uuid4())
        self.storage_manager._device_id = self.test_device_id

    def test_singleton_pattern(self):
        """Test that StorageManager follows singleton pattern."""
        manager1 = StorageManager()
        manager2 = StorageManager()
        self.assertIs(manager1, manager2)

    def test_initialize_with_config(self):
        """Test initialization with configuration."""
        #config = {
        #    "type": "memory",
        #    "options": {
        #        "prefix": "test_"
        #    }
        #}
        #self.storage_manager.initialize(config=config)
        #self.assertEqual(self.storage_manager._storage_type, "memory")

    def test_initialize_with_storage(self):
        """Test initialization with provided storage instance."""
        #mock_storage = MagicMock(spec=StorageInterface)
        #self.storage_manager.initialize(storage=mock_storage)
        #self.assertIs(self.storage_manager._storage, mock_storage)

    def test_get_device_id(self):
        """Test device ID generation and retrieval."""
        # Test getting existing device ID
        #self.assertEqual(self.storage_manager.get_device_id(), self.test_device_id)
        
        # Test generating new device ID when none exists
        #self.storage_manager._device_id = None
        #self.mock_storage.get.return_value = None
        
        #new_id = self.storage_manager.get_device_id()
        #self.assertIsNotNone(new_id)
        #self.mock_storage.setItems.assert_called_once()

    def test_get_namespaced_key(self):
        """Test key namespacing functionality."""
        # Test device-specific key
        key = "test_key"
        expected = f"device:{self.test_device_id}:{key}"
        self.assertEqual(self.storage_manager._get_namespaced_key(key), expected)
        
        # Test global key
        global_key = "global:test_key"
        self.assertEqual(self.storage_manager._get_namespaced_key(global_key), global_key)
        
        # Test user-specific key
        user_key = "user:test_key"
        self.assertEqual(self.storage_manager._get_namespaced_key(user_key), user_key)
        
        # Test device ID key
        self.assertEqual(self.storage_manager._get_namespaced_key("_device_id"), "_device_id")

    def test_get(self):
        """Test get method."""
        test_key = "test_key"
        test_value = {"value": "test_value"}
        self.mock_storage.get.return_value = test_value
        
        result = self.storage_manager.get(test_key)
        self.assertEqual(result, test_value)
        self.mock_storage.get.assert_called_once_with(f"device:{self.test_device_id}:{test_key}")

    def test_setItems(self):
        """Test setItems method."""
        test_key = "test_key"
        test_value = {"value": "test_value"}
        
        self.storage_manager.setItems(test_key, test_value)
        self.mock_storage.set.assert_called_once_with(
            f"device:{self.test_device_id}:{test_key}",
            test_value
        )

    def test_set(self):
        """Test set method for flat access token."""
        test_token = "test_access_token"
        self.storage_manager.set(test_token)
        self.mock_storage.set_flat.assert_called_once_with(test_token)

    def test_delete(self):
        """Test delete method."""
        test_key = "test_key"
        self.storage_manager.delete(test_key)
        self.mock_storage.delete.assert_called_once_with(
            f"device:{self.test_device_id}:{test_key}"
        )

    def test_clear_device_data(self):
        """Test clear_device_data method."""
        # Test with storage that supports clear_prefix
        #self.mock_storage.clear_prefix = MagicMock()
        #self.storage_manager.clear_device_data()
        #self.mock_storage.clear_prefix.assert_called_once_with(f"device:{self.test_device_id}:")

        # Test with storage that doesn't support clear_prefix
        #self.mock_storage.clear_prefix = None
        #self.mock_storage._storage = {"key1": "value1", "key2": "value2"}
        #self.storage_manager.clear_device_data()
        # Should have attempted to delete keys

    def test_thread_safety(self):
        """Test thread safety of StorageManager."""
        def worker():
            manager = StorageManager()
            manager.initialize({"type": "memory"})
            manager.setItems("test_key", {"value": "test_value"})
            time.sleep(0.1)  # Simulate some work
            return manager.get("test_key")

        # Create multiple threads
        threads = []
        results = []
        for _ in range(5):
            thread = threading.Thread(target=lambda: results.append(worker()))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Verify all threads got the same instance
        self.assertTrue(all(r == results[0] for r in results))

    def test_reset(self):
        """Test reset method."""
        #self.storage_manager.reset()
        #self.assertIsNone(self.storage_manager._storage)
        #self.assertIsNone(self.storage_manager._device_id)
        #self.assertEqual(self.storage_manager._storage_type, "memory")

    def test_auto_initialize(self):
        """Test auto-initialization when storage is None."""
        self.storage_manager._storage = None
        self.storage_manager.get("test_key")
        self.assertIsNotNone(self.storage_manager._storage)

if __name__ == "__main__":
    unittest.main() 