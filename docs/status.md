# Status

_Last updated: 2026-11-06_

## Running

- **v0.1.2** live at dashboard.jarrodturpin.dev on Python 3.15, amd64 + arm64 image on GHCR.
- CI: ruff format check, ruff, pytest, then a multi-arch build; images are pushed only for `v*` tags, with provenance and an SBOM.
- Secret scan: gitleaks over the full history in `.github/workflows/secret-scan.yaml`.
- Repo baseline (since 2026-11-04): Commitizen enforces Conventional Commits; pre-commit runs the secret checks and shellcheck.
- Renovate: low-risk updates auto-merge after a 3-day wait, with a weekly lock file refresh; the rest wait for a Monday batch reviewed with the `homelab-pr-review` skill. No Renovate PRs are open.
- Rulesets (`protect-main`, `protect-release-tags`, both active): `main` can't be deleted or force-pushed; `v*` tags can't be moved or deleted.

## Next

Nothing scheduled. Ideas: per-app response times, a small uptime history.

## Known issues

- `v0.1.1` was tagged on the wrong commit and is skipped. Tags are protected, so it stays.

## Don't repeat

- Files with mode 600 broke the non-root image; the Dockerfile now runs `chmod -R a+rX main.py static`.
- `.dockerignore` once held the text of the `printf` command meant to create it, so nothing was ignored. Check generated files with `cat` after creating them.
- `httpx2` (Starlette's suggested successor) was blocked as an unvetted package; staying on `httpx`.
