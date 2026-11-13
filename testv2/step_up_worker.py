"""
A Flask worker process for the multi-worker step-up tests.

Each worker is a separate Python process with its own in-memory caches, like a
``gunicorn`` worker. The workers share one server-side session directory. The
network is faked inside the worker: the token endpoint behaves as Kinde does,
so a refresh keeps the ``acr`` of the grant its refresh token came from.
"""

import asyncio
import os
import time
import traceback

HOST = "https://test.kinde.com"


def _fake_kinde(worker_name, token_requests):
    from unittest.mock import MagicMock

    import jwt

    def tokens(label, mfa, refresh_token):
        now = int(time.time())
        claims = {"sub": "kp_user", "auth_time": now if mfa else now - 3600}
        if mfa:
            claims.update(acr="mfa", amr=["pwd", "totp"])
        return {
            "access_token": jwt.encode(
                {**claims, "jti": f"access-{label}"}, "k" * 32, algorithm="HS256"
            ),
            "id_token": jwt.encode(
                {**claims, "jti": f"id-{label}"}, "k" * 32, algorithm="HS256"
            ),
            "refresh_token": refresh_token,
            "expires_in": 3600,
        }

    def get(url, **kwargs):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "authorization_endpoint": f"{HOST}/oauth2/auth",
            "token_endpoint": f"{HOST}/oauth2/token",
            "end_session_endpoint": f"{HOST}/logout",
            "userinfo_endpoint": f"{HOST}/oauth2/userinfo",
            "acr_values_supported": ["mfa", "phr"],
        }
        return response

    def post(url, data=None, **kwargs):
        token_requests.append(
            {key: data.get(key) for key in ("grant_type", "code", "refresh_token")}
        )
        response = MagicMock()
        response.status_code = 200
        if data["grant_type"] == "authorization_code":
            code = data["code"]
            response.json.return_value = tokens(
                code, code.startswith("stepup"), f"refresh-from-{code}"
            )
        else:
            # A refresh never upgrades: it keeps the context of its refresh token
            refresh_token = data["refresh_token"]
            response.json.return_value = tokens(
                f"refreshed-by-{worker_name}", "stepup" in refresh_token, refresh_token
            )
        return response

    return get, post


def run(worker_name, connection, session_dir):
    """Serve requests sent over ``connection`` until ``None`` arrives."""
    os.environ["SECRET_KEY"] = "shared-secret"
    os.environ["SESSION_FILE_DIR"] = session_dir

    import logging
    from unittest.mock import AsyncMock

    logging.disable(logging.CRITICAL)

    import requests

    token_requests = []
    requests.get, requests.post = _fake_kinde(worker_name, token_requests)

    from flask import Flask, jsonify, redirect

    import kinde_sdk.auth.oauth as oauth_module
    from kinde_sdk.auth.oauth import OAuth

    oauth_module.helper_get_user_details = AsyncMock(return_value={"id": "kp_user"})

    app = Flask(__name__)
    app.testing = True
    oauth = OAuth(
        client_id="test_client_id",
        client_secret="test_client_secret",
        redirect_uri="http://localhost/callback",
        framework="flask",
        app=app,
        host=HOST,
    )

    def token_manager():
        user_id = oauth._framework.get_user_id()
        return oauth._session_manager.get_token_manager(user_id) if user_id else None

    @app.route("/payouts")
    def payouts():
        if not oauth.is_authenticated():
            return redirect("/login")
        if not oauth.has_authentication_context(acr="mfa"):
            return redirect(asyncio.run(oauth.step_up(acr="mfa")))
        return "payouts"

    @app.route("/whoami")
    def whoami():
        authenticated = oauth.is_authenticated()
        manager = token_manager()
        return jsonify(
            worker=worker_name,
            authenticated=authenticated,
            acr=oauth.get_authentication_context()["acr"],
            access_token=(
                manager.get_claims("access_token").get("jti") if manager else None
            ),
            refresh_token=manager.tokens.get("refresh_token") if manager else None,
        )

    @app.route("/expire")
    def expire():
        token_manager().tokens["expires_at"] = time.time() - 1
        return "expired"

    client = app.test_client()
    while True:
        message = connection.recv()
        if message is None:
            break
        path, cookie = message
        try:
            client.delete_cookie("session")
            if cookie:
                client.set_cookie("session", cookie)
            sent = len(token_requests)
            response = client.get(path)
            for header in response.headers.getlist("Set-Cookie"):
                if header.startswith("session="):
                    cookie = header.split(";")[0].split("=", 1)[1]
            connection.send(
                {
                    "status": response.status_code,
                    "location": response.headers.get("Location"),
                    "body": response.get_data(as_text=True),
                    "json": response.get_json(silent=True),
                    "cookie": cookie,
                    "token_requests": token_requests[sent:],
                }
            )
        except Exception:
            connection.send({"error": traceback.format_exc()})
