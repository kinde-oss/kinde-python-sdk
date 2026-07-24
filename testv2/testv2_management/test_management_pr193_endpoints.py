"""
HTTP-mocked regression tests for new Management API surface introduced in PR #193.

Covers the 18 new operations across:
- DirectoriesApi
- OrganizationsApi (invites, passkeys, role users)
- RolesApi (system permissions, role users)
- EnvironmentsApi (passkeys)
"""

from __future__ import annotations

import pytest

from kinde_sdk.management.models.create_directory_request import CreateDirectoryRequest
from kinde_sdk.management.models.create_organization_invite_request import (
    CreateOrganizationInviteRequest,
)
from kinde_sdk.management.models.update_directory_request import UpdateDirectoryRequest
from kinde_sdk.management.models.update_organization_passkey_request import (
    UpdateOrganizationPasskeyRequest,
)
from kinde_sdk.management.models.update_passkey_request import UpdatePasskeyRequest
from kinde_sdk.management.models.update_role_system_permissions_request import (
    UpdateRoleSystemPermissionsRequest,
)
from kinde_sdk.management.models.update_role_system_permissions_request_system_permissions_inner import (
    UpdateRoleSystemPermissionsRequestSystemPermissionsInner,
)

from .helpers import ManagementHttpTestCase, assert_auth_header, parse_request_call


