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


def test_sanitize_html_removes_script_and_disallowed_tags():
    raw = "<h3>ok</h3><script>alert(1)</script><img src='x'/>"
    safe = sanitize_basic_html(raw)
    assert "<script" not in safe
    assert "<img" not in safe
    assert "ok" in safe


def test_sanitize_html_allows_http_links_only():
    raw = "<a href='https://example.com'>good</a><a href='ftp://x'>bad</a>"
    safe = sanitize_basic_html(raw)
    assert 'href="https://example.com"' in safe
    assert "ftp://" not in safe
