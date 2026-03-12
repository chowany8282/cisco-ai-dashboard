from services.parsers import parse_log_analysis, sanitize_basic_html


def test_parse_log_analysis_success():
    sample = "[PART_1]원인A [PART_2]영향B [PART_3]조치C"
    parsed = parse_log_analysis(sample)
    assert parsed is not None
    assert parsed["part1"] == "원인A"
    assert parsed["part2"] == "영향B"
    assert parsed["part3"] == "조치C"


def test_parse_log_analysis_fail_returns_none():
    assert parse_log_analysis("invalid") is None


def test_sanitize_html_blocks_javascript_protocol():
    raw = "<a href='javascript:alert(1)'>bad</a>"
    safe = sanitize_basic_html(raw)
    assert "javascript:" not in safe
