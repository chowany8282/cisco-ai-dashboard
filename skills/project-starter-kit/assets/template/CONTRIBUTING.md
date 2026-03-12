# Contributing Guide

## Branch Rule
- `main`: 배포 가능한 코드만 유지
- 기능 개발: `feat/*`
- 버그 수정: `fix/*`

## Required before merge
1. `ruff check .`
2. `pytest -q`
3. PR 템플릿 체크리스트 작성

## Merge Policy (권장)
- GitHub Branch protection에서 `main` 직접 push 금지
- PR 리뷰 1명 이상 승인 후 merge
