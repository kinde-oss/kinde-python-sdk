# Changelog

All notable changes to the Kinde Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.9] - 2024-12-19

### Fixed
- **OAuth2 Introspection Authentication**: Fixed `validate_and_set_via_introspection` method to use Bearer token authentication instead of client credentials for the introspection endpoint. This resolves 401 Unauthorized errors when validating bearer tokens.
- **Token Expiration Handling**: Fixed edge case in `set_tokens` method where `expires_in=0` was being treated as `None` and defaulting to 3600 seconds. Now properly handles zero expiration values.
- **Exception Handling**: Improved exception handling in introspection method with proper exception chaining for better error reporting and debugging.

### Improved
- **Code Quality**: Simplified expiration calculation in introspection method using conditional expression for cleaner code.
- **Test Coverage**: Added comprehensive unit tests for the `validate_and_set_via_introspection` method covering success cases, error scenarios, edge cases, and thread safety.
- **Documentation**: Fixed logging in FastAPI example to correctly access `UsersResponse` object properties.

### Technical Details
- The introspection method now first obtains a management token using client credentials, then uses that token to authenticate the introspection request with Bearer authentication
- Added proper timeout handling (30 seconds) for introspection requests
- Improved thread safety with proper locking mechanisms
- Enhanced error messages for better debugging

## [2.0.8] - Previous Release

Initial release of Kinde Python SDK v2.0.x series. 