import base64
import time

import httpx
import pytest

from kinde_sdk.agents import (
    AgentAuthConfig,
    AgentConfigError,
    AuthenticationRequired,
    InsufficientScopeError,
    InvalidTokenError,
    KindeAgentAuth,
    PermissionDeniedError,
    VerificationUnavailableError,
    find_bearer_challenge,
    has_permission,
    require_permission,
)
from testv2.testv2_agents.kinde_fake import (
    APP_ID,
    APP_SECRET,
    DOMAIN,
    ISSUER,
    RESOURCE_URL,
    FakeKinde,
    make_token,
    other_key,
)


def make_auth(fake: FakeKinde, **options) -> KindeAgentAuth:
    config = AgentAuthConfig(
        domain=options.pop("domain", "test.kinde.com"),
        client_id=APP_ID,
        client_secret=APP_SECRET,
        resource_url=options.pop("resource_url", RESOURCE_URL),
        **options,
    )
    return KindeAgentAuth(config, http_client=fake.client(), async_http_client=fake.async_client())


@pytest.fixture
def fake():
    return FakeKinde()


class TestConfig:
    def test_derived_urls(self, fake):
        config = make_auth(fake).config
        assert config.domain == DOMAIN
        assert config.issuer == ISSUER
        assert config.authorization_server_metadata_url == (
            f"{DOMAIN}/.well-known/oauth-authorization-server/oauth2/agents/{APP_ID}"
        )
        assert config.introspection_url == f"{ISSUER}/introspect"
        assert config.revocation_url == f"{ISSUER}/revoke"
        assert config.jwks_url == f"{DOMAIN}/.well-known/jwks"
        assert config.protected_resource_metadata_path == "/.well-known/oauth-protected-resource/mcp"
        assert config.protected_resource_metadata_url == (
            "https://api.example.com/.well-known/oauth-protected-resource/mcp"
        )

    def test_root_resource_has_root_metadata_path(self, fake):
        config = make_auth(fake, resource_url="https://api.example.com/").config
        assert config.protected_resource_metadata_path == "/.well-known/oauth-protected-resource"

    def test_domain_normalisation(self):
        for value in ("test.kinde.com", "https://test.kinde.com/", "https://test.kinde.com"):
            config = AgentAuthConfig(domain=value, client_id=APP_ID, client_secret="x", resource_url=RESOURCE_URL)
            assert config.domain == DOMAIN

    @pytest.mark.parametrize(
        "options",
        [
            {"client_id": ""},
            {"resource_url": "ftp://api.example.com/mcp"},
            {"resource_url": "http://api.example.com/mcp"},
            {"domain": "http://test.kinde.com"},
            {"domain": "https://test.kinde.com/oauth2"},
            {"domain": "https://test.kinde.com@evil.example"},
            {"client_secret": None},
            {"verification": "magic"},
        ],
    )
    def test_rejects_bad_config(self, options):
        values = {"domain": DOMAIN, "client_id": APP_ID, "client_secret": "x", "resource_url": RESOURCE_URL}
        values.update(options)
        with pytest.raises(AgentConfigError):
            AgentAuthConfig(**values)

    def test_jwt_verification_needs_no_secret(self):
        config = AgentAuthConfig(domain=DOMAIN, client_id=APP_ID, resource_url=RESOURCE_URL, verification="jwt")
        assert config.client_secret is None

    def test_loopback_resource_allowed_over_http(self):
        config = AgentAuthConfig(
            domain=DOMAIN, client_id=APP_ID, client_secret="x", resource_url="http://localhost:3001/mcp"
        )
        assert (
            config.protected_resource_metadata_url == "http://localhost:3001/.well-known/oauth-protected-resource/mcp"
        )

    def test_from_env_uses_agents_variables_not_login_app(self, monkeypatch):
        monkeypatch.setenv("KINDE_HOST", "https://test.kinde.com")
        monkeypatch.setenv("KINDE_CLIENT_ID", "login-app")
        monkeypatch.setenv("KINDE_AGENTS_CLIENT_ID", APP_ID)
        monkeypatch.setenv("KINDE_AGENTS_CLIENT_SECRET", "secret")
        monkeypatch.setenv("KINDE_AGENTS_RESOURCE_URL", RESOURCE_URL)
        config = AgentAuthConfig.from_env()
        assert config.client_id == APP_ID
        assert config.issuer == ISSUER

    def test_secret_not_in_repr(self, fake):
        assert APP_SECRET not in repr(make_auth(fake).config)


