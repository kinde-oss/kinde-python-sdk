# Async/Sync Consistency Tests

This directory contains comprehensive tests for the new async/sync consistency solution in the Kinde Python SDK.

## Overview

The tests verify that the new SmartOAuth, AsyncOAuth, and factory function work correctly in both synchronous and asynchronous contexts, providing a consistent API while maintaining backward compatibility.

## Test Files

### 1. `test_smart_oauth.py`
Tests for the SmartOAuth client that automatically adapts to sync/async contexts.

**Key Test Areas:**
- Context detection (sync vs async)
- Warning behavior when using sync methods in async contexts
- Method delegation to underlying clients
- Error handling and exception propagation
- Integration with both sync and async methods

**Test Classes:**
- `TestSmartOAuthContextDetection` - Tests context detection functionality
- `TestSmartOAuthSyncMethods` - Tests sync methods in sync context
- `TestSmartOAuthAsyncMethods` - Tests async methods
- `TestSmartOAuthWarningBehavior` - Tests warning behavior
- `TestSmartOAuthAttributeDelegation` - Tests attribute delegation
- `TestSmartOAuthInitialization` - Tests initialization
- `TestSmartOAuthErrorHandling` - Tests error handling
- `TestSmartOAuthIntegration` - Integration tests
- `TestCreateOAuthClientFactory` - Tests factory function

### 2. `test_async_oauth.py`
Tests for the AsyncOAuth client that provides async versions of all OAuth operations.

**Key Test Areas:**
- Async method implementations
- Integration with async helper functions
- Error handling for async operations
- Parameter passing and delegation

**Test Classes:**
- `TestAsyncOAuthInitialization` - Tests initialization
- `TestAsyncOAuthSyncMethods` - Tests sync method delegation
- `TestAsyncOAuthAsyncMethods` - Tests async methods
- `TestAsyncOAuthAttributeDelegation` - Tests attribute delegation
- `TestAsyncOAuthErrorHandling` - Tests error handling
- `TestAsyncOAuthIntegration` - Integration tests
- `TestAsyncOAuthHelperIntegration` - Tests helper function integration

### 3. `test_factory_function.py`
Tests for the factory function that creates appropriate OAuth clients.

**Key Test Areas:**
- Client type selection based on `async_mode` parameter
- Argument passing to different client types
- Error handling during client creation
- Consistent behavior across multiple calls

**Test Classes:**
- `TestCreateOAuthClientFactory` - Tests factory function
- `TestFactoryFunctionIntegration` - Integration tests

### 4. `test_smart_oauth_integration.py`
Integration tests that verify SmartOAuth works in real-world scenarios.

**Key Test Areas:**
- Real-world application scenarios (Flask, FastAPI)
- Performance characteristics
- Memory usage and thread safety
- Context switching behavior

**Test Classes:**
- `TestSmartOAuthRealWorldScenarios` - Real-world scenario tests
- `TestSmartOAuthContextSwitching` - Context switching tests
- `TestSmartOAuthPerformance` - Performance tests
- `TestSmartOAuthMemoryUsage` - Memory usage tests
- `TestSmartOAuthThreadSafety` - Thread safety tests

## Running the Tests

### Prerequisites

```bash
pip install pytest pytest-asyncio
```

### Run All Tests

```bash
# From the project root
python testv2/run_async_sync_tests.py
```

### Run Individual Test Files

```bash
# Run SmartOAuth tests
pytest testv2/testv2_auth/test_smart_oauth.py -v

# Run AsyncOAuth tests
pytest testv2/testv2_auth/test_async_oauth.py -v

# Run factory function tests
pytest testv2/testv2_auth/test_factory_function.py -v

# Run integration tests
pytest testv2/testv2_auth/test_smart_oauth_integration.py -v
```

### Run with Coverage

```bash
# Install coverage
pip install coverage

# Run tests with coverage
pytest --cov=kinde_sdk.auth.smart_oauth --cov=kinde_sdk.auth.async_oauth --cov=kinde_sdk.auth.base_oauth --cov-report=html testv2/testv2_auth/test_*.py
```

## Test Coverage

The tests cover:

### SmartOAuth
- ✅ Context detection (sync/async)
- ✅ Warning behavior
- ✅ Method delegation
- ✅ Error handling
- ✅ Attribute delegation
- ✅ Initialization
- ✅ Integration scenarios

### AsyncOAuth
- ✅ Async method implementations
- ✅ Sync method delegation
- ✅ Helper function integration
- ✅ Error handling
- ✅ Parameter passing

### Factory Function
- ✅ Client type selection
- ✅ Argument passing
- ✅ Error handling
- ✅ Consistent behavior

### Integration
- ✅ Real-world scenarios
- ✅ Performance characteristics
- ✅ Memory usage
- ✅ Thread safety
- ✅ Context switching

## Test Scenarios

### Flask Application (Sync Context)
```python
# Tests verify that SmartOAuth works correctly in sync contexts
oauth = SmartOAuth(framework="flask", app=app)
is_auth = oauth.is_authenticated()  # No warnings
user_info = oauth.get_user_info()   # No warnings
```

### FastAPI Application (Async Context)
```python
# Tests verify that SmartOAuth works correctly in async contexts
oauth = SmartOAuth(framework="fastapi", app=app)
user_info = await oauth.get_user_info_async()  # Preferred
is_auth = oauth.is_authenticated()  # Shows warning
```

### Mixed Context Usage
```python
# Tests verify that SmartOAuth handles mixed usage correctly
oauth = SmartOAuth(framework="fastapi", app=app)
# Sync operations
is_auth = oauth.is_authenticated()
# Async operations
user_info = await oauth.get_user_info_async()
```

## Expected Test Results

When all tests pass, you should see:

```
✅ All tests together: PASSED
✅ Individual test suites: PASSED
✅ Coverage tests: PASSED

🎉 All tests passed! The async/sync consistency solution is working correctly.
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure you're running from the project root
   - Check that `kinde_sdk` is in your Python path

2. **Missing Dependencies**
   - Install required packages: `pip install pytest pytest-asyncio coverage`

3. **Test Failures**
   - Check that the new async/sync modules are properly implemented
   - Verify that imports are correct
   - Ensure mock objects are properly configured

### Debugging

To debug test failures:

```bash
# Run with verbose output
pytest testv2/testv2_auth/test_smart_oauth.py -v -s

# Run specific test
pytest testv2/testv2_auth/test_smart_oauth.py::TestSmartOAuthContextDetection::test_is_async_context_in_sync -v -s

# Run with full traceback
pytest testv2/testv2_auth/test_smart_oauth.py --tb=long
```

## Contributing

When adding new tests:

1. Follow the existing naming conventions
2. Use descriptive test names
3. Add appropriate docstrings
4. Include both positive and negative test cases
5. Test error conditions and edge cases
6. Ensure tests are isolated and don't depend on each other

## Test Maintenance

- Keep tests up to date with API changes
- Add tests for new features
- Remove tests for deprecated functionality
- Update mocks when dependencies change
- Monitor test performance and optimize if needed
