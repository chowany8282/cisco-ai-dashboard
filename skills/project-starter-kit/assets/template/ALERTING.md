# ALERTING

- Workflow: `.github/workflows/ops-monitor.yml`
- Interval: every 30 minutes
- Checks: homepage marker + Streamlit health endpoint
- Failure handling: create/update incident issue (`incident`, `ops`)

After merge, run `ops-monitor` once manually to verify.