class TestMetadata:
    def test_protected_resource_metadata(self, fake):
        document = make_auth(fake, resource_name="Docs").protected_resource_metadata()
        assert document == {
            "resource": RESOURCE_URL,
            "authorization_servers": [ISSUER],
            "bearer_methods_supported": ["header"],
            "scopes_supported": ["offline"],
            "resource_name": "Docs",
        }

    def test_offline_always_advertised(self, fake):
        document = make_auth(fake, scopes_supported=["profile", "email"]).protected_resource_metadata()
        assert document["scopes_supported"] == ["offline", "profile", "email"]

    def test_static_as_metadata_supports_cimd(self, fake):
        document = make_auth(fake).authorization_server_metadata()
        assert document["issuer"] == ISSUER
        assert document["client_id_metadata_document_supported"] is True
        assert "openid" not in document["scopes_supported"]

    def test_as_metadata_proxy_is_cached_and_forces_cimd_flag(self, fake):
        fake.as_metadata = {**fake.as_metadata, "client_id_metadata_document_supported": False, "extra": 1}
        auth = make_auth(fake)
        first = auth.fetch_authorization_server_metadata()
        second = auth.fetch_authorization_server_metadata()
        assert first["client_id_metadata_document_supported"] is True
        assert first["extra"] == 1
        assert second == first
        assert fake.count("/oauth2/agents/" + APP_ID) == 1

    async def test_as_metadata_proxy_falls_back_to_static(self):
        def down(request):
            raise httpx.ConnectError("down", request=request)

        config = AgentAuthConfig(domain=DOMAIN, client_id=APP_ID, client_secret="x", resource_url=RESOURCE_URL)
        auth = KindeAgentAuth(config, async_http_client=httpx.AsyncClient(transport=httpx.MockTransport(down)))
        document = await auth.fetch_authorization_server_metadata_async()
        assert document["issuer"] == ISSUER
        assert document["client_id_metadata_document_supported"] is True


class TestChallenges:
    def test_missing_header_challenge_has_no_error(self, fake):
        auth = make_auth(fake)
        with pytest.raises(AuthenticationRequired) as caught:
            auth.authenticate(None)
        response = auth.error_response(caught.value)
        assert response.status_code == 401
        assert response.headers["WWW-Authenticate"] == (
            'Bearer resource_metadata="https://api.example.com/.well-known/oauth-protected-resource/mcp"'
        )
        assert response.headers["Access-Control-Expose-Headers"] == "WWW-Authenticate"

    @pytest.mark.parametrize(
        "header", ["Basic dXNlcjpwYXNz", "Bearer", "Bearer  two-spaces", "Bearer a b", "Token abc"]
    )
    def test_malformed_header_is_invalid_token(self, fake, header):
        auth = make_auth(fake)
        with pytest.raises(InvalidTokenError) as caught:
            auth.authenticate(header)
        response = auth.error_response(caught.value)
        assert response.status_code == 401
        challenge = find_bearer_challenge(response.headers["WWW-Authenticate"])
        assert challenge.get("error") == "invalid_token"
        assert challenge.get("resource_metadata").endswith("/oauth-protected-resource/mcp")
        assert fake.requests == []

    def test_scheme_is_case_insensitive(self, fake):
        token = fake.issue()
        assert make_auth(fake).authenticate(f"bearer {token}").user_id == "kp_user"

    def test_insufficient_scope_challenge(self, fake):
        response = make_auth(fake).error_response(InsufficientScopeError(["email"]))
        assert response.status_code == 403
        challenge = find_bearer_challenge(response.headers["WWW-Authenticate"])
        assert challenge.get("error") == "insufficient_scope"
        assert challenge.get("scope") == "email"

    def test_missing_permission_is_plain_403_without_challenge(self, fake):
        response = make_auth(fake).error_response(PermissionDeniedError(["read:docs"]))
        assert response.status_code == 403
        assert "WWW-Authenticate" not in response.headers
        assert response.body["error"] == "forbidden"

    def test_outage_is_503_without_challenge(self, fake):
        response = make_auth(fake).error_response(VerificationUnavailableError())
        assert response.status_code == 503
        assert "WWW-Authenticate" not in response.headers


