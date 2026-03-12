# OPS_CHECKLIST

## Daily (5 min)
- [ ] App opens without error (`*.streamlit.app`)
- [ ] Log analysis tab smoke test
- [ ] Spec lookup tab smoke test
- [ ] OS recommendation tab smoke test
- [ ] Check Streamlit app logs for new errors

## Weekly
- [ ] Review API usage/cost trend (Gemini)
- [ ] Review slow/error patterns in logs
- [ ] Validate secrets are still valid and not rotated unexpectedly
- [ ] Verify branch protection/ruleset still active

## Release checklist
- [ ] `ruff check .` pass
- [ ] `pytest -q` pass
- [ ] PR created and approved
- [ ] Post-deploy smoke test complete
