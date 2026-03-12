# RUNBOOK

## 1) Symptom: UI error shown to users
### Check
1. Open Streamlit Cloud app dashboard
2. Inspect logs around error time
3. Identify tab (log/spec/os) and failing input

### Immediate action
- If recent deploy caused issue: rollback to previous commit on `main`
- If secret/API issue: re-enter secrets and reboot app

---

## 2) Symptom: Gemini/API failures increase
### Check
- Error message in app expander
- Provider status and quota
- API key validity

### Immediate action
- Retry after short interval
- Switch model in sidebar to lower-cost/faster option
- Notify users with temporary degraded mode message

---

## 3) Symptom: Deployment not reflecting latest code
### Check
- Confirm PR merged to `main`
- Confirm Streamlit app points to `main` and `app.py`
- Trigger manual reboot/redeploy

---

## 4) Rollback procedure
1. GitHub: identify last known good commit
2. Revert problematic commit via PR
3. Merge PR to `main`
4. Wait for auto redeploy and run smoke tests

---

## 5) Smoke tests (post-change)
- Log tab: sample interface down log should return 3 sections
- Spec tab: `C9300-48P`
- OS tab: `Nexus 93180YC-FX`, version `17.06.01`
