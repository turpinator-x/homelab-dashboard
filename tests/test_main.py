import httpx
import pytest
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def empty_cache():
    main.cache.update(data=None, time=0.0)


def fake_prometheus(monkeypatch, answer=1.0):
    """Replace the Prometheus call with one that counts calls and returns `answer`."""
    calls = []

    async def fake_query(client, promql):
        calls.append(promql)
        if isinstance(answer, Exception):
            raise answer
        return answer

    monkeypatch.setattr(main, "query", fake_query)
    return calls


def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_stats_has_every_number_and_app(monkeypatch):
    fake_prometheus(monkeypatch, answer=2.0)
    data = client.get("/api/stats").json()
    for name in main.QUERIES:
        assert data[name] == 2.0
    assert data["apps"] == {"linkding": True, "audiobookshelf": True}


def test_app_with_no_replicas_is_down(monkeypatch):
    fake_prometheus(monkeypatch, answer=None)
    assert client.get("/api/stats").json()["apps"]["linkding"] is False


def test_second_request_uses_the_cache(monkeypatch):
    calls = fake_prometheus(monkeypatch)
    client.get("/api/stats")
    first = len(calls)
    client.get("/api/stats")
    assert len(calls) == first


def test_prometheus_down_returns_503(monkeypatch):
    fake_prometheus(monkeypatch, answer=httpx.ConnectError("down"))
    assert client.get("/api/stats").status_code == 503


def test_homepage_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "Homelab" in response.text
