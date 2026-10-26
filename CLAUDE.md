# CLAUDE.md

Public status page for Jarrod's k3s homelab (dashboard.jarrodturpin.dev). A small FastAPI app (`main.py`) runs fixed PromQL queries against the cluster's Prometheus, caches them for 15 s and serves `/api/stats`; `static/index.html` polls it. The Kubernetes manifests live in the `homelab` repo (`apps/*/dashboard`), not here.

## Commands

- `uv run pytest`, `uv run ruff check .`, `uv run ruff format .` — the same checks CI runs. A Claude Code hook formats the edited file and runs ruff + pytest after any `.py` edit.
- Run locally: port-forward Prometheus to 9090, then `PROMETHEUS_URL=http://localhost:9090 uv run uvicorn main:app --reload`.

## Rules

- **Public repo, public page.** Show totals only: no pod names, IPs or internal hostnames. PromQL stays fixed in code; visitors never send queries.
- Keep the container locked down (non-root UID 10001, read-only root FS, no SA token). Files copied into the image must be world-readable.
- Frontend: no frameworks, CDNs, third-party scripts or fonts.
- New Python dependencies may be added without asking if they pass all of: established project (clear maintainer, active releases, widely used), name checked against typosquats, wheels available for amd64 and arm64, few new transitive packages. Add with `uv add`, commit `uv.lock`, and list each new package in the commit message. Anything failing a check: ask Jarrod.
- Claude Code wrote the app code. Docs must keep saying so; never describe it as Jarrod's own Python.
- Jarrod is learning Python: explain changes in plain words.
- Ask before pushing to main or creating a `v*` tag (a tag publishes an image to GHCR; deploy is a separate PR in `homelab`).

## Done means

ruff and pytest pass, the README matches the behaviour, and `docs/status.md` is updated. For a release: bump `pyproject.toml` version, tag `vX.Y.Z` on the right commit, then bump the image in the `homelab` repo.
