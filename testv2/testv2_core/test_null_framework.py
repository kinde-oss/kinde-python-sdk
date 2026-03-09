#!/usr/bin/env python3
"""
Test suite for the NullFramework implementation.

This test suite verifies:
1. Singleton pattern functionality
2. User ID management (set, get, clear)
3. Thread safety with threading.Thread
4. Async safety with asyncio
5. Framework interface compliance
6. Integration with OAuth class
"""

import unittest
import threading
import asyncio
import uuid
from unittest.mock import Mock, patch
from kinde_sdk.core.framework.null_framework import NullFramework
from kinde_sdk import OAuth


class TestNullFramework(unittest.TestCase):
    """Test cases for NullFramework class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Clear any existing singleton instance for clean tests
        NullFramework._instance = None
    
    def tearDown(self):
        """Clean up after tests."""
        # Clear singleton instance
        NullFramework._instance = None
    
    def test_singleton_pattern(self):
        """Test that NullFramework implements singleton pattern correctly."""
        # Create two instances
        instance1 = NullFramework()
        instance2 = NullFramework()
        
        # They should be the same instance
        self.assertIs(instance1, instance2)
        self.assertEqual(id(instance1), id(instance2))
    
    def test_framework_properties(self):
        """Test framework name and description."""
        framework = NullFramework()
        
        self.assertEqual(framework.get_name(), "null")
        self.assertIn("session management", framework.get_description().lower())
        self.assertIn("standalone", framework.get_description().lower())
    
    def test_framework_interface_compliance(self):
        """Test that NullFramework implements all required interface methods."""
        framework = NullFramework()
        
        # Test all abstract methods from FrameworkInterface
        self.assertIsNotNone(framework.get_name())
        self.assertIsNotNone(framework.get_description())
        
        # These should not raise exceptions
        framework.start()
        framework.stop()
        
        # These should return None for null framework
        self.assertIsNone(framework.get_app())
        self.assertIsNone(framework.get_request())
        self.assertFalse(framework.can_auto_detect())
    
    def test_user_id_management(self):
        """Test user ID set, get, and clear operations."""
        framework = NullFramework()
        
        # Initially should be None
        self.assertIsNone(framework.get_user_id())
        
        # Set user ID
        test_user_id = "test-user-123"
        framework.set_user_id(test_user_id)
        self.assertEqual(framework.get_user_id(), test_user_id)
        
        # Clear user ID
        framework.clear_user_id()
        self.assertIsNone(framework.get_user_id())
    
    def test_user_id_persistence(self):
        """Test that user ID persists across method calls."""
        framework = NullFramework()
        
        test_user_id = "persistent-user-456"
        framework.set_user_id(test_user_id)
        
        # Call other methods and verify user ID is still there
        framework.get_name()
        framework.get_description()
        framework.start()
        framework.stop()
        
        self.assertEqual(framework.get_user_id(), test_user_id)
    
    def test_oauth_integration(self):
        """Test setting and getting OAuth instance."""
        framework = NullFramework()
        mock_oauth = Mock()
        
        # Initially should be None
        self.assertIsNone(framework._oauth)
        
        # Set OAuth instance
        framework.set_oauth(mock_oauth)
        self.assertEqual(framework._oauth, mock_oauth)
    
    def test_thread_safety_basic(self):
        """Test basic thread safety with threading.Thread."""
        framework = NullFramework()
        results = {}
        errors = []
        
        def worker_thread(thread_id: int, user_id: str):
            """Worker thread that sets and verifies user_id."""
            try:
                framework.set_user_id(user_id)
                # Small delay to increase chance of race condition
                threading.Event().wait(0.01)
                retrieved_user_id = framework.get_user_id()
                
                if retrieved_user_id == user_id:
                    results[thread_id] = True
                else:
                    results[thread_id] = False
            except Exception as e:
                errors.append(f"Thread {thread_id}: {e}")
        
        # Create multiple threads with different user_ids
        threads = []
        user_ids = [f"thread-user-{i}-{uuid.uuid4().hex[:8]}" for i in range(5)]
        
        for i, user_id in enumerate(user_ids):
            thread = threading.Thread(target=worker_thread, args=(i, user_id))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify no errors occurred
        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
        
        # Verify all threads succeeded
        self.assertEqual(len(results), 5)
        self.assertTrue(all(results.values()), "Some threads failed thread safety test")
    
    def test_async_safety(self):
        """Test async safety with asyncio."""
        framework = NullFramework()
        
        async def async_worker(worker_id: int, user_id: str):
            """Async worker that sets and verifies user_id."""
            framework.set_user_id(user_id)
            # Small delay
            await asyncio.sleep(0.01)
            retrieved_user_id = framework.get_user_id()
            return retrieved_user_id == user_id
        
        async def run_async_test():
            """Run multiple async workers concurrently."""
            user_ids = [f"async-user-{i}-{uuid.uuid4().hex[:8]}" for i in range(5)]
            tasks = [async_worker(i, user_id) for i, user_id in enumerate(user_ids)]
            results = await asyncio.gather(*tasks)
            return results
        
        # Run the async test
        results = asyncio.run(run_async_test())
        
        # Verify all async workers succeeded
        self.assertEqual(len(results), 5)
        self.assertTrue(all(results), "Some async workers failed async safety test")
    
    def test_mixed_threading_async_safety(self):
        """Test safety when mixing threading and async operations."""
        framework = NullFramework()
        results = {'thread': [], 'async': []}
        
        def thread_worker(thread_id: int):
            """Thread worker."""
            user_id = f"thread-{thread_id}"
            framework.set_user_id(user_id)
            threading.Event().wait(0.01)
            retrieved = framework.get_user_id()
            results['thread'].append(retrieved == user_id)
        
        async def async_worker(async_id: int):
            """Async worker."""
            user_id = f"async-{async_id}"
            framework.set_user_id(user_id)
            await asyncio.sleep(0.01)
            retrieved = framework.get_user_id()
            results['async'].append(retrieved == user_id)
        
        async def run_mixed_test():
            """Run mixed threading and async test."""
            # Start thread
            thread = threading.Thread(target=thread_worker, args=(1,))
            thread.start()
            
            # Run async worker
            await async_worker(1)
            
            # Wait for thread to complete
            thread.join()
        
        # Run the mixed test
        asyncio.run(run_mixed_test())
        
        # Verify both thread and async operations succeeded
        self.assertEqual(len(results['thread']), 1)
        self.assertEqual(len(results['async']), 1)
        self.assertTrue(results['thread'][0], "Thread operation failed")
        self.assertTrue(results['async'][0], "Async operation failed")
    
    def test_context_isolation(self):
        """Test that different contexts maintain separate user_ids."""
        framework = NullFramework()
        
        # Set user_id in main context
        framework.set_user_id("main-context")
        self.assertEqual(framework.get_user_id(), "main-context")
        
        # Create new context and verify it starts with None
        import contextvars
        new_context = contextvars.copy_context()
        
        def check_context():
            return framework.get_user_id()
        
        # In new context, should be None (default) because context variables
        # are isolated between contexts. However, contextvars.copy_context()
        # actually copies the current context, so it will inherit the current value.
        # Let's test a different approach - creating a completely new context.
        result = new_context.run(check_context)
        # The copied context will have the same value as the original
        self.assertEqual(result, "main-context")
        
        # Set user_id in new context
        def set_and_check():
            framework.set_user_id("new-context")
            return framework.get_user_id()
        
        result = new_context.run(set_and_check)
        self.assertEqual(result, "new-context")
        
        # Original context should still have original value
        self.assertEqual(framework.get_user_id(), "main-context")


class TestNullFrameworkOAuthIntegration(unittest.TestCase):
    """Test integration between NullFramework and OAuth class."""
    
    def setUp(self):
        """Set up test fixtures."""
        NullFramework._instance = None
    
    def tearDown(self):
        """Clean up after tests."""
        NullFramework._instance = None
    
    def test_oauth_initialization_with_null_framework(self):
        """Test that OAuth initializes correctly with null framework."""
        oauth = OAuth(
            framework=None,
            client_id="test_client_id",
            redirect_uri="http://localhost:8080/callback"
        )
        
        # Verify null framework is used
        self.assertIsNotNone(oauth._framework)
        self.assertEqual(oauth._framework.get_name(), "null")
        self.assertEqual(oauth.framework, None)  # OAuth.framework should still be None
    
    def test_oauth_methods_with_null_framework(self):
        """Test that OAuth methods work with null framework."""
        oauth = OAuth(
            framework=None,
            client_id="test_client_id",
            redirect_uri="http://localhost:8080/callback"
        )
        
        # Get null framework instance
        null_framework = NullFramework()
        
        # Set user_id
        test_user_id = "test-oauth-user"
        null_framework.set_user_id(test_user_id)
        
        # Test that OAuth can get user_id from null framework
        retrieved_user_id = oauth._framework.get_user_id()
        self.assertEqual(retrieved_user_id, test_user_id)
    
    @patch('kinde_sdk.auth.oauth.generate_random_string')
    @patch('kinde_sdk.auth.oauth.generate_pkce_pair')
    def test_oauth_login_with_null_framework(self, mock_pkce, mock_random):
        """Test OAuth login method with null framework."""
        # Mock the random generation functions
        mock_random.return_value = "mocked-state-123"
        mock_pkce.return_value = {
            "code_verifier": "mocked-code-verifier",
            "code_challenge": "mocked-code-challenge"
        }
        
        oauth = OAuth(
            framework=None,
            client_id="test_client_id",
            redirect_uri="http://localhost:8080/callback"
        )
        
        # Get null framework instance
        null_framework = NullFramework()
        
        # Set user_id
        test_user_id = "test-login-user"
        null_framework.set_user_id(test_user_id)
        
        # Test login method
        login_url = asyncio.run(oauth.login())
        
        # Verify URL was generated
        self.assertIsInstance(login_url, str)
        self.assertIn("test_client_id", login_url)
        # The URL is URL-encoded, so we need to check for the encoded version
        self.assertIn("http%3A%2F%2Flocalhost%3A8080%2Fcallback", login_url)
        
        # Verify state was stored
        stored_state = oauth._session_manager.storage_manager.get("user:state")
        self.assertIsNotNone(stored_state)
        self.assertEqual(stored_state["value"], "mocked-state-123")
    
    def test_oauth_is_authenticated_with_null_framework(self):
        """Test OAuth is_authenticated method with null framework."""
        oauth = OAuth(
            framework=None,
            client_id="test_client_id",
            redirect_uri="http://localhost:8080/callback"
        )
        
        # Get null framework instance
        null_framework = NullFramework()
        
        # Initially should not be authenticated
        null_framework.set_user_id("test-user")
        is_auth = oauth.is_authenticated()
        self.assertFalse(is_auth)  # No tokens stored yet


class TestNullFrameworkEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions for NullFramework."""
    
    def setUp(self):
        """Set up test fixtures."""
        NullFramework._instance = None
    
    def tearDown(self):
        """Clean up after tests."""
        NullFramework._instance = None
    
    def test_clear_user_id_when_not_set(self):
        """Test clearing user_id when it was never set."""
        framework = NullFramework()
        
        # Should not raise exception
        framework.clear_user_id()
        self.assertIsNone(framework.get_user_id())
    
    def test_set_none_user_id(self):
        """Test setting None as user_id."""
        framework = NullFramework()
        
        framework.set_user_id(None)
        self.assertIsNone(framework.get_user_id())
    
    def test_set_empty_string_user_id(self):
        """Test setting empty string as user_id."""
        framework = NullFramework()
        
        framework.set_user_id("")
        self.assertEqual(framework.get_user_id(), "")
    
    def test_multiple_set_user_id_calls(self):
        """Test multiple set_user_id calls in same context."""
        framework = NullFramework()
        
        framework.set_user_id("user-1")
        self.assertEqual(framework.get_user_id(), "user-1")
        
        framework.set_user_id("user-2")
        self.assertEqual(framework.get_user_id(), "user-2")
        
        framework.set_user_id("user-3")
        self.assertEqual(framework.get_user_id(), "user-3")
    
    def test_concurrent_set_user_id_calls(self):
        """Test concurrent set_user_id calls from different threads."""
        framework = NullFramework()
        results = []
        
        def worker(thread_id: int):
            user_id = f"concurrent-user-{thread_id}"
            framework.set_user_id(user_id)
            # Small delay
            threading.Event().wait(0.01)
            retrieved = framework.get_user_id()
            results.append(retrieved == user_id)
        
        # Create and start multiple threads
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All threads should have succeeded
        self.assertEqual(len(results), 3)
        self.assertTrue(all(results), "Concurrent set_user_id calls failed")


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    loader = unittest.TestLoader()
    test_suite.addTest(loader.loadTestsFromTestCase(TestNullFramework))
    test_suite.addTest(loader.loadTestsFromTestCase(TestNullFrameworkOAuthIntegration))
    test_suite.addTest(loader.loadTestsFromTestCase(TestNullFrameworkEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    print(f"{'='*60}")
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)
