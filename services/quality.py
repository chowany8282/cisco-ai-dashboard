from __future__ import annotations

REQUIRED_ACTION_SECTIONS = [
    "즉시 조치",
    "원인별 상세 조치",
    "검증 절차",
    "롤백 계획",
    "재발 방지 체크리스트",
]


def has_required_action_sections(part3_text: str) -> bool:
    return all(section in (part3_text or "") for section in REQUIRED_ACTION_SECTIONS)


def normalize_action_sections(part3_text: str) -> str:
    text = (part3_text or "").strip()
    if not text:
        text = "원문 권장 조치가 비어 있습니다. 로그를 재확인하세요."

    if has_required_action_sections(text):
        return text

    verify_cmds = (
        "```\n"
        "show interface status\n"
        "show logging | inc ERROR|UPDOWN|SPANTREE\n"
        "show spanning-tree interface <INTERFACE> detail\n"
        "```"
    )
    rollback_cmds = (
        "```\n"
        "configure terminal\n"
        "interface <INTERFACE>\n"
        "shutdown\n"
        "no shutdown\n"
        "end\n"
        "```"
    )
    fallback_detail = (
        "- 물리 계층(케이블/SFP), 인접 장비 설정(STP/LACP), "
        "오류 카운터를 순서대로 점검합니다."
    )
    fallback_prevent = (
        "- 반복 장애 시 포트 정책(BPDU Guard/Loop Guard), "
        "소프트웨어 버전, 변경 이력을 점검합니다."
    )

    return (
        f"1) 즉시 조치\n{text}\n\n"
        f"2) 원인별 상세 조치\n{fallback_detail}\n\n"
        f"3) 검증 절차\n{verify_cmds}\n\n"
        f"4) 롤백 계획\n{rollback_cmds}\n\n"
        f"5) 재발 방지 체크리스트\n{fallback_prevent}"
    )


def has_os_recommendation_markers(html: str) -> bool:
    lowered = (html or "").lower()
    has_gold_or_md = ("gold" in lowered) or ("md" in lowered)
    has_evidence = ("근거" in (html or "")) or ("evidence" in lowered)
    return has_gold_or_md and has_evidence


def has_structured_os_html(html: str) -> bool:
    lowered = (html or "").lower()
    return ("<table" in lowered) and ("<tr" in lowered) and ("<td" in lowered)
