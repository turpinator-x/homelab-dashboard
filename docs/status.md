# Status

_Last updated: 2026-10-26_

## Running

- **v0.1.2** live at dashboard.jarrodturpin.dev on Python 3.15, amd64 + arm64 image on GHCR.
- CI: ruff format check, ruff, pytest, then a multi-arch build; images are pushed only for `v*` tags, with provenance and an SBOM.
- Renovate: low-risk updates auto-merge; the rest wait for a Monday batch reviewed with the `homelab-pr-review` skill.
- Rulesets: `main` can't be deleted or force-pushed; `v*` tags can't be moved or deleted.

## Next

Nothing scheduled. Ideas: per-app response times, a small uptime history.

## Known issues

- `v0.1.1` was tagged on the wrong commit and is skipped. Tags are protected, so it stays.
- `.dockerignore` holds the text of the `printf` command that was meant to create it, so it ignores nothing and `.venv` is sent as build context. The image is unaffected (the Dockerfile copies files by name), but builds upload more than they need.

## Don't repeat

- Files with mode 600 broke the non-root image; the Dockerfile now runs `chmod -R a+rX main.py static`.
- `httpx2` (Starlette's suggested successor) was blocked as an unvetted package; staying on `httpx`.
