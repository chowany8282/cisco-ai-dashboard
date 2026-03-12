# RUNBOOK

## 1) Symptom: UI error shown to users
1. Open app dashboard/logs
2. Identify failing tab and input
3. Roll back recent bad change if needed

## 2) Symptom: API failures increase
- Verify provider status/quota/key
- Retry with lower-cost model
- Announce temporary degraded mode

## 3) Rollback
1. Find last known good commit
2. Revert via PR
3. Merge and redeploy

## 4) Smoke tests
- __SMOKE_CASE_1__
- __SMOKE_CASE_2__
- __SMOKE_CASE_3__
