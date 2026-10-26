# Decisions

Newest first.

## 2026-10-22 — Renovate auto-merges low-risk updates

Patch/digest/pin updates, GitHub Actions minors, ruff/pytest minors and weekly lock-file maintenance merge on their own once CI passes; the rest wait for a Monday review. **Why:** the weekly review was mostly rubber-stamping.

## 2026-10-21 — Read from Prometheus, not the Kubernetes API

**Why:** the pod needs no service-account token at all, and Prometheus already has the numbers.

## 2026-10-21 — Fixed PromQL with a 15-second cache

Visitors only read cached results. **Why:** a public page must not let anyone run queries, and a traffic flood costs at most one round of queries every 15 s.

## 2026-10-21 — Publish images only from `v*` tags with the workflow token

**Why:** a release is a deliberate act, and no long-lived registry password exists to leak. Deploying is a separate PR in the `homelab` repo, so publishing and deploying stay two steps.

## 2026-10-21 — NetworkPolicy: in from the tunnel, out to DNS and Prometheus

**Why:** if the app were ever compromised, it can't reach anything else in the cluster.
