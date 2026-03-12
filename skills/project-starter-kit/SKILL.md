---
name: project-starter-kit
description: Bootstrap a new software project with a production-ready collaboration and operations baseline. Use when starting a new repo or standardizing an existing one with branch/PR rules, CI, runbook, ops checklist, cost guardrails, optional scheduled health alerts, GitHub CLI merge automation readiness, and quality regression guardrails.
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
6. Merge PR (user UI merge or agent-driven `gh` merge), then run one manual Actions execution for validation.

## Required baseline

- CI workflow
- PR template
- CONTRIBUTING rules
- RUNBOOK
- OPS checklist
- COST guardrails
- Optional ops-monitor scheduled workflow
- GitHub CLI ready state (`gh` 설치 + `gh auth login`) for agent-driven PR/merge
- Quality regression guardrails (format/quality assertions for critical outputs)

## Notes

- Prioritize real-user experience over internal elegance.
- For user-facing AI flows, keep this priority order: (1) response speed, (2) information density, (3) error readability.
- Add stability/refactor layers only when they do not degrade perceived speed or output richness.
- Keep error UX direct: one-line cause + one-line next action.
- Never hardcode secrets.
- Keep ruleset-compatible flow (PR-based merge to `main`).
- Prefer small, reviewable commits.
- If user wants the agent to create/merge PR directly, verify `gh auth status` first.
- Treat deployment smoke tests as mandatory before declaring completion.

## References

- Baseline details: `references/baseline.md`
- Copy/apply steps: `references/apply.md`
