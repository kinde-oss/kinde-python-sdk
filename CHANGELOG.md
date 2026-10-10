# Changelog

All notable changes to the Kinde Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security
- **Secrets in session storage**: `client_secret` is no longer written to session storage
  (which may be a browser cookie); it is kept in process memory. Legacy sessions that still
  contain it are cleaned on load and save.
- **Secrets in logs**: the SDK no longer logs the token-exchange payload or response, the OAuth
  `state`, session contents, user details or storage values, and no longer raises its own
  loggers to INFO.
- **Token endpoint errors**: a failed code exchange now reports only the HTTP status and the
  standard OAuth `error` code. The response body is no longer included in exceptions, logs, or
  the Flask / FastAPI callback responses, which now return a generic HTTP 400.
- **OAuth callback validation**: `state` is always required and must match the login started
  in the same session; the ID token `nonce` is verified. Both are single-use.
- **FastAPI**: the callback no longer forwards the consumed `state` to the post-login URL, and
  logout now clears the user's server-side tokens (previously only the session cookie was
  cleared).
- **Flask**: the session is bound to a user only after a successful callback.
- **Account API errors**: the permissions, roles and feature flag helpers log only the
  exception type and HTTP status when an Account API call fails, not the response body.

### Changed
- Callbacks without a `state` parameter, and token responses without an ID token (e.g. custom
  scopes that omit `openid`), are now rejected.

### Fixed
- **Token refresh deadlock**: `TokenManager.get_access_token()` hung forever when the access
  token had expired and a refresh token was available (non-reentrant lock re-acquired in
  `set_tokens`).
- **Account API host**: permission, role and feature flag lookups with `force_api=True` were sent
  to the generated client's placeholder host (`your_kinde_subdomain.kinde.com`) and silently
  returned empty results. They now use the issuer of the user's access token, falling back to
  `KINDE_HOST`.
- **Account API permissions**: with `force_api=True`, `get_permission()` never granted anything
  because the API's `{id, name, key}` objects were compared with the key string;
  `get_permissions()` now returns keys, as in token mode.
- **Account API feature flags**: with `force_api=True`, flags were read from a non-existent
  `data.flags` attribute and always came back empty; the `data.feature_flags` list is now parsed.
- **Management API feature flags**: `environments_api.get_environement_feature_flags()` and
  `organizations_api.get_organization_feature_flags()` raised a `ValidationError` for any
  boolean or integer flag, because the published spec declares every flag value as a string.
  Values are now `bool`, `int` or `str`, and the generator re-applies the correction
  (`SPEC_ERRATA` in `generate_management_sdk.py`) until the spec is fixed upstream.
- **Signed out after a restart or on another worker**: session data is keyed by a device ID that
  was generated per process and never saved (there is no request at startup), so after a restart,
  or with several workers (e.g. `gunicorn -w 4`), the tokens in a user's session couldn't be found.
  The device ID is now stored in the user's session and read from there. Sessions created
  before this fix will need to sign in once more.
- **Refreshed tokens persisted**: tokens from a refresh were only kept in process memory, so with
  server-side or cookie sessions, a restart or another worker kept using (and refreshing with) the
  old ones. `UserSession` now writes them back to session storage after every refresh.
- **StorageManager.reset() deadlock**: `reset()` held the class lock while calling `initialize()`,
  which takes the same non-reentrant lock; the lock is now reentrant.
- **KindeSessionManagement**: the standalone-only guard never fired, because constructing the
  `NullFramework` singleton always marks it initialized; it now raises inside Flask / FastAPI
  apps as documented, and requires a standalone `OAuth` client to exist.
- **Feature flag codes**: `get_all_flags()` in token mode returned flags with an empty `code`.
- **Logout redirect**: the logout URL now includes the `redirect` parameter that Kinde's
  `/logout` endpoint reads (`redirect_uri` is still sent). The target is
  `post_logout_redirect_uri`, then the new `KINDE_POST_LOGOUT_REDIRECT_URI` environment
  variable, then `KINDE_REDIRECT_URI` as before, so the built-in `/logout` routes can return
  users to your home page instead of the callback.
- Previously unbounded `requests` calls now use a 30 second timeout.
- **CI**: Hardened `renovate.json` so Renovate can no longer re-propose bumping the Python
  `<3.12` `django` pin in `requirements.txt` to Django 6.x (Django 6.0+ requires Python
  3.12+). Django is a test-only dependency for this SDK (no runtime usage), and the
  `>=4.2.0,<5.0.0` pin for `python_version < "3.12"` is intentional; the same breaking
  bump was already rejected once in PR #198 and recurred in PR #200.

## [2.4.0] - 2026-08-20

### Added
- **Management client**: Regenerated from the latest OpenAPI spec, adding the `directories_api`
  and `environments_api` namespaces, plus expanded `organizations_api`, `roles_api`, `users_api`
  and `applications_api` surfaces (including application access roles and billing customer
  endpoints/models)

### Improved
- **Documentation**: Refreshed `README_management_client.md` examples to use the namespaced
  management client accessors (e.g. `client.users_api.get_users()`,
  `client.environments_api.get_environement_feature_flags()`) instead of the flattened,
  deprecated top-level methods
- **CI**: Bumped `actions/setup-python` to v7

## [2.3.1] - 2026-07-06

### Fixed
- **Dependencies (security)**: Updated `cryptography` (v48, then v49), `requests` (2.33.1, 2.34.0, then 2.34.2 with Python-version-specific pins), and `pytest` (^9.0.3, addressing CVE-2025-71176)
- **CI**: Fixed the test suite for Django 6 on Python 3.9–3.11 and corrected the `requests` marker for Python 3.9

### Improved
- **Dependencies**: Upgraded `django` to v6 and `pylint` to v4 for the development toolchain; bumped `actions/checkout` and `codecov/codecov-action` to v7
- **Versioning**: Consolidated the SDK version into a single source of truth in `kinde_sdk/_version.py`, extracted shared helpers into `_sdk_generator_utils.py`, and made the OpenAPI generator configs derived artifacts via an `SDK_VERSION` placeholder
- **Housekeeping**: Removed an incidental `poetry.lock` (the project uses setuptools)

## [2.3.0] - 2026-04-16

### Added
- **OAuth & management**: Invitation codes in the OAuth login flow; management client regenerated from the latest spec (OpenAPI Generator 7.19) with improved dynamic OpenAPI class generation
- **Documentation**: README development setup and refreshed management client examples

### Fixed
- **Auth & frameworks**: OAuth fixes for FastAPI and Flask (including call signatures and namespaced state keys), hardened example apps, and more reliable Flask async handling and tests
- **Management client**: Wrapper and token handling corrections, plus fetching the OpenAPI spec from the canonical URL
- **Build & tests**: Dependency and security alignment (`requirements.txt` / Snyk), pytest-cov v7–compatible coverage configuration

### Improved
- **Management client**: DRYer delegation over the generated management API
- **Dependencies & CI**: Wider compatible ranges (including Python-specific `requests` pins), routine dependency bumps, updated GitHub Actions, Python 3.9–friendly pylint tooling, and removal of unused generated OpenAPI test stubs

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