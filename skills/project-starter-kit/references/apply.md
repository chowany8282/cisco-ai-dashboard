# Apply Steps

1. Create branch:
```bash
git checkout -b feat/bootstrap-starter-kit
```

2. Copy template files from `assets/template/` to repo root.

3. Replace placeholders:
- `__APP_NAME__` -> app display name
- `__APP_URL__` -> deployed app URL
- smoke cases -> project-specific checks

4. Validate:
```bash
ruff check .
pytest -q
```

5. Commit/push and open PR.

6. After merge, run workflow manually once:
- `ops-monitor` -> Run workflow
