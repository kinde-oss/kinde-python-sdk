"""
Smoke checks for a Kinde "AI agents and MCP" setup, run against real Kinde and your local server.

Reads the same environment as the examples (KINDE_HOST, KINDE_AGENTS_CLIENT_ID,
KINDE_AGENTS_CLIENT_SECRET, KINDE_AGENTS_RESOURCE_URL). Start mcp_server.py first.

    python examples/agents/smoke_check.py
    python examples/agents/smoke_check.py --cimd-url https://agent.onzs.co.za/oauth/client-metadata.json
    python examples/agents/smoke_check.py --token "$ACCESS_TOKEN"     # a token an agent received

Tokens and secrets are never printed. Exits non-zero if any check fails.
"""

import argparse
import json
import sys

import httpx
import jwt

from kinde_sdk.agents import AgentAuthConfig, find_bearer_challenge, validate_client_metadata_url

results = {"PASS": 0, "WARN": 0, "FAIL": 0}


def report(status: str, message: str) -> None:
    results[status] += 1
    print(f"  [{status}] {message}")


def check(condition: bool, message: str, warn_only: bool = False) -> bool:
    report("PASS" if condition else ("WARN" if warn_only else "FAIL"), message)
    return condition


def get_json(client: httpx.Client, url: str):
    try:
        response = client.get(url)
    except httpx.HTTPError as exc:
        report("FAIL", f"GET {url}: {type(exc).__name__}")
        return None, None
    try:
        body = response.json()
    except ValueError:
        return response, None
    return response, body if isinstance(body, dict) else None


def check_kinde_discovery(client: httpx.Client, config: AgentAuthConfig) -> None:
    print(f"\n1. Kinde discovery: {config.authorization_server_metadata_url}")
    response, document = get_json(client, config.authorization_server_metadata_url)
    if response is None:
        return
    if not check(
        response.status_code == 200, f"HTTP {response.status_code} (404 means the flag is off or the app ID is wrong)"
    ):
        return
    if not check(document is not None, "the body is a JSON object"):
        return
    check(document.get("issuer") == config.issuer, f"issuer is the scoped issuer {config.issuer}")
    check(
        document.get("client_id_metadata_document_supported") is True, "client_id_metadata_document_supported is true"
    )
    check(bool(document.get("registration_endpoint")), "registration_endpoint is advertised (DCR)")
    check("openid" not in (document.get("scopes_supported") or []), "openid is not offered")
    check("offline" in (document.get("scopes_supported") or []), "offline is offered")


def check_protected_resource(client: httpx.Client, config: AgentAuthConfig) -> None:
    print(f"\n2. Your protected resource metadata: {config.protected_resource_metadata_url}")
    response, document = get_json(client, config.protected_resource_metadata_url)
    if response is None:
        report("FAIL", "Is mcp_server.py running?")
        return
    if not check(response.status_code == 200, f"HTTP {response.status_code}"):
        return
    if not check(document is not None, "the body is a JSON object"):
        return
    check(document.get("resource") == config.resource_url, "resource matches KINDE_AGENTS_RESOURCE_URL exactly")
    check(document.get("authorization_servers") == [config.issuer], "authorization_servers is [scoped issuer]")
    check("offline" in (document.get("scopes_supported") or []), "scopes_supported includes offline")


def check_challenge(client: httpx.Client, config: AgentAuthConfig) -> None:
    print(f"\n3. Challenge from {config.resource_url}")
    headers = {"Accept": "application/json, text/event-stream", "Content-Type": "application/json"}
    for label, extra, expected_error in (
        ("no token", {}, None),
        ("bad token", {"Authorization": "Bearer not-a-real-token"}, "invalid_token"),
    ):
        try:
            response = client.post(config.resource_url, headers={**headers, **extra}, content=b"{}")
        except httpx.HTTPError as exc:
            report("FAIL", f"{label}: {type(exc).__name__}")
            continue
        if not check(response.status_code == 401, f"{label}: HTTP {response.status_code} (expected 401)"):
            if response.status_code >= 500:
                print("     A 5xx here means the server couldn't verify with Kinde: check the server log for")
                print("     'introspection' errors (wrong app ID or secret, or the feature flag is off).")
            continue
        challenge = find_bearer_challenge(response.headers.get_list("www-authenticate"))
        check(
            challenge is not None and challenge.get("resource_metadata") == config.protected_resource_metadata_url,
            f"{label}: WWW-Authenticate points at the metadata URL",
        )
        if expected_error:
            check(
                challenge is not None and challenge.get("error") == expected_error, f"{label}: error={expected_error}"
            )