class TestDirectoriesApi(ManagementHttpTestCase):
    def test_create_directory(self):
        response_body = {
            "code": "DIRECTORY_CREATED",
            "message": "Directory created",
            "directory": {
                "id": "dir_123",
                "directory_name": "Okta SCIM",
                "status": "Pending",
                "organization_code": "org_abc",
            },
        }
        with self.patch_http(self.mock_response(201, response_body)) as mock_request:
            result = self.client.directories_api.create_directory(
                create_directory_request=CreateDirectoryRequest(
                    org_code="org_abc",
                    directory_name="Okta SCIM",
                    provider_code="okta",
                    enterprise_connection_id="conn_1",
                )
            )

            method, url, headers, body = parse_request_call(mock_request)
            assert method == "POST"
            assert url.endswith("/api/v1/directories")
            assert_auth_header(headers)
            assert body["org_code"] == "org_abc"
            assert body["directory_name"] == "Okta SCIM"
            assert body["provider_code"] == "okta"
            assert body["enterprise_connection_id"] == "conn_1"
            assert result is not None
            assert getattr(result, "directory", None) is not None or (
                isinstance(result, dict) and "directory" in result
            )

    def test_get_directories(self):
        response_body = {
            "code": "OK",
            "message": "Success",
            "directories": [
                {
                    "id": "dir_123",
                    "directory_name": "Okta SCIM",
                    "status": "Active",
                    "organization_code": "org_abc",
                }
            ],
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.directories_api.get_directories(
                organization_code="org_abc", page_size=10
            )

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "GET"
            assert "/api/v1/directories" in url
            assert "organization_code=org_abc" in url
            assert "page_size=10" in url
            assert_auth_header(headers)
            assert result is not None

    def test_get_directory(self):
        response_body = {
            "code": "OK",
            "message": "Success",
            "directory": {
                "id": "dir_123",
                "directory_name": "Okta SCIM",
                "status": "Active",
            },
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.directories_api.get_directory(directory_id="dir_123")

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "GET"
            assert url.endswith("/api/v1/directories/dir_123")
            assert_auth_header(headers)
            assert result is not None

    def test_update_directory(self):
        response_body = {
            "code": "DIRECTORY_UPDATED",
            "message": "Directory updated",
            "directory": {"id": "dir_123", "directory_name": "Renamed", "status": "Active"},
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.directories_api.update_directory(
                directory_id="dir_123",
                update_directory_request=UpdateDirectoryRequest(directory_name="Renamed"),
            )

            method, url, headers, body = parse_request_call(mock_request)
            assert method == "PATCH"
            assert url.endswith("/api/v1/directories/dir_123")
            assert_auth_header(headers)
            assert body["directory_name"] == "Renamed"
            assert result is not None

    def test_delete_directory(self):
        response_body = {"code": "DIRECTORY_DELETED", "message": "Directory deleted"}
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.directories_api.delete_directory(directory_id="dir_123")

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "DELETE"
            assert url.endswith("/api/v1/directories/dir_123")
            assert_auth_header(headers)
            assert result is not None


class TestOrganizationInvitesApi(ManagementHttpTestCase):
    def test_create_organization_invite(self):
        response_body = {
            "code": "INVITE_CREATED",
            "message": "Invite created",
            "invite": {
                "id": "inv_1",
                "code": "invite_code_1",
                "email": "user@example.com",
                "roles": [{"id": "role_1", "key": "admin"}],
            },
        }
        with self.patch_http(self.mock_response(201, response_body)) as mock_request:
            result = self.client.organizations_api.create_organization_invite(
                org_code="org_abc",
                create_organization_invite_request=CreateOrganizationInviteRequest(
                    email="user@example.com",
                    first_name="Ada",
                    last_name="Lovelace",
                    roles=["admin"],
                    send_email=True,
                ),
            )

            method, url, headers, body = parse_request_call(mock_request)
            assert method == "POST"
            assert url.endswith("/api/v1/organization/org_abc/invites")
            assert_auth_header(headers)
            assert body["email"] == "user@example.com"
            assert body["roles"] == ["admin"]
            assert body["send_email"] is True
            assert result is not None

    def test_get_organization_invites(self):
        response_body = {
            "code": "OK",
            "message": "Success",
            "invites": [{"id": "inv_1", "code": "invite_code_1", "email": "user@example.com"}],
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.organizations_api.get_organization_invites(
                org_code="org_abc",
                page_size=5,
                include_revoked=True,
                include_accepted=False,
            )

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "GET"
            assert "/api/v1/organization/org_abc/invites" in url
            assert "page_size=5" in url
            assert "include_revoked=true" in url.lower() or "include_revoked=True" in url
            assert_auth_header(headers)
            assert result is not None

    def test_get_organization_invite(self):
        response_body = {
            "message": "Success",
            "id": "inv_1",
            "code": "invite_code_1",
            "email": "user@example.com",
            "roles": [{"id": "role_1", "key": "admin"}],
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.organizations_api.get_organization_invite(
                org_code="org_abc", invite_code="invite_code_1"
            )

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "GET"
            assert url.endswith("/api/v1/organization/org_abc/invites/invite_code_1")
            assert_auth_header(headers)
            assert result is not None

    def test_delete_organization_invite(self):
        response_body = {"code": "INVITE_DELETED", "message": "Invite deleted"}
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.organizations_api.delete_organization_invite(
                org_code="org_abc", invite_code="invite_code_1"
            )

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "DELETE"
            assert url.endswith("/api/v1/organization/org_abc/invites/invite_code_1")
            assert_auth_header(headers)
            assert result is not None


class TestPasskeysApi(ManagementHttpTestCase):
    def test_get_environment_passkey(self):
        response_body = {"policy": "optional"}
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.environments_api.get_passkey()

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "GET"
            assert url.endswith("/api/v1/passkey")
            assert_auth_header(headers)
            assert result is not None
            assert getattr(result, "policy", None) == "optional" or (
                isinstance(result, dict) and result.get("policy") == "optional"
            )

    def test_update_environment_passkey(self):
        response_body = {"policy": "mandatory"}
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.environments_api.update_passkey(
                update_passkey_request=UpdatePasskeyRequest(policy="mandatory")
            )

            method, url, headers, body = parse_request_call(mock_request)
            # Spec uses PUT for environment passkey update
            assert method == "PUT"
            assert url.endswith("/api/v1/passkey")
            assert_auth_header(headers)
            assert body["policy"] == "mandatory"
            assert result is not None

    def test_get_organization_passkey(self):
        response_body = {
            "policy": "optional",
            "is_override_environment_passkey_settings": True,
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.organizations_api.get_organization_passkey(
                org_code="org_abc"
            )

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "GET"
            assert url.endswith("/api/v1/organizations/org_abc/passkey")
            assert_auth_header(headers)
            assert result is not None

    def test_update_organization_passkey(self):
        response_body = {
            "policy": "off",
            "is_override_environment_passkey_settings": True,
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.organizations_api.update_organization_passkey(
                org_code="org_abc",
                update_organization_passkey_request=UpdateOrganizationPasskeyRequest(
                    policy="off",
                    is_override_environment_passkey_settings=True,
                ),
            )

            method, url, headers, body = parse_request_call(mock_request)
            assert method == "PUT"
            assert url.endswith("/api/v1/organizations/org_abc/passkey")
            assert_auth_header(headers)
            assert body["policy"] == "off"
            assert body["is_override_environment_passkey_settings"] is True
            assert result is not None


class TestRoleSystemPermissionsApi(ManagementHttpTestCase):
    def test_get_system_permissions(self):
        response_body = {
            "code": "OK",
            "message": "Success",
            "system_permissions": [{"id": "sp_1", "key": "read:users"}],
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.roles_api.get_system_permissions(page_size=20)

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "GET"
            assert "/api/v1/system_permissions" in url
            assert "page_size=20" in url
            assert_auth_header(headers)
            assert result is not None

    def test_get_role_system_permissions(self):
        response_body = {
            "code": "OK",
            "message": "Success",
            "system_permissions": [{"id": "sp_1", "key": "read:users"}],
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.roles_api.get_role_system_permissions(role_id="role_1")

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "GET"
            assert url.endswith("/api/v1/roles/role_1/system_permissions")
            assert_auth_header(headers)
            assert result is not None

    def test_update_role_system_permissions(self):
        response_body = {
            "code": "SYSTEM_PERMISSIONS_UPDATED",
            "message": "Updated",
        }
        request = UpdateRoleSystemPermissionsRequest(
            system_permissions=[
                UpdateRoleSystemPermissionsRequestSystemPermissionsInner(
                    id="sp_1", operation=None
                ),
                UpdateRoleSystemPermissionsRequestSystemPermissionsInner(
                    id="sp_2", operation="delete"
                ),
            ]
        )
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.roles_api.update_role_system_permissions(
                role_id="role_1",
                update_role_system_permissions_request=request,
            )

            method, url, headers, body = parse_request_call(mock_request)
            assert method == "PATCH"
            assert url.endswith("/api/v1/roles/role_1/system_permissions")
            assert_auth_header(headers)
            assert isinstance(body["system_permissions"], list)
            assert body["system_permissions"][0]["id"] == "sp_1"
            assert body["system_permissions"][1]["operation"] == "delete"
            assert result is not None

    def test_get_role_users(self):
        response_body = {
            "code": "OK",
            "message": "Success",
            "users": [{"id": "kp_1", "org_codes": ["org_abc"]}],
            "next_token": None,
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.roles_api.get_role_users(
                role_id="role_1", page_size=10, next_token="tok_1"
            )

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "GET"
            assert "/api/v1/roles/role_1/users" in url
            assert "page_size=10" in url
            assert "next_token=tok_1" in url
            assert_auth_header(headers)
            assert result is not None

    def test_get_organization_role_users(self):
        response_body = {
            "code": "OK",
            "message": "Success",
            "users": [{"id": "kp_1"}],
        }
        with self.patch_http(self.mock_response(200, response_body)) as mock_request:
            result = self.client.organizations_api.get_organization_role_users(
                org_code="org_abc", role_id="role_1", page_size=5
            )

            method, url, headers, _ = parse_request_call(mock_request)
            assert method == "GET"
            assert "/api/v1/organizations/org_abc/roles/role_1/users" in url
            assert "page_size=5" in url
            assert_auth_header(headers)
            assert result is not None


@pytest.mark.parametrize(
    "attr_name",
    [
        "directories_api",
        "organizations_api",
        "roles_api",
        "environments_api",
    ],
)
def test_pr193_apis_exposed_on_client(attr_name):
    """Smoke: PR #193-related API attributes remain dynamically exposed."""
    from .helpers import build_management_client

    client = build_management_client()
    assert hasattr(client, attr_name)
    assert hasattr(getattr(client, attr_name), "api_client")