class TestIntrospection:
    def test_active_token(self, fake):
        token = fake.issue(
            scope="offline email",
            permissions=["read:docs"],
            roles=[{"id": "r1", "key": "admin", "name": "Admin"}],
            org_code="org_123",
            email="user@example.com",
        )
        context = make_auth(fake).verify_token(token)
        assert context.user_id == "kp_user"
        assert context.client_id == "https://agent.example.com/cimd.json"
        assert context.scopes == ["offline", "email"]
        assert context.permissions == ["read:docs"]
        assert context.roles == ["admin"]
        assert context.org_code == "org_123"
        assert context.email == "user@example.com"
        assert context.expires_at
        assert has_permission(context, "read:docs")
        assert not has_permission(context, "write:docs")
        assert token not in repr(context)

    def test_sends_application_basic_credentials(self, fake):
        token = fake.issue()
        make_auth(fake).verify_token(token)
        request = fake.requests[-1]
        assert str(request.url) == f"{ISSUER}/introspect"
        expected = base64.b64encode(f"{APP_ID}:{APP_SECRET}".encode()).decode()
        assert request.headers["authorization"] == f"Basic {expected}"
        assert request.content == f"token={token}".encode()

    async def test_async_active_token(self, fake):
        token = fake.issue()
        context = await make_auth(fake).verify_token_async(token)
        assert context.user_id == "kp_user"

    def test_inactive_token_as_kinde_answers_it(self, fake):
        # Kinde answers 401 token_inactive: a bad token, not bad application credentials
        auth = make_auth(fake)
        with pytest.raises(InvalidTokenError):
            auth.verify_token(make_token())
        assert auth.error_response(InvalidTokenError()).status_code == 401

    def test_wrong_application_credentials_are_misconfiguration(self, fake, caplog):
        config = AgentAuthConfig(domain=DOMAIN, client_id=APP_ID, client_secret="wrong", resource_url=RESOURCE_URL)
        auth = KindeAgentAuth(config, http_client=fake.client())
        with pytest.raises(VerificationUnavailableError):
            auth.verify_token(fake.issue())
        assert "request_unauthorized" in caplog.text

    def test_inactive_token_as_rfc_7662_answers_it(self, fake):
        fake.inactive_as_200 = True
        with pytest.raises(InvalidTokenError):
            make_auth(fake).verify_token(make_token())

    def test_inactive_token(self, fake):
        with pytest.raises(InvalidTokenError):
            make_auth(fake).verify_token(make_token())

    def test_wrong_audience_from_introspection(self, fake):
        token = fake.issue()
        fake.active_tokens[token]["aud"] = ["https://other.example.com/mcp"]
        with pytest.raises(InvalidTokenError):
            make_auth(fake).verify_token(token)

    def test_expired_by_introspection(self, fake):
        token = fake.issue()
        fake.active_tokens[token]["exp"] = int(time.time()) - 120
        with pytest.raises(InvalidTokenError):
            make_auth(fake).verify_token(token)

    @pytest.mark.parametrize("status", [500, 502, 429])
    def test_kinde_errors_are_unavailable_not_invalid(self, fake, status):
        fake.introspection_status = status
        with pytest.raises(VerificationUnavailableError):
            make_auth(fake).verify_token(fake.issue())

    @pytest.mark.parametrize("status", [401, 404])
    def test_misconfiguration_is_logged_and_unavailable(self, fake, status, caplog):
        fake.introspection_status = status
        with pytest.raises(VerificationUnavailableError):
            make_auth(fake).verify_token(fake.issue())
        assert any(record.levelname == "ERROR" for record in caplog.records)

    async def test_network_failure_is_unavailable(self, fake):
        fake.introspection_raises = True
        with pytest.raises(VerificationUnavailableError):
            await make_auth(fake).verify_token_async(fake.issue())

    def test_positive_results_cached_by_hash(self, fake):
        token = fake.issue()
        auth = make_auth(fake, introspection_cache_seconds=30)
        auth.verify_token(token)
        auth.verify_token(token)
        assert fake.count("/introspect") == 1
        assert token not in auth._introspection_cache

    def test_negative_results_not_cached(self, fake):
        auth = make_auth(fake, introspection_cache_seconds=30)
        token = make_token()
        for _ in range(2):
            with pytest.raises(InvalidTokenError):
                auth.verify_token(token)
        assert fake.count("/introspect") == 2

    def test_cache_off_by_default(self, fake):
        token = fake.issue()
        auth = make_auth(fake)
        auth.verify_token(token)
        auth.verify_token(token)
        assert fake.count("/introspect") == 2

    def test_revoke_uses_application_credentials_and_clears_cache(self, fake):
        token = fake.issue()
        auth = make_auth(fake, introspection_cache_seconds=30)
        auth.verify_token(token)
        auth.revoke_token(token, "access_token")
        request = fake.requests[-1]
        assert str(request.url) == f"{ISSUER}/revoke"
        assert request.headers["authorization"].startswith("Basic ")
        with pytest.raises(InvalidTokenError):
            auth.verify_token(token)

    def test_revoking_one_token_evicts_its_cached_pair(self, fake):
        access_token = fake.issue()
        auth = make_auth(fake, introspection_cache_seconds=30)
        auth.verify_token(access_token)
        auth.revoke_token("paired-refresh-token", "refresh_token")
        fake.active_tokens.pop(access_token)  # Kinde revokes both tokens of the pair
        with pytest.raises(InvalidTokenError):
            auth.verify_token(access_token)


