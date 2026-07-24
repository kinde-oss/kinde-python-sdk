"""
Pydantic round-trip regression for models added/changed in PR #193.
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from kinde_sdk.management.models.create_directory_request import CreateDirectoryRequest
from kinde_sdk.management.models.create_directory_response import CreateDirectoryResponse
from kinde_sdk.management.models.create_organization_invite_request import (
    CreateOrganizationInviteRequest,
)
from kinde_sdk.management.models.create_organization_invite_response import (
    CreateOrganizationInviteResponse,
)
from kinde_sdk.management.models.delete_directory_response import DeleteDirectoryResponse
from kinde_sdk.management.models.directory import Directory
from kinde_sdk.management.models.get_directories_response import GetDirectoriesResponse
from kinde_sdk.management.models.get_directory_response import GetDirectoryResponse
from kinde_sdk.management.models.get_organization_invite_response import (
    GetOrganizationInviteResponse,
)
from kinde_sdk.management.models.get_organization_invites_response import (
    GetOrganizationInvitesResponse,
)
from kinde_sdk.management.models.get_organization_passkey200_response import (
    GetOrganizationPasskey200Response,
)
from kinde_sdk.management.models.get_organization_role_users_response import (
    GetOrganizationRoleUsersResponse,
)
from kinde_sdk.management.models.get_passkey200_response import GetPasskey200Response
from kinde_sdk.management.models.get_role_users_response import GetRoleUsersResponse
from kinde_sdk.management.models.get_system_permissions_response import (
    GetSystemPermissionsResponse,
)
from kinde_sdk.management.models.identity import Identity
from kinde_sdk.management.models.organization_invite import OrganizationInvite
from kinde_sdk.management.models.role_system_permissions_response import (
    RoleSystemPermissionsResponse,
)
from kinde_sdk.management.models.set_user_password_request import SetUserPasswordRequest
from kinde_sdk.management.models.system_permissions import SystemPermissions
from kinde_sdk.management.models.update_directory_request import UpdateDirectoryRequest
from kinde_sdk.management.models.update_directory_response import UpdateDirectoryResponse
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
from kinde_sdk.management.models.update_role_system_permissions_response import (
    UpdateRoleSystemPermissionsResponse,
)
from kinde_sdk.management.models.users_response_users_inner_identities_inner import (
    UsersResponseUsersInnerIdentitiesInner,
)


def _round_trip(model_cls, payload: dict):
    instance = model_cls.from_dict(payload)
    assert instance is not None
    as_dict = instance.to_dict()
    # Re-hydrate from serialized form
    again = model_cls.from_dict(as_dict)
    assert again is not None
    # JSON path also works
    from_json = model_cls.from_json(json.dumps(as_dict))
    assert from_json is not None
    return instance, as_dict


class TestDirectoryModels:
    def test_create_directory_request_round_trip(self):
        instance, data = _round_trip(
            CreateDirectoryRequest,
            {
                "org_code": "org_abc",
                "directory_name": "Okta SCIM",
                "provider_code": "okta",
                "enterprise_connection_id": "conn_1",
            },
        )
        assert instance.provider_code == "okta"
        assert data["provider_code"] == "okta"

    def test_create_directory_request_rejects_invalid_provider(self):
        with pytest.raises(ValidationError):
            CreateDirectoryRequest(
                org_code="org_abc",
                directory_name="Bad",
                provider_code="not_a_provider",
            )

    def test_directory_status_enum(self):
        directory = Directory.from_dict(
            {
                "id": "dir_1",
                "directory_name": "Okta",
                "status": "Active",
                "organization_code": "org_abc",
            }
        )
        assert directory.status == "Active"
        with pytest.raises(ValidationError):
            Directory(status="Nope")

    def test_directory_response_models(self):
        _round_trip(
            CreateDirectoryResponse,
            {
                "code": "CREATED",
                "message": "ok",
                "directory": {"id": "dir_1", "status": "Pending"},
            },
        )
        _round_trip(
            GetDirectoryResponse,
            {"code": "OK", "message": "ok", "directory": {"id": "dir_1"}},
        )
        _round_trip(
            GetDirectoriesResponse,
            {
                "code": "OK",
                "message": "ok",
                "directories": [{"id": "dir_1", "status": "Active"}],
            },
        )
        _round_trip(
            UpdateDirectoryResponse,
            {
                "code": "UPDATED",
                "message": "ok",
                "directory": {"id": "dir_1", "directory_name": "Renamed"},
            },
        )
        _round_trip(DeleteDirectoryResponse, {"code": "DELETED", "message": "ok"})
        _round_trip(UpdateDirectoryRequest, {"directory_name": "Renamed"})


class TestOrganizationInviteModels:
    def test_create_invite_request_validation(self):
        req = CreateOrganizationInviteRequest(
            email="user@example.com",
            roles=["admin"],
            send_email=False,
        )
        data = req.to_dict()
        assert data["email"] == "user@example.com"
        assert data["roles"] == ["admin"]

        with pytest.raises(ValidationError):
            CreateOrganizationInviteRequest(
                email="x" * 255,
                roles=["admin"],
            )

    def test_invite_response_round_trips(self):
        _round_trip(
            CreateOrganizationInviteResponse,
            {
                "code": "INVITE_CREATED",
                "message": "ok",
                "invite": {
                    "id": "inv_1",
                    "code": "invite_code_1",
                    "email": "user@example.com",
                },
            },
        )
        _round_trip(
            GetOrganizationInviteResponse,
            {
                "message": "ok",
                "id": "inv_1",
                "code": "invite_code_1",
                "email": "user@example.com",
                "roles": [{"id": "role_1", "key": "admin"}],
            },
        )
        _round_trip(
            GetOrganizationInvitesResponse,
            {
                "code": "OK",
                "message": "ok",
                "invites": [
                    {
                        "id": "inv_1",
                        "code": "invite_code_1",
                        "email": "user@example.com",
                    }
                ],
            },
        )
        _round_trip(
            OrganizationInvite,
            {
                "id": "inv_1",
                "code": "invite_code_1",
                "email": "user@example.com",
                "is_revoked": False,
            },
        )


class TestPasskeyModels:
    def test_passkey_policy_enums(self):
        env = UpdatePasskeyRequest(policy="mandatory")
        assert env.to_dict()["policy"] == "mandatory"
        with pytest.raises(ValidationError):
            UpdatePasskeyRequest(policy="sometimes")

        org = UpdateOrganizationPasskeyRequest(
            policy="optional", is_override_environment_passkey_settings=True
        )
        assert org.to_dict()["is_override_environment_passkey_settings"] is True

        _round_trip(
            GetPasskey200Response,
            {"policy": "optional", "enabled": True, "code": "OK", "message": "ok"},
        )
        _round_trip(
            GetOrganizationPasskey200Response,
            {
                "policy": "off",
                "is_override_environment_passkey_settings": False,
            },
        )


class TestRoleSystemPermissionModels:
    def test_system_permissions_round_trip(self):
        _round_trip(
            SystemPermissions,
            {"id": "sp_1", "key": "read:users", "name": "Read users"},
        )
        _round_trip(
            GetSystemPermissionsResponse,
            {
                "code": "OK",
                "message": "ok",
                "system_permissions": [{"id": "sp_1", "key": "read:users"}],
            },
        )
        _round_trip(
            RoleSystemPermissionsResponse,
            {
                "code": "OK",
                "message": "ok",
                "system_permissions": [{"id": "sp_1", "key": "read:users"}],
            },
        )
        req = UpdateRoleSystemPermissionsRequest(
            system_permissions=[
                UpdateRoleSystemPermissionsRequestSystemPermissionsInner(
                    id="sp_1"
                ),
                UpdateRoleSystemPermissionsRequestSystemPermissionsInner(
                    id="sp_2", operation="delete"
                ),
            ]
        )
        data = req.to_dict()
        assert data["system_permissions"][1]["operation"] == "delete"
        _round_trip(
            UpdateRoleSystemPermissionsResponse,
            {"code": "UPDATED", "message": "ok"},
        )

    def test_role_users_responses(self):
        _round_trip(
            GetRoleUsersResponse,
            {
                "code": "OK",
                "message": "ok",
                "users": [{"id": "kp_1", "org_codes": ["org_abc"]}],
            },
        )
        _round_trip(
            GetOrganizationRoleUsersResponse,
            {
                "code": "OK",
                "message": "ok",
                "users": [{"id": "kp_1"}],
            },
        )


class TestModifiedModels:
    def test_identity_connection_id(self):
        identity = Identity.from_dict(
            {
                "id": "id_1",
                "type": "email",
                "name": "user@example.com",
                "connection_id": "conn_social_1",
                "is_primary": True,
            }
        )
        data = identity.to_dict()
        assert data["connection_id"] == "conn_social_1"

        # Explicit None should be preserved when set
        identity_none = Identity(id="id_2", connection_id=None)
        assert "connection_id" in identity_none.model_fields_set

    def test_set_user_password_pbkdf2_fields(self):
        req = SetUserPasswordRequest(
            hashed_password="abc123",
            hashing_method="pbkdf2",
            salt="c2FsdA==",
            iterations=24000,
            variant="salted-pbkdf2-hmac-sha256",
        )
        data = req.to_dict()
        assert data["hashing_method"] == "pbkdf2"
        assert data["iterations"] == 24000
        assert data["variant"] == "salted-pbkdf2-hmac-sha256"

        with pytest.raises(ValidationError):
            SetUserPasswordRequest(
                hashed_password="abc",
                hashing_method="argon2",
            )

    def test_users_response_identity_inner(self):
        _round_trip(
            UsersResponseUsersInnerIdentitiesInner,
            {
                "type": "email",
                "identity": "user@example.com",
                "connection_id": None,
            },
        )
