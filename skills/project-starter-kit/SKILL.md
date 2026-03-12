---
name: project-starter-kit
description: Bootstrap a new software project with a production-ready collaboration and operations baseline. Use when starting a new repo or standardizing an existing one with branch/PR rules, CI, runbook, ops checklist, cost guardrails, and optional scheduled health alerts.
---

# Project Starter Kit

Apply this skill when a user asks to start a new project with the same workflow quality used in prior productionized projects.

## What to do

1. Create a feature branch for setup work.
2. Copy the template baseline from `assets/template/` into the target repository.
3. Replace placeholders:
   - `__APP_NAME__`
   - `__APP_URL__`
   - `__SMOKE_CASE_1__`, `__SMOKE_CASE_2__`, `__SMOKE_CASE_3__`
4. Run checks:
   - `ruff check .`
   - `pytest -q`
5. Commit and push a setup PR.
6. Ask user to merge PR and run one manual Actions execution for validation.

## Required baseline

- CI workflow
- PR template
- CONTRIBUTING rules
- RUNBOOK
- OPS checklist
- COST guardrails
- Optional ops-monitor scheduled workflow

## Notes

- Never hardcode secrets.
- Keep ruleset-compatible flow (PR-based merge to `main`).
- Prefer small, reviewable commits.

## References

- Baseline details: `references/baseline.md`
- Copy/apply steps: `references/apply.md`
