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

5. Ensure GitHub CLI is ready (for agent-driven PR/merge):
```bash
gh --version
gh auth status
```
If not authenticated:
```bash
gh auth login
```

6. Commit/push and open PR.

7. Merge options:
- Manual merge on GitHub UI, or
- Agent-driven merge:
```bash
gh pr checks <PR_NUMBER> --watch --interval 10
gh pr merge <PR_NUMBER> --merge --delete-branch
```

8. After merge, run workflow manually once:
- `ops-monitor` -> Run workflow

9. Before calling the change complete, run UX regression checks for user-facing AI tabs/features:
- Speed: response time is not worse than baseline (quick smoke with representative inputs).
- Information density: outputs are at least as useful/complete as baseline.
- Error readability: failures show "원인 1줄 + 바로 할 행동 1줄".
- If any item regresses, rollback or scope down refactor/stability changes.