class TestJwtVerification:
    def jwt_auth(self, fake, strategy="jwt"):
        return make_auth(fake, verification=strategy)

    def test_valid_token(self, fake):
        context = self.jwt_auth(fake).verify_token(make_token(permissions=["read:docs"]))
        assert context.user_id == "kp_user"
        assert context.permissions == ["read:docs"]
        assert fake.count("/introspect") == 0

    def test_scoped_issuer_is_rejected(self, fake):
        # The most common bug: iss is the domain, not the scoped issuer
        with pytest.raises(InvalidTokenError):
            self.jwt_auth(fake).verify_token(make_token(iss=ISSUER))

    def test_domain_with_trailing_slash_accepted(self, fake):
        assert self.jwt_auth(fake).verify_token(make_token(iss=DOMAIN + "/")).user_id == "kp_user"

    def test_other_audience_rejected(self, fake):
        with pytest.raises(InvalidTokenError):
            self.jwt_auth(fake).verify_token(make_token(aud=["https://other.example.com/mcp"]))

    def test_audience_array_with_extra_entries(self, fake):
        token = make_token(aud=["https://linked-api.example.com", RESOURCE_URL])
        assert self.jwt_auth(fake).verify_token(token).audience == ["https://linked-api.example.com", RESOURCE_URL]

    def test_audience_compared_exactly(self, fake):
        with pytest.raises(InvalidTokenError):
            self.jwt_auth(fake).verify_token(make_token(aud=[RESOURCE_URL + "/"]))

    def test_expired_beyond_leeway(self, fake):
        with pytest.raises(InvalidTokenError):
            self.jwt_auth(fake).verify_token(make_token(exp_in=-120))

    def test_expired_within_leeway(self, fake):
        assert self.jwt_auth(fake).verify_token(make_token(exp_in=-5)).user_id == "kp_user"

    def test_not_yet_valid(self, fake):
        with pytest.raises(InvalidTokenError):
            self.jwt_auth(fake).verify_token(make_token(nbf=int(time.time()) + 600))

    @pytest.mark.parametrize("algorithm", ["HS256", "none"])
    def test_non_rs256_rejected(self, fake, algorithm):
        if algorithm == "none":
            import jwt as pyjwt

            token = pyjwt.encode(
                {"iss": DOMAIN, "aud": [RESOURCE_URL], "exp": int(time.time()) + 60},
                None,
                algorithm="none",
                headers={"kid": "test-key"},
            )
        else:
            token = make_token(algorithm=algorithm)
        with pytest.raises(InvalidTokenError):
            self.jwt_auth(fake).verify_token(token)
        assert fake.count("/jwks") == 0

    def test_wrong_signature(self, fake):
        with pytest.raises(InvalidTokenError):
            self.jwt_auth(fake).verify_token(make_token(key=other_key()))

    def test_unknown_kid_refetches_once_then_rate_limits(self, fake):
        auth = self.jwt_auth(fake)
        auth.verify_token(make_token())
        assert fake.count("/jwks") == 1
        for _ in range(5):
            with pytest.raises(InvalidTokenError):
                auth.verify_token(make_token(kid="unknown", key=other_key()))
        assert fake.count("/jwks") == 2

    async def test_jwks_unavailable(self, fake):
        fake.jwks_status = 500
        with pytest.raises(VerificationUnavailableError):
            await self.jwt_auth(fake).verify_token_async(make_token())

    def test_stale_jwks_refresh_failure_keeps_cached_keys(self, fake, monkeypatch):
        from kinde_sdk.agents import resource_server

        auth = self.jwt_auth(fake)
        auth.verify_token(make_token())
        fake.jwks_status = 500
        monkeypatch.setattr(resource_server, "_JWKS_CACHE_SECONDS", 0)
        monkeypatch.setattr(resource_server, "_JWKS_RETRY_SECONDS", 0)
        assert auth.verify_token(make_token()).user_id == "kp_user"
        assert fake.count("/jwks") == 2

    @pytest.mark.parametrize("keys", [None, 42, "keys", {"kid": "x"}])
    def test_jwks_without_a_keys_list_is_unavailable(self, fake, keys):
        fake.jwks_body = {"keys": keys}
        with pytest.raises(VerificationUnavailableError):
            self.jwt_auth(fake).verify_token(make_token())

    def test_unknown_kid_during_jwks_outage_is_unavailable(self, fake, monkeypatch):
        from kinde_sdk.agents import resource_server

        auth = self.jwt_auth(fake)
        auth.verify_token(make_token())
        fake.jwks_status = 500
        # The new key might be a rotation we couldn't fetch: 503, not 401
        with pytest.raises(VerificationUnavailableError):
            auth.verify_token(make_token(kid="rotated", key=other_key()))
        fake.jwks_status = 200
        monkeypatch.setattr(resource_server, "_JWKS_MIN_REFETCH_SECONDS", 0)
        with pytest.raises(InvalidTokenError):
            auth.verify_token(make_token(kid="rotated", key=other_key()))

    def test_jwt_plus_introspection_requires_both(self, fake):
        auth = self.jwt_auth(fake, "jwt+introspection")
        with pytest.raises(InvalidTokenError):
            auth.verify_token(make_token())  # signed correctly, but Kinde says inactive
        token = fake.issue()
        assert auth.verify_token(token).user_id == "kp_user"
        assert fake.count("/introspect") == 2


class TestPermissions:
    def test_require_permission(self, fake):
        context = make_auth(fake).verify_token(fake.issue(permissions=["read:docs"]))
        require_permission(context, "read:docs")
        with pytest.raises(PermissionDeniedError) as caught:
            require_permission(context, "read:docs", "write:docs")
        assert caught.value.permissions == ["write:docs"]

    def test_has_permission_without_context(self):
        assert has_permission(None, "read:docs") is False
