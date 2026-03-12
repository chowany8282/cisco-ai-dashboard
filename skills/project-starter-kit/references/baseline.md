# Baseline Components

## Collaboration
- `.github/pull_request_template.md`
- `CONTRIBUTING.md`

## Quality
- `.github/workflows/ci.yml`

## Operations
- `RUNBOOK.md`
- `OPS_CHECKLIST.md`
- `COST_GUARDRAILS.md`
- `ALERTING.md`
- `.github/workflows/ops-monitor.yml` (optional, recommended)

## Minimal verification
- lint: `ruff check .`
- tests: `pytest -q`
- deploy smoke test on real app URL
