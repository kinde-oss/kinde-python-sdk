import pytest


@pytest.fixture(autouse=True)
def dns(monkeypatch):
    """Fake DNS for the agent client, so no test does a real lookup.

    Every name resolves to a public address unless a test maps it: ``dns["host"] = ["10.0.0.5"]``.
    """
    records = {}

    async def resolve(host):
        return records.get(host, ["93.184.216.34"])

    monkeypatch.setattr("kinde_sdk.agents.client._resolve_host", resolve)
    return records