def check_cimd(client: httpx.Client, url: str) -> None:
    print(f"\n4. Client ID metadata document: {url}")
    try:
        validate_client_metadata_url(url)
    except ValueError as exc:
        report("FAIL", str(exc))
        return
    try:
        response = client.get(url)
    except httpx.HTTPError as exc:
        report("FAIL", f"GET failed: {type(exc).__name__}")
        return
    if not check(response.status_code == 200, f"HTTP {response.status_code} with no redirect"):
        return
    check(response.headers.get("content-type", "").startswith("application/json"), "Content-Type is application/json")
    check(len(response.content) < 64 * 1024, "under 64 KiB")
    check("max-age" in response.headers.get("cache-control", ""), "Cache-Control has max-age", warn_only=True)
    try:
        document = response.json()
    except ValueError:
        document = None
    if not isinstance(document, dict):
        report("FAIL", "body is not a JSON object")
        return
    check(document.get("client_id") == url, "client_id equals the URL it's served at")
    check(bool(document.get("client_name")), "client_name is set")
    check(bool(document.get("redirect_uris")), "redirect_uris is not empty")
    print("     Reminder: the host must be in the application's Trusted agent hosts.")


def check_token(client: httpx.Client, config: AgentAuthConfig, token: str) -> None:
    print("\n5. Access token")
    try:
        claims = jwt.decode(token, options={"verify_signature": False})
    except jwt.PyJWTError:
        report("FAIL", "not a JWT")
        return
    audience = claims.get("aud")
    audiences = [audience] if isinstance(audience, str) else audience or []
    scopes = claims.get("scp") if isinstance(claims.get("scp"), list) else str(claims.get("scope") or "").split()
    print(f"     iss={claims.get('iss')}  aud={audiences}  azp={claims.get('azp')}  scopes={scopes}")
    check(str(claims.get("iss", "")).rstrip("/") == config.domain, "iss is the Kinde domain (not the scoped issuer)")
    check(config.resource_url in audiences, "aud contains the Resource URL")
    check("openid" not in scopes, "no openid scope")
    check("offline" in scopes, "token scopes include offline (kinde_auth_settings requires it)")

    try:
        response = client.post(
            config.introspection_url,
            data={"token": token},
            auth=(config.client_id, config.client_secret or ""),
        )
    except httpx.HTTPError as exc:
        report("FAIL", f"introspection request failed: {type(exc).__name__}")
        return
    if response.status_code != 200:
        # Kinde answers 401 token_inactive for a bad token, and 401 request_unauthorized for bad app credentials
        try:
            error = response.json().get("error")
        except ValueError:
            error = None
        report("FAIL", f"introspection HTTP {response.status_code} {error or ''}".rstrip())
        return
    try:
        data = response.json()
    except ValueError:
        data = None
    if not isinstance(data, dict):
        report("FAIL", "introspection body is not a JSON object")
        return
    if not check(data.get("active") is True, "introspection says active"):
        return
    introspected_aud = data.get("aud") if isinstance(data.get("aud"), list) else [data.get("aud")]
    check(config.resource_url in introspected_aud, "introspection aud contains the Resource URL")
    check(
        "offline" in str(data.get("scope") or "").split(),
        "introspection scope includes offline (the SDK reads scopes from here)",
    )
    print(f"     introspection fields: {sorted(k for k in data if k != 'token')}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cimd-url", help="your agent's client ID metadata document URL")
    parser.add_argument("--token", help="an access token an agent received (decoded and introspected)")
    args = parser.parse_args()

    config = AgentAuthConfig.from_env()
    print(f"Domain {config.domain}, application {config.client_id}, resource {config.resource_url}")
    with httpx.Client(timeout=10, follow_redirects=False) as client:
        check_kinde_discovery(client, config)
        check_protected_resource(client, config)
        check_challenge(client, config)
        if args.cimd_url:
            check_cimd(client, args.cimd_url)
        if args.token:
            check_token(client, config, args.token)

    print("\n" + json.dumps(results))
    return 1 if results["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
