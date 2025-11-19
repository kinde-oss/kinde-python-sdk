"""
Test cases to reproduce and verify the deadlock issue fix reported by customer.

This module tests various scenarios that could cause the ManagementClient
to hang on the `with self.lock:` line in management_token_manager.py and
verifies that the RLock fix resolves the issue.

Customer Issue: SDK hangs on "with self.lock:" in set_tokens method
Root Cause: Non-reentrant lock deadlock in call chain:
  get_access_token() -> request_new_token() -> set_tokens()
Fix: Use threading.RLock() instead of threading.Lock()
"""

import pytest
import time
import threading
import unittest
from unittest.mock import Mock, patch, MagicMock
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.exceptions import Timeout, ConnectionError

from kinde_sdk.management.management_client import ManagementClient
from kinde_sdk.management.management_token_manager import ManagementTokenManager


class TestManagementClientDeadlock(unittest.TestCase):
    """Test cases to reproduce and verify deadlock scenarios are fixed."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.domain = "test.kinde.com"
        self.client_id = "test_client_id"
        self.client_secret = "test_client_secret"
        
        # Reset token manager instances before each test
        ManagementTokenManager.reset_instances()

    def tearDown(self):
        """Clean up after each test."""
        ManagementTokenManager.reset_instances()

    def test_customer_deadlock_issue_fixed(self):
        """
        MAIN TEST: Verifies the customer's exact deadlock issue is fixed.
        
        Tests the reentrant lock scenario where get_access_token() calls request_new_token()
        which calls set_tokens() while already holding the lock.
        
        Before fix: Would hang indefinitely on "with self.lock:" in set_tokens
        After fix: Completes quickly with RLock
        """
        with patch('requests.post') as mock_post:
            # Configure mock to return a valid token response
            mock_response = Mock()
            mock_response.json.return_value = {
                "access_token": "customer_fix_token",
                "expires_in": 3600,
                "token_type": "Bearer"
            }
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            # Create token manager and clear tokens to force the reentrant lock scenario
            token_manager = ManagementTokenManager(self.domain, self.client_id, self.client_secret)
            token_manager.tokens = {}  # Force new token request
            
            # Test the exact deadlock scenario that was hanging for the customer
            start_time = time.time()
            
            try:
                # This call chain was causing the deadlock:
                # get_access_token() -> request_new_token() -> set_tokens()
                # All three methods acquire the same lock
                token = token_manager.get_access_token()
                elapsed_time = time.time() - start_time
                
                # With RLock fix, this should complete quickly
                assert elapsed_time < 1, f"Token request took too long: {elapsed_time} seconds - possible deadlock"
                assert token == "customer_fix_token"
                
                print(f"✅ CUSTOMER ISSUE FIXED: Token obtained in {elapsed_time:.3f} seconds")
                
            except Exception as e:
                elapsed_time = time.time() - start_time
                if elapsed_time > 5:  # If it took more than 5 seconds, it's likely a deadlock
                    pytest.fail(f"Customer deadlock still exists: operation took {elapsed_time} seconds, error: {e}")
                raise

    def test_network_timeout_handling(self):
        """
        Test that network timeouts are handled properly without hanging.
        """
        with patch('requests.post') as mock_post:
            # Simulate network timeout
            mock_post.side_effect = Timeout("Network timeout")
            
            token_manager = ManagementTokenManager(self.domain, self.client_id, self.client_secret)
            token_manager.tokens = {}  # Force new token request
            
            start_time = time.time()
            
            # This should raise our custom timeout exception, not hang
            with pytest.raises(Exception) as exc_info:
                token_manager.get_access_token()
            
            elapsed_time = time.time() - start_time
            
            # Should fail quickly due to timeout, not hang
            assert elapsed_time < 5, f"Timeout handling took too long: {elapsed_time} seconds"
            
            # Verify it's our timeout exception (which is working correctly)
            assert "timed out" in str(exc_info.value).lower(), f"Expected timeout error, got: {exc_info.value}"

    def test_management_client_integration_fixed(self):
        """
        Test that ManagementClient methods (get_users, get_api_applications) work
        without hanging - reproduces customer's exact usage pattern.
        """
        with patch('requests.post') as mock_post:
            # Configure token response
            mock_response = Mock()
            mock_response.json.return_value = {
                "access_token": "integration_test_token",
                "expires_in": 3600,
                "token_type": "Bearer"
            }
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            # Mock the ApiClient and Configuration to avoid parameter mismatch
            with patch('kinde_sdk.management.management_client.ApiClient') as mock_api_client_class:
                mock_api_client_instance = Mock()
                
                # Mock param_serialize to return expected values
                mock_api_client_instance.param_serialize.return_value = (
                    'GET', 'https://test.kinde.com/api/v1/users', {}, None, None
                )
                
                # Mock REST client response
                mock_rest_response = Mock()
                mock_rest_response.read.return_value = None
                mock_rest_response.status = 200
                mock_rest_response.data = b'{"users": []}'
                mock_rest_response.getheader.return_value = 'application/json'
                
                mock_api_client_instance.rest_client.request.return_value = mock_rest_response
                
                # Mock response_deserialize
                mock_api_response = Mock()
                mock_api_response.data = {"users": []}
                mock_api_client_instance.response_deserialize.return_value = mock_api_response
                
                mock_api_client_class.return_value = mock_api_client_instance
                
                with patch('kinde_sdk.management.management_client.Configuration') as mock_config:
                    mock_config.return_value = Mock()
                    
                    # Test customer's exact usage pattern
                    client = ManagementClient(self.domain, self.client_id, self.client_secret)
                    
                    start_time = time.time()
                    
                    # These calls were hanging for the customer
                    try:
                        users = client.get_users()
                        api_apps = client.get_api_applications()
                        
                        elapsed_time = time.time() - start_time
                        
                        # Should complete quickly now
                        assert elapsed_time < 2, f"Management client calls took too long: {elapsed_time} seconds"
                        
                        print(f"✅ Management client integration working: Completed in {elapsed_time:.3f} seconds")
                        
                    except Exception as e:
                        elapsed_time = time.time() - start_time
                        if elapsed_time > 10:
                            pytest.fail(f"Management client still hanging: {elapsed_time} seconds - {e}")
                        raise

    def test_concurrent_access_no_deadlock(self):
        """
        Test concurrent access to ManagementTokenManager from multiple threads
        to ensure no deadlock occurs under load.
        """
        with patch('requests.post') as mock_post:
            # Configure mock to return a valid token response
            mock_response = Mock()
            mock_response.json.return_value = {
                "access_token": "concurrent_test_token",
                "expires_in": 3600,
                "token_type": "Bearer"
            }
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            # Create token manager
            token_manager = ManagementTokenManager(self.domain, self.client_id, self.client_secret)
            
            results = []
            errors = []
            
            def get_token_concurrent(thread_id):
                """Function to be called by each thread."""
                try:
                    start_time = time.time()
                    token = token_manager.get_access_token()
                    elapsed_time = time.time() - start_time
                    results.append((thread_id, elapsed_time, token))
                    return f"Thread {thread_id} completed"
                except Exception as e:
                    errors.append((thread_id, str(e)))
                    return f"Thread {thread_id} failed: {e}"
            
            # Create multiple threads trying to access tokens simultaneously
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(get_token_concurrent, i) for i in range(5)]
                
                # Wait for all threads to complete with a timeout
                completed_count = 0
                for future in as_completed(futures, timeout=10):  # 10-second timeout
                    try:
                        result = future.result()
                        completed_count += 1
                    except Exception as e:
                        errors.append(f"Thread execution error: {e}")
            
            # All threads should complete successfully
            assert len(errors) == 0, f"Errors occurred: {errors}"
            assert completed_count == 5, f"Only {completed_count} out of 5 threads completed"
            
            # No thread should take unreasonably long
            for thread_id, elapsed_time, token in results:
                assert elapsed_time < 2, f"Thread {thread_id} took too long: {elapsed_time} seconds"
                assert token == "concurrent_test_token"

    def test_token_expiry_concurrent_refresh(self):
        """
        Test concurrent token refresh when multiple threads detect expired tokens.
        This scenario could cause deadlock if not handled properly with RLock.
        """
        with patch('kinde_sdk.management.management_token_manager.requests.post') as mock_post:
            # Configure mock to return new token
            mock_response = Mock()
            mock_response.json.return_value = {
                "access_token": "refreshed_token",
                "expires_in": 3600,
                "token_type": "Bearer"
            }
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            # Create token manager with expired token
            token_manager = ManagementTokenManager(self.domain, self.client_id, self.client_secret)
            
            # Set an expired token to force refresh
            expired_token_data = {
                "access_token": "expired_token",
                "expires_in": -1,  # Already expired
                "token_type": "Bearer"
            }
            token_manager.set_tokens(expired_token_data)
            
            results = []
            errors = []
            
            def refresh_token_concurrent(thread_id):
                """Get token from each thread (will trigger refresh)."""
                try:
                    start_time = time.time()
                    token = token_manager.get_access_token()
                    elapsed_time = time.time() - start_time
                    results.append((thread_id, token, elapsed_time))
                    return token
                except Exception as e:
                    errors.append((thread_id, str(e)))
                    raise
            
            # Multiple threads trying to refresh expired token simultaneously
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(refresh_token_concurrent, i) for i in range(3)]
                
                for future in as_completed(futures, timeout=10):
                    future.result()
            
            # Should not have any errors
            assert len(errors) == 0, f"Errors during concurrent token refresh: {errors}"
            assert len(results) == 3, f"Expected 3 results, got {len(results)}"
            
            # All threads should get the new token
            for thread_id, token, elapsed_time in results:
                assert token == "refreshed_token", f"Thread {thread_id} got wrong token: {token}"
                assert elapsed_time < 5, f"Thread {thread_id} took too long: {elapsed_time} seconds"

    def test_singleton_pattern_with_threading(self):
        """
        Test the singleton pattern behavior with multiple threads
        creating ManagementTokenManager instances.
        """
        with patch('requests.post') as mock_post:
            # Configure mock
            mock_response = Mock()
            mock_response.json.return_value = {
                "access_token": "singleton_test_token",
                "expires_in": 3600,
                "token_type": "Bearer"
            }
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            managers = []
            errors = []
            
            def create_token_manager(thread_id):
                """Create token manager in each thread."""
                try:
                    manager = ManagementTokenManager(self.domain, self.client_id, self.client_secret)
                    managers.append((thread_id, manager))
                    return manager
                except Exception as e:
                    errors.append((thread_id, str(e)))
                    raise
            
            # Create managers from multiple threads simultaneously
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = [executor.submit(create_token_manager, i) for i in range(3)]
                
                for future in as_completed(futures, timeout=5):
                    future.result()  # This will raise if any thread failed
            
            # Should not have any errors
            assert len(errors) == 0, f"Errors during manager creation: {errors}"
            assert len(managers) == 3, f"Expected 3 managers, got {len(managers)}"
            
            # All managers should be the same instance (singleton)
            first_manager = managers[0][1]
            for i, (thread_id, manager) in enumerate(managers[1:], 1):
                assert manager is first_manager, f"Thread {thread_id} has different manager instance"

    def test_lock_timeout_detection(self):
        """
        Test to ensure locks are not held for unreasonably long periods.
        """
        with patch('requests.post') as mock_post:
            # Simulate a slow network request
            def slow_response(*args, **kwargs):
                time.sleep(1)  # 1-second delay
                mock_response = Mock()
                mock_response.json.return_value = {
                    "access_token": "slow_response_token",
                    "expires_in": 3600,
                    "token_type": "Bearer"
                }
                mock_response.raise_for_status.return_value = None
                return mock_response
            
            mock_post.side_effect = slow_response
            
            token_manager = ManagementTokenManager(self.domain, self.client_id, self.client_secret)
            token_manager.tokens = {}  # Force new token request
            
            # Monitor how long the operation takes
            start_time = time.time()
            
            token = token_manager.get_access_token()
            
            elapsed_time = time.time() - start_time
            
            # Should complete within reasonable time (network delay + processing)
            assert elapsed_time < 5, f"Token request took too long: {elapsed_time} seconds"
            assert token == "slow_response_token"

    def test_deadlock_regression_prevention(self):
        """
        Regression test to ensure the deadlock fix doesn't break in the future.
        This test simulates the exact conditions that caused the original deadlock.
        """
        with patch('requests.post') as mock_post:
            mock_response = Mock()
            mock_response.json.return_value = {
                "access_token": "regression_test_token",
                "expires_in": 3600,
                "token_type": "Bearer"
            }
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            # Test multiple scenarios that could trigger deadlock
            test_scenarios = [
                "scenario_1_fresh_manager",
                "scenario_2_expired_token", 
                "scenario_3_empty_tokens"
            ]
            
            for scenario in test_scenarios:
                with self.subTest(scenario=scenario):
                    ManagementTokenManager.reset_instances()
                    token_manager = ManagementTokenManager(f"{scenario}.kinde.com", "client", "secret")
                    
                    if scenario == "scenario_2_expired_token":
                        # Set expired token
                        token_manager.set_tokens({
                            "access_token": "expired_token",
                            "expires_in": -1,
                            "token_type": "Bearer"
                        })
                    elif scenario == "scenario_3_empty_tokens":
                        # Clear tokens
                        token_manager.tokens = {}
                    
                    # Each scenario should complete without deadlock
                    start_time = time.time()
                    token = token_manager.get_access_token()
                    elapsed_time = time.time() - start_time
                    
                    assert elapsed_time < 1, f"{scenario} took too long: {elapsed_time} seconds"
                    assert token == "regression_test_token"
            
            print("✅ All regression scenarios passed - deadlock fix is stable")


if __name__ == '__main__':
    # Print information about the tests
    print("🔍 KINDE MANAGEMENT CLIENT DEADLOCK TESTS")
    print("=" * 50)
    print("These tests reproduce and verify the fix for the customer's deadlock issue.")
    print("Customer reported: SDK hangs on 'with self.lock:' in set_tokens method")
    print("Fix: Changed threading.Lock() to threading.RLock() for reentrant access")
    print("=" * 50)
    print()
    
    # Run the tests
    unittest.main(verbosity=2)