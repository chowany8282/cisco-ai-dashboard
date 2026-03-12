# PROJECT_STATUS.md

Last Updated: 2026-03-12 (Asia/Seoul)
Project: cisco-ai-dashboard

---

## 1) 프로젝트 목적
Cisco 네트워크 엔지니어를 위한 Streamlit 기반 AI 도우미:
- 로그 분석
- 하드웨어 스펙 조회
- OS 추천

운영 목표:
- PR 기반 협업
- 배포 안정성 확보
- 장애 감지/대응 자동화

---

## 2) 현재 상태 (요약)
- 상태: **운영 가능 (Production-Ready v1)**
- 코드: GitHub `main` 반영 완료
- 배포: Streamlit Cloud 연결 및 실동작 확인
- 품질: `ruff` 통과, `pytest` 통과
- 운영: 체크리스트/런북/비용 가드레일/자동 모니터링 구축 완료

---

## 3) 타임라인 이력 (상세)

### Phase 1 — 기반 세팅
목표:
- 로컬 실행/테스트 가능한 기본 프로젝트 형태 확립

실행:
- `app.py` 반영
- `requirements.txt`, `.gitignore`, `.streamlit/secrets.toml.example` 생성
- `tests/` 기본 스모크/설정 테스트 추가
- 가상환경 구성 + 의존성 설치

결과:
- 기본 실행 가능
- 테스트 통과 기반 확보

---

### Phase 2 — 안정화 리팩토링
목표:
- 코드 구조 분리 및 파싱 안정화

실행:
- `services/llm.py` 분리
- `services/parsers.py` 분리
- `prompts/` 파일 외부화
- 에러 처리 보강
- 파서 테스트 확장

결과:
- 유지보수성 향상
- 응답 파싱 실패 리스크 감소

---

### Phase 3 — 신뢰성 강화
목표:
- 실운영 전 신뢰성(재시도/검증/CI) 보강

실행:
- LLM timeout/retry(backoff) 적용
- 스키마 검증(`services/schemas.py`, pydantic) 추가
- CI 워크플로우(`.github/workflows/ci.yml`) 추가
- `SETUP.md`, `pyproject.toml` 정리
- Python 3.11 전환

결과:
- 로컬/CI 기준 일치
- 검증 루프 고정

---

### Phase 4 — GitHub 협업 체계 확립
목표:
- PR 기반 운영 체계로 전환

실행:
- 새 repo 생성 및 연결: `chowany8282/cisco-ai-dashboard`
- 초기 커밋/푸시
- PR 템플릿/CONTRIBUTING 반영
- ruleset(직접 main push 금지 + PR 머지) 적용

결과:
- 협업 프로세스 표준화

---

### Phase 5 — 배포/실서비스 검증
목표:
- Streamlit Cloud 배포 정상화

실행:
- 배포 연결
- 실사용 테스트 중 `KeyError` 발견 (`prompt.format`과 JSON 템플릿 충돌)
- 핫픽스: `render_prompt()` 방식으로 안전 치환
- PR 머지 후 재배포 확인

결과:
- 런타임 장애 해결
- 로그 분석 탭 실동작 재검증 완료

---

### Phase 6 — 운영 안정화 1차
목표:
- 운영 문서/체크리스트 체계 구축

실행:
- `RUNBOOK.md`
- `OPS_CHECKLIST.md`
- `COST_GUARDRAILS.md`
- `ALERTING.md`

결과:
- 장애 대응 및 주기 점검 프로세스 문서화 완료

---

### Phase 7 — 자동 알림 고도화
목표:
- 장애 감지 자동화 + 알림 노이즈 제어

실행:
- `.github/workflows/ops-monitor.yml` 추가
  - 30분 주기 점검
  - 홈/헬스 엔드포인트 확인
  - 실패 시 incident issue 생성
- 후속 개선:
  - 중복 incident 이슈 생성 방지 (기존 이슈 코멘트 누적)
  - 실패 run 링크 포함

결과:
- 자동 감시/이슈화 루프 구축

---

### Phase 8 — 재사용 체계 구축
목표:
- 다음 프로젝트에 동일 운영 체계 재사용

실행:
- `skills/project-starter-kit/` 생성
- SKILL + references + template assets 구성
- `.skill` 패키징 완료:
  - `skills/dist/project-starter-kit.skill`

결과:
- 신규 프로젝트 온보딩 속도 향상 기반 확보

---

## 4) 현재 주요 파일 맵
- 앱 엔트리: `app.py`
- 서비스 로직: `services/`
- 프롬프트: `prompts/`
- 테스트: `tests/`
- CI: `.github/workflows/ci.yml`
- 운영 모니터링: `.github/workflows/ops-monitor.yml`
- 운영 문서:
  - `RUNBOOK.md`
  - `OPS_CHECKLIST.md`
  - `COST_GUARDRAILS.md`
  - `ALERTING.md`
- 협업 규칙:
  - `CONTRIBUTING.md`
  - `.github/pull_request_template.md`

