# ALERTING

## 자동 알림 (GitHub Actions)
- Workflow: `.github/workflows/ops-monitor.yml`
- 주기: 30분
- 점검 대상:
  1. 앱 메인 페이지 타이틀 문자열
  2. Streamlit health endpoint (`_stcore/health`)

## 실패 시 동작
- GitHub Incident Issue 자동 관리 (`incident`, `ops` 라벨)
- 제목: `[OPS ALERT] Streamlit smoke check failed` (고정)
- 이미 열려 있는 Incident가 있으면 새 이슈를 만들지 않고 코멘트로 누적

## 운영자가 할 일
1. 생성된 Incident Issue 확인
2. Streamlit Cloud 로그 확인
3. `RUNBOOK.md` 절차대로 원인 분석/복구
4. 복구 후 수동으로 workflow_dispatch 실행해서 정상 여부 재검증

## 주의
- Actions 권한에서 Issues 쓰기 권한이 필요할 수 있음
- 라벨(`incident`, `ops`)은 없으면 자동 생성되지 않을 수 있으니 초기 1회 수동 생성 권장
