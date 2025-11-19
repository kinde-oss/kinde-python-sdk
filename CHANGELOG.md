# Changelog

All notable changes to the Kinde Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2025-10-14

### Fixed
- **Security Improvements**: Fixed XSS vulnerabilities by properly escaping JSON user data and HTML error messages
- **Cookie Security**: Enhanced cookie security and code quality in OAuth server
- **Storage Initialization**: Improved storage initialization with enhanced security logging
- **Error Handling**: Better error handling across multiple modules with proper exception chaining
- **Framework Support**: Fixed framework support for null framework with improved error handling

### Improved
- **Code Quality**: Enhanced error handling, thread safety, and code organization across the SDK
- **Cookie Parsing**: Improved OAuth server functionality with better cookie handling and security
- **Session Management**: Added KindeSessionManagement for standalone mode
- **Configuration**: Simplified configuration error messages and parameter masking logic

## [2.1.1] - 2025-09-04

### Fixed
- **Management API**: Fixed users get/update/delete endpoints to use correct `/api/v1/user?id=...` format
- **Project Configuration**: Updated project configuration and dependencies

### Improved
- **Dependency Management**: Configured Renovate for automated dependency updates

## [2.1.0] - 2025-08-28

### Added
- **Entitlements Support**: Enhanced entitlements functionality with improved API integration
- **Force API Configuration**: Added SDK-level force_api configuration support

## [2.0.10] - 2025-08-07

### Added
- **Reauth Functionality**: Implemented reauth functionality in FastAPI and Flask frameworks
- **HTTPX Upgrade**: Upgraded httpx dependency version for better performance and security

### Improved
- **Code Structure**: Restructured kinde_client_api for improved modularity

## [2.0.9] - 2025-07-15

### Added
- **Token Management**: Enhanced token manager with comprehensive testing and introspection logic
- **Management API**: Improved management API client with better token handling

## [2.0.8] - 2025-07-08

### Fixed
- **Management API**: Resolved mapping and claims logic issues in management and auth modules

## [2.0.6] - 2025-07-08

### Fixed
- **User Details Bug**: Resolved user details bug in SDK components
- **Management API**: Fixed management API client issues and endpoint configurations
- **Project Configuration**: Updated project configuration and dependencies

## [2.0.1] - 2025-07-04

### Added
- **Permissions, Claims, and Feature Flags**: Added comprehensive permissions, claims, and feature flags functionality
- **Billing Profile Support**: Added billing profile support with pricing table key parameter
- **Portal Implementation**: Converted profiles to portals implementation with improved URL handling
- **Management Client**: Added management client wrapper with comprehensive documentation
- **Migration Documentation**: Added detailed migration documentation from v1 to v2

### Fixed
- **Token Claims Handling**: Improved token claims handling with enhanced tests and examples
- **URL Handling**: Improved URL handling in portals authentication
- **Deadlock Issues**: Resolved deadlock issues in management module
- **Dependencies**: Updated project dependencies and requirements
- **Import Issues**: Fixed management client import issues in OpenAPI build process

### Improved
- **Code Coverage**: Enhanced test coverage and added edge cases
- **Framework Support**: Better support for Flask and FastAPI frameworks
- **Error Handling**: Improved error handling across multiple modules