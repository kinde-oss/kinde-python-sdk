import json

import pytest

from kinde_sdk.agents import (
    AgentConfigError,
    build_challenge,
    build_client_metadata_document,
    client_metadata_response,
    find_bearer_challenge,
    parse_www_authenticate,
)

CIMD_URL = "https://agent.onzs.co.za/oauth/client-metadata.json"


class TestWwwAuthenticate:
    def test_build_quotes_and_escapes(self):
        header = build_challenge("Bearer", [("error", "invalid_token"), ("error_description", 'say "hi" \\ bye')])
        assert header == 'Bearer error="invalid_token", error_description="say \\"hi\\" \\\\ bye"'
        assert find_bearer_challenge(header).get("error_description") == 'say "hi" \\ bye'

    def test_build_without_params(self):
        assert build_challenge("Bearer") == "Bearer"

    def test_several_challenges_with_commas_inside_quotes(self):
        challenges = parse_www_authenticate(
            'Basic realm="a, b", Bearer error="invalid_token", error_description="bad, very bad", '
            'resource_metadata="https://api.example.com/.well-known/oauth-protected-resource/mcp"'
        )
        assert [c.scheme for c in challenges] == ["Basic", "Bearer"]
        assert challenges[0].get("realm") == "a, b"
        bearer = challenges[1]
        assert bearer.get("error_description") == "bad, very bad"
        assert bearer.get("resource_metadata").endswith("/oauth-protected-resource/mcp")

    def test_case_insensitive_scheme_and_names(self):
        challenge = find_bearer_challenge('BEARER Resource_Metadata="https://x/y"')
        assert challenge.get("resource_metadata") == "https://x/y"

    def test_several_header_values(self):
        challenge = find_bearer_challenge(["Negotiate abc==", 'Bearer scope="offline email"'])
        assert challenge.get("scope") == "offline email"

    def test_token68(self):
        challenges = parse_www_authenticate("Negotiate a87421000492aa874209af8bc028==, Bearer")
        assert challenges[0].token68 == "a87421000492aa874209af8bc028=="
        assert challenges[1].scheme == "Bearer"

    def test_unquoted_values(self):
        assert find_bearer_challenge("Bearer error=invalid_token").get("error") == "invalid_token"

    @pytest.mark.parametrize("header", ["", ",,,", "=x", 'Bearer error="unterminated', "\x00\x01"])
    def test_malformed_input_never_raises(self, header):
        parse_www_authenticate(header)

    def test_none(self):
        assert parse_www_authenticate(None) == []
        assert find_bearer_challenge(None) is None


class TestClientMetadataDocument:
    def test_builds_document(self):
        document = build_client_metadata_document(
            CIMD_URL,
            "Onzs Agent",
            ["https://agent.onzs.co.za/oauth/callback", "http://127.0.0.1/callback", "http://localhost:8765/cb"],
            client_uri="https://agent.onzs.co.za",
        )
        assert document == {
            "client_id": CIMD_URL,
            "client_name": "Onzs Agent",
            "redirect_uris": [
                "https://agent.onzs.co.za/oauth/callback",
                "http://127.0.0.1/callback",
                "http://localhost:8765/cb",
            ],
            "grant_types": ["authorization_code", "refresh_token"],
            "response_types": ["code"],
            "token_endpoint_auth_method": "none",
            "client_uri": "https://agent.onzs.co.za",
        }

    @pytest.mark.parametrize(
        "client_id",
        [
            "https://agent.onzs.co.za",
            "https://agent.onzs.co.za/",
            "http://agent.onzs.co.za/cimd.json",
            "https://user@agent.onzs.co.za/cimd.json",
            "https://agent.onzs.co.za/cimd.json?v=1",
            "https://agent.onzs.co.za/cimd.json#x",
            "https://localhost/cimd.json",
        ],
    )
    def test_rejects_bad_client_id(self, client_id):
        with pytest.raises(AgentConfigError):
            build_client_metadata_document(client_id, "Agent", ["http://127.0.0.1/callback"])

    def test_requires_name_and_redirects(self):
        with pytest.raises(AgentConfigError):
            build_client_metadata_document(CIMD_URL, " ", ["http://127.0.0.1/callback"])
        with pytest.raises(AgentConfigError):
            build_client_metadata_document(CIMD_URL, "Agent", [])

    @pytest.mark.parametrize(
        "redirect_uri",
        ["https://other.example.com/callback", "myapp://callback", "http://agent.onzs.co.za/callback"],
    )
    def test_redirects_kinde_would_drop(self, redirect_uri):
        with pytest.raises(AgentConfigError):
            build_client_metadata_document(CIMD_URL, "Agent", [redirect_uri])
        with pytest.warns(UserWarning):
            build_client_metadata_document(CIMD_URL, "Agent", [redirect_uri], strict=False)

    @pytest.mark.parametrize("redirect_uri", ["https://agent.onzs.co.za/cb#frag", "https://u:p@agent.onzs.co.za/cb"])
    def test_fragment_and_userinfo_always_fatal(self, redirect_uri):
        with pytest.raises(AgentConfigError):
            build_client_metadata_document(CIMD_URL, "Agent", [redirect_uri], strict=False)

    def test_response_headers(self):
        document = build_client_metadata_document(CIMD_URL, "Agent", ["http://127.0.0.1/callback"])
        body, headers = client_metadata_response(document)
        assert json.loads(body) == document
        assert headers == {"Content-Type": "application/json", "Cache-Control": "public, max-age=3600"}

    def test_size_limit(self):
        with pytest.raises(AgentConfigError):
            build_client_metadata_document(CIMD_URL, "Agent", ["http://127.0.0.1/callback"], padding="x" * 70000)
