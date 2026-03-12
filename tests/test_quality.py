from pathlib import Path

from services.quality import (
    REQUIRED_ACTION_SECTIONS,
    has_os_recommendation_markers,
    has_required_action_sections,
    normalize_action_sections,
)


def test_normalize_action_sections_fills_missing_sections():
    raw = "인터페이스 다운 원인 점검 필요"
    normalized = normalize_action_sections(raw)
    for section in REQUIRED_ACTION_SECTIONS:
        assert section in normalized


def test_normalize_action_sections_keeps_complete_text():
    full_text = "\n".join(
        [
            "즉시 조치: A",
            "원인별 상세 조치: B",
            "검증 절차: C",
            "롤백 계획: D",
            "재발 방지 체크리스트: E",
        ]
    )
    assert has_required_action_sections(full_text)
    assert normalize_action_sections(full_text) == full_text


def test_has_os_recommendation_markers_requires_gold_md_and_evidence():
    ok_html = "<table><tr><th>근거</th></tr><tr><td>Gold Star release note</td></tr></table>"
    bad_html = "<table><tr><td>recommended release</td></tr></table>"

    assert has_os_recommendation_markers(ok_html)
    assert not has_os_recommendation_markers(bad_html)


def test_prompts_include_quality_constraints():
    root = Path(__file__).resolve().parents[1]
    log_prompt = (root / "prompts" / "log_analysis.txt").read_text(encoding="utf-8")
    os_prompt = (root / "prompts" / "os_recommendation.txt").read_text(encoding="utf-8")

    assert "즉시 조치" in log_prompt
    assert "롤백 계획" in log_prompt
    assert "재발 방지 체크리스트" in log_prompt

    assert "Gold Star" in os_prompt
    assert "MD" in os_prompt
    assert "근거" in os_prompt
