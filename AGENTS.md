# AGENTS.md

## Cursor Cloud specific instructions

This repo is the **Kinde Python SDK** — a client library (plus optional `kinde_fastapi` and `kinde_flask` framework integrations), not a standalone server product. There are **no long-running services** required for development, and the automated test suite (`testv2/`) is fully mocked, so it needs no network, database, or Kinde account.

### Environment
- Python dependencies are installed into a virtualenv at `.venv/` (Ubuntu's system Python is PEP 668 "externally managed", so a venv is used instead of global installs). The startup update script keeps `.venv` in sync with `requirements.txt`.
- Run tools via the venv without needing to activate it, e.g. `.venv/bin/pytest`, `.venv/bin/black`, `.venv/bin/flake8`. To activate for an interactive shell: `source .venv/bin/activate`.
- `requirements.txt` is the source of truth for dev (matches CI); `pip install -e ".[fastapi,flask,dev]"` also works.

### Test / lint / build
- Tests: `.venv/bin/pytest` (config in `pytest.ini`; `testpaths=testv2`, coverage + 30s per-test timeout). CI mirrors this across Python 3.9–3.13 (`.github/workflows/ci.yml`).
- Lint/format: `black` and `flake8` are available. Note the repo's pre-commit pins an older `black` (22.12.0) than the version installed from `requirements.txt`, so `black --check` reports many "would reformat" files against the newer version — this is pre-existing and not caused by your changes.

### Running the example apps (manual E2E)
- FastAPI example: `.venv/bin/python -m uvicorn kinde_fastapi.examples.example_app:app --host 127.0.0.1 --port 8000`. Flask example lives at `kinde_flask/examples/example_app.py`.
- The example apps read `KINDE_CLIENT_ID`, `KINDE_CLIENT_SECRET`, `KINDE_REDIRECT_URI`, `KINDE_HOST` (from env or a `.env` beside the example). Only `KINDE_CLIENT_ID` is strictly required for the app to boot.
- With placeholder credentials the app still boots and `/login` correctly generates a full OAuth2/OIDC + PKCE authorization redirect to `${KINDE_HOST}/oauth2/auth?...`. **Completing an actual login requires a real Kinde account/app** whose allowed callback URLs include the configured redirect URI; otherwise Kinde returns "Invalid callback URL" (expected with placeholders).
