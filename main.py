"""Homelab dashboard: a few live numbers from the cluster's Prometheus."""

import asyncio
import os
import time
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

PROMETHEUS_URL = os.environ.get(
    "PROMETHEUS_URL", "http://kube-prometheus-stack-prometheus.monitoring:9090"
)
CACHE_SECONDS = int(os.environ.get("CACHE_SECONDS", "15"))
APPS = os.environ.get("APPS", "linkding,audiobookshelf").split(",")
# Fixed queries: visitors never send PromQL, they only read the answers.
QUERIES = {
    "cpu_percent": '100 * (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])))',
    "memory_used_bytes": "sum(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)",
    "memory_total_bytes": "sum(node_memory_MemTotal_bytes)",
    "pods_running": 'sum(kube_pod_status_phase{phase="Running"})',
    "nodes_ready": 'sum(kube_node_status_condition{condition="Ready",status="true"})',
    "nodes_total": "count(kube_node_info)",
    "uptime_seconds": "max(time() - node_boot_time_seconds)",
}

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
cache = {"data": None, "time": 0.0}


async def query(client: httpx.AsyncClient, promql: str) -> float | None:
    """Run one PromQL query and return its single number, or None if empty."""
    response = await client.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": promql})
    response.raise_for_status()
    result = response.json()["data"]["result"]
    if not result:
        return None
    return float(result[0]["value"][1])


async def collect() -> dict:
    """Ask Prometheus every question at once and build the response."""
    app_queries = {
        name: f'sum(kube_deployment_status_replicas_available{{deployment="{name}"}})'
        for name in APPS
    }
    async with httpx.AsyncClient(timeout=5) as client:
        stats = await asyncio.gather(*(query(client, q) for q in QUERIES.values()))
        apps = await asyncio.gather(*(query(client, q) for q in app_queries.values()))
    data = dict(zip(QUERIES, stats, strict=True))
    data["apps"] = {name: (up or 0) > 0 for name, up in zip(app_queries, apps, strict=True)}
    data["updated"] = int(time.time())
    return data


@app.get("/healthz")
async def healthz():
    # Doesn't touch Prometheus: a Prometheus outage shouldn't restart this pod.
    return {"status": "ok"}


@app.get("/api/stats")
async def stats():
    if cache["data"] is None or time.monotonic() - cache["time"] > CACHE_SECONDS:
        cache["time"] = time.monotonic()
        try:
            cache["data"] = await collect()
        except httpx.HTTPError:
            if cache["data"] is None:
                raise HTTPException(status_code=503, detail="metrics unavailable") from None
    return cache["data"]


app.mount(
    "/",
    StaticFiles(directory=Path(__file__).parent / "static", html=True),
    name="static",
)