---

## 5) 운영 시 즉시 참고 절차
1. `main` 최신 동기화
2. 이 파일(`PROJECT_STATUS.md`)의 "다음 작업" 확인
3. 브랜치 생성 (`feat/*` 또는 `fix/*`)
4. 개발/수정
5. 검증:
   - `ruff check .`
   - `pytest -q`
6. PR 생성/머지
7. 배포 후 스모크 테스트

---

## 6) 다음 작업 후보 (우선순위)
1. 스펙/OS 탭에 대한 추가 실사용 회귀 테스트 케이스 확장
2. 비용 모니터링 수치 수집 자동화(주간 리포트)
3. 알림 채널 확장(선택: Telegram/Slack)
4. HTML sanitize 정책 고급화(필요 시 라이브러리 기반)

---

## 7) 의사결정 기록 (핵심)
- 대규모 기능 추가보다 안정화/운영성 우선 전략 채택
- `main` 직푸시 금지, PR 중심 운영 확정
- Python 3.11 표준화 확정
- 배포는 Streamlit Cloud 우선, 필요 시 추후 고도화
- 반복 가능한 표준화를 위해 starter skill 생성

---

## 8) 재개 시작 프롬프트 (복붙용)
"현재 `PROJECT_STATUS.md` 기준으로 다음 우선순위 1번부터 진행해줘. 변경은 `feat/*` 브랜치에서 하고, `ruff + pytest` 통과 후 PR 기준으로 보고해줘."

---

## 9) 2026-03-13 상세 작업 기록 (실사용 체감 이슈 대응)

### 배경
- 사용자 피드백: 로그 진단 탭 결과가 이전보다 짧고, 전반적인 체감 속도/품질이 저하됨.
- 초기 오해: GitHub Actions 로그 truncation 이슈로 착각했으나, 실제 이슈는 앱의 `로그 진단` 탭 출력/체감 품질 문제였음.

### 확인한 사실
- `app.py` 기준 로그 진단은 JSON 스키마/파싱 기반 구조와, 통합형 `[PART_1]/[PART_2]/[PART_3]` 구조 간 동작 체감이 다름.
- 사용자 체감상 `chowany8282/cisco_log_spec_os` 버전이 더 빠르고 정보량이 많았음.
- 원인 분석 결론:
  1. 안정화 계층(검증/파싱/재시도)의 오버헤드로 체감 속도 저하 가능
  2. 출력 강제 형식 차이로 정보량/가독성 차이 발생
  3. 사용자 목표(즉시성+풍부한 진단) 대비 과도한 구조화가 UX를 악화시킨 구간 존재

### 조치 내역
1. 사용자 제공 원본 파일(신버전) 기준으로 `app.py` 재적용 및 문법/테스트 확인
2. 참조 레포 직접 확인:
   - `https://github.com/chowany8282/cisco_log_spec_os`
   - 핵심 파일 `Cisco_Master_Tool.py` 확보/비교
3. 동기화 브랜치 생성 및 반영:
   - branch: `sync/from-cisco_log_spec_os`
   - `app.py`를 참조 레포 버전과 정렬
4. 검증:
   - `python3 -m py_compile app.py` 통과
   - `.venv/bin/pytest -q` 통과 (10 passed)
5. PR 생성/머지:
   - PR: #19
   - main 반영 커밋: `4257372` (`sync: align app.py with cisco_log_spec_os reference (#19)`)

### 운영/프로세스 교정
- 잘못된 흐름 정정: 스킬/개인 운영 문서 변경을 GitHub 반영 대상으로 자동 취급한 점을 교정.
- 확정 운영 원칙:
  - 스킬/개인 메모는 기본 로컬 관리
  - 원격 반영은 사용자 명시 요청 시에만 수행

### 재발 방지 규칙 (UX-First)
- 우선순위 고정: **속도 > 정보량 > 오류 직관성**
- 안정화/리팩토링은 체감 품질 저하가 없을 때만 적용
- 에러 메시지 표준: **원인 1줄 + 바로 할 행동 1줄**
- 배포/완료 전 필수 체크:
  1. 대표 입력 기준 응답 시간 회귀 없음
  2. 결과 정보량/실무 유용성 회귀 없음
  3. 실패 시 안내 문구가 비개발자도 즉시 이해 가능

### 연동 문서 반영
- `memory/2026-03-13.md`에 교훈 및 실행 원칙 기록
- `skills/project-starter-kit/SKILL.md` 반영
- `skills/project-starter-kit/references/apply.md` 반영
- 로컬 커밋: `1e43029` (`docs(skill): enforce UX-first checks to prevent regressions`)

### 현재 상태 결론
- 앱 동작 기준은 사용자 체감이 좋았던 참조 버전으로 복귀/정렬 완료.
- 실사용 품질 우선 원칙이 문서/스킬/메모에 모두 반영되어 다음 작업부터 동일 실수 가능성 낮춤.
